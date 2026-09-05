#!/usr/bin/env python3
"""Validate consistency between runtime locale resources and documentation catalog."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "i18n" / "languages.json"
QUALITY = ROOT / "i18n" / "quality.json"
REQUIRED_COMMON = ("core/common/AGENT.md", "core/common/SKILL.md", "core/common/ENVIRONMENT.md")


def load_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"invalid JSON in {path.relative_to(ROOT)}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"JSON object required: {path.relative_to(ROOT)}")
    return value


def entries(catalog: dict, key: str) -> dict[str, dict]:
    value = catalog.get(key)
    if not isinstance(value, list):
        raise ValueError(f"i18n/languages.json {key} must be a list")
    result: dict[str, dict] = {}
    for entry in value:
        if not isinstance(entry, dict) or not isinstance(entry.get("locale"), str):
            raise ValueError(f"i18n/languages.json {key} contains an invalid entry")
        locale = entry["locale"]
        if locale in result:
            raise ValueError(f"duplicate locale in {key}: {locale}")
        result[locale] = entry
    return result


def validate() -> int:
    try:
        catalog = load_json(CATALOG)
        quality = load_json(QUALITY)
        runtime = entries(catalog, "runtime_resources")
        docs = entries(catalog, "documentation")
    except ValueError as exc:
        print(f"i18n consistency failed: {exc}", file=sys.stderr)
        return 1

    required = quality.get("required_runtime_locales")
    if not isinstance(required, list) or not required:
        print("i18n consistency failed: required_runtime_locales must be a non-empty list", file=sys.stderr)
        return 1

    errors: list[str] = []
    runtime_locales = set(runtime)
    required_locales = set(required)
    if runtime_locales != required_locales:
        errors.append(
            "runtime locale set mismatch: "
            f"catalog-only={sorted(runtime_locales - required_locales)}, "
            f"quality-only={sorted(required_locales - runtime_locales)}"
        )

    for locale in required:
        entry = runtime.get(locale)
        if entry is None:
            continue
        path_value = entry.get("path")
        if not isinstance(path_value, str):
            errors.append(f"{locale}: runtime path is missing")
            continue
        runtime_root = ROOT / path_value
        if not runtime_root.is_dir():
            errors.append(f"{locale}: runtime path does not exist: {path_value}")
            continue
        for rel in REQUIRED_COMMON:
            if not (runtime_root / rel).is_file():
                errors.append(f"{locale}: missing runtime resource: {path_value}/{rel}")

        doc = docs.get(locale)
        if doc is None:
            errors.append(f"{locale}: missing documentation catalog entry")
            continue
        doc_path = doc.get("path")
        if not isinstance(doc_path, str):
            errors.append(f"{locale}: documentation path is missing")
        elif not (ROOT / doc_path).is_file():
            errors.append(f"{locale}: documentation file does not exist: {doc_path}")

    doc_locales = set(docs)
    if not required_locales.issubset(doc_locales):
        errors.append(f"documentation missing runtime locales: {sorted(required_locales - doc_locales)}")

    if errors:
        print("i18n consistency failed:")
        for error in sorted(set(errors)):
            print(f"- {error}")
        return 1

    print(f"i18n consistency OK: {len(required)} runtime locales mapped to documentation")
    return 0


if __name__ == "__main__":
    raise SystemExit(validate())
