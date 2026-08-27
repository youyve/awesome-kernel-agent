"""Deterministic, dependency-free SVG views backed exclusively by catalog data.

Layouts favor height over tiny text. Every free-form label is wrapped with a
conservative width model; no renderer truncates text or imposes a line cap.
"""

from __future__ import annotations

import html
import unicodedata
from collections import defaultdict
from collections.abc import Mapping, Sequence

from .field_analysis import (
    build_landscape_groups,
    build_presentation_model,
    catalog_agents,
)
from .markdown import baseline_counts


TIERS = [*[f"T{i}" for i in range(7)], "unknown", "not-applicable"]

BG = "#f8fafc"
CARD = "#ffffff"
TEXT = "#0f172a"
MUTED = "#475569"
LINE = "#cbd5e1"
BLUE = "#2563eb"
BLUE_LIGHT = "#dbeafe"
BLUE_MID = "#60a5fa"
PROCESS = "#0072b2"
PROCESS_LIGHT = "#e6f2f8"
TARGET = "#a85600"
TARGET_LIGHT = "#fff2dd"
SUBSTRATE = "#007d5a"
SUBSTRATE_LIGHT = "#e5f5ef"
UNKNOWN = "#b45309"
NOT_APPLICABLE = "#64748b"
GROUP_COLORS = {
    "agent-mechanism": (PROCESS, PROCESS_LIGHT),
    "optimization-target": (TARGET, TARGET_LIGHT),
    "execution-substrate": (SUBSTRATE, SUBSTRATE_LIGHT),
}


def _sequence(value: object) -> list[object]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        return []
    return list(value)


def _esc(value: object) -> str:
    return html.escape(str(value if value is not None else ""), quote=True)


def text_units(value: object) -> float:
    """Conservative approximate glyph width in em units.

    The estimate intentionally over-allocates common wide ASCII and all
    East-Asian wide/full-width glyphs. It is used only for deterministic line
    breaking; exact counts and semantic content never depend on it.
    """

    total = 0.0
    for char in str(value):
        if unicodedata.combining(char):
            continue
        if char.isspace():
            total += 0.38
        elif unicodedata.east_asian_width(char) in {"W", "F"}:
            total += 1.0
        elif char in "MW@#%&QO0":
            total += 0.82
        elif char.isupper():
            total += 0.68
        elif char.isdigit():
            total += 0.60
        elif char in "ilI.,:;!'`|()[]{}":
            total += 0.34
        else:
            total += 0.58
    return total


def _split_token(token: str, max_units: float) -> list[str]:
    chunks: list[str] = []
    current = ""
    for char in token:
        if current and text_units(current + char) > max_units:
            chunks.append(current)
            current = char
        else:
            current += char
    if current:
        chunks.append(current)
    return chunks or [""]


def wrap_text(value: object, max_width: float, font_size: float) -> list[str]:
    """Wrap text to ``max_width`` without truncation or a line-count limit."""

    source = " ".join(str(value if value is not None else "").split())
    if not source:
        return [""]
    max_units = max(max_width / max(font_size, 1), 1.0)
    lines: list[str] = []
    current = ""
    for token in source.split(" "):
        chunks = _split_token(token, max_units)
        for chunk_index, chunk in enumerate(chunks):
            if chunk_index > 0:
                if current:
                    lines.append(current)
                current = chunk
                continue
            candidate = f"{current} {chunk}".strip()
            if current and text_units(candidate) > max_units:
                lines.append(current)
                current = chunk
            else:
                current = candidate
        if len(chunks) > 1 and text_units(current) >= max_units * 0.98:
            lines.append(current)
            current = ""
    if current:
        lines.append(current)
    return lines or [""]


def _svg_start(width: int, height: int, title: str, description: str) -> list[str]:
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        f'  <title id="title">{_esc(title)}</title>',
        f'  <desc id="desc">{_esc(description)}</desc>',
        "  <style>",
        "    text { font-family: system-ui, -apple-system, 'Segoe UI', sans-serif; }",
        f"    .title {{ fill: {TEXT}; font-size: 26px; font-weight: 700; }}",
        f"    .subtitle {{ fill: {MUTED}; font-size: 15px; }}",
        f"    .group-title {{ fill: {TEXT}; font-size: 18px; font-weight: 700; }}",
        f"    .label {{ fill: {TEXT}; font-size: 15px; font-weight: 650; }}",
        f"    .body {{ fill: {MUTED}; font-size: 14px; }}",
        f"    .small {{ fill: {MUTED}; font-size: 12px; }}",
        "  </style>",
        f'  <rect width="{width}" height="{height}" rx="14" fill="{BG}"/>',
    ]


def _finish(lines: list[str]) -> str:
    lines.append("</svg>")
    return "\n".join(lines) + "\n"


def _text_block(
    lines: list[str],
    text_lines: Sequence[str],
    x: float,
    y: float,
    css_class: str,
    line_height: float,
    *,
    indent: str = "  ",
    attrs: str = "",
) -> None:
    attributes = f' {attrs}' if attrs else ""
    lines.append(f'{indent}<text x="{x:g}" y="{y:g}" class="{css_class}"{attributes}>')
    for index, value in enumerate(text_lines):
        dy = 0 if index == 0 else line_height
        lines.append(
            f'{indent}  <tspan x="{x:g}" dy="{dy:g}">{_esc(value)}</tspan>'
        )
    lines.append(f"{indent}</text>")


def _header(
    lines: list[str], width: int, title: str, subtitle: str, note: str = ""
) -> int:
    margin = 36
    lines.append(f'  <text x="{margin}" y="46" class="title">{_esc(title)}</text>')
    subtitle_lines = wrap_text(subtitle, width - 2 * margin, 15)
    _text_block(lines, subtitle_lines, margin, 74, "subtitle", 19)
    cursor = 74 + (len(subtitle_lines) - 1) * 19 + 22
    if note:
        note_lines = wrap_text(note, width - 2 * margin, 12)
        _text_block(lines, note_lines, margin, cursor, "small", 16)
        cursor += len(note_lines) * 16 + 8
    return cursor


def _landscape_card_model(facet: Mapping[str, object], width: int) -> dict[str, object]:
    inner = width - 32
    label = wrap_text(facet.get("label"), inner, 15)
    key = wrap_text(str(facet.get("key", "")).replace("_", " · "), inner, 12)
    question = wrap_text(facet.get("question"), inner, 14)
    height = 18 + len(label) * 19 + 4 + len(key) * 15 + 9 + len(question) * 18 + 17
    return {"facet": facet, "label": label, "key": key, "question": question, "height": height}


def render_landscape(catalog: Mapping[str, object]) -> str:
    groups = build_landscape_groups(catalog)
    width, margin, gap, columns = 1200, 36, 14, 3
    inner_width = width - 2 * margin
    card_width = (inner_width - 2 * gap) // columns
    group_models: list[dict[str, object]] = []
    for group in groups:
        facets = [
            _landscape_card_model(facet, card_width)
            for facet in _sequence(group.get("facets"))
            if isinstance(facet, Mapping)
        ]
        definition = wrap_text(group.get("definition"), inner_width - 36, 13)
        relation = wrap_text(f"Group predicate: {group.get('relation', '')}.", inner_width - 36, 12)
        rows: list[list[dict[str, object]]] = [
            facets[index : index + columns] for index in range(0, len(facets), columns)
        ]
        row_heights = [max(int(card["height"]) for card in row) for row in rows]
        header_height = 42 + len(definition) * 17 + len(relation) * 16
        group_height = header_height + sum(row_heights) + gap * max(0, len(rows) - 1) + 22
        group_models.append(
            {
                "group": group,
                "definition": definition,
                "relation": relation,
                "rows": rows,
                "row_heights": row_heights,
                "header_height": header_height,
                "height": group_height,
            }
        )

    header_probe: list[str] = []
    top = _header(
        header_probe,
        width,
        "Kernel Agent Functional Landscape",
        "Question: which distinct questions define the catalog data model, and what semantic role does each question play?",
        "Ontology view only: containment is semantic grouping; there is no time, rank, causality, maturity, or representative-system selection.",
    )
    footer_lines = wrap_text(
        "All facet families come from schema/vocab.yaml. Multi-label evidence and coverage belong to the Field Map; chronology belongs to the complete Timeline.",
        inner_width,
        12,
    )
    height = top + sum(int(model["height"]) + 18 for model in group_models) + len(footer_lines) * 16 + 24
    lines = _svg_start(
        width,
        height,
        "Kernel Agent Functional Landscape",
        "Ontology grouping every catalog facet family by its declared semantic role. It encodes only containment and includes no selected systems or empirical edges.",
    )
    y = _header(
        lines,
        width,
        "Kernel Agent Functional Landscape",
        "Question: which distinct questions define the catalog data model, and what semantic role does each question play?",
        "Ontology view only: containment is semantic grouping; there is no time, rank, causality, maturity, or representative-system selection.",
    )
    for model in group_models:
        group = model["group"]
        assert isinstance(group, Mapping)
        group_key = str(group.get("key"))
        color, light = GROUP_COLORS[group_key]
        group_height = int(model["height"])
        lines.extend(
            [
                f'  <g id="landscape-{_esc(group_key)}" data-role="landscape-group">',
                f'    <rect x="{margin}" y="{y}" width="{inner_width}" height="{group_height}" rx="14" fill="{light}" stroke="{color}" stroke-width="2"/>',
                f'    <text x="{margin + 18}" y="{y + 29}" class="group-title" fill="{color}">{_esc(group.get("label"))}</text>',
            ]
        )
        cursor = y + 52
        definition = model["definition"]
        assert isinstance(definition, list)
        _text_block(lines, definition, margin + 18, cursor, "body", 17, indent="    ")
        cursor += len(definition) * 17 + 2
        relation = model["relation"]
        assert isinstance(relation, list)
        _text_block(lines, relation, margin + 18, cursor, "small", 16, indent="    ")
        card_y = y + int(model["header_height"])
        rows = model["rows"]
        row_heights = model["row_heights"]
        assert isinstance(rows, list) and isinstance(row_heights, list)
        for row, row_height in zip(rows, row_heights):
            for column, card in enumerate(row):
                facet = card["facet"]
                assert isinstance(facet, Mapping)
                x = margin + column * (card_width + gap)
                lines.extend(
                    [
                        f'    <g id="landscape-facet-{_esc(facet.get("key"))}" data-role="facet-card">',
                        f'      <rect x="{x}" y="{card_y}" width="{card_width}" height="{row_height}" rx="10" fill="{CARD}" stroke="{color}"/>',
                        f'      <rect x="{x}" y="{card_y}" width="6" height="{row_height}" rx="3" fill="{color}"/>',
                    ]
                )
                text_y = card_y + 25
                _text_block(lines, card["label"], x + 18, text_y, "label", 19, indent="      ")
                text_y += len(card["label"]) * 19 + 2
                _text_block(lines, card["key"], x + 18, text_y, "small", 15, indent="      ")
                text_y += len(card["key"]) * 15 + 7
                _text_block(lines, card["question"], x + 18, text_y, "body", 18, indent="      ")
                lines.append("    </g>")
            card_y += int(row_height) + gap
        lines.append("  </g>")
        y += group_height + 18
    _text_block(lines, footer_lines, margin, y + 1, "small", 16)
    return _finish(lines)


def _timeline_model(catalog: Mapping[str, object], content_width: int) -> list[dict[str, object]]:
    agents = catalog_agents(catalog)
    by_month: dict[str, list[Mapping[str, object]]] = defaultdict(list)
    for entry in agents:
        by_month[str(entry.get("date"))].append(entry)
    columns, gap = 3, 18
    cell_width = (content_width - 36 - gap * (columns - 1)) // columns
    result: list[dict[str, object]] = []
    for month, raw_entries in sorted(by_month.items()):
        entries = sorted(
            raw_entries,
            key=lambda entry: (str(entry.get("name")).casefold(), str(entry.get("id"))),
        )
        wrapped = [wrap_text(entry.get("name"), cell_width - 8, 14) for entry in entries]
        rows = [
            list(zip(entries[index : index + columns], wrapped[index : index + columns]))
            for index in range(0, len(entries), columns)
        ]
        row_heights = [max(len(name_lines) for _, name_lines in row) * 18 + 12 for row in rows]
        result.append(
            {
                "month": month,
                "entries": entries,
                "rows": rows,
                "row_heights": row_heights,
                "height": 48 + sum(row_heights) + 12,
                "cell_width": cell_width,
            }
        )
    return result


def render_timeline(catalog: Mapping[str, object]) -> str:
    agents = catalog_agents(catalog)
    width, margin = 1200, 36
    axis_x, content_x = 118, 142
    content_width = width - content_x - margin
    months = _timeline_model(catalog, content_width)
    probe: list[str] = []
    top = _header(
        probe,
        width,
        "Complete Kernel Agent Timeline",
        f"All {len(agents)} systems, grouped by first-public-release month; months are chronological and names are sorted by name then stable ID.",
        "Complete index: no milestone, importance, popularity, citation, or representative-system filtering.",
    )
    height = top + sum(int(month["height"]) + 12 for month in months) + 28
    lines = _svg_start(
        width,
        height,
        "Complete Kernel Agent Timeline",
        f"All {len(agents)} Agent systems grouped by first-public-release month in chronological order; no selection is used.",
    )
    y = _header(
        lines,
        width,
        "Complete Kernel Agent Timeline",
        f"All {len(agents)} systems, grouped by first-public-release month; months are chronological and names are sorted by name then stable ID.",
        "Complete index: no milestone, importance, popularity, citation, or representative-system filtering.",
    )
    lines.append(
        f'  <line x1="{axis_x}" y1="{y}" x2="{axis_x}" y2="{height - 24}" stroke="{BLUE_MID}" stroke-width="3"/>'
    )
    for month_index, month in enumerate(months):
        block_height = int(month["height"])
        fill = CARD if month_index % 2 == 0 else "#f1f5f9"
        month_name = str(month["month"])
        entries = month["entries"]
        assert isinstance(entries, list)
        lines.extend(
            [
                f'  <g id="timeline-month-{_esc(month_name)}" data-role="timeline-month">',
                f'    <rect x="{content_x}" y="{y}" width="{content_width}" height="{block_height}" rx="10" fill="{fill}" stroke="{LINE}"/>',
                f'    <circle cx="{axis_x}" cy="{y + 22}" r="7" fill="{BLUE}"/>',
                f'    <text x="{axis_x - 14}" y="{y + 27}" text-anchor="end" class="label">{_esc(month_name)}</text>',
                f'    <text x="{content_x + 18}" y="{y + 27}" class="small">{len(entries)} system{"s" if len(entries) != 1 else ""}</text>',
            ]
        )
        row_y = y + 51
        cell_width = int(month["cell_width"])
        rows = month["rows"]
        row_heights = month["row_heights"]
        assert isinstance(rows, list) and isinstance(row_heights, list)
        for row, row_height in zip(rows, row_heights):
            for column, (entry, name_lines) in enumerate(row):
                name_x = content_x + 18 + column * (cell_width + 18)
                lines.append(f'    <g id="timeline-{_esc(entry.get("id"))}" data-role="timeline-entry">')
                _text_block(lines, name_lines, name_x, row_y, "body", 18, indent="      ")
                lines.append("    </g>")
            row_y += int(row_height)
        lines.append("  </g>")
        y += block_height + 12
    return _finish(lines)


def _field_card_model(dimension: Mapping[str, object], width: int) -> dict[str, object]:
    inner = width - 32
    label = wrap_text(dimension.get("label"), inner, 16)
    question = wrap_text(dimension.get("question"), inner, 14)
    facets: list[tuple[Mapping[str, object], list[str]]] = []
    for facet in _sequence(dimension.get("facets")):
        if not isinstance(facet, Mapping):
            continue
        detail = f"{facet.get('label')}: {facet.get('tagged')}/{facet.get('total')} tagged"
        facets.append((facet, wrap_text(detail, inner, 12)))
    height = (
        18
        + len(label) * 20
        + 7
        + len(question) * 18
        + 12
        + sum(len(lines) * 16 + 3 for _, lines in facets)
        + 54
    )
    return {"dimension": dimension, "label": label, "question": question, "facets": facets, "height": height}


def render_field_map(catalog: Mapping[str, object]) -> str:
    dimensions = build_presentation_model(catalog)
    total = len(catalog_agents(catalog))
    width, margin, gap, columns = 1200, 36, 14, 3
    inner_width = width - 2 * margin
    card_width = (inner_width - gap * (columns - 1)) // columns
    cards = [_field_card_model(dimension, card_width) for dimension in dimensions]
    rows = [cards[index : index + columns] for index in range(0, len(cards), columns)]
    row_heights = [max(int(card["height"]) for card in row) for row in rows]
    probe: list[str] = []
    top = _header(
        probe,
        width,
        "Field Map: nine-dimension evidence projection",
        "Question: along which major dimensions can Kernel Agent systems be understood and compared, and where does the catalog contain positive evidence?",
        f"All {total} Agent entries are the denominator. Each card is a union of explicitly mapped detailed facets; multi-label counts are inclusive and empty means unannotated, not absent.",
    )
    footer = wrap_text(
        "This projection partitions every detailed facet family exactly once. Complete controlled values, boundaries, system reverse links, and primary sources: reports/field-map.md.",
        inner_width,
        12,
    )
    height = top + sum(row_heights) + gap * max(0, len(rows) - 1) + len(footer) * 16 + 36
    lines = _svg_start(
        width,
        height,
        "Kernel Agent Evidence Field Map",
        f"A complete nine-dimension presentation projection over all {total} Agent systems. It selects no facets or representative systems.",
    )
    y = _header(
        lines,
        width,
        "Field Map: nine-dimension evidence projection",
        "Question: along which major dimensions can Kernel Agent systems be understood and compared, and where does the catalog contain positive evidence?",
        f"All {total} Agent entries are the denominator. Each card is a union of explicitly mapped detailed facets; multi-label counts are inclusive and empty means unannotated, not absent.",
    )
    for row, row_height in zip(rows, row_heights):
        for column, card in enumerate(row):
            dimension = card["dimension"]
            assert isinstance(dimension, Mapping)
            x = margin + column * (card_width + gap)
            key = str(dimension.get("key"))
            lines.extend(
                [
                    f'  <g id="field-map-{_esc(key)}" data-role="presentation-dimension">',
                    f'    <rect x="{x}" y="{y}" width="{card_width}" height="{row_height}" rx="12" fill="{CARD}" stroke="{BLUE_MID}"/>',
                    f'    <rect x="{x}" y="{y}" width="6" height="{row_height}" rx="3" fill="{BLUE}"/>',
                ]
            )
            cursor = y + 27
            _text_block(lines, card["label"], x + 18, cursor, "group-title", 20, indent="    ")
            cursor += len(card["label"]) * 20 + 3
            _text_block(lines, card["question"], x + 18, cursor, "body", 18, indent="    ")
            cursor += len(card["question"]) * 18 + 8
            facets = card["facets"]
            assert isinstance(facets, list)
            for facet, detail_lines in facets:
                _text_block(lines, detail_lines, x + 18, cursor, "small", 16, indent="    ")
                cursor += len(detail_lines) * 16 + 3
            cursor += 4
            tagged = int(dimension.get("tagged", 0))
            bar_width = card_width - 36
            fill_width = 0 if tagged == 0 else max(3, round(bar_width * tagged / max(total, 1)))
            lines.extend(
                [
                    f'    <rect x="{x + 18}" y="{cursor}" width="{bar_width}" height="12" rx="4" fill="{BLUE_LIGHT}"/>',
                    f'    <rect x="{x + 18}" y="{cursor}" width="{fill_width}" height="12" rx="4" fill="{BLUE}"/>',
                    f'    <text x="{x + 18}" y="{cursor + 32}" class="small">Union evidence {tagged}/{total} · used values {dimension.get("used_values")}/{dimension.get("controlled_values")}</text>',
                ]
            )
            lines.append("  </g>")
        y += int(row_height) + gap
    _text_block(lines, footer, margin, y + 4, "small", 16)
    return _finish(lines)


def render_baseline_distribution(catalog: Mapping[str, object]) -> str:
    counts = baseline_counts(catalog)
    width, margin, row_height = 1200, 36, 44
    total = sum(counts.values())
    max_count = max([counts.get(tier, 0) for tier in TIERS] + [1])
    probe: list[str] = []
    chart_y = _header(
        probe,
        width,
        "Baseline Distribution",
        f"{total} structured claims; T0–T6 classify implementation baseline provenance/specialization, not a strict performance ordering.",
        "Unknown = implementation tier unresolved. N/A = implementation-tier model does not apply. The generator never infers a tier from a product or library name.",
    )
    height = chart_y + len(TIERS) * row_height + 30
    lines = _svg_start(
        width,
        height,
        "Claim Baseline Distribution",
        "Counts of structured numerical claims by implementation baseline tier T0 through T6, unresolved tier, and tier-not-applicable state.",
    )
    chart_y = _header(
        lines,
        width,
        "Baseline Distribution",
        f"{total} structured claims; T0–T6 classify implementation baseline provenance/specialization, not a strict performance ordering.",
        "Unknown = implementation tier unresolved. N/A = implementation-tier model does not apply. The generator never infers a tier from a product or library name.",
    )
    label_x, chart_x, chart_width, count_x = 168, 190, 840, 1060
    for index, tier in enumerate(TIERS):
        y = chart_y + index * row_height
        count = counts.get(tier, 0)
        bar_width = round(chart_width * count / max_count)
        label = {"unknown": "Unknown", "not-applicable": "N/A"}.get(tier, tier)
        color = UNKNOWN if tier == "unknown" else NOT_APPLICABLE if tier == "not-applicable" else BLUE
        lines.extend(
            [
                f'  <g id="baseline-{_esc(tier)}" data-role="baseline-state">',
                f'    <text x="{label_x}" y="{y + 18}" text-anchor="end" class="label">{label}</text>',
                f'    <rect x="{chart_x}" y="{y}" width="{chart_width}" height="24" rx="6" fill="{BLUE_LIGHT}"/>',
                f'    <rect x="{chart_x}" y="{y}" width="{bar_width}" height="24" rx="6" fill="{color}"/>',
                f'    <text x="{count_x}" y="{y + 18}" class="body">{count}</text>',
                "  </g>",
            ]
        )
    return _finish(lines)


def render_svgs(catalog: Mapping[str, object]) -> dict[str, str]:
    return {
        "assets/landscape.svg": render_landscape(catalog),
        "assets/timeline.svg": render_timeline(catalog),
        "assets/field-map.svg": render_field_map(catalog),
        "assets/baseline-distribution.svg": render_baseline_distribution(catalog),
    }
