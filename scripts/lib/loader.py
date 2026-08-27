"""Strict YAML loading for catalog data and controlled vocabularies."""

from __future__ import annotations

from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover - exercised by the CLI environment
    raise SystemExit("PyYAML is required: pip install pyyaml") from exc


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CATALOG = ROOT / "data" / "agents.yaml"
DEFAULT_VOCAB = ROOT / "schema" / "vocab.yaml"


class CatalogLoadError(ValueError):
    """Raised when a YAML document cannot be loaded as catalog data."""


class DuplicateKeyError(CatalogLoadError):
    """Raised when YAML contains a mapping key more than once."""


class UniqueKeyLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects silently overwritten mapping keys."""


def _construct_unique_mapping(
    loader: UniqueKeyLoader, node: yaml.MappingNode, deep: bool = False
) -> dict[Any, Any]:
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        try:
            duplicate = key in mapping
        except TypeError as exc:
            raise CatalogLoadError(
                f"unhashable YAML mapping key at line {key_node.start_mark.line + 1}"
            ) from exc
        if duplicate:
            line = key_node.start_mark.line + 1
            raise DuplicateKeyError(f"duplicate YAML key {key!r} at line {line}")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_unique_mapping
)


def load_yaml(path: str | Path) -> Any:
    """Load one YAML document with duplicate-key protection."""

    source = Path(path)
    try:
        with source.open(encoding="utf-8") as handle:
            return yaml.load(handle, Loader=UniqueKeyLoader)
    except DuplicateKeyError:
        raise
    except (OSError, yaml.YAMLError) as exc:
        raise CatalogLoadError(f"could not load {source}: {exc}") from exc


def load_catalog(path: str | Path | None = None) -> dict[str, Any]:
    """Load the v2 catalog, leaving validation to ``validate_catalog``."""

    document = load_yaml(path or DEFAULT_CATALOG)
    if not isinstance(document, dict):
        raise CatalogLoadError("catalog root must be a mapping")
    return document


def load_vocab(path: str | Path | None = None) -> dict[str, Any]:
    """Load the v2 controlled vocabulary."""

    document = load_yaml(path or DEFAULT_VOCAB)
    if not isinstance(document, dict):
        raise CatalogLoadError("vocabulary root must be a mapping")
    return document
