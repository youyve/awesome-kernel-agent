from __future__ import annotations

import collections
import re
import unittest

from scripts import build_readme as build


class DataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.entries = build.load_entries()

    def test_data_validates(self) -> None:
        self.assertEqual([], build.validate(self.entries))

    def test_code_link_is_not_another_entrys_repository(self) -> None:
        # A paper's reproducibility section often lists the benchmark or evaluator it used
        # (e.g. KernelBench). Those repositories must not be shown as the paper's own code.
        users = collections.defaultdict(list)
        for entry in self.entries:
            match = build.GITHUB_RE.match(entry.get("code") or "")
            if match and not match.group(3):
                users[f"{match.group(1)}/{match.group(2)}".lower()].append(entry)
        for repo, entries in users.items():
            if len(entries) < 2:
                continue
            repo_name = build.norm(repo.split("/")[1])
            for entry in entries:
                with self.subTest(repo=repo, entry=entry["id"]):
                    name = build.norm(entry["name"])
                    self.assertTrue(repo_name in name or name in repo_name or repo_name[:4] in name,
                                    f"{entry['id']} links {repo}, which other entries also use as their code")


class OutputTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.outputs = build.render(build.load_entries())

    def test_outputs_are_committed_and_current(self) -> None:
        for path, body in self.outputs.items():
            with self.subTest(path=path.name):
                self.assertTrue(path.exists(), f"{path} missing; run python3 scripts/build_readme.py")
                self.assertEqual(body, path.read_text(encoding="utf-8"), f"{path} is stale")

    def test_relative_links_resolve(self) -> None:
        for path, body in self.outputs.items():
            for target in re.findall(r"\]\((?!https?:|#|mailto:)([^)#\s]+)", body):
                with self.subTest(page=path.name, target=target):
                    self.assertTrue((path.parent / target).resolve().exists())

    def test_readme_anchors_exist(self) -> None:
        readme = self.outputs[build.README]
        anchors = {build.anchor(h) for h in re.findall(r"(?m)^#+ (.+)$", readme)}
        for target in re.findall(r"\]\((#[^)]+)\)", readme):
            with self.subTest(anchor=target):
                self.assertIn(target, anchors)


if __name__ == "__main__":
    unittest.main()
