from __future__ import annotations

from copy import deepcopy
import re
import unittest
import xml.etree.ElementTree as ET

from scripts.generate import build_outputs
from scripts.lib.loader import load_catalog
from scripts.lib.svg import render_timeline, text_units, wrap_text


SVG_NS = {"svg": "http://www.w3.org/2000/svg"}


def svg_size(content: str) -> tuple[float, float]:
    root = ET.fromstring(content)
    view_box = [float(value) for value in root.attrib["viewBox"].split()]
    return view_box[2], view_box[3]


class SvgLayoutTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.catalog = load_catalog()
        cls.outputs = build_outputs(cls.catalog)
        cls.svgs = {
            path: content for path, content in cls.outputs.items() if path.endswith(".svg")
        }

    def test_width_aware_wrapper_preserves_long_text_without_ellipsis(self) -> None:
        cases = (
            "A realistic multi-word label with WWWW and several semantic qualifiers",
            "超长中文标签用于验证换行不会截断任何受控词表内容",
            "W" * 120,
        )
        for source in cases:
            with self.subTest(source=source[:20]):
                lines = wrap_text(source, 120, 14)
                self.assertGreater(len(lines), 1)
                self.assertTrue(all(text_units(line) * 14 <= 120.01 for line in lines))
                self.assertNotIn("…", "".join(lines))
                if " " in source:
                    self.assertEqual(" ".join(source.split()), " ".join(lines))
                else:
                    self.assertEqual(source, "".join(lines))

    def test_every_svg_is_1200px_wide_and_all_rectangles_are_in_canvas(self) -> None:
        for path, content in self.svgs.items():
            with self.subTest(path=path):
                root = ET.fromstring(content)
                width, height = svg_size(content)
                self.assertEqual(1200, width)
                self.assertEqual(str(int(width)), root.attrib["width"])
                self.assertEqual(str(int(height)), root.attrib["height"])
                for rect in root.findall(".//svg:rect", SVG_NS):
                    x = float(rect.attrib.get("x", 0))
                    y = float(rect.attrib.get("y", 0))
                    rect_width = float(rect.attrib["width"])
                    rect_height = float(rect.attrib["height"])
                    self.assertGreaterEqual(x, 0)
                    self.assertGreaterEqual(y, 0)
                    self.assertLessEqual(x + rect_width, width + 0.01)
                    self.assertLessEqual(y + rect_height, height + 0.01)

    def test_generated_svgs_never_truncate_or_clip_text(self) -> None:
        for path, content in self.svgs.items():
            with self.subTest(path=path):
                self.assertNotIn("…", content)
                self.assertNotIn("<clipPath", content)
                self.assertNotIn("text-overflow", content)

    def test_semantic_view_card_counts_are_complete(self) -> None:
        landscape = self.svgs["assets/landscape.svg"]
        field_map = self.svgs["assets/field-map.svg"]
        baseline = self.svgs["assets/baseline-distribution.svg"]
        self.assertEqual(14, landscape.count('data-role="facet-card"'))
        self.assertEqual(9, field_map.count('data-role="presentation-dimension"'))
        self.assertEqual(9, baseline.count('data-role="baseline-state"'))
        for state in [*[f"T{i}" for i in range(7)], "unknown", "not-applicable"]:
            self.assertEqual(1, baseline.count(f'id="baseline-{state}"'))

    def test_timeline_height_expands_for_long_names_without_losing_id(self) -> None:
        before = render_timeline(self.catalog)
        modified = deepcopy(self.catalog)
        target = next(entry for entry in modified["agents"] if entry["entry_type"] == "agent")
        target["name"] = "W" * 220 + " 超长系统名称" * 20
        after = render_timeline(modified)
        self.assertGreater(svg_size(after)[1], svg_size(before)[1])
        self.assertEqual(1, after.count(f'id="timeline-{target["id"]}"'))
        self.assertNotIn("…", after)
        rendered_text = "".join(
            re.findall(
                rf'<g id="timeline-{re.escape(target["id"])}".*?</g>',
                after,
                flags=re.DOTALL,
            )
        )
        self.assertIn("超长系统名称", rendered_text)
        self.assertEqual(after, render_timeline(modified))


if __name__ == "__main__":
    unittest.main()
