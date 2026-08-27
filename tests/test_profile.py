from __future__ import annotations

from copy import deepcopy
import unittest

from scripts.lib.loader import load_catalog
from scripts.lib.profile import compact_representations, derive_profile


class ProfileTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.catalog = load_catalog()
        cls.agent = next(
            entry for entry in cls.catalog["agents"] if entry["entry_type"] == "agent"
        )

    def empty_agent(self) -> dict:
        entry = deepcopy(self.agent)
        entry["taxonomy"] = {key: [] for key in entry["taxonomy"]}
        entry["representations"] = []
        return entry

    def test_profile_is_independent_of_entry_value_order(self) -> None:
        entry = next(
            deepcopy(item)
            for item in self.catalog["agents"]
            if item["id"] == "kernelfoundry"
        )
        before = derive_profile(entry)
        for values in entry["taxonomy"].values():
            values.reverse()
        entry["representations"].reverse()
        after = derive_profile(entry)
        self.assertEqual(before[0], after[0])
        self.assertEqual(list(reversed(before[1])), after[1])

    def test_implied_parent_values_are_suppressed(self) -> None:
        entry = self.empty_agent()
        entry["taxonomy"]["policy_adaptation"] = [
            "reinforcement-learning",
            "agentic-reinforcement-learning",
        ]
        self.assertEqual(["Agentic RL"], derive_profile(entry)[0])

        entry = self.empty_agent()
        entry["taxonomy"]["search_strategy"] = [
            "quality-diversity",
            "map-elites",
            "evolutionary-search",
        ]
        self.assertEqual(["MAP-Elites"], derive_profile(entry)[0])

    def test_profile_uses_configured_order_with_generic_fallbacks(self) -> None:
        entry = self.empty_agent()
        entry["taxonomy"]["policy_adaptation"] = ["prompting"]
        entry["taxonomy"]["search_strategy"] = ["mcts"]
        self.assertEqual("MCTS", derive_profile(entry)[0][0])

        entry["taxonomy"]["policy_adaptation"] = ["reinforcement-learning"]
        self.assertEqual("Reinforcement learning", derive_profile(entry)[0][0])

        entry["taxonomy"]["policy_adaptation"] = []
        entry["taxonomy"]["search_strategy"] = ["autotuning", "evolutionary-search"]
        self.assertEqual("Evolution", derive_profile(entry)[0][0])

    def test_compiler_actor_does_not_repeat_compiler_feedback(self) -> None:
        entry = self.empty_agent()
        entry["taxonomy"]["participants"] = ["compiler-in-the-loop"]
        entry["taxonomy"]["feedback_source"] = ["compiler"]
        self.assertEqual(["Compiler in loop"], derive_profile(entry)[0])

    def test_unannotated_profile_and_representation_use_neutral_dash(self) -> None:
        entry = self.empty_agent()
        profile, representations = derive_profile(entry)
        self.assertEqual(["—"], profile)
        self.assertEqual("—", compact_representations(representations))
        self.assertNotIn("Unclassified", " ".join(profile))

    def test_tool_profile_remains_explicit(self) -> None:
        tool = next(
            item for item in self.catalog["agents"] if item["entry_type"] == "tool"
        )
        self.assertEqual(["Tooling / infrastructure"], derive_profile(tool)[0])


if __name__ == "__main__":
    unittest.main()
