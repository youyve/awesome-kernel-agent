"""Derive compact, human-readable profiles from the v2 taxonomy.

Profiles are deliberately presentation-only. They are never persisted in the
catalog because the faceted taxonomy is the source of truth.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence

from .loader import load_vocab


_VOCAB = load_vocab()

LABELS_EN = {
    "agentic-reinforcement-learning": "Agentic RL",
    "reinforcement-learning": "Reinforcement learning",
    "supervised-fine-tuning": "SFT",
    "preference-optimization": "Preference optimization",
    "self-training": "Self-training",
    "distillation": "Distillation",
    "continual-learning": "Continual learning",
    "in-context-learning": "In-context learning",
    "prompting": "Prompting",
    "direct": "Direct generation",
    "iterative-refinement": "Iterative refinement",
    "best-of-n": "Best-of-N",
    "beam-search": "Beam search",
    "mcts": "MCTS",
    "evolutionary-search": "Evolution",
    "map-elites": "MAP-Elites",
    "quality-diversity": "Quality-diversity",
    "local-search": "Local search",
    "autotuning": "Autotuning",
    "portfolio-search": "Portfolio search",
    "single-agent": "Single-agent",
    "multi-agent": "Multi-agent",
    "hierarchical": "Hierarchical",
    "compiler-in-the-loop": "Compiler in loop",
    "compiler": "Compiler feedback",
    "correctness": "Correctness feedback",
    "execution": "Execution feedback",
    "runtime": "Runtime feedback",
    "profiler": "Profiler",
    "hardware-counters": "Hardware counters",
    "roofline": "Roofline",
    "ir": "IR feedback",
    "formal-verification": "Formal verification",
    "differential-testing": "Differential testing",
    "simulator": "Simulator",
    "model-level": "Model-level feedback",
    "trajectory": "Trajectory memory",
    "reflection": "Reflection",
    "retrieval": "Retrieval memory",
    "skill-library": "Skill library",
    "archive": "Archive",
    "cross-run": "Cross-run memory",
    "episodic": "Episodic memory",
    "population": "Population memory",
}

LABELS_ZH = {
    "agentic-reinforcement-learning": "Agentic RL",
    "reinforcement-learning": "强化学习",
    "supervised-fine-tuning": "SFT",
    "preference-optimization": "偏好优化",
    "self-training": "自训练",
    "distillation": "蒸馏",
    "continual-learning": "持续学习",
    "in-context-learning": "上下文学习",
    "prompting": "提示工程",
    "direct": "直接生成",
    "iterative-refinement": "迭代精化",
    "best-of-n": "Best-of-N",
    "beam-search": "束搜索",
    "mcts": "MCTS",
    "evolutionary-search": "进化搜索",
    "map-elites": "MAP-Elites",
    "quality-diversity": "质量多样性搜索",
    "local-search": "局部搜索",
    "autotuning": "自动调优",
    "portfolio-search": "组合搜索",
    "single-agent": "单智能体",
    "multi-agent": "多智能体",
    "hierarchical": "分层编排",
    "compiler-in-the-loop": "Agent / 编译器协同",
    "compiler": "编译器反馈",
    "compiler-diagnostics": "编译器反馈",
    "correctness": "正确性反馈",
    "execution": "执行反馈",
    "runtime": "运行时反馈",
    "profiler": "Profiler",
    "hardware-counters": "硬件计数器",
    "roofline": "Roofline",
    "ir": "IR 反馈",
    "formal-verification": "形式化验证",
    "differential-testing": "差分测试",
    "simulator": "模拟器",
    "model-level": "模型级反馈",
    "trajectory": "轨迹记忆",
    "reflection": "反思记忆",
    "retrieval": "检索记忆",
    "skill-library": "技能库",
    "archive": "搜索档案",
    "cross-run": "跨运行记忆",
    "episodic": "情景记忆",
    "population": "种群记忆",
}


def _as_values(value: object) -> list[str]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        return []
    return [str(item) for item in value]


def _label(value: str, locale: str) -> str:
    labels = LABELS_ZH if locale == "zh" else LABELS_EN
    if value in labels:
        return labels[value]
    return value.replace("-", " ").replace("_", " ").title()


def _configured_dimensions(field: str) -> list[str]:
    profile = _VOCAB.get("profile_derivation")
    profile = profile if isinstance(profile, Mapping) else {}
    return _as_values(profile.get(field))


def _ordered_specific_values(
    taxonomy: Mapping[str, object], dimension: str, excluded: set[str]
) -> list[str]:
    """Order by vocabulary and remove parents implied by selected children."""

    selected = set(_as_values(taxonomy.get(dimension, []))) - excluded
    constraints = _VOCAB.get("facet_constraints")
    constraints = constraints if isinstance(constraints, Mapping) else {}
    implications = constraints.get("implies")
    implications = implications if isinstance(implications, Mapping) else {}
    rules = implications.get(dimension)
    rules = rules if isinstance(rules, Mapping) else {}
    implied_parents = {
        parent
        for child, parents in rules.items()
        if child in selected
        for parent in _as_values(parents)
    }
    selected -= implied_parents
    taxonomy_vocab = _VOCAB.get("taxonomy")
    taxonomy_vocab = taxonomy_vocab if isinstance(taxonomy_vocab, Mapping) else {}
    values = taxonomy_vocab.get(dimension)
    values = values if isinstance(values, Mapping) else {}
    return [str(value) for value in values if value in selected]


def _pick(
    taxonomy: Mapping[str, object], dimensions: Sequence[str], excluded: set[str] | None = None
) -> str | None:
    blocked = excluded or set()
    profile = _VOCAB.get("profile_derivation")
    profile = profile if isinstance(profile, Mapping) else {}
    fallback_values = set(_as_values(profile.get("fallback_values")))
    fallback: str | None = None
    for dimension in dimensions:
        values = _ordered_specific_values(taxonomy, dimension, blocked)
        for value in values:
            if value not in fallback_values:
                return value
            if fallback is None:
                fallback = value
    return fallback


def _suppressed_by(value: str | None) -> set[str]:
    if value is None:
        return set()
    profile = _VOCAB.get("profile_derivation")
    profile = profile if isinstance(profile, Mapping) else {}
    suppressions = profile.get("suppressions")
    suppressions = suppressions if isinstance(suppressions, Mapping) else {}
    return set(_as_values(suppressions.get(value)))


def derive_profile(entry: Mapping[str, object], locale: str = "en") -> tuple[list[str], list[str]]:
    """Return ``(profile labels, representations)`` for a catalog entry."""

    if entry.get("entry_type") == "tool":
        method_labels = ["工具 / 基础设施" if locale == "zh" else "Tooling / infrastructure"]
    else:
        taxonomy = entry.get("taxonomy")
        taxonomy = taxonomy if isinstance(taxonomy, Mapping) else {}
        approach = _pick(taxonomy, _configured_dimensions("approach_dimensions"))
        grounding = _pick(
            taxonomy,
            _configured_dimensions("grounding_dimensions"),
            _suppressed_by(approach),
        )
        selected = [value for value in (approach, grounding) if value]
        # Avoid duplicate display labels (for example compiler/compiler-diagnostics).
        method_labels = []
        for value in selected:
            label = _label(value, locale)
            if label not in method_labels:
                method_labels.append(label)
        if not method_labels:
            method_labels = ["—"]

    representations = _as_values(entry.get("representations", []))
    return method_labels[:2], representations


def compact_representations(representations: Sequence[str], limit: int = 3) -> str:
    shown = [str(value) for value in representations[:limit]]
    remaining = len(representations) - len(shown)
    if remaining:
        shown.append(f"+{remaining}")
    return " · ".join(shown) if shown else "—"
