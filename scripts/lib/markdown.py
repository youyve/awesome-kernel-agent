"""Deterministic Markdown renderers for the v2 research catalog."""

from __future__ import annotations

import html
import re
from collections import Counter, defaultdict
from collections.abc import Iterable, Mapping, Sequence

from .field_analysis import (
    build_facet_model,
    build_landscape_groups,
    build_presentation_model,
)
from .loader import load_vocab
from .profile import compact_representations, derive_profile


LINK_ORDER = (
    "paper",
    "code",
    "article",
    "project",
    "artifact",
    "model",
    "dataset",
)
LINK_LABELS = {
    "paper": "Paper",
    "code": "Code",
    "article": "Article",
    "project": "Project",
    "artifact": "Artifact",
    "model": "Model",
    "dataset": "Dataset",
}
STATUS_LABELS = {
    "en": {
        "open": "open",
        "partial": "partial",
        "wip": "wip",
        "closed": "closed",
        "proprietary": "proprietary",
    },
    "zh": {
        "open": "开源",
        "partial": "部分公开",
        "wip": "开发中",
        "closed": "未公开",
        "proprietary": "专有",
    },
}
EVIDENCE_BADGES = {"yes": "✓", "partial": "◐", "no": "—", "unknown": "?"}
_VOCAB = load_vocab()
TAXONOMY_DIMENSIONS = tuple(_VOCAB.get("taxonomy", {}))
_FACET_METADATA = _VOCAB.get("facet_dimensions", {})
TAXONOMY_LABELS = {
    dimension: str(_FACET_METADATA.get(dimension, {}).get("label", dimension))
    for dimension in TAXONOMY_DIMENSIONS
}
BASELINE_DESCRIPTIONS = {
    "T0": "Reference / framework",
    "T1": "General compiler-generated",
    "T2": "Optimized generic / vendor library",
    "T3": "Specialized expert implementation",
    "T4": "Production incumbent",
    "T5": "Externally verified best-known implementation",
    "T6": "Hardware ceiling",
    "unknown": "Implementation baseline tier unresolved",
    "not-applicable": "Implementation baseline tier not applicable",
}


def _sequence(value: object) -> list[object]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        return []
    return list(value)


def _text(value: object, fallback: str = "unknown") -> str:
    if value is None or value == "":
        return fallback
    return str(value)


def baseline_tier_label(value: object) -> str:
    """Return the compact display label for a baseline tier or state."""

    tier = _text(value)
    return {"unknown": "Unknown", "not-applicable": "N/A"}.get(tier, tier)


def md_text(value: object) -> str:
    """Escape user/catalog text for a Markdown table cell or link label."""

    escaped = html.escape(_text(value, ""), quote=False)
    return escaped.replace("\\", "\\\\").replace("|", "\\|").replace("\n", " ")


def _plain(value: object) -> str:
    return html.escape(_text(value, ""), quote=False)


def _safe_url(value: object) -> str:
    # URLs are schema-validated.  Angle brackets and whitespace are escaped so
    # malformed migration data cannot break generated Markdown or HTML.
    return str(value or "").replace(" ", "%20").replace("<", "%3C").replace(">", "%3E")


def sorted_entries(entries: Iterable[Mapping[str, object]]) -> list[Mapping[str, object]]:
    alphabetical = sorted(
        entries,
        key=lambda entry: (
            _text(entry.get("name")).casefold(),
            _text(entry.get("id")),
        ),
    )
    return sorted(alphabetical, key=lambda entry: _text(entry.get("date")), reverse=True)


def sorted_entries_in_month(entries: Iterable[Mapping[str, object]]) -> list[Mapping[str, object]]:
    return sorted(
        entries,
        key=lambda entry: (
            _text(entry.get("name")).casefold(),
            _text(entry.get("id")),
        ),
    )


def agent_entries(catalog: Mapping[str, object]) -> list[Mapping[str, object]]:
    return [
        entry
        for entry in _sequence(catalog.get("agents"))
        if isinstance(entry, Mapping) and entry.get("entry_type") == "agent"
    ]


def tool_entries(catalog: Mapping[str, object]) -> list[Mapping[str, object]]:
    return [
        entry
        for entry in _sequence(catalog.get("agents"))
        if isinstance(entry, Mapping) and entry.get("entry_type") == "tool"
    ]


def catalog_link(entry: Mapping[str, object], prefix: str = "") -> str:
    return f"{prefix}catalog/{_text(entry.get('date'))[:4]}.md#{_text(entry.get('id'))}"


def typed_links(entry: Mapping[str, object], *, prefix: str = "") -> str:
    del prefix  # Reserved for future internal links; typed links are external.
    links = entry.get("links")
    links = links if isinstance(links, Mapping) else {}
    rendered: list[str] = []
    for link_type in LINK_ORDER:
        values = [value for value in _sequence(links.get(link_type)) if isinstance(value, Mapping)]
        base_label = LINK_LABELS[link_type]

        def is_generic_label(link: Mapping[str, object]) -> bool:
            supplied_label = _text(link.get("label"), "")
            generic_labels = {
                base_label.casefold(),
                f"{base_label} page".casefold(),
                f"{base_label} card".casefold(),
                "implementation" if link_type == "code" else "",
                "blog" if link_type == "article" else "",
            }
            return not supplied_label or supplied_label.casefold() in generic_labels

        generic_count = sum(is_generic_label(link) for link in values)
        generic_ordinal = 0
        for link in values:
            supplied = _text(link.get("label"), "")
            if not is_generic_label(link):
                label = f"{base_label}: {supplied}"
            else:
                generic_ordinal += 1
                label = (
                    f"{base_label} {generic_ordinal}"
                    if generic_count > 1
                    else base_label
                )
            provenance = _text(link.get("provenance"), "")
            if provenance == "community":
                label += " (community)"
            elif provenance == "third-party":
                label += " (third-party)"
            rendered.append(f"[{md_text(label)}]({_safe_url(link.get('url'))})")
    return " · ".join(rendered) if rendered else "No public link"


def source_link(entry: Mapping[str, object]) -> str:
    links = entry.get("links")
    links = links if isinstance(links, Mapping) else {}
    for link_type in LINK_ORDER:
        values = [value for value in _sequence(links.get(link_type)) if isinstance(value, Mapping)]
        if values:
            link = values[0]
            return f"[{LINK_LABELS[link_type]}]({_safe_url(link.get('url'))})"
    return "No public source"


def primary_claim(entry: Mapping[str, object]) -> Mapping[str, object] | None:
    claim_id = entry.get("primary_claim")
    if not claim_id:
        return None
    for claim in _sequence(entry.get("claims")):
        if isinstance(claim, Mapping) and claim.get("id") == claim_id:
            return claim
    return None


def _format_number(value: float | int) -> str:
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, int):
        return f"{value:,}"
    rendered = f"{value:.6f}".rstrip("0").rstrip(".")
    integer, dot, fractional = rendered.partition(".")
    grouped = f"{int(integer):,}"
    return grouped + (dot + fractional if dot else "")


def _metric_label(metric: str, locale: str) -> str:
    labels = {
        "en": {
            "latency": "latency",
            "throughput": "throughput",
            "correctness": "correctness",
            "accuracy": "accuracy",
            "pass-rate": "pass rate",
            "compilation-rate": "compilation rate",
            "coverage": "coverage",
            "win-rate": "win rate",
            "efficiency": "efficiency",
            "fraction-of-ceiling": "of hardware ceiling",
            "energy-reduction": "energy reduction",
            "time-reduction": "time reduction",
            "token-reduction": "token reduction",
            "cost": "cost",
            "count": "count",
            "other": "reported metric",
        },
        "zh": {
            "latency": "延迟",
            "throughput": "吞吐量",
            "correctness": "正确率",
            "accuracy": "准确率",
            "pass-rate": "通过率",
            "compilation-rate": "编译通过率",
            "coverage": "覆盖量",
            "win-rate": "胜率",
            "efficiency": "效率",
            "fraction-of-ceiling": "硬件上限",
            "energy-reduction": "能耗降低",
            "time-reduction": "时间降低",
            "token-reduction": "token 降低",
            "cost": "成本",
            "count": "计数",
            "other": "报告指标",
        },
    }
    return labels.get(locale, labels["en"]).get(metric, metric.replace("-", " "))


def claim_result(claim: Mapping[str, object], locale: str = "en") -> str:
    value = claim.get("value")
    if isinstance(value, Mapping) and isinstance(value.get("min"), (int, float)) and isinstance(value.get("max"), (int, float)):
        rendered = f"{_format_number(value['min'])}–{_format_number(value['max'])}"
    elif isinstance(value, (int, float)) and not isinstance(value, bool):
        rendered = _format_number(value)
    else:
        rendered = _text(value)

    unit = _text(claim.get("unit"), "")
    if unit.casefold() in {"x", "times", "speedup"}:
        rendered += "×"
    elif unit in {"%", "percent"}:
        rendered += "%"
    elif unit == "milliseconds":
        rendered += " ms"
    elif unit == "microseconds":
        rendered += " µs"
    elif unit == "seconds":
        rendered += " s"
    elif unit == "usd":
        rendered = "$" + rendered
    elif unit in {"count", "ratio"}:
        pass
    elif unit and unit not in {"unknown", "none", "n/a"}:
        rendered += f" {unit}"

    # README headlines remain compact but never discard a structured metric.
    # Free-form prose stays in the yearly catalog; only semantics needed to
    # interpret the number are carried here.
    qualifier = _text(claim.get("qualifier"), "")
    aggregation = _text(claim.get("aggregation"), "")
    metric = _text(claim.get("metric"), "")
    metric_label = _metric_label(metric, locale)
    workload = claim.get("workload")
    subset = _text(workload.get("subset"), "") if isinstance(workload, Mapping) else ""

    if aggregation == "pass-at-k":
        match = re.search(r"pass\s*@\s*(\d+)", subset, re.IGNORECASE)
        rendered += f" pass@{match.group(1)}" if match else " pass@k"
    elif metric == "speedup" and unit in {"%", "percent"}:
        rendered += " speedup" if locale == "en" else " 加速"
        if aggregation != "maximum" and not rendered.startswith("+"):
            rendered = "+" + rendered
    elif metric == "throughput" and unit in {"%", "percent"}:
        if "preserved verbatim" in qualifier.casefold():
            rendered += " of baseline throughput" if locale == "en" else " 基线吞吐量"
        else:
            rendered += f" {metric_label}"
            if any(marker in qualifier.casefold() for marker in (" gain", "improv", "reported as +")):
                rendered = "+" + rendered
    elif metric == "throughput" and unit.casefold() in {"x", "times", "speedup"}:
        rendered += f" {metric_label}"
    elif metric == "fraction-of-ceiling":
        rendered += f" {metric_label}"
    elif metric == "win-rate" and unit == "count":
        rendered += " wins" if locale == "en" else " 次胜出"
    elif metric == "coverage" and unit == "count":
        if subset and subset.casefold() not in {"unknown", "n/a"}:
            rendered += f" {subset} covered" if locale == "en" else f" 个{subset}已覆盖"
        else:
            rendered += f" {metric_label}"
    elif metric == "count" and unit == "count":
        rendered += f" {subset}" if subset else f" {metric_label}"
    elif metric not in {"speedup"}:
        rendered += f" {metric_label}"

    if aggregation == "maximum" or qualifier in {"up-to", "up_to", "maximum", "max"}:
        rendered = ("最高 " if locale == "zh" else "up to ") + rendered.lstrip("+")
    elif qualifier in {"at-least", "at_least"}:
        rendered = ("至少 " if locale == "zh" else "at least ") + rendered
    return rendered


def _claim_hardware(claim: Mapping[str, object], entry: Mapping[str, object]) -> str:
    hardware = claim.get("hardware")
    if isinstance(hardware, Sequence) and not isinstance(hardware, (str, bytes)):
        values = [str(value) for value in hardware]
        if values:
            return " / ".join(values)
    if hardware not in (None, "", "unknown"):
        return str(hardware)
    values = [str(value) for value in _sequence(entry.get("hardware"))]
    return " / ".join(values) if values else "hardware unknown"


def headline(entry: Mapping[str, object], locale: str = "en") -> tuple[str, str, str]:
    claim = primary_claim(entry)
    if claim is None:
        return "—", "", "—"

    baseline = claim.get("baseline")
    baseline = baseline if isinstance(baseline, Mapping) else {}
    tier = _text(baseline.get("tier"))
    baseline_name = _text(baseline.get("name"), "denominator unknown")
    result = f"{claim_result(claim, locale)} · {_claim_hardware(claim, entry)}"
    tier_display = baseline_tier_label(tier)
    denominator = f"{tier_display} · {baseline_name}"

    reproducibility = claim.get("reproducibility")
    reproducibility = reproducibility if isinstance(reproducibility, Mapping) else {}
    budget = claim.get("budget")
    budget = budget if isinstance(budget, Mapping) else {}
    k_status = _text(reproducibility.get("claim_linked_artifact"))
    b_status = _text(budget.get("status"))
    evidence = f"K {EVIDENCE_BADGES.get(k_status, '?')} · B {EVIDENCE_BADGES.get(b_status, '?')}"
    return result, denominator, evidence


def render_catalog_row(entry: Mapping[str, object], locale: str = "en") -> str:
    profile, representations = derive_profile(entry, locale)
    result, denominator, evidence = headline(entry, locale)
    status = STATUS_LABELS[locale].get(_text(entry.get("status")), _text(entry.get("status")))
    detail = catalog_link(entry)
    system = (
        f"**[{md_text(entry.get('name'))}]({detail})**<br>"
        f"<sub>{md_text(entry.get('organization'))} · {md_text(status)} · {typed_links(entry)}</sub>"
    )
    profile_cell = (
        f"{md_text(' · '.join(profile))}<br>"
        f"<sub>{md_text(compact_representations(representations))}</sub>"
    )
    claim_cell = md_text(result)
    if denominator:
        claim_cell += f"<br><sub>{md_text(denominator)}</sub>"
    return f"| {system} | {profile_cell} | {claim_cell} | {evidence} |"


def render_agent_catalog(catalog: Mapping[str, object], locale: str = "en") -> str:
    by_month: dict[str, list[Mapping[str, object]]] = defaultdict(list)
    for entry in agent_entries(catalog):
        by_month[_text(entry.get("date"))].append(entry)
    blocks: list[str] = []
    headers = (
        ("系统", "画像", "主 claim", "证据")
        if locale == "zh"
        else ("System", "Profile", "Headline claim", "Evidence")
    )
    for month in sorted(by_month, reverse=True):
        blocks.extend(
            [
                f"### {month}",
                "",
                "| " + " | ".join(headers) + " |",
                "| --- | --- | --- | :---: |",
            ]
        )
        blocks.extend(render_catalog_row(entry, locale) for entry in sorted_entries_in_month(by_month[month]))
        blocks.append("")
    return "\n".join(blocks).rstrip()


def render_latest(catalog: Mapping[str, object], locale: str = "en", limit: int = 5) -> str:
    del locale
    entries = sorted_entries(agent_entries(catalog))[:limit]
    return " · ".join(
        f"[{md_text(entry.get('name'))}]({catalog_link(entry)})" for entry in entries
    )


def render_stats(catalog: Mapping[str, object], locale: str = "en") -> str:
    agents = agent_entries(catalog)
    tools = tool_entries(catalog)
    claims = [claim for entry in agents for claim in _sequence(entry.get("claims"))]
    linked = 0
    for claim in claims:
        if not isinstance(claim, Mapping):
            continue
        repro = claim.get("reproducibility")
        if isinstance(repro, Mapping) and repro.get("claim_linked_artifact") in {"yes", "partial"}:
            linked += 1
    hardware = {str(value) for entry in agents for value in _sequence(entry.get("hardware"))}
    cutoff = _text(catalog.get("research_cutoff"))
    if locale == "zh":
        return (
            f"**{len(agents)} 个 Agent 系统** · **{len(claims)} 条结构化 claims** · "
            f"**{linked} 条带 claim 对应 artifact** · **{len(hardware)} 类硬件目标** · "
            f"另收录 **{len(tools)} 个工具条目** · 检索截止 **{cutoff}**"
        )
    return (
        f"**{len(agents)} agent systems** · **{len(claims)} structured claims** · "
        f"**{linked} claims with linked artifacts** · **{len(hardware)} hardware targets** · "
        f"**{len(tools)} tooling entries** · research cutoff **{cutoff}**"
    )


def fill_template(template: str, replacements: Mapping[str, str]) -> str:
    rendered = template
    for key, value in replacements.items():
        rendered = rendered.replace("{{" + key + "}}", value)
    leftovers = sorted(set(re.findall(r"\{\{[A-Z0-9_]+\}\}", rendered)))
    if leftovers:
        raise ValueError(f"unresolved template placeholders: {', '.join(leftovers)}")
    return rendered.rstrip() + "\n"


def render_readme(catalog: Mapping[str, object], template: str, locale: str = "en") -> str:
    return fill_template(
        template,
        {
            "STATS": render_stats(catalog, locale),
            "LATEST": render_latest(catalog, locale),
            "AGENT_CATALOG": render_agent_catalog(catalog, locale),
            "RESEARCH_CUTOFF": _text(catalog.get("research_cutoff")),
        },
    )


def _join_values(value: object) -> str:
    values = [md_text(item) for item in _sequence(value)]
    return " · ".join(values) if values else "unknown"


def _status_with_urls(value: object) -> str:
    if not isinstance(value, Mapping):
        return "unknown"
    status = md_text(value.get("status"))
    urls = [str(url) for url in _sequence(value.get("urls"))]
    if urls:
        status += " · " + " · ".join(
            f"[Artifact {index}]({_safe_url(url)})" for index, url in enumerate(urls, 1)
        )
    return status


def _render_claim_value(claim: Mapping[str, object]) -> str:
    value = claim.get("value")
    if isinstance(value, Mapping):
        value_display = f"{_text(value.get('min'))}–{_text(value.get('max'))}"
    else:
        value_display = _text(value)
    fields = [
        _text(claim.get("metric")),
        value_display,
        _text(claim.get("unit")),
        _text(claim.get("aggregation")),
        _text(claim.get("qualifier")),
    ]
    return " · ".join(md_text(field) for field in fields)


def _render_claim(entry: Mapping[str, object], claim: Mapping[str, object]) -> str:
    is_primary = claim.get("id") == entry.get("primary_claim")
    title = f"#### {md_text(claim.get('id'))}" + (" — primary claim" if is_primary else "")
    workload = claim.get("workload")
    workload = workload if isinstance(workload, Mapping) else {}
    baseline = claim.get("baseline")
    baseline = baseline if isinstance(baseline, Mapping) else {}
    evidence = baseline.get("evidence")
    if isinstance(evidence, Mapping):
        baseline_evidence = (
            f"[{md_text(evidence.get('as_of'))}]({_safe_url(evidence.get('url'))})"
        )
    else:
        baseline_evidence = "n/a"
    budget = claim.get("budget")
    budget = budget if isinstance(budget, Mapping) else {}
    repro = claim.get("reproducibility")
    repro = repro if isinstance(repro, Mapping) else {}
    artifact_url = repro.get("artifact_url")
    artifact = md_text(repro.get("claim_linked_artifact"))
    if artifact_url:
        artifact += f" · [claim-linked artifact]({_safe_url(artifact_url)})"
    source = claim.get("primary_source")
    source = source if isinstance(source, Mapping) else {}
    source_display = f"[Primary source]({_safe_url(source.get('url'))})"
    locator = _text(source.get("locator"), "")
    if locator:
        source_display += f" · {md_text(locator)}"
    caveats = _sequence(claim.get("caveats"))
    caveat_display = "<br>".join(f"- {md_text(item)}" for item in caveats) if caveats else "None recorded"
    rows = [
        ("Result", _render_claim_value(claim)),
        ("Workload", f"{md_text(workload.get('benchmark'))} · {md_text(workload.get('subset'))}"),
        ("Hardware", md_text(claim.get("hardware"))),
        ("Scope", md_text(claim.get("scope"))),
        (
            "Baseline",
            f"{md_text(baseline_tier_label(baseline.get('tier')))} · "
            f"{md_text(baseline.get('kind'))} · "
            f"{md_text(baseline.get('name'))} · evidence: {baseline_evidence}",
        ),
        ("Search / optimization budget", f"{md_text(budget.get('status'))} · {md_text(budget.get('details'))}"),
        ("Claim reproducibility", artifact),
        ("Primary source", source_display),
        ("Caveats", caveat_display),
    ]
    table = ["| Claim field | Evidence |", "| --- | --- |"]
    table.extend(f"| **{label}** | {value} |" for label, value in rows)
    return title + "\n\n" + "\n".join(table)


def render_year_catalog(year: str, entries: Sequence[Mapping[str, object]]) -> str:
    agents = [entry for entry in entries if entry.get("entry_type") == "agent"]
    tools = [entry for entry in entries if entry.get("entry_type") == "tool"]
    blocks = [
        f"# {year} Kernel Agent Catalog",
        "",
        "_Generated from [`data/agents.yaml`](../data/agents.yaml). Stable anchors use entry IDs._",
        "",
        "[README](../README.md) · [Field Map](../reports/field-map.md) · "
        "[Timeline](../reports/timeline.md) · [Data](../data/agents.json)",
        "",
        "---",
    ]
    by_month: dict[str, list[Mapping[str, object]]] = defaultdict(list)
    for entry in agents:
        by_month[_text(entry.get("date"))].append(entry)
    for month in sorted(by_month, reverse=True):
        blocks.extend(["", f"## {month}"])
        for entry in sorted_entries_in_month(by_month[month]):
            blocks.extend(["", _render_catalog_detail(entry)])
    if tools:
        blocks.extend(["", "## Tooling"])
        for entry in sorted_entries_in_month(tools):
            blocks.extend(["", _render_catalog_detail(entry)])
    return "\n".join(blocks).rstrip() + "\n"


def _render_catalog_detail(entry: Mapping[str, object]) -> str:
    profile, representations = derive_profile(entry, "en")
    artifacts = entry.get("artifacts")
    artifacts = artifacts if isinstance(artifacts, Mapping) else {}
    taxonomy = entry.get("taxonomy")
    taxonomy = taxonomy if isinstance(taxonomy, Mapping) else {}
    caveats = _sequence(entry.get("caveats"))
    lines = [
        f"<a id=\"{html.escape(_text(entry.get('id')), quote=True)}\"></a>",
        f"### {md_text(entry.get('name'))}",
        "",
        f"{md_text(entry.get('organization'))} · `{md_text(entry.get('id'))}` · "
        f"{md_text(entry.get('date'))} · {md_text(entry.get('status'))}",
        "",
        typed_links(entry),
        "",
        _plain(entry.get("summary")),
        "",
        "| Metadata | Value |",
        "| --- | --- |",
        f"| **Derived profile** | {md_text(' · '.join(profile))} |",
        f"| **Representations** | {md_text(compact_representations(representations, limit=99))} |",
        f"| **Hardware** | {_join_values(entry.get('hardware'))} |",
    ]
    for dimension in TAXONOMY_DIMENSIONS:
        lines.append(f"| **{TAXONOMY_LABELS[dimension]}** | {_join_values(taxonomy.get(dimension))} |")
    for artifact_name in ("implementation", "generated_kernels", "harness", "model_weights", "trajectories"):
        label = artifact_name.replace("_", " ").title()
        lines.append(f"| **Artifact: {label}** | {_status_with_urls(artifacts.get(artifact_name))} |")
    if caveats:
        lines.extend(["", "Caveats:", ""])
        lines.extend(f"- {_plain(item)}" for item in caveats)
    claims = [claim for claim in _sequence(entry.get("claims")) if isinstance(claim, Mapping)]
    if claims:
        for claim in claims:
            lines.extend(["", _render_claim(entry, claim)])
    else:
        lines.extend(["", "No safely structured numerical claim is recorded."])
    return "\n".join(lines)


def render_catalogs(catalog: Mapping[str, object]) -> dict[str, str]:
    by_year: dict[str, list[Mapping[str, object]]] = defaultdict(list)
    for entry in _sequence(catalog.get("agents")):
        if isinstance(entry, Mapping):
            by_year[_text(entry.get("date"))[:4]].append(entry)
    return {
        f"catalog/{year}.md": render_year_catalog(year, entries)
        for year, entries in sorted(by_year.items(), reverse=True)
    }


def _entry_reference(entry: Mapping[str, object], prefix: str = "../") -> str:
    detail = catalog_link(entry, prefix)
    return f"[{md_text(entry.get('name'))}]({detail}) ({source_link(entry)})"


def reverse_indexes(catalog: Mapping[str, object]) -> dict[str, dict[str, list[Mapping[str, object]]]]:
    entries = agent_entries(catalog)
    indexes: dict[str, dict[str, list[Mapping[str, object]]]] = {}
    for dimension in TAXONOMY_DIMENSIONS:
        values: dict[str, list[Mapping[str, object]]] = defaultdict(list)
        for entry in entries:
            taxonomy = entry.get("taxonomy")
            taxonomy = taxonomy if isinstance(taxonomy, Mapping) else {}
            for value in _sequence(taxonomy.get(dimension)):
                values[str(value)].append(entry)
        indexes[f"taxonomy.{dimension}"] = dict(values)
    for field in ("representations", "hardware"):
        values = defaultdict(list)
        for entry in entries:
            for value in _sequence(entry.get(field)):
                values[str(value)].append(entry)
        indexes[field] = dict(values)
    return indexes


def render_field_map_report(catalog: Mapping[str, object]) -> str:
    facets = build_facet_model(catalog, _VOCAB)
    presentation = build_presentation_model(catalog, _VOCAB)
    total = len(agent_entries(catalog))
    configured_groups = _VOCAB.get("facet_groups")
    configured_groups = configured_groups if isinstance(configured_groups, Mapping) else {}

    def group_label(group_key: object) -> str:
        definition = configured_groups.get(group_key)
        if isinstance(definition, Mapping):
            return _text(definition.get("label"), str(group_key))
        return str(group_key)

    blocks = [
        "# Kernel Agent Field Map",
        "",
        "**Research question:** Along which major dimensions can Kernel Agent systems be understood "
        f"and compared, and where does the catalog contain positive evidence across {total} systems?",
        "",
        "[README](../README.md) · [Landscape](landscape.md) · [Data](../data/agents.json)",
        "",
        "---",
        "",
        "## README presentation projection",
        "",
        "The README projection is a lossless partition of facet *families*, not a replacement for "
        "the detailed ontology. It groups related questions for rapid reading while preserving "
        "generation mode versus search strategy, signal versus source, workload versus integration "
        "scope, and artifact level versus representation below.",
        "",
        "| Presentation dimension | Detailed facet families | Tagged union | Unannotated | Used values |",
        "| --- | --- | ---: | ---: | ---: |",
    ]
    for dimension in presentation:
        facet_labels = " · ".join(
            f"**{md_text(facet['label'])}** (`{md_text(facet['key'])}`)"
            for facet in dimension["facets"]
        )
        blocks.append(
            f"| **{md_text(dimension['label'])}** — {md_text(dimension['question'])} | "
            f"{facet_labels} | {dimension['tagged']}/{dimension['total']} | "
            f"{dimension['unannotated']} | "
            f"{dimension['used_values']}/{dimension['controlled_values']} |"
        )
    blocks.extend(
        [
        "",
        "## Interpretation rules",
        "",
        f"- The denominator is the complete set of **{total} Agent entries**; tooling entries are excluded.",
        "- Counts are positive, multi-label annotations. A system contributes once to every value it is explicitly tagged with.",
        "- `Unannotated` means the catalog does not currently contain positive evidence for that facet family; it is not a verified negative.",
        "- A zero-value row means no positive catalog evidence at the research cutoff, not that the research direction is impossible or absent.",
        "- Every controlled value is included. Values are ordered by descending support, then by controlled-vocabulary order and stable key.",
        "- Presentation groups and detailed semantic roles come only from `schema/vocab.yaml`; position is deterministic layout, not rank, sequence, or causality.",
        "- Reverse-index system lists are sorted by system name and then stable ID.",
        "",
        "## Coverage provenance audit",
        "",
        "- **Workload scope:** the unconditional `operator` migration default was removed. For migrated entries, "
        "`operator` is retained where an operator-scoped structured claim supplies positive evidence; otherwise an "
        "entry remains unannotated unless another workload-scope value is explicitly present.",
        "- **Artifact level:** coarse levels were deterministically mapped from explicit representation annotations "
        "during migration. This is a parent-category derivation, not an independent second evidence channel; no "
        "catch-all level was inserted.",
        "- **Representation and hardware:** both fields are structurally present, but the schema permits empty lists. "
        "Their full coverage comes from non-empty source annotations for every migrated Agent, not a generated "
        "fallback. Coverage therefore means annotated, not independently re-verified and not exhaustive.",
        "",
        "## Facet-family coverage",
        "",
        "| Facet family | Semantic role | Research question | Tagged | Unannotated | Assignments | Used values |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: |",
        ]
    )
    for facet in facets:
        used = sum(int(value["count"]) > 0 for value in facet["values"])
        blocks.append(
            f"| **{md_text(facet['label'])}** | {md_text(group_label(facet['group']))} | "
            f"{md_text(facet['question'])} | "
            f"{facet['tagged']}/{facet['total']} | {facet['unannotated']} | "
            f"{facet['assignments']} | {used}/{len(facet['values'])} |"
        )
    for facet in facets:
        blocks.extend(
            [
                "",
                f"## {md_text(facet['label'])}",
                "",
                f"**Question:** {md_text(facet['question'])}",
                "",
                f"**Boundary:** {md_text(facet['boundary'])}",
                "",
                f"**Coverage:** {facet['tagged']}/{facet['total']} tagged · "
                f"{facet['unannotated']} unannotated · {facet['assignments']} assignments.",
                "",
                "| Value | Count | Systems |",
                "| --- | ---: | --- |",
            ]
        )
        for value in facet["values"]:
            entries = value["entries"]
            systems = (
                " · ".join(
                    _entry_reference(entry)
                    for entry in sorted_entries_in_month(entries)
                )
                or "No positive catalog evidence"
            )
            blocks.append(
                f"| **{md_text(value['label'])}** (`{md_text(value['key'])}`) | "
                f"{value['count']} | {systems} |"
            )
    return "\n".join(blocks).rstrip() + "\n"


def render_landscape_report(catalog: Mapping[str, object]) -> str:
    groups = build_landscape_groups(catalog, _VOCAB)
    constraints = _VOCAB.get("facet_constraints")
    constraints = constraints if isinstance(constraints, Mapping) else {}
    blocks = [
        "# Kernel Agent Functional Landscape",
        "",
        "**Research question:** Which distinct questions define this catalog's Kernel Agent data model, and what semantic role does each question play?",
        "",
        "[README](../README.md) · [Field Map](field-map.md) · [Data](../data/agents.json)",
        "",
        "This is a versioned catalog ontology, not a timeline, maturity ladder, causal graph, or performance ranking. "
        "Containment expresses semantic role only; screen position and group order do not imply research evolution. "
        "The facets are separate annotation questions, not a claim of statistical independence.",
    ]
    for group in groups:
        blocks.extend(
            [
                "",
                f"## {md_text(group['label'])}",
                "",
                md_text(group["definition"]),
                "",
                f"Group predicate: **{md_text(group['relation'])}**.",
                "",
                "| Facet family | Question | Inclusion boundary |",
                "| --- | --- | --- |",
            ]
        )
        for facet in group["facets"]:
            blocks.append(
                f"| **{md_text(facet['label'])}** (`{md_text(facet['key'])}`) | "
                f"{md_text(facet['question'])} | {md_text(facet['boundary'])} |"
            )
    blocks.extend(
        [
            "",
            "## Declared value relations",
            "",
            "Values are positive and multi-label by default. The following are the only logical value relations enforced by the validator; they do not encode chronology or causality.",
        ]
    )
    exclusive = constraints.get("mutually_exclusive")
    if isinstance(exclusive, Mapping):
        for dimension, values in exclusive.items():
            rendered = ", ".join(f"`{md_text(value)}`" for value in _sequence(values))
            blocks.append(f"- Mutually exclusive within `{md_text(dimension)}`: {rendered}.")
    implications = constraints.get("implies")
    if isinstance(implications, Mapping):
        for dimension, rules in implications.items():
            if not isinstance(rules, Mapping):
                continue
            for value, required in rules.items():
                rendered = ", ".join(f"`{md_text(item)}`" for item in _sequence(required))
                blocks.append(
                    f"- Within `{md_text(dimension)}`, `{md_text(value)}` implies {rendered}."
                )
    blocks.extend(
        [
            "",
            "## Reproducibility rules",
            "",
            "1. Facet families, questions, boundaries, groups, and group predicates come from `schema/vocab.yaml`.",
            "2. Every declared facet family appears exactly once; no representative system or preferred research direction is selected.",
            "3. The Landscape contains no empirical edge, causal arrow, time ordering, or undeclared exclusivity.",
            "4. Multi-label membership and corpus coverage belong to the Field Map, not this ontology view.",
            "5. Empty lists mean unannotated evidence and never create a negative ontology relation.",
            "6. Group and facet order follow the controlled vocabulary; card placement is layout only and carries no empirical meaning.",
        ]
    )
    return "\n".join(blocks).rstrip() + "\n"


def render_timeline_report(catalog: Mapping[str, object]) -> str:
    entries = agent_entries(catalog)
    by_month: dict[str, list[Mapping[str, object]]] = defaultdict(list)
    for entry in entries:
        by_month[_text(entry.get("date"))].append(entry)
    blocks = [
        "# Complete Kernel Agent Timeline",
        "",
        "_Every Agent system, grouped by first-public-release month in chronological order. Within each month, systems are sorted by name and then stable ID. No milestone selection is used._",
        "",
        "[README](../README.md) · [Data](../data/agents.json)",
        "",
        "---",
    ]
    for month in sorted(by_month):
        blocks.extend(
            [
                "",
                f"## {month}",
                "",
                "| System | Profile | Direct links |",
                "| --- | --- | --- |",
            ]
        )
        for entry in sorted_entries_in_month(by_month[month]):
            profile, representations = derive_profile(entry, "en")
            profile_display = md_text(" · ".join(profile) + " / " + compact_representations(representations))
            blocks.append(
                f"| **[{md_text(entry.get('name'))}]({catalog_link(entry, '../')})** | "
                f"{profile_display} | {typed_links(entry)} |"
            )
    return "\n".join(blocks).rstrip() + "\n"


def render_migration_review(catalog: Mapping[str, object]) -> str:
    rows: list[tuple[Mapping[str, object], Mapping[str, object]]] = []
    for entry in agent_entries(catalog) + tool_entries(catalog):
        for issue in _sequence(entry.get("migration_review")):
            if isinstance(issue, Mapping):
                rows.append((entry, issue))
    blocks = [
        "# v2 Migration Review",
        "",
        "_Facts that could not be safely inferred during the v1 → v2 migration. `unknown` is intentional until primary evidence resolves an item._",
        "",
        f"**{len(rows)} review items** across **{len({entry.get('id') for entry, _ in rows})} entries**.",
        "",
        "| System | Field | Review item |",
        "| --- | --- | --- |",
    ]
    if rows:
        for entry, issue in sorted(
            rows,
            key=lambda row: (
                _text(row[0].get("date")),
                _text(row[0].get("id")),
                _text(row[1].get("field")),
                _text(row[1].get("issue")),
            ),
            reverse=True,
        ):
            blocks.append(
                f"| [{md_text(entry.get('name'))}]({catalog_link(entry, '../')}) | "
                f"`{md_text(issue.get('field'))}` | {md_text(issue.get('issue'))} |"
            )
    else:
        blocks.append("| — | — | No unresolved migration items. |")
    return "\n".join(blocks).rstrip() + "\n"


def baseline_counts(catalog: Mapping[str, object]) -> Counter[str]:
    counts: Counter[str] = Counter()
    for entry in agent_entries(catalog):
        for claim in _sequence(entry.get("claims")):
            baseline = claim.get("baseline") if isinstance(claim, Mapping) else None
            tier = baseline.get("tier") if isinstance(baseline, Mapping) else "unknown"
            allowed = {*[f"T{i}" for i in range(7)], "unknown", "not-applicable"}
            counts[str(tier) if tier in allowed else "unknown"] += 1
    return counts


def render_baseline_report(catalog: Mapping[str, object]) -> str:
    counts = baseline_counts(catalog)
    total = sum(counts.values())
    blocks = [
        "# Claim Baseline Distribution",
        "",
        "_Counts are computed from structured claims. Tiers express provenance and specialization, not a strict performance ranking._",
        "",
        f"**{total} claims** are represented. **Unknown** means an implementation baseline exists "
        "but its tier is unresolved; **N/A** means the implementation-tier model does not apply.",
        "",
        "| Tier / state | Meaning | Claims | Share |",
        "| --- | --- | ---: | ---: |",
    ]
    for tier in [*[f"T{i}" for i in range(7)], "unknown", "not-applicable"]:
        count = counts.get(tier, 0)
        share = f"{count / total:.1%}" if total else "0.0%"
        label = baseline_tier_label(tier)
        blocks.append(f"| **{label}** | {BASELINE_DESCRIPTIONS[tier]} | {count} | {share} |")
    return "\n".join(blocks).rstrip() + "\n"


def render_reports(catalog: Mapping[str, object]) -> dict[str, str]:
    return {
        "reports/landscape.md": render_landscape_report(catalog),
        "reports/field-map.md": render_field_map_report(catalog),
        "reports/timeline.md": render_timeline_report(catalog),
        "reports/migration-review.md": render_migration_review(catalog),
        "reports/baseline-distribution.md": render_baseline_report(catalog),
    }
