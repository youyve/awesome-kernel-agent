#!/usr/bin/env python3
"""Validate the v2 catalog without regenerating repository artifacts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

try:
    from jsonschema import Draft202012Validator
    from jsonschema.exceptions import SchemaError
except ImportError as exc:  # pragma: no cover - CLI dependency failure
    raise SystemExit(
        "jsonschema is required for full validation: "
        "python3 -m pip install -r requirements-dev.txt"
    ) from exc

try:  # ``python scripts/validate.py``
    from lib.loader import CatalogLoadError, DEFAULT_CATALOG, load_catalog
    from lib.validation import DEFAULT_ID_MANIFEST, validate_catalog
except ImportError:  # ``python -m scripts.validate``
    from scripts.lib.loader import CatalogLoadError, DEFAULT_CATALOG, load_catalog
    from scripts.lib.validation import DEFAULT_ID_MANIFEST, validate_catalog


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schema" / "agents.schema.json"


def validate_json_schema(catalog: object) -> list[str]:
    """Validate the portable Draft 2020-12 schema before semantic checks."""

    try:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
    except (OSError, json.JSONDecodeError, SchemaError) as exc:
        return [f"JSON Schema: {exc}"]

    validator = Draft202012Validator(schema)
    errors: list[str] = []
    for error in sorted(
        validator.iter_errors(catalog),
        key=lambda item: tuple(str(part) for part in item.absolute_path),
    ):
        location = "$" + "".join(
            f"[{part}]" if isinstance(part, int) else f".{part}"
            for part in error.absolute_path
        )
        errors.append(f"JSON Schema {location}: {error.message}")
    return errors


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate catalog structure, controlled vocabulary, and claim semantics."
    )
    parser.add_argument(
        "path",
        nargs="?",
        type=Path,
        default=DEFAULT_CATALOG,
        help="catalog YAML path (default: data/agents.yaml)",
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=DEFAULT_ID_MANIFEST,
        help="pre-v2 ID manifest used for migration-preservation checks",
    )
    parser.add_argument(
        "--no-id-manifest",
        action="store_true",
        help="skip the pre-v2 ID preservation check (useful only for isolated fixtures)",
    )
    parser.add_argument("--quiet", action="store_true", help="suppress the success message")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        catalog = load_catalog(args.path)
    except CatalogLoadError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    errors = validate_json_schema(catalog)
    errors.extend(validate_catalog(
        catalog,
        args.manifest,
        require_legacy_ids=not args.no_id_manifest,
    ))
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"{len(errors)} validation error(s)", file=sys.stderr)
        return 1

    if not args.quiet:
        agents = catalog.get("agents", [])
        claim_count = sum(len(entry.get("claims", [])) for entry in agents)
        print(f"validated {len(agents)} entries and {claim_count} claims")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
