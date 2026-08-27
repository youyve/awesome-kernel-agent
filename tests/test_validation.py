from __future__ import annotations

from copy import deepcopy
from collections import Counter
import json
from pathlib import Path
import tempfile
import unittest

from scripts.lib.loader import DuplicateKeyError, ROOT, load_catalog, load_vocab, load_yaml
from scripts.lib.field_analysis import facet_keys
from scripts.lib.markdown import baseline_counts
from scripts.lib.validation import DEFAULT_ID_MANIFEST, validate_catalog
from scripts.migrate_v2 import migrate_document
from scripts.validate import validate_json_schema


PAPER_URL = "https://arxiv.org/abs/2501.00001"
ARTIFACT_URL = "https://github.com/example/kernel-agent/tree/main/results"


def valid_claim() -> dict:
    return {
        "id": "h100-speedup",
        "metric": "speedup",
        "value": 1.2,
        "unit": "x",
        "aggregation": "geometric-mean",
        "qualifier": "reported over the full benchmark",
        "workload": {"benchmark": "KernelBench", "subset": "Level 1"},
        "hardware": "NVIDIA H100",
        "scope": "operator",
        "baseline": {
            "tier": "T0",
            "kind": "framework-reference",
            "name": "PyTorch eager",
            "evidence": None,
        },
        "budget": {"status": "unknown", "details": ""},
        "reproducibility": {
            "claim_linked_artifact": "no",
            "artifact_url": None,
        },
        "primary_source": {"url": PAPER_URL, "locator": "Table 2"},
        "caveats": [],
    }


def valid_entry(entry_id: str = "example-agent") -> dict:
    unknown_artifact = {"status": "unknown", "urls": []}
    return {
        "id": entry_id,
        "name": "Example Agent",
        "organization": "Example Lab",
        "date": "2025-01",
        "entry_type": "agent",
        "status": "closed",
        "summary": "An evidence-backed example used by the validation tests.",
        "caveats": [],
        "taxonomy": {
            "policy_adaptation": ["prompting"],
            "generation_mode": ["iterative-refinement"],
            "search_strategy": [],
            "participants": ["single-agent"],
            "coordination": [],
            "feedback_signal": ["correctness", "runtime"],
            "feedback_source": ["compiler"],
            "memory": [],
            "workload_scope": ["operator"],
            "integration_scope": [],
            "optimization_level": ["source"],
            "optimization_focus": [],
        },
        "representations": ["CUDA"],
        "hardware": ["NVIDIA"],
        "links": {
            "paper": [{"label": "Paper", "url": PAPER_URL, "provenance": "official"}],
            "code": [],
            "article": [],
            "project": [],
            "artifact": [],
            "model": [],
            "dataset": [],
        },
        "artifacts": {
            "implementation": deepcopy(unknown_artifact),
            "generated_kernels": deepcopy(unknown_artifact),
            "harness": deepcopy(unknown_artifact),
            "model_weights": deepcopy(unknown_artifact),
            "trajectories": deepcopy(unknown_artifact),
        },
        "claims": [valid_claim()],
        "primary_claim": "h100-speedup",
    }


def valid_catalog() -> dict:
    return {
        "schema_version": 2,
        "research_cutoff": "2026-08-25",
        "agents": [valid_entry()],
    }


class LoaderTests(unittest.TestCase):
    def test_duplicate_yaml_keys_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "duplicate.yaml"
            path.write_text("schema_version: 2\nschema_version: 2\n", encoding="utf-8")
            with self.assertRaises(DuplicateKeyError):
                load_yaml(path)

    def test_schema_json_is_well_formed_and_closed(self) -> None:
        schema = json.loads((ROOT / "schema" / "agents.schema.json").read_text(encoding="utf-8"))
        self.assertFalse(schema["additionalProperties"])
        self.assertFalse(schema["$defs"]["entry"]["additionalProperties"])
        self.assertFalse(schema["$defs"]["claim"]["additionalProperties"])

    def test_repository_catalog_satisfies_json_schema(self) -> None:
        self.assertEqual([], validate_json_schema(load_catalog()))

    def test_v1_manifest_has_115_unique_ids(self) -> None:
        ids = [
            line.strip()
            for line in DEFAULT_ID_MANIFEST.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        ]
        self.assertEqual(115, len(ids))
        self.assertEqual(len(ids), len(set(ids)))


class ValidationTests(unittest.TestCase):
    def errors(self, catalog: dict) -> list[str]:
        return validate_catalog(
            catalog,
            require_legacy_ids=False,
            vocab=load_vocab(),
        )

    def assert_error_contains(self, catalog: dict, text: str) -> None:
        errors = self.errors(catalog)
        self.assertTrue(
            any(text in error for error in errors),
            msg=f"expected {text!r} in errors:\n" + "\n".join(errors),
        )

    def test_valid_catalog(self) -> None:
        self.assertEqual([], self.errors(valid_catalog()))

    def test_unknown_top_level_field_is_rejected(self) -> None:
        catalog = valid_catalog()
        catalog["routes"] = []
        self.assert_error_contains(catalog, "unknown field 'routes'")

    def test_legacy_entry_fields_are_rejected(self) -> None:
        for field in ("route", "dsl", "dsl_also", "claim_baseline", "ships_kernels"):
            with self.subTest(field=field):
                catalog = valid_catalog()
                catalog["agents"][0][field] = "legacy"
                self.assert_error_contains(catalog, "legacy v1 field is forbidden")

    def test_duplicate_entry_ids_are_rejected(self) -> None:
        catalog = valid_catalog()
        catalog["agents"].append(deepcopy(catalog["agents"][0]))
        self.assert_error_contains(catalog, "duplicate entry id")

    def test_preserved_dot_separated_id_is_valid(self) -> None:
        catalog = valid_catalog()
        catalog["agents"][0]["id"] = "qwen3.7-max-kernel-opt"
        self.assertEqual([], self.errors(catalog))

    def test_taxonomy_values_are_controlled_and_unique(self) -> None:
        catalog = valid_catalog()
        catalog["agents"][0]["taxonomy"]["feedback_source"] = ["profiler", "profiler", "guess"]
        self.assert_error_contains(catalog, "duplicate value 'profiler'")
        self.assert_error_contains(catalog, "unknown controlled-vocabulary value 'guess'")

    def test_single_and_multi_agent_are_mutually_exclusive(self) -> None:
        catalog = valid_catalog()
        catalog["agents"][0]["taxonomy"]["participants"] = [
            "single-agent", "multi-agent"
        ]
        self.assert_error_contains(catalog, "mutually exclusive")

    def test_direct_and_iterative_modes_are_mutually_exclusive(self) -> None:
        catalog = valid_catalog()
        catalog["agents"][0]["taxonomy"]["generation_mode"] = [
            "direct", "iterative-refinement"
        ]
        self.assert_error_contains(catalog, "mutually exclusive")

    def test_hierarchical_facet_implications_are_enforced(self) -> None:
        catalog = valid_catalog()
        catalog["agents"][0]["taxonomy"]["policy_adaptation"] = [
            "agentic-reinforcement-learning"
        ]
        self.assert_error_contains(catalog, "requires ['reinforcement-learning']")

        catalog = valid_catalog()
        catalog["agents"][0]["taxonomy"]["search_strategy"] = ["map-elites"]
        self.assert_error_contains(
            catalog, "requires ['evolutionary-search', 'quality-diversity']"
        )

    def test_representations_are_controlled(self) -> None:
        catalog = valid_catalog()
        catalog["agents"][0]["representations"] = ["Primary DSL"]
        self.assert_error_contains(catalog, "unknown controlled-vocabulary value 'Primary DSL'")

    def test_duplicate_claim_ids_are_rejected(self) -> None:
        catalog = valid_catalog()
        catalog["agents"][0]["claims"].append(valid_claim())
        self.assert_error_contains(catalog, "duplicate claim id")

    def test_claim_ids_are_unique_across_entries(self) -> None:
        catalog = valid_catalog()
        catalog["agents"].append(valid_entry("second-agent"))
        self.assert_error_contains(catalog, "duplicate catalog-wide claim id")

    def test_dangling_primary_claim_is_rejected(self) -> None:
        catalog = valid_catalog()
        catalog["agents"][0]["primary_claim"] = "missing-claim"
        self.assert_error_contains(catalog, "dangling claim id")

    def test_claims_require_a_primary_claim(self) -> None:
        catalog = valid_catalog()
        catalog["agents"][0]["primary_claim"] = None
        self.assert_error_contains(catalog, "must select one claim")

    def test_t5_requires_dated_evidence(self) -> None:
        catalog = valid_catalog()
        baseline = catalog["agents"][0]["claims"][0]["baseline"]
        baseline.update({"tier": "T5", "kind": "best-known", "evidence": None})
        self.assert_error_contains(catalog, "T5 requires dated external evidence")

    def test_invalid_baseline_tier_is_rejected(self) -> None:
        catalog = valid_catalog()
        catalog["agents"][0]["claims"][0]["baseline"]["tier"] = "T7"
        self.assert_error_contains(catalog, "unknown value 'T7'")

    def test_t5_accepts_dated_evidence(self) -> None:
        catalog = valid_catalog()
        baseline = catalog["agents"][0]["claims"][0]["baseline"]
        baseline.update(
            {
                "tier": "T5",
                "kind": "best-known",
                "evidence": {"url": PAPER_URL, "as_of": "2025-01-15"},
            }
        )
        self.assertEqual([], self.errors(catalog))

    def test_baseline_tier_and_kind_must_agree(self) -> None:
        catalog = valid_catalog()
        catalog["agents"][0]["claims"][0]["baseline"]["kind"] = "hardware-ceiling"
        self.assert_error_contains(catalog, "is inconsistent with kind")

    def test_unknown_and_not_applicable_baseline_states_are_strict(self) -> None:
        valid_pairs = (
            ("unknown", "unresolved-implementation"),
            ("unknown", "self-baseline"),
            ("unknown", "prior-agent"),
            ("not-applicable", "ablation"),
            ("not-applicable", "evaluation-reference"),
        )
        for tier, kind in valid_pairs:
            with self.subTest(valid=(tier, kind)):
                catalog = valid_catalog()
                catalog["agents"][0]["claims"][0]["baseline"].update(
                    {"tier": tier, "kind": kind}
                )
                self.assertEqual([], self.errors(catalog))

        invalid_pairs = (
            ("T0", "ablation"),
            ("unknown", "ablation"),
            ("not-applicable", "unresolved-implementation"),
            ("T4", "unresolved-implementation"),
        )
        for tier, kind in invalid_pairs:
            with self.subTest(invalid=(tier, kind)):
                catalog = valid_catalog()
                catalog["agents"][0]["claims"][0]["baseline"].update(
                    {"tier": tier, "kind": kind}
                )
                self.assert_error_contains(catalog, "is inconsistent with kind")

    def test_implementation_performance_relational_baseline_is_not_na(self) -> None:
        for kind in ("self-baseline", "prior-agent"):
            with self.subTest(kind=kind):
                catalog = valid_catalog()
                catalog["agents"][0]["claims"][0]["baseline"].update(
                    {"tier": "not-applicable", "kind": kind}
                )
                self.assert_error_contains(catalog, "real implementation denominator")

    def test_nonimplementation_relational_result_may_be_na(self) -> None:
        catalog = valid_catalog()
        claim = catalog["agents"][0]["claims"][0]
        claim.update({"metric": "win-rate", "unit": "count", "aggregation": "total"})
        claim["baseline"].update(
            {"tier": "not-applicable", "kind": "prior-agent"}
        )
        self.assertEqual([], self.errors(catalog))

    def test_positive_annotation_lists_may_be_empty(self) -> None:
        catalog = valid_catalog()
        entry = catalog["agents"][0]
        entry["claims"] = []
        entry["primary_claim"] = None
        entry["representations"] = []
        entry["hardware"] = []
        for dimension in entry["taxonomy"]:
            entry["taxonomy"][dimension] = []
        self.assertEqual([], self.errors(catalog))

    def test_presentation_taxonomy_must_partition_every_facet_once(self) -> None:
        vocab = load_vocab()
        flattened = [
            facet
            for definition in vocab["presentation_taxonomy"].values()
            for facet in definition["facets"]
        ]
        self.assertEqual(Counter({facet: 1 for facet in facet_keys(vocab)}), Counter(flattened))

        missing = deepcopy(vocab)
        missing["presentation_taxonomy"]["hardware"]["facets"] = []
        errors = validate_catalog(valid_catalog(), require_legacy_ids=False, vocab=missing)
        self.assertTrue(any("facets missing from projection" in error for error in errors))

        duplicated = deepcopy(vocab)
        duplicated["presentation_taxonomy"]["adaptation"]["facets"].append("hardware")
        errors = validate_catalog(valid_catalog(), require_legacy_ids=False, vocab=duplicated)
        self.assertTrue(any("facets must appear exactly once" in error for error in errors))

    def test_baseline_evidence_cannot_postdate_research_cutoff(self) -> None:
        catalog = valid_catalog()
        baseline = catalog["agents"][0]["claims"][0]["baseline"]
        baseline.update(
            {
                "tier": "T5",
                "kind": "best-known",
                "evidence": {"url": PAPER_URL, "as_of": "2026-08-26"},
            }
        )
        self.assert_error_contains(catalog, "falls after research_cutoff")

    def test_t6_rejects_ordinary_speedup(self) -> None:
        catalog = valid_catalog()
        baseline = catalog["agents"][0]["claims"][0]["baseline"]
        baseline.update({"tier": "T6", "kind": "hardware-ceiling"})
        self.assert_error_contains(catalog, "T6 claims must use efficiency")

    def test_claim_linked_artifact_yes_requires_url(self) -> None:
        catalog = valid_catalog()
        reproducibility = catalog["agents"][0]["claims"][0]["reproducibility"]
        reproducibility["claim_linked_artifact"] = "yes"
        self.assert_error_contains(catalog, "requires artifact_url")

    def test_claim_linked_artifact_url_must_be_a_typed_link(self) -> None:
        catalog = valid_catalog()
        reproducibility = catalog["agents"][0]["claims"][0]["reproducibility"]
        reproducibility.update(
            {"claim_linked_artifact": "yes", "artifact_url": ARTIFACT_URL}
        )
        self.assert_error_contains(catalog, "must also appear in the entry's typed links")

    def test_claim_linked_artifact_no_rejects_url(self) -> None:
        catalog = valid_catalog()
        reproducibility = catalog["agents"][0]["claims"][0]["reproducibility"]
        reproducibility["artifact_url"] = ARTIFACT_URL
        self.assert_error_contains(catalog, "requires artifact_url=null")

    def test_project_artifact_status_and_url_must_agree(self) -> None:
        catalog = valid_catalog()
        catalog["agents"][0]["artifacts"]["implementation"]["status"] = "yes"
        self.assert_error_contains(catalog, "requires at least one URL")

    def test_primary_source_must_be_a_typed_link(self) -> None:
        catalog = valid_catalog()
        catalog["agents"][0]["claims"][0]["primary_source"]["url"] = (
            "https://example.com/untracked"
        )
        self.assert_error_contains(catalog, "must also appear in the entry's typed links")

    def test_claim_scope_must_appear_in_entry_taxonomy(self) -> None:
        catalog = valid_catalog()
        catalog["agents"][0]["claims"][0]["scope"] = "system"
        self.assert_error_contains(catalog, "must also appear in taxonomy.workload_scope")

    def test_migration_manifest_detects_removed_ids(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            manifest = Path(directory) / "ids.txt"
            manifest.write_text("example-agent\nremoved-agent\n", encoding="utf-8")
            errors = validate_catalog(
                valid_catalog(), manifest_path=manifest, vocab=load_vocab()
            )
        self.assertTrue(any("removed-agent" in error for error in errors))

    def test_yaml_boolean_is_not_an_evidence_status(self) -> None:
        catalog = valid_catalog()
        catalog["agents"][0]["artifacts"]["implementation"]["status"] = True
        self.assert_error_contains(catalog, "must be a string")

    def test_range_values_preserve_bounds(self) -> None:
        catalog = valid_catalog()
        catalog["agents"][0]["claims"][0]["value"] = {"min": 48, "max": 17}
        self.assert_error_contains(catalog, "range min must be <= max")

    def test_range_value_and_aggregation_must_agree(self) -> None:
        catalog = valid_catalog()
        catalog["agents"][0]["claims"][0]["value"] = {"min": 1.0, "max": 1.2}
        self.assert_error_contains(catalog, "range value requires aggregation 'range'")

    def test_metric_and_unit_must_agree(self) -> None:
        catalog = valid_catalog()
        catalog["agents"][0]["claims"][0]["unit"] = "seconds"
        self.assert_error_contains(catalog, "is incompatible with unit")


class RepositoryIntegrationTests(unittest.TestCase):
    def test_repository_catalog_is_valid(self) -> None:
        catalog = load_catalog()
        errors = validate_catalog(catalog)
        self.assertEqual([], errors, msg="\n".join(errors))

    def test_repository_baseline_state_migration_is_exact(self) -> None:
        catalog = load_catalog()
        counts = baseline_counts(catalog)
        expected = {
            "T0": 43,
            "T1": 7,
            "T2": 15,
            "T3": 21,
            "T4": 14,
            "T5": 0,
            "T6": 3,
            "unknown": 15,
            "not-applicable": 27,
        }
        self.assertEqual(expected, {key: counts.get(key, 0) for key in expected})
        self.assertEqual(145, sum(counts.values()))
        unresolved = {
            claim["id"]
            for entry in catalog["agents"]
            for claim in entry["claims"]
            if claim["baseline"]["tier"] == "unknown"
        }
        self.assertEqual(
            {
                "agentcompile-claim-2",
                "kforge-claim-1",
                "compiler-grounded-hierarchical-diagnosis-claim-1",
                "cursor-nvidia-multi-agent-kernels-claim-1",
                "automegakernel-claim-1",
                "stitchcuda-claim-2",
                "stitchcuda-claim-3",
                "geak-v4-claim-1",
                "geak-v4-claim-2",
                "geak-v4-claim-3",
                "geak-v4-claim-4",
                "geak-v4-claim-5",
                "amd-apex-claim-1",
                "asmevo-claim-2",
                "asmevo-claim-3",
            },
            unresolved,
        )

    def test_migration_tool_validates_an_existing_v2_catalog(self) -> None:
        catalog = load_catalog()
        self.assertEqual(catalog, migrate_document(deepcopy(catalog)))

    def test_migration_tool_rejects_invalid_existing_v2_catalog(self) -> None:
        catalog = load_catalog()
        catalog["agents"][0]["route"] = "A"
        with self.assertRaisesRegex(ValueError, "v2 validation failed"):
            migrate_document(catalog)


if __name__ == "__main__":
    unittest.main()
