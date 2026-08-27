from __future__ import annotations

import re
from copy import deepcopy
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

from scripts.generate import ROOT, build_outputs, check_outputs
from scripts.lib.field_analysis import (
    build_facet_model,
    build_presentation_model,
    facet_keys,
)
from scripts.lib.loader import load_catalog, load_vocab
from scripts.lib.markdown import agent_entries, headline, sorted_entries


STATIC_OUTPUTS = {
    "README.md",
    "README.zh.md",
    "data/agents.json",
    "reports/baseline-distribution.md",
    "reports/field-map.md",
    "reports/landscape.md",
    "reports/migration-review.md",
    "reports/timeline.md",
    "assets/baseline-distribution.svg",
    "assets/field-map.svg",
    "assets/landscape.svg",
    "assets/timeline.svg",
}


class GenerationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.catalog = load_catalog()
        cls.outputs = build_outputs(cls.catalog)

    def test_output_graph_is_complete_and_matches_disk(self) -> None:
        years = {entry["date"][:4] for entry in self.catalog["agents"]}
        expected = STATIC_OUTPUTS | {f"catalog/{year}.md" for year in years}
        self.assertEqual(expected, set(self.outputs))
        self.assertEqual([], check_outputs(self.outputs))

    def test_rendering_is_deterministic_in_memory(self) -> None:
        self.assertEqual(self.outputs, build_outputs(self.catalog))

    def test_readmes_list_every_agent_with_stable_catalog_anchor(self) -> None:
        agents = agent_entries(self.catalog)
        for readme_name in ("README.md", "README.zh.md"):
            readme = self.outputs[readme_name]
            for entry in agents:
                expected = f"catalog/{entry['date'][:4]}.md#{entry['id']}"
                self.assertIn(expected, readme, msg=f"{readme_name}: missing {entry['id']}")

    def test_readmes_expose_every_typed_agent_link_directly(self) -> None:
        for readme_name in ("README.md", "README.zh.md"):
            readme = self.outputs[readme_name]
            for entry in agent_entries(self.catalog):
                for links in entry["links"].values():
                    for link in links:
                        rendered_url = (
                            link["url"]
                            .replace(" ", "%20")
                            .replace("<", "%3C")
                            .replace(">", "%3E")
                        )
                        self.assertIn(
                            f"]({rendered_url})",
                            readme,
                            msg=f"{readme_name}: missing typed link for {entry['id']}",
                        )

    def test_readme_months_are_reverse_chronological(self) -> None:
        catalog_section = self.outputs["README.md"].split("## Agent Catalog\n", 1)[1]
        catalog_section = catalog_section.split("\n## Field Map", 1)[0]
        months = re.findall(r"^### (\d{4}-\d{2})$", catalog_section, re.MULTILINE)
        expected = sorted({entry["date"] for entry in agent_entries(self.catalog)}, reverse=True)
        self.assertEqual(expected, months)

    def test_readme_embeds_required_generated_visuals(self) -> None:
        readme = self.outputs["README.md"]
        for path in (
            "assets/landscape.svg",
            "assets/field-map.svg",
            "assets/baseline-distribution.svg",
            "assets/timeline.svg",
        ):
            self.assertIn(path, readme)
        self.assertIn("## Timeline", readme)

    def test_readme_primary_section_order_and_locale_alignment(self) -> None:
        headings = {
            "README.md": [
                "## Research Landscape",
                "## Latest",
                "## How to Read the Catalog",
                "## Agent Catalog",
                "## Field Map",
                "## Baseline Distribution",
                "## Timeline",
            ],
            "README.zh.md": [
                "## Research Landscape",
                "## 最新工作",
                "## 如何阅读 Catalog",
                "## Agent Catalog",
                "## Field Map",
                "## Baseline 分布",
                "## Timeline",
            ],
        }
        for filename, ordered in headings.items():
            readme = self.outputs[filename]
            positions = [readme.index(heading) for heading in ordered]
            self.assertEqual(sorted(positions), positions, msg=filename)
            self.assertLess(positions[-1], readme.index("## Benchmarks"))

    def test_latest_is_one_deterministic_link_line(self) -> None:
        expected = sorted_entries(agent_entries(self.catalog))[:5]
        for filename, latest_heading, legend_heading in (
            ("README.md", "## Latest", "## How to Read the Catalog"),
            ("README.zh.md", "## 最新工作", "## 如何阅读 Catalog"),
        ):
            readme = self.outputs[filename]
            section = readme.split(latest_heading, 1)[1].split(legend_heading, 1)[0]
            self.assertNotIn("| ---", section)
            self.assertNotIn("<br>", section)
            positions = []
            for entry in expected:
                link = f"catalog/{entry['date'][:4]}.md#{entry['id']}"
                self.assertEqual(1, section.count(link), msg=f"{filename}: {entry['id']}")
                positions.append(section.index(link))
            self.assertEqual(sorted(positions), positions)

    def test_targeted_coverage_audit_is_reflected(self) -> None:
        facets = {facet["key"]: facet for facet in build_facet_model(self.catalog)}
        expected = {
            "workload_scope": (57, 55),
            "optimization_level": (112, 0),
            "representations": (112, 0),
            "hardware": (112, 0),
        }
        for key, (tagged, unannotated) in expected.items():
            with self.subTest(facet=key):
                self.assertEqual(tagged, facets[key]["tagged"])
                self.assertEqual(unannotated, facets[key]["unannotated"])

        artifact_level = facets["optimization_level"]
        self.assertEqual(142, artifact_level["assignments"])
        compiler_ir = next(
            value for value in artifact_level["values"] if value["key"] == "compiler-ir"
        )
        self.assertEqual(0, compiler_ir["count"])

        self.assertIn("unconditional `operator` migration default was removed", self.outputs["reports/field-map.md"])
        self.assertIn("schema permits empty lists", self.outputs["reports/field-map.md"])

    def test_catalog_legend_precedes_baseline_tiers(self) -> None:
        for filename, legend_heading, catalog_heading in (
            ("README.md", "## How to Read the Catalog", "## Agent Catalog"),
            ("README.zh.md", "## 如何阅读 Catalog", "## Agent Catalog"),
        ):
            readme = self.outputs[filename]
            legend = readme.split(legend_heading, 1)[1].split(catalog_heading, 1)[0]
            for tier in ("T0", "T1", "T2", "T3", "T4", "T5", "T6"):
                self.assertIn(tier, legend)
            self.assertIn("10× @ T0", legend)
            self.assertIn("1.1× @ T4", legend)
            self.assertIn("`K`", legend)
            self.assertIn("`B`", legend)
            self.assertIn("`Unknown`", legend)
            self.assertIn("`N/A`", legend)

    def test_baseline_state_labels_are_consistent(self) -> None:
        for filename in ("README.md", "README.zh.md"):
            readme = self.outputs[filename]
            self.assertNotIn("<sub>Tier unknown ·", readme)
            self.assertNotIn("<sub>Tier N/A ·", readme)
            self.assertNotIn("<sub>层级未知 ·", readme)
            self.assertNotIn("<sub>层级不适用 ·", readme)
            self.assertIn("Unknown · original recovered AMDGPU code object", readme)
            self.assertIn("N/A · fresh CANNBot-style regeneration", readme)

        catalogs = self.outputs["catalog/2025.md"] + self.outputs["catalog/2026.md"]
        self.assertNotIn("| **Baseline** | unknown ·", catalogs)
        self.assertNotIn("| **Baseline** | not-applicable ·", catalogs)
        self.assertIn("| **Baseline** | Unknown ·", catalogs)
        self.assertIn("| **Baseline** | N/A ·", catalogs)

    def test_primary_pass_at_k_semantics_are_visible(self) -> None:
        self.assertIn("66.7% pass@1 · Ascend NPU", self.outputs["README.md"])

    def test_primary_claims_are_metric_aware(self) -> None:
        readme = self.outputs["README.md"]
        for expected in (
            "92.4% pass rate · NVIDIA A100",
            "80.8% pass rate · NVIDIA GPU",
            "10 wins · NVIDIA GPU",
            "481 ATen operators covered · MTIA",
            "89% of hardware ceiling · NVIDIA H100",
            "115% of baseline throughput · NVIDIA GPU",
        ):
            self.assertIn(expected, readme)
        for forbidden in ("10 count", "481 count", "+115%", "+124%"):
            self.assertNotIn(forbidden, readme)

    def test_no_primary_claim_uses_compact_dash(self) -> None:
        evomem = next(entry for entry in agent_entries(self.catalog) if entry["id"] == "evomem")
        self.assertEqual(("—", "", "—"), headline(evomem))
        for readme in (self.outputs["README.md"], self.outputs["README.zh.md"]):
            self.assertNotIn("No verified numerical claim", readme)
            self.assertNotIn("denominator unknown", readme)
            self.assertNotIn("暂无已核验数值主张", readme)
            row = next(line for line in readme.splitlines() if "#evomem)" in line and line.startswith("|"))
            self.assertIn("| — | — |", row)

    def test_field_map_covers_every_controlled_value_without_selection(self) -> None:
        report = self.outputs["reports/field-map.md"]
        self.assertNotIn("Focused queries", report)
        self.assertIn("(../catalog/", report)
        for facet in build_facet_model(self.catalog, load_vocab()):
            self.assertIn(f"## {facet['label']}", report)
            self.assertIn(f"{facet['unannotated']} unannotated", report)
            for value in facet["values"]:
                self.assertIn(f"(`{value['key']}`) | {value['count']} |", report)

    def test_field_map_projection_partitions_full_schema(self) -> None:
        vocab = load_vocab()
        projection = build_presentation_model(self.catalog, vocab)
        self.assertEqual(9, len(projection))
        projected = [facet for dimension in projection for facet in dimension["facet_keys"]]
        self.assertCountEqual(facet_keys(vocab), projected)
        self.assertEqual(len(projected), len(set(projected)))
        report = self.outputs["reports/field-map.md"]
        for dimension in projection:
            self.assertIn(f"**{dimension['label']}** — {dimension['question']}", report)
        self.assertIn("reading projection", self.outputs["README.md"])
        self.assertIn("not the detailed schema", self.outputs["README.md"])

    def test_field_counts_are_agent_level_multilabel_and_data_driven(self) -> None:
        catalog = deepcopy(self.catalog)
        before = {
            facet["key"]: facet for facet in build_facet_model(catalog, load_vocab())
        }
        entry = next(
            entry
            for entry in catalog["agents"]
            if entry["entry_type"] == "agent"
            and "preference-optimization" not in entry["taxonomy"]["policy_adaptation"]
        )
        entry["taxonomy"]["policy_adaptation"].append("preference-optimization")
        after = {
            facet["key"]: facet for facet in build_facet_model(catalog, load_vocab())
        }
        before_value = next(
            value for value in before["policy_adaptation"]["values"]
            if value["key"] == "preference-optimization"
        )
        after_value = next(
            value for value in after["policy_adaptation"]["values"]
            if value["key"] == "preference-optimization"
        )
        self.assertEqual(before_value["count"] + 1, after_value["count"])
        self.assertEqual(
            before["policy_adaptation"]["assignments"] + 1,
            after["policy_adaptation"]["assignments"],
        )

    def test_landscape_is_complete_ontology_without_system_selection(self) -> None:
        report = self.outputs["reports/landscape.md"]
        svg = self.outputs["assets/landscape.svg"]
        for facet in facet_keys(load_vocab()):
            self.assertIn(f"`{facet}`", report)
            self.assertEqual(1, svg.count(f'id="landscape-facet-{facet}"'), msg=facet)
        self.assertNotIn("Execution Feedback", svg)
        self.assertNotIn("Learned / RL Optimization", svg)
        self.assertNotIn("A/B/C", svg)
        self.assertNotIn(">A</text>", svg)
        self.assertNotIn(">B</text>", svg)
        self.assertNotIn(">C</text>", svg)
        for entry in agent_entries(self.catalog):
            self.assertNotIn(f"timeline-{entry['id']}", svg)

    def test_timeline_report_lists_every_agent(self) -> None:
        report = self.outputs["reports/timeline.md"]
        svg = self.outputs["assets/timeline.svg"]
        for entry in agent_entries(self.catalog):
            link = f"../catalog/{entry['date'][:4]}.md#{entry['id']}"
            self.assertEqual(1, report.count(link + ")"))
            self.assertEqual(1, svg.count(f'id="timeline-{entry["id"]}"'))
        actual_ids = re.findall(
            r'<g id="timeline-(?!month-)([^"]+)" data-role="timeline-entry">', svg
        )
        expected_ids = [
            entry["id"]
            for month in sorted({entry["date"] for entry in agent_entries(self.catalog)})
            for entry in sorted(
                [item for item in agent_entries(self.catalog) if item["date"] == month],
                key=lambda item: (item["name"].casefold(), item["id"]),
            )
        ]
        self.assertEqual(expected_ids, actual_ids)

    def test_svg_outputs_are_well_formed_and_self_contained(self) -> None:
        for relative_path, content in self.outputs.items():
            if not relative_path.endswith(".svg"):
                continue
            ET.fromstring(content)
            self.assertNotIn("<script", content.casefold())
            self.assertNotIn("<foreignobject", content.casefold())
            self.assertNotIn("@import", content.casefold())
            self.assertNotIn("http://", content.replace('xmlns="http://www.w3.org/2000/svg"', ""))

    def test_all_generated_internal_markdown_links_exist(self) -> None:
        generated_markdown = {
            path: content
            for path, content in self.outputs.items()
            if path.endswith(".md")
        }
        link_pattern = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
        for relative_path, content in generated_markdown.items():
            parent = (ROOT / relative_path).parent
            for target in link_pattern.findall(content):
                if "://" in target or target.startswith(("mailto:", "#")):
                    continue
                file_target = target.split("#", 1)[0]
                if not file_target:
                    continue
                resolved = (parent / file_target).resolve()
                self.assertTrue(
                    resolved.exists(),
                    msg=f"{relative_path}: missing internal link target {target}",
                )


if __name__ == "__main__":
    unittest.main()
