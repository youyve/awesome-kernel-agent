#!/usr/bin/env python3
"""Generate every v2 catalog artifact from ``data/agents.yaml``.

The YAML catalog is the only factual source. This command validates it, builds
all Markdown/JSON/SVG outputs in memory, and then either writes them atomically
or compares them byte-for-byte in ``--check`` mode.

Usage:
    python3 scripts/generate.py
    python3 scripts/generate.py --check
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
from pathlib import Path

try:  # Package imports for tests and module execution.
    from .lib.loader import load_catalog
    from .lib.markdown import render_catalogs, render_readme, render_reports
    from .lib.svg import render_svgs
    from .lib.validation import validate_catalog
except ImportError:  # Direct execution: ``python3 scripts/generate.py``.
    from lib.loader import load_catalog
    from lib.markdown import render_catalogs, render_readme, render_reports
    from lib.svg import render_svgs
    from lib.validation import validate_catalog


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "agents.yaml"
TEMPLATE_DIR = ROOT / "templates"


def _read_template(name: str) -> str:
    path = TEMPLATE_DIR / name
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise SystemExit(f"missing README template: {path.relative_to(ROOT)}") from exc


def build_outputs(catalog: dict[str, object]) -> dict[str, str]:
    """Render the complete output graph without mutating the filesystem."""

    outputs = {
        "README.md": render_readme(catalog, _read_template("README.md.tmpl"), "en"),
        "README.zh.md": render_readme(catalog, _read_template("README.zh.md.tmpl"), "zh"),
        "data/agents.json": json.dumps(catalog, indent=2, ensure_ascii=False) + "\n",
    }
    outputs.update(render_catalogs(catalog))
    outputs.update(render_reports(catalog))
    outputs.update(render_svgs(catalog))
    return dict(sorted(outputs.items()))


def _stale_catalogs(expected: set[str]) -> list[Path]:
    catalog_dir = ROOT / "catalog"
    if not catalog_dir.exists():
        return []
    return sorted(
        path
        for path in catalog_dir.glob("*.md")
        if re.fullmatch(r"\d{4}\.md", path.name)
        and path.relative_to(ROOT).as_posix() not in expected
    )


def _atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(content)
        os.replace(temporary_name, path)
    except BaseException:
        try:
            os.unlink(temporary_name)
        except FileNotFoundError:
            pass
        raise


def write_outputs(outputs: dict[str, str]) -> None:
    expected = set(outputs)
    for relative_path, content in outputs.items():
        _atomic_write(ROOT / relative_path, content)
        print(f"wrote {relative_path}")
    for stale in _stale_catalogs(expected):
        stale.unlink()
        print(f"removed stale generated catalog {stale.relative_to(ROOT)}")


def check_outputs(outputs: dict[str, str]) -> list[str]:
    errors: list[str] = []
    expected = set(outputs)
    for relative_path, expected_content in outputs.items():
        path = ROOT / relative_path
        if not path.exists():
            errors.append(f"missing generated output: {relative_path}")
            continue
        actual = path.read_text(encoding="utf-8")
        if actual != expected_content:
            errors.append(f"stale generated output: {relative_path}")
    for stale in _stale_catalogs(expected):
        errors.append(f"stale generated output: {stale.relative_to(ROOT)}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="validate and compare every generated output without writing",
    )
    args = parser.parse_args()

    catalog = load_catalog(DATA_PATH)
    validation_errors = validate_catalog(catalog)
    if validation_errors:
        for error in validation_errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"{len(validation_errors)} validation error(s)", file=sys.stderr)
        return 1

    outputs = build_outputs(catalog)
    if args.check:
        generation_errors = check_outputs(outputs)
        if generation_errors:
            for error in generation_errors:
                print(f"ERROR: {error}", file=sys.stderr)
            print("run `python3 scripts/generate.py` and commit every generated file", file=sys.stderr)
            return 1
        print(f"validated catalog and verified {len(outputs)} generated outputs")
        return 0

    write_outputs(outputs)
    print(f"validated catalog and generated {len(outputs)} outputs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
