#!/usr/bin/env python3
"""Validate v1.16 i18n quality through stable policy intents."""
from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
QUALITY = ROOT / "i18n" / "quality.json"
VOCABULARY = ROOT / "i18n" / "concepts" / "policy-vocabulary.json"
CATALOG = ROOT / "i18n" / "languages.json"
REQUIRED_COMMON = ("core/common/AGENT.md", "core/common/SKILL.md", "core/common/ENVIRONMENT.md")

sys.path.insert(0, str(ROOT / "scripts" / "validation"))
check_i18n = importlib.import_module("check_i18n")


def load_json(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"invalid JSON in {path.relative_to(ROOT)}: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"JSON object required: {path.relative_to(ROOT)}")
    return data


def contains_any(text: str, alternatives: tuple[str, ...] | list[str]) -> bool:
    lowered = text.casefold()
    return any(term.casefold() in lowered for term in alternatives)


def runtime_entries(catalog: dict) -> dict[str, dict]:
    entries = catalog.get("runtime_resources")
    if not isinstance(entries, list):
        raise ValueError("i18n/languages.json runtime_resources must be a list")
    return {e["locale"]: e for e in entries if isinstance(e, dict) and isinstance(e.get("locale"), str)}


def documentation_entries(catalog: dict) -> dict[str, dict]:
    entries = catalog.get("documentation")
    if not isinstance(entries, list):
        raise ValueError("i18n/languages.json documentation must be a list")
    return {e["locale"]: e for e in entries if isinstance(e, dict) and isinstance(e.get("locale"), str)}


def resource_completeness(locale: str, entry: dict) -> list[str]:
    if locale == "en":
        return []
    root = ROOT / entry["path"]
    missing = [rel for rel in REQUIRED_COMMON if not (root / rel).is_file()]
    if not (root / "README.md").is_file():
        missing.append("README.md")
    return missing


def semantic_parity(locale: str, entry: dict, vocabulary: dict) -> list[str]:
    if locale == "en":
        return []
    root = ROOT / entry["path"]
    failures: list[str] = []
    for intent_id, spec in vocabulary.get("concepts", {}).items():
        if not isinstance(spec, dict) or not spec.get("required"):
            continue
        source_concepts = spec.get("source_concepts", [])
        if source_concepts:
            mappings = []
            for source_concept in source_concepts:
                alternatives = check_i18n.CONCEPT_ALTERNATIVES.get(source_concept)
                if not alternatives or locale not in alternatives:
                    failures.append(f"{intent_id}: missing concept catalog for locale '{locale}'")
                    continue
                mappings.append(alternatives)
        else:
            canonical = spec.get("canonical", [])
            localized = spec.get("locales", {}).get(locale, []) if isinstance(spec.get("locales"), dict) else []
            mappings = [{"en": tuple(canonical), locale: tuple(localized)}] if canonical and localized else []
            if not mappings:
                failures.append(f"{intent_id}: no localized concept mapping for locale '{locale}'")
                continue

        for rel in REQUIRED_COMMON:
            canonical_path = ROOT / rel
            localized_path = root / rel
            if not canonical_path.is_file() or not localized_path.is_file():
                continue
            canonical_text = canonical_path.read_text(encoding="utf-8")
            localized_text = localized_path.read_text(encoding="utf-8")
            for mapping in mappings:
                if contains_any(canonical_text, mapping["en"]) and not contains_any(localized_text, mapping[locale]):
                    failures.append(f"{rel}: intent '{intent_id}' missing localized concept")
    return sorted(set(failures))


def runtime_documentation_consistency(locale: str, runtime: dict, docs: dict) -> list[str]:
    if locale not in docs:
        return ["missing documentation entry"]
    runtime_path = ROOT / runtime["path"]
    docs_path = ROOT / docs[locale]["path"]
    failures: list[str] = []
    if not runtime_path.is_dir():
        failures.append("runtime resource root is missing")
    if not docs_path.is_file():
        failures.append("documentation entrypoint is missing")
    if runtime_path.is_dir() and not (runtime_path / "README.md").is_file():
        failures.append("runtime locale README.md is missing")
    return failures


def grade(resource: bool, semantic: bool, consistency: bool) -> str:
    if resource and semantic and consistency:
        return "A"
    if resource and semantic:
        return "B"
    if resource:
        return "C"
    if semantic or consistency:
        return "D"
    return "F"


def validate() -> int:
    try:
        quality = load_json(QUALITY)
        vocabulary = load_json(VOCABULARY)
        catalog = load_json(CATALOG)
        runtime = runtime_entries(catalog)
        docs = documentation_entries(catalog)
    except ValueError as exc:
        print(f"i18n quality failed: {exc}", file=sys.stderr)
        return 1

    required = quality.get("required_runtime_locales", [])
    if not isinstance(required, list) or not required:
        print("i18n quality failed: required_runtime_locales must be a non-empty list", file=sys.stderr)
        return 1
    canonical_locale = quality.get("canonical_locale", "en")
    if canonical_locale not in runtime:
        print(f"i18n quality failed: canonical runtime locale missing: {canonical_locale}", file=sys.stderr)
        return 1
    minimum = quality.get("quality_levels", {}).get("runtime_minimum", "A")
    scores = {"A": 4, "B": 3, "C": 2, "D": 1, "F": 0}
    errors: list[str] = []
    rows: list[tuple[str, str, list[str], list[str], list[str]]] = []

    for locale in required:
        if locale not in runtime:
            errors.append(f"required runtime locale missing from catalog: {locale}")
            continue
        resource = resource_completeness(locale, runtime[locale])
        semantic = semantic_parity(locale, runtime[locale], vocabulary)
        consistency = runtime_documentation_consistency(locale, runtime[locale], docs)
        current = grade(not resource, not semantic, not consistency)
        rows.append((locale, current, resource, semantic, consistency))
        if scores.get(current, 0) < scores.get(minimum, 4):
            details = resource + semantic + consistency
            errors.append(f"{locale}: quality {current} below runtime minimum {minimum}: " + "; ".join(details))

    if errors:
        print("i18n quality failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    counts = {name: sum(1 for _, current, *_ in rows if current == name) for name in scores}
    print("i18n quality OK")
    print(f"Runtime locales: {len(rows)}")
    print(f"Resource completeness: {sum(not x for _, _, x, _, _ in rows)}/{len(rows)}")
    print(f"Semantic parity:       {sum(not x for _, _, _, x, _ in rows)}/{len(rows)}")
    print(f"Runtime/doc consistency: {sum(not x for _, _, _, _, x in rows)}/{len(rows)}")
    print("Quality: " + ", ".join(f"{name}: {counts[name]}" for name in scores))
    return 0


if __name__ == "__main__":
    raise SystemExit(validate())
