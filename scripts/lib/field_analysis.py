"""Shared, selection-free view model for Landscape and Field Map.

The catalog stores positive, multi-label evidence. Empty lists are therefore
reported as *unannotated*, never as evidence that an attribute is absent.
Every controlled value participates in the view model, including zero-support
values; no top-k facet or representative system selection is permitted here.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from .loader import load_vocab


EXTERNAL_FACETS = ("representations", "hardware")


def _sequence(value: object) -> list[object]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        return []
    return list(value)


def catalog_agents(catalog: Mapping[str, object]) -> list[Mapping[str, object]]:
    return [
        entry
        for entry in _sequence(catalog.get("agents"))
        if isinstance(entry, Mapping) and entry.get("entry_type") == "agent"
    ]


def facet_keys(vocab: Mapping[str, object] | None = None) -> list[str]:
    active = vocab or load_vocab()
    taxonomy = active.get("taxonomy")
    dimensions = list(taxonomy) if isinstance(taxonomy, Mapping) else []
    return [*dimensions, *EXTERNAL_FACETS]


def facet_values(entry: Mapping[str, object], facet: str) -> list[str]:
    if facet in EXTERNAL_FACETS:
        value = entry.get(facet)
    else:
        taxonomy = entry.get("taxonomy")
        value = taxonomy.get(facet) if isinstance(taxonomy, Mapping) else []
    return [str(item) for item in _sequence(value)]


def _controlled_values(vocab: Mapping[str, object], facet: str) -> Mapping[str, object]:
    if facet in EXTERNAL_FACETS:
        configured = vocab.get(facet)
    else:
        taxonomy = vocab.get("taxonomy")
        configured = taxonomy.get(facet) if isinstance(taxonomy, Mapping) else None
    return configured if isinstance(configured, Mapping) else {}


def value_label(vocab: Mapping[str, object], facet: str, value: str) -> str:
    configured = _controlled_values(vocab, facet).get(value)
    if isinstance(configured, Mapping):
        label = configured.get("label")
        return str(label) if label else value
    return str(configured) if configured else value


def build_facet_model(
    catalog: Mapping[str, object],
    vocab: Mapping[str, object] | None = None,
) -> list[dict[str, Any]]:
    """Return complete agent-level support counts for every controlled facet."""

    active = dict(vocab) if vocab is not None else load_vocab()
    agents = catalog_agents(catalog)
    metadata = active.get("facet_dimensions")
    metadata = metadata if isinstance(metadata, Mapping) else {}
    result: list[dict[str, Any]] = []
    for facet in facet_keys(active):
        definition = metadata.get(facet)
        definition = definition if isinstance(definition, Mapping) else {}
        configured = _controlled_values(active, facet)
        support: dict[str, list[Mapping[str, object]]] = {
            str(value): [] for value in configured
        }
        tagged = 0
        assignments = 0
        for entry in agents:
            values = facet_values(entry, facet)
            if values:
                tagged += 1
            assignments += len(values)
            for value in values:
                support.setdefault(value, []).append(entry)
        order = {str(value): index for index, value in enumerate(configured)}
        values = [
            {
                "key": value,
                "label": value_label(active, facet, value),
                "count": len(entries),
                "entries": entries,
            }
            for value, entries in support.items()
        ]
        values.sort(
            key=lambda item: (
                -int(item["count"]),
                order.get(str(item["key"]), len(order)),
                str(item["key"]).casefold(),
            )
        )
        result.append(
            {
                "key": facet,
                "label": str(definition.get("label", facet.replace("_", " ").title())),
                "question": str(definition.get("question", "")),
                "boundary": str(definition.get("boundary", "")),
                "group": str(definition.get("group", "")),
                "total": len(agents),
                "tagged": tagged,
                "unannotated": len(agents) - tagged,
                "assignments": assignments,
                "values": values,
            }
        )
    return result


def build_landscape_groups(
    catalog: Mapping[str, object],
    vocab: Mapping[str, object] | None = None,
) -> list[dict[str, Any]]:
    """Group every facet by its declared semantic role, preserving vocab order."""

    active = dict(vocab) if vocab is not None else load_vocab()
    configured = active.get("facet_groups")
    configured = configured if isinstance(configured, Mapping) else {}
    facets = build_facet_model(catalog, active)
    result: list[dict[str, Any]] = []
    for key, definition in configured.items():
        definition = definition if isinstance(definition, Mapping) else {}
        result.append(
            {
                "key": str(key),
                "label": str(definition.get("label", key)),
                "definition": str(definition.get("definition", "")),
                "relation": str(definition.get("relation", "")),
                "facets": [facet for facet in facets if facet["group"] == key],
            }
        )
    return result


def build_presentation_model(
    catalog: Mapping[str, object],
    vocab: Mapping[str, object] | None = None,
) -> list[dict[str, Any]]:
    """Return the complete, configured README projection of detailed facets.

    Each presentation dimension is a union over one or more evidence facets.
    The vocabulary validator guarantees that every detailed facet appears in
    exactly one union, so this view cannot silently select or omit a direction.
    """

    active = dict(vocab) if vocab is not None else load_vocab()
    configured = active.get("presentation_taxonomy")
    configured = configured if isinstance(configured, Mapping) else {}
    facets = build_facet_model(catalog, active)
    facets_by_key = {str(facet["key"]): facet for facet in facets}
    agents = catalog_agents(catalog)
    result: list[dict[str, Any]] = []
    for key, definition in configured.items():
        definition = definition if isinstance(definition, Mapping) else {}
        child_keys = [str(value) for value in _sequence(definition.get("facets"))]
        children = [facets_by_key[value] for value in child_keys if value in facets_by_key]
        tagged_entries = {
            str(entry.get("id"))
            for entry in agents
            if any(facet_values(entry, facet) for facet in child_keys)
        }
        result.append(
            {
                "key": str(key),
                "label": str(definition.get("label", key)),
                "question": str(definition.get("question", "")),
                "facets": children,
                "facet_keys": child_keys,
                "total": len(agents),
                "tagged": len(tagged_entries),
                "unannotated": len(agents) - len(tagged_entries),
                "assignments": sum(int(facet["assignments"]) for facet in children),
                "used_values": sum(
                    sum(int(value["count"]) > 0 for value in facet["values"])
                    for facet in children
                ),
                "controlled_values": sum(len(facet["values"]) for facet in children),
            }
        )
    return result
