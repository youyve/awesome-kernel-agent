"""Structural and semantic validation for the v2 research catalog.

The repository intentionally avoids a runtime dependency on ``jsonschema``.
``schema/agents.schema.json`` remains the portable schema for editors and
downstream consumers; this module implements the same contract plus semantic
checks that JSON Schema cannot conveniently express.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import re
from typing import Any, Iterable, Mapping
from urllib.parse import urlsplit

from .loader import ROOT, load_vocab


DEFAULT_ID_MANIFEST = ROOT / "schema" / "v1-entry-ids.txt"

ENTRY_REQUIRED = {
    "id", "name", "organization", "date", "entry_type", "status",
    "summary", "caveats", "taxonomy", "representations", "hardware",
    "links", "artifacts", "claims", "primary_claim",
}
ENTRY_ALLOWED = ENTRY_REQUIRED | {"migration_review"}
LINK_TYPES = {"paper", "code", "article", "project", "artifact", "model", "dataset"}
ARTIFACT_TYPES = {
    "implementation", "generated_kernels", "harness", "model_weights", "trajectories"
}
CLAIM_REQUIRED = {
    "id", "metric", "value", "unit", "aggregation", "qualifier", "workload",
    "hardware", "scope", "baseline", "budget", "reproducibility",
    "primary_source", "caveats",
}
LEGACY_FIELDS = {
    "route", "dsl", "dsl_also", "claim_baseline", "ships_kernels",
    "budget_disclosed", "evaluated_on", "code", "paper", "blog", "desc", "note",
    "org",
}
# Stable v1 IDs are lowercase slug identifiers. One preserved ID
# (qwen3.7-max-kernel-opt) contains a dot, so v2 explicitly supports both
# hyphen- and dot-separated segments without permitting arbitrary punctuation.
ID_RE = re.compile(r"^[a-z0-9]+(?:[.-][a-z0-9]+)*$")
TIER_KINDS = {
    "T0": {"framework-reference"},
    "T1": {"compiler-generated", "compiler-default"},
    "T2": {"vendor-library"},
    "T3": {"expert-implementation"},
    "T4": {"production-incumbent"},
    "T5": {"best-known"},
    "T6": {"hardware-ceiling"},
    "unknown": {
        "unresolved-implementation",
        "prior-agent",
        "self-baseline",
    },
    "not-applicable": {
        "none",
        "ablation",
        "prior-agent",
        "self-baseline",
        "evaluation-reference",
    },
}
IMPLEMENTATION_PERFORMANCE_METRICS = {
    "speedup",
    "latency",
    "throughput",
    "efficiency",
    "fraction-of-ceiling",
    "energy-reduction",
    "time-reduction",
}
RELATIONAL_BASELINE_KINDS = {"prior-agent", "self-baseline"}
METRIC_UNITS = {
    "speedup": {"x", "percent", "unknown"},
    "latency": {"milliseconds", "microseconds", "seconds", "unknown"},
    "throughput": {"x", "percent", "tokens", "count", "unknown"},
    "correctness": {"percent", "ratio", "count", "unknown"},
    "accuracy": {"percent", "ratio", "unknown"},
    "pass-rate": {"percent", "ratio", "unknown"},
    "compilation-rate": {"percent", "ratio", "unknown"},
    "coverage": {"percent", "ratio", "count", "unknown"},
    "win-rate": {"percent", "ratio", "count", "unknown"},
    "efficiency": {"percent", "ratio", "unknown"},
    "fraction-of-ceiling": {"percent", "ratio", "unknown"},
    "energy-reduction": {"percent", "ratio", "unknown"},
    "time-reduction": {"percent", "ratio", "unknown"},
    "token-reduction": {"percent", "ratio", "unknown"},
    "cost": {"usd", "unknown"},
    "count": {"count", "unknown"},
}


class ValidationError(ValueError):
    """Raised by :func:`validate_or_raise` when validation fails."""

    def __init__(self, errors: Iterable[str]):
        self.errors = list(errors)
        super().__init__(f"{len(self.errors)} catalog validation error(s)")


def _is_mapping(value: Any) -> bool:
    return isinstance(value, Mapping)


def _sequence(value: Any) -> list[Any]:
    return list(value) if isinstance(value, list) else []


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _check_exact_keys(
    value: Any,
    required: set[str],
    allowed: set[str],
    path: str,
    errors: list[str],
) -> bool:
    if not _is_mapping(value):
        errors.append(f"{path}: must be a mapping")
        return False
    keys = set(value)
    for key in sorted(required - keys):
        errors.append(f"{path}: missing required field '{key}'")
    for key in sorted(keys - allowed):
        errors.append(f"{path}: unknown field '{key}'")
    return not (required - keys)


def _check_nonempty_string(value: Any, path: str, errors: list[str]) -> bool:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{path}: must be a non-empty string")
        return False
    return True


def _check_enum(
    value: Any, choices: set[str], path: str, errors: list[str]
) -> bool:
    if not isinstance(value, str):
        errors.append(f"{path}: must be a string")
        return False
    if value not in choices:
        errors.append(f"{path}: unknown value {value!r}; expected one of {sorted(choices)}")
        return False
    return True


def _check_unique_string_list(
    value: Any,
    path: str,
    errors: list[str],
    choices: set[str] | None = None,
) -> list[str] | None:
    if not isinstance(value, list):
        errors.append(f"{path}: must be a list")
        return None
    result: list[str] = []
    seen: set[str] = set()
    for index, item in enumerate(value):
        item_path = f"{path}[{index}]"
        if not _check_nonempty_string(item, item_path, errors):
            continue
        assert isinstance(item, str)
        if item in seen:
            errors.append(f"{path}: duplicate value {item!r}")
        seen.add(item)
        result.append(item)
        if choices is not None and item not in choices:
            errors.append(f"{item_path}: unknown controlled-vocabulary value {item!r}")
    return result


def _check_date(value: Any, fmt: str, path: str, errors: list[str]) -> bool:
    if not isinstance(value, str):
        errors.append(f"{path}: must be a string")
        return False
    try:
        parsed = datetime.strptime(value, fmt)
    except ValueError:
        errors.append(f"{path}: invalid date {value!r}; expected {fmt.replace('%', '')}")
        return False
    # strptime accepts a few non-zero-padded forms; require canonical rendering.
    if parsed.strftime(fmt) != value:
        errors.append(f"{path}: date must use canonical zero-padded form")
        return False
    return True


def _check_url(value: Any, path: str, errors: list[str]) -> bool:
    if not isinstance(value, str):
        errors.append(f"{path}: must be an HTTPS URL string")
        return False
    parts = urlsplit(value)
    if parts.scheme != "https" or not parts.netloc or any(char.isspace() for char in value):
        errors.append(f"{path}: must be an absolute HTTPS URL, got {value!r}")
        return False
    return True


def _vocab_keys(vocab: Mapping[str, Any], key: str) -> set[str]:
    values = vocab.get(key, {})
    return set(values) if _is_mapping(values) else set()


def _validate_link(
    link: Any,
    path: str,
    provenance: set[str],
    errors: list[str],
) -> str | None:
    if not _check_exact_keys(link, {"label", "url", "provenance"}, {"label", "url", "provenance"}, path, errors):
        return None
    _check_nonempty_string(link.get("label"), f"{path}.label", errors)
    valid_url = _check_url(link.get("url"), f"{path}.url", errors)
    _check_enum(link.get("provenance"), provenance, f"{path}.provenance", errors)
    return link.get("url") if valid_url else None


def _validate_links(
    links: Any, path: str, vocab: Mapping[str, Any], errors: list[str]
) -> set[str]:
    if not _check_exact_keys(links, LINK_TYPES, LINK_TYPES, path, errors):
        return set()
    provenance = _vocab_keys(vocab, "link_provenance")
    all_urls: set[str] = set()
    link_count = 0
    for link_type in sorted(LINK_TYPES):
        items = links.get(link_type)
        item_path = f"{path}.{link_type}"
        if not isinstance(items, list):
            errors.append(f"{item_path}: must be a list")
            continue
        seen_urls: set[str] = set()
        for index, link in enumerate(items):
            link_count += 1
            url = _validate_link(link, f"{item_path}[{index}]", provenance, errors)
            if url is None:
                continue
            if url in seen_urls:
                errors.append(f"{item_path}: duplicate URL {url!r}")
            seen_urls.add(url)
            all_urls.add(url)
    if link_count == 0:
        errors.append(f"{path}: at least one typed link is required")
    return all_urls


def _validate_artifacts(
    artifacts: Any,
    path: str,
    statuses: set[str],
    link_urls: set[str],
    errors: list[str],
) -> None:
    if not _check_exact_keys(artifacts, ARTIFACT_TYPES, ARTIFACT_TYPES, path, errors):
        return
    for artifact_type in sorted(ARTIFACT_TYPES):
        state = artifacts.get(artifact_type)
        state_path = f"{path}.{artifact_type}"
        if not _check_exact_keys(state, {"status", "urls"}, {"status", "urls"}, state_path, errors):
            continue
        status_ok = _check_enum(state.get("status"), statuses, f"{state_path}.status", errors)
        urls = state.get("urls")
        if not isinstance(urls, list):
            errors.append(f"{state_path}.urls: must be a list")
            continue
        seen: set[str] = set()
        for index, url in enumerate(urls):
            if _check_url(url, f"{state_path}.urls[{index}]", errors):
                if url in seen:
                    errors.append(f"{state_path}.urls: duplicate URL {url!r}")
                seen.add(url)
                if url not in link_urls:
                    errors.append(
                        f"{state_path}.urls[{index}]: URL must also appear in the entry's typed links"
                    )
        if status_ok:
            status = state.get("status")
            if status in {"yes", "partial"} and not urls:
                errors.append(f"{state_path}: status {status!r} requires at least one URL")
            if status in {"no", "unknown"} and urls:
                errors.append(f"{state_path}: status {status!r} must not carry URLs")


def _validate_value(value: Any, path: str, errors: list[str]) -> None:
    if value == "unknown" and isinstance(value, str):
        return
    if _is_number(value):
        return
    if _is_mapping(value):
        if not _check_exact_keys(value, {"min", "max"}, {"min", "max"}, path, errors):
            return
        low, high = value.get("min"), value.get("max")
        if not _is_number(low):
            errors.append(f"{path}.min: must be a number")
        if not _is_number(high):
            errors.append(f"{path}.max: must be a number")
        if _is_number(low) and _is_number(high) and low > high:
            errors.append(f"{path}: range min must be <= max")
        return
    errors.append(f"{path}: must be a number, {{min, max}}, or 'unknown'")


def _validate_evidence(evidence: Any, path: str, errors: list[str]) -> bool:
    if evidence is None:
        return False
    if not _check_exact_keys(evidence, {"url", "as_of"}, {"url", "as_of"}, path, errors):
        return False
    url_ok = _check_url(evidence.get("url"), f"{path}.url", errors)
    date_ok = _check_date(evidence.get("as_of"), "%Y-%m-%d", f"{path}.as_of", errors)
    return url_ok and date_ok


def _validate_claim(
    claim: Any,
    path: str,
    vocab: Mapping[str, Any],
    entry_link_urls: set[str],
    cutoff: str | None,
    errors: list[str],
) -> str | None:
    if not _check_exact_keys(claim, CLAIM_REQUIRED, CLAIM_REQUIRED, path, errors):
        return None

    claim_id = claim.get("id")
    if not isinstance(claim_id, str) or not ID_RE.fullmatch(claim_id):
        errors.append(f"{path}.id: must be a lowercase stable slug identifier")
        claim_id = None

    metric = claim.get("metric")
    metric_valid = _check_enum(metric, _vocab_keys(vocab, "claim_metrics"), f"{path}.metric", errors)
    _validate_value(claim.get("value"), f"{path}.value", errors)
    unit = claim.get("unit")
    unit_valid = _check_enum(unit, _vocab_keys(vocab, "claim_units"), f"{path}.unit", errors)
    aggregation = claim.get("aggregation")
    aggregation_valid = _check_enum(
        aggregation,
        _vocab_keys(vocab, "claim_aggregations"),
        f"{path}.aggregation",
        errors,
    )
    if metric_valid and unit_valid and metric in METRIC_UNITS and unit not in METRIC_UNITS[metric]:
        errors.append(
            f"{path}: metric {metric!r} is incompatible with unit {unit!r}; "
            f"expected one of {sorted(METRIC_UNITS[metric])}"
        )
    is_range = isinstance(claim.get("value"), Mapping)
    if aggregation_valid and is_range and aggregation != "range":
        errors.append(f"{path}: a range value requires aggregation 'range'")
    if aggregation_valid and aggregation == "range" and not is_range:
        errors.append(f"{path}: aggregation 'range' requires a {{min, max}} value")
    if not isinstance(claim.get("qualifier"), str):
        errors.append(f"{path}.qualifier: must be a string")

    workload = claim.get("workload")
    if _check_exact_keys(workload, {"benchmark", "subset"}, {"benchmark", "subset"}, f"{path}.workload", errors):
        _check_nonempty_string(workload.get("benchmark"), f"{path}.workload.benchmark", errors)
        if not isinstance(workload.get("subset"), str):
            errors.append(f"{path}.workload.subset: must be a string")
    _check_nonempty_string(claim.get("hardware"), f"{path}.hardware", errors)
    _check_enum(claim.get("scope"), _vocab_keys(vocab, "claim_scopes"), f"{path}.scope", errors)

    baseline = claim.get("baseline")
    tier: Any = None
    if _check_exact_keys(
        baseline,
        {"tier", "kind", "name", "evidence"},
        {"tier", "kind", "name", "evidence"},
        f"{path}.baseline",
        errors,
    ):
        tier = baseline.get("tier")
        _check_enum(tier, _vocab_keys(vocab, "baseline_tiers"), f"{path}.baseline.tier", errors)
        kind = baseline.get("kind")
        kind_valid = _check_enum(
            kind,
            _vocab_keys(vocab, "baseline_kinds"),
            f"{path}.baseline.kind",
            errors,
        )
        _check_nonempty_string(baseline.get("name"), f"{path}.baseline.name", errors)
        evidence_valid = _validate_evidence(baseline.get("evidence"), f"{path}.baseline.evidence", errors)
        if tier in TIER_KINDS and kind_valid and kind not in TIER_KINDS[tier]:
            errors.append(
                f"{path}.baseline: tier {tier} is inconsistent with kind {kind!r}; "
                f"expected one of {sorted(TIER_KINDS[tier])}"
            )
        if (
            tier == "not-applicable"
            and kind in RELATIONAL_BASELINE_KINDS
            and metric in IMPLEMENTATION_PERFORMANCE_METRICS
        ):
            errors.append(
                f"{path}.baseline: {metric!r} against {kind!r} has a real "
                "implementation denominator; use tier 'unknown' unless T0-T6 "
                "can be evidenced"
            )
        if tier == "T5" and not evidence_valid:
            errors.append(f"{path}.baseline: T5 requires dated external evidence with URL and as_of")
        if evidence_valid and cutoff is not None and baseline["evidence"]["as_of"] > cutoff:
            errors.append(
                f"{path}.baseline.evidence.as_of: falls after research_cutoff {cutoff}"
            )
        if tier == "T6" and claim.get("metric") not in {"efficiency", "fraction-of-ceiling"}:
            errors.append(
                f"{path}: T6 claims must use efficiency or fraction-of-ceiling, not {claim.get('metric')!r}"
            )

    budget = claim.get("budget")
    if _check_exact_keys(budget, {"status", "details"}, {"status", "details"}, f"{path}.budget", errors):
        budget_status_ok = _check_enum(
            budget.get("status"),
            _vocab_keys(vocab, "evidence_statuses"),
            f"{path}.budget.status",
            errors,
        )
        details = budget.get("details")
        if not isinstance(details, str):
            errors.append(f"{path}.budget.details: must be a string")
        elif budget_status_ok and budget.get("status") in {"yes", "partial"} and not details.strip():
            errors.append(f"{path}.budget: status {budget.get('status')!r} requires details")

    reproducibility = claim.get("reproducibility")
    if _check_exact_keys(
        reproducibility,
        {"claim_linked_artifact", "artifact_url"},
        {"claim_linked_artifact", "artifact_url"},
        f"{path}.reproducibility",
        errors,
    ):
        artifact_status_ok = _check_enum(
            reproducibility.get("claim_linked_artifact"),
            _vocab_keys(vocab, "evidence_statuses"),
            f"{path}.reproducibility.claim_linked_artifact",
            errors,
        )
        artifact_url = reproducibility.get("artifact_url")
        status = reproducibility.get("claim_linked_artifact")
        if artifact_status_ok and status in {"yes", "partial"}:
            if artifact_url is None:
                errors.append(
                    f"{path}.reproducibility: claim-linked artifact {status!r} requires artifact_url"
                )
            else:
                artifact_url_ok = _check_url(
                    artifact_url,
                    f"{path}.reproducibility.artifact_url",
                    errors,
                )
                if artifact_url_ok and artifact_url not in entry_link_urls:
                    errors.append(
                        f"{path}.reproducibility.artifact_url: URL must also appear "
                        "in the entry's typed links"
                    )
        elif artifact_status_ok and status in {"no", "unknown"} and artifact_url is not None:
            errors.append(
                f"{path}.reproducibility: claim-linked artifact {status!r} requires artifact_url=null"
            )

    source = claim.get("primary_source")
    if _check_exact_keys(source, {"url", "locator"}, {"url", "locator"}, f"{path}.primary_source", errors):
        if _check_url(source.get("url"), f"{path}.primary_source.url", errors):
            if source.get("url") not in entry_link_urls:
                errors.append(
                    f"{path}.primary_source.url: URL must also appear in the entry's typed links"
                )
        if not isinstance(source.get("locator"), str):
            errors.append(f"{path}.primary_source.locator: must be a string")

    _check_unique_string_list(claim.get("caveats"), f"{path}.caveats", errors)
    return claim_id


def _validate_review(value: Any, path: str, errors: list[str]) -> None:
    if not isinstance(value, list):
        errors.append(f"{path}: must be a list")
        return
    seen: set[tuple[str, str]] = set()
    for index, item in enumerate(value):
        item_path = f"{path}[{index}]"
        if not _check_exact_keys(item, {"field", "issue"}, {"field", "issue"}, item_path, errors):
            continue
        field_ok = _check_nonempty_string(item.get("field"), f"{item_path}.field", errors)
        issue_ok = _check_nonempty_string(item.get("issue"), f"{item_path}.issue", errors)
        if field_ok and issue_ok:
            key = (item["field"], item["issue"])
            if key in seen:
                errors.append(f"{path}: duplicate migration-review item {key!r}")
            seen.add(key)


def _validate_entry(
    entry: Any,
    index: int,
    vocab: Mapping[str, Any],
    cutoff: str | None,
    errors: list[str],
) -> str | None:
    path = f"agents[{index}]"
    if not _is_mapping(entry):
        errors.append(f"{path}: must be a mapping")
        return None

    for field in sorted(set(entry) & LEGACY_FIELDS):
        errors.append(f"{path}.{field}: legacy v1 field is forbidden")
    _check_exact_keys(entry, ENTRY_REQUIRED, ENTRY_ALLOWED, path, errors)

    entry_id = entry.get("id")
    if not isinstance(entry_id, str) or not ID_RE.fullmatch(entry_id):
        errors.append(f"{path}.id: must be a lowercase stable slug identifier")
        entry_id = None
    _check_nonempty_string(entry.get("name"), f"{path}.name", errors)
    _check_nonempty_string(entry.get("organization"), f"{path}.organization", errors)
    date_ok = _check_date(entry.get("date"), "%Y-%m", f"{path}.date", errors)
    cutoff_month = cutoff[:7] if cutoff is not None else None
    if date_ok and cutoff_month is not None and entry.get("date") > cutoff_month:
        errors.append(f"{path}.date: falls after research_cutoff {cutoff_month}")
    _check_enum(entry.get("entry_type"), _vocab_keys(vocab, "entry_types"), f"{path}.entry_type", errors)
    _check_enum(entry.get("status"), _vocab_keys(vocab, "statuses"), f"{path}.status", errors)
    _check_nonempty_string(entry.get("summary"), f"{path}.summary", errors)
    _check_unique_string_list(entry.get("caveats"), f"{path}.caveats", errors)

    taxonomy = entry.get("taxonomy")
    vocab_taxonomy = vocab.get("taxonomy", {})
    taxonomy_dimensions = set(vocab_taxonomy) if _is_mapping(vocab_taxonomy) else set()
    if _check_exact_keys(
        taxonomy,
        taxonomy_dimensions,
        taxonomy_dimensions,
        f"{path}.taxonomy",
        errors,
    ):
        for dimension in sorted(taxonomy_dimensions):
            choices = set(vocab_taxonomy.get(dimension, {})) if _is_mapping(vocab_taxonomy) else set()
            _check_unique_string_list(
                taxonomy.get(dimension), f"{path}.taxonomy.{dimension}", errors, choices
            )
        constraints = vocab.get("facet_constraints")
        constraints = constraints if _is_mapping(constraints) else {}
        exclusive = constraints.get("mutually_exclusive")
        if _is_mapping(exclusive):
            for dimension, values in exclusive.items():
                selected = set(taxonomy.get(dimension, []))
                conflicts = selected & set(values if isinstance(values, list) else [])
                if len(conflicts) > 1:
                    errors.append(
                        f"{path}.taxonomy.{dimension}: mutually exclusive values "
                        f"cannot coexist: {sorted(conflicts)!r}"
                    )
        implications = constraints.get("implies")
        if _is_mapping(implications):
            for dimension, rules in implications.items():
                if not _is_mapping(rules):
                    continue
                selected = set(taxonomy.get(dimension, []))
                for value, required_values in rules.items():
                    required = set(required_values if isinstance(required_values, list) else [])
                    missing = required - selected
                    if value in selected and missing:
                        errors.append(
                            f"{path}.taxonomy.{dimension}: {value!r} requires "
                            f"{sorted(missing)!r}"
                        )

    _check_unique_string_list(
        entry.get("representations"),
        f"{path}.representations",
        errors,
        _vocab_keys(vocab, "representations"),
    )
    _check_unique_string_list(
        entry.get("hardware"),
        f"{path}.hardware",
        errors,
        _vocab_keys(vocab, "hardware"),
    )

    link_urls = _validate_links(entry.get("links"), f"{path}.links", vocab, errors)
    _validate_artifacts(
        entry.get("artifacts"),
        f"{path}.artifacts",
        _vocab_keys(vocab, "evidence_statuses"),
        link_urls,
        errors,
    )

    claims = entry.get("claims")
    claim_ids: set[str] = set()
    if not isinstance(claims, list):
        errors.append(f"{path}.claims: must be a list")
    else:
        for claim_index, claim in enumerate(claims):
            claim_id = _validate_claim(
                claim,
                f"{path}.claims[{claim_index}]",
                vocab,
                link_urls,
                cutoff,
                errors,
            )
            if claim_id is None:
                continue
            if claim_id in claim_ids:
                errors.append(f"{path}.claims: duplicate claim id {claim_id!r}")
            claim_ids.add(claim_id)
            if isinstance(claim, Mapping):
                claim_scope = claim.get("scope")
                taxonomy_scopes = (
                    [
                        *_sequence(taxonomy.get("workload_scope")),
                        *_sequence(taxonomy.get("integration_scope")),
                    ]
                    if isinstance(taxonomy, Mapping)
                    else None
                )
                if (
                    isinstance(claim_scope, str)
                    and claim_scope != "unknown"
                    and isinstance(taxonomy_scopes, list)
                    and claim_scope not in taxonomy_scopes
                ):
                    errors.append(
                        f"{path}.claims[{claim_index}].scope: {claim_scope!r} must also "
                        "appear in taxonomy.workload_scope or taxonomy.integration_scope"
                    )

    primary_claim = entry.get("primary_claim")
    if primary_claim is not None and not isinstance(primary_claim, str):
        errors.append(f"{path}.primary_claim: must be a claim id or null")
    elif primary_claim is not None and primary_claim not in claim_ids:
        errors.append(f"{path}.primary_claim: dangling claim id {primary_claim!r}")
    elif claim_ids and primary_claim is None:
        errors.append(f"{path}.primary_claim: must select one claim when claims are present")

    if "migration_review" in entry:
        _validate_review(entry.get("migration_review"), f"{path}.migration_review", errors)
    return entry_id


def _load_manifest(path: str | Path, errors: list[str]) -> set[str]:
    manifest = Path(path)
    try:
        lines = manifest.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        errors.append(f"id manifest: could not read {manifest}: {exc}")
        return set()
    ids: set[str] = set()
    for line_number, raw in enumerate(lines, 1):
        value = raw.strip()
        if not value or value.startswith("#"):
            continue
        if not ID_RE.fullmatch(value):
            errors.append(f"id manifest:{line_number}: invalid id {value!r}")
        if value in ids:
            errors.append(f"id manifest:{line_number}: duplicate id {value!r}")
        ids.add(value)
    if not ids:
        errors.append("id manifest: contains no entry ids")
    return ids


def _validate_facet_vocab(vocab: Mapping[str, Any], errors: list[str]) -> None:
    """Validate the single-source metadata used by Landscape and Field Map."""

    taxonomy = vocab.get("taxonomy")
    if not _is_mapping(taxonomy) or not taxonomy:
        errors.append("vocab.taxonomy: must be a non-empty mapping")
        return
    dimensions = {*taxonomy, "representations", "hardware"}
    metadata = vocab.get("facet_dimensions")
    if not _is_mapping(metadata):
        errors.append("vocab.facet_dimensions: must be a mapping")
        return
    missing = dimensions - set(metadata)
    extra = set(metadata) - dimensions
    if missing:
        errors.append(f"vocab.facet_dimensions: missing dimensions {sorted(missing)!r}")
    if extra:
        errors.append(f"vocab.facet_dimensions: unknown dimensions {sorted(extra)!r}")

    groups = vocab.get("facet_groups")
    if not _is_mapping(groups) or not groups:
        errors.append("vocab.facet_groups: must be a non-empty mapping")
        groups = {}
    for group, definition in groups.items():
        path = f"vocab.facet_groups.{group}"
        if _check_exact_keys(
            definition,
            {"label", "definition", "relation"},
            {"label", "definition", "relation"},
            path,
            errors,
        ):
            for field in ("label", "definition", "relation"):
                _check_nonempty_string(definition.get(field), f"{path}.{field}", errors)

    for dimension, definition in metadata.items():
        path = f"vocab.facet_dimensions.{dimension}"
        if _check_exact_keys(
            definition,
            {"label", "question", "boundary", "group"},
            {"label", "question", "boundary", "group"},
            path,
            errors,
        ):
            for field in ("label", "question", "boundary", "group"):
                _check_nonempty_string(definition.get(field), f"{path}.{field}", errors)
            if definition.get("group") not in groups:
                errors.append(f"{path}.group: unknown facet group {definition.get('group')!r}")

    presentation = vocab.get("presentation_taxonomy")
    if not _is_mapping(presentation) or not presentation:
        errors.append("vocab.presentation_taxonomy: must be a non-empty mapping")
    else:
        projected: list[str] = []
        for key, definition in presentation.items():
            path = f"vocab.presentation_taxonomy.{key}"
            if _check_exact_keys(
                definition,
                {"label", "question", "facets"},
                {"label", "question", "facets"},
                path,
                errors,
            ):
                _check_nonempty_string(definition.get("label"), f"{path}.label", errors)
                _check_nonempty_string(definition.get("question"), f"{path}.question", errors)
                values = _check_unique_string_list(
                    definition.get("facets"), f"{path}.facets", errors, dimensions
                )
                if values is not None:
                    projected.extend(values)
        missing_projection = dimensions - set(projected)
        duplicate_projection = sorted(
            facet for facet in set(projected) if projected.count(facet) > 1
        )
        if missing_projection:
            errors.append(
                "vocab.presentation_taxonomy: facets missing from projection "
                f"{sorted(missing_projection)!r}"
            )
        if duplicate_projection:
            errors.append(
                "vocab.presentation_taxonomy: facets must appear exactly once; "
                f"duplicates {duplicate_projection!r}"
            )

    profile = vocab.get("profile_derivation")
    if not _is_mapping(profile):
        errors.append("vocab.profile_derivation: must be a mapping")
    elif _check_exact_keys(
        profile,
        {"approach_dimensions", "grounding_dimensions", "fallback_values", "suppressions"},
        {"approach_dimensions", "grounding_dimensions", "fallback_values", "suppressions"},
        "vocab.profile_derivation",
        errors,
    ):
        selected_dimensions: list[str] = []
        for field in ("approach_dimensions", "grounding_dimensions"):
            values = _check_unique_string_list(
                profile.get(field),
                f"vocab.profile_derivation.{field}",
                errors,
                set(taxonomy),
            )
            if values is not None:
                selected_dimensions.extend(values)
        duplicate_dimensions = sorted(
            dimension
            for dimension in set(selected_dimensions)
            if selected_dimensions.count(dimension) > 1
        )
        if duplicate_dimensions:
            errors.append(
                "vocab.profile_derivation: dimensions cannot occur in both slots; "
                f"duplicates {duplicate_dimensions!r}"
            )
        known_values = {
            str(value)
            for configured in taxonomy.values()
            if _is_mapping(configured)
            for value in configured
        }
        _check_unique_string_list(
            profile.get("fallback_values"),
            "vocab.profile_derivation.fallback_values",
            errors,
            known_values,
        )
        suppressions = profile.get("suppressions")
        if not _is_mapping(suppressions):
            errors.append("vocab.profile_derivation.suppressions: must be a mapping")
        else:
            for value, suppressed in suppressions.items():
                if value not in known_values:
                    errors.append(
                        "vocab.profile_derivation.suppressions: unknown source value "
                        f"{value!r}"
                    )
                _check_unique_string_list(
                    suppressed,
                    f"vocab.profile_derivation.suppressions.{value}",
                    errors,
                    known_values,
                )

    constraints = vocab.get("facet_constraints")
    if not _is_mapping(constraints):
        errors.append("vocab.facet_constraints: must be a mapping")
        return
    _check_exact_keys(
        constraints,
        {"mutually_exclusive", "implies"},
        {"mutually_exclusive", "implies"},
        "vocab.facet_constraints",
        errors,
    )
    exclusive = constraints.get("mutually_exclusive")
    if not _is_mapping(exclusive):
        errors.append("vocab.facet_constraints.mutually_exclusive: must be a mapping")
    else:
        for dimension, values in exclusive.items():
            choices = set(taxonomy.get(dimension, {})) if dimension in taxonomy else set()
            if dimension not in taxonomy:
                errors.append(f"vocab.facet_constraints.mutually_exclusive: unknown dimension {dimension!r}")
            _check_unique_string_list(
                values,
                f"vocab.facet_constraints.mutually_exclusive.{dimension}",
                errors,
                choices,
            )
    implications = constraints.get("implies")
    if not _is_mapping(implications):
        errors.append("vocab.facet_constraints.implies: must be a mapping")
    else:
        for dimension, rules in implications.items():
            choices = set(taxonomy.get(dimension, {})) if dimension in taxonomy else set()
            if dimension not in taxonomy or not _is_mapping(rules):
                errors.append(f"vocab.facet_constraints.implies.{dimension}: invalid dimension or rules")
                continue
            for value, required in rules.items():
                if value not in choices:
                    errors.append(
                        f"vocab.facet_constraints.implies.{dimension}: unknown value {value!r}"
                    )
                _check_unique_string_list(
                    required,
                    f"vocab.facet_constraints.implies.{dimension}.{value}",
                    errors,
                    choices,
                )


def validate_catalog(
    catalog: Any,
    manifest_path: str | Path | None = None,
    *,
    require_legacy_ids: bool = True,
    vocab: Mapping[str, Any] | None = None,
) -> list[str]:
    """Return every deterministic structural or semantic validation error.

    External links are checked syntactically only. Network availability belongs
    to the separate weekly audit and can never make deterministic validation fail.
    """

    errors: list[str] = []
    active_vocab = dict(vocab) if vocab is not None else load_vocab()
    _validate_facet_vocab(active_vocab, errors)

    if not _check_exact_keys(
        catalog,
        {"schema_version", "research_cutoff", "agents"},
        {"schema_version", "research_cutoff", "agents"},
        "catalog",
        errors,
    ):
        return errors
    if type(catalog.get("schema_version")) is not int or catalog.get("schema_version") != 2:
        errors.append("catalog.schema_version: must be integer 2")

    cutoff = catalog.get("research_cutoff")
    cutoff_ok = _check_date(cutoff, "%Y-%m-%d", "catalog.research_cutoff", errors)

    agents = catalog.get("agents")
    ids: set[str] = set()
    if not isinstance(agents, list):
        errors.append("catalog.agents: must be a list")
        agents = []
    elif not agents:
        errors.append("catalog.agents: must contain at least one entry")
    for index, entry in enumerate(agents):
        entry_id = _validate_entry(
            entry,
            index,
            active_vocab,
            cutoff if cutoff_ok else None,
            errors,
        )
        if entry_id is None:
            continue
        if entry_id in ids:
            errors.append(f"catalog.agents: duplicate entry id {entry_id!r}")
        ids.add(entry_id)

    claim_owners: dict[str, str] = {}
    for index, entry in enumerate(agents):
        if not isinstance(entry, Mapping) or not isinstance(entry.get("claims"), list):
            continue
        entry_id = str(entry.get("id", f"agents[{index}]"))
        for claim_index, claim in enumerate(entry["claims"]):
            if not isinstance(claim, Mapping) or not isinstance(claim.get("id"), str):
                continue
            claim_id = claim["id"]
            previous_owner = claim_owners.get(claim_id)
            if previous_owner is not None and previous_owner != entry_id:
                errors.append(
                    f"agents[{index}].claims[{claim_index}].id: duplicate catalog-wide "
                    f"claim id {claim_id!r}; already used by {previous_owner!r}"
                )
            else:
                claim_owners[claim_id] = entry_id

    if require_legacy_ids:
        legacy_ids = _load_manifest(manifest_path or DEFAULT_ID_MANIFEST, errors)
        missing = sorted(legacy_ids - ids)
        if missing:
            errors.append(
                "catalog.agents: missing v1 entry ids: " + ", ".join(missing)
            )
    return errors


def validate_or_raise(
    catalog: Any,
    manifest_path: str | Path | None = None,
    *,
    require_legacy_ids: bool = True,
    vocab: Mapping[str, Any] | None = None,
) -> None:
    """Validate a catalog and raise one aggregate :class:`ValidationError`."""

    errors = validate_catalog(
        catalog,
        manifest_path,
        require_legacy_ids=require_legacy_ids,
        vocab=vocab,
    )
    if errors:
        raise ValidationError(errors)
