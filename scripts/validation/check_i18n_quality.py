#!/usr/bin/env python3
"""Validate i18n quality gates from the v1.16 quality contract."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
QUALITY = ROOT / "i18n" / "quality.json"
VOCABULARY = ROOT / "i18n" / "concepts" / "policy-vocabulary.json"
CATALOG = ROOT / "i18n" / "languages.json"

REQUIRED_COMMON = (
    "core/common/AGENT.md",
    "core/common/SKILL.md",
    "core/common/ENVIRONMENT.md",
)


def load_json(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"invalid JSON in {path.relative_to(ROOT)}: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"JSON object required: {path.relative_to(ROOT)}")
    return data


def contains_any(text: str, alternatives: list[str] | tuple[str, ...]) -> bool:
    lowered = text.casefold()
    return any(term.casefold() in lowered for term in alternatives)


def runtime_entries(catalog: dict) -> dict[str, dict]:
    entries = catalog.get("runtime_resources")
    if not isinstance(entries, list):
        raise ValueError("i18n/languages.json runtime_resources must be a list")
    result: dict[str, dict] = {}
    for entry in entries:
        if isinstance(entry, dict) and isinstance(entry.get("locale"), str):
            result[entry["locale"]] = entry
    return result


def documentation_entries(catalog: dict) -> dict[str, dict]:
    entries = catalog.get("documentation")
    if not isinstance(entries, list):
        raise ValueError("i18n/languages.json documentation must be a list")
    result: dict[str, dict] = {}
    for entry in entries:
        if isinstance(entry, dict) and isinstance(entry.get("locale"), str):
            result[entry["locale"]] = entry
    return result


def resource_completeness(locale: str, entry: dict, canonical: Path) -> list[str]:
    if locale == "en":
        return []
    root = ROOT / entry["path"]
    missing: list[str] = []
    for rel in REQUIRED_COMMON:
        if not (root / rel).is_file():
            missing.append(rel)
    if not (root / "README.md").is_file():
        missing.append("README.md")
    return missing


def semantic_parity(locale: str, entry: dict, vocabulary: dict) -> list[str]:
    if locale == "en":
        return []
    root = ROOT / entry["path"]
    failures: list[str] = []
    concepts = vocabulary.get("concepts", {})
    if not isinstance(concepts, dict):
        return ["policy vocabulary concepts must be an object"]

    checked = 0
    for rel in REQUIRED_COMMON:
        canonical_path = ROOT / rel
        localized_path = root / rel
        if not canonical_path.is_file() or not localized_path.is_file():
            continue
        checked += 1
        canonical_text = canonical_path.read_text(encoding="utf-8")
        localized_text = localized_path.read_text(encoding="utf-8")
        for concept_id, spec in concepts.items():
            if not isinstance(spec, dict) or not spec.get("required"):
                continue
            alternatives = spec.get("alternatives", [])
            localized_alternatives = spec.get("locales", {}).get(locale, []) if isinstance(spec.get("locales"), dict) else []
            if not localized_alternatives:
                localized_alternatives = alternatives
            canonical_alternatives = spec.get("canonical", [concept_id.split(".")[-1].replace("_", " ")])
            if contains_any(canonical_text, canonical_alternatives) and not contains_any(localized_text, localized_alternatives):
                failures.append(f"{rel}: missing semantic concept '{concept_id}'")
    if checked == 0:
        failures.append("no common semantic resources available for comparison")
    return failures


def runtime_documentation_consistency(locale: str, runtime: dict, docs: dict) -> list[str]:
    failures: list[str] = []
    if locale not in docs:
        return ["missing documentation entry"]
    runtime_path = ROOT / runtime["path"]
    docs_path = ROOT / docs[locale]["path"]
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
    if consistency or semantic:
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

    required_locales = quality.get("required_runtime_locales", [])
    if not isinstance(required_locales, list) or not required_locales:
        print("i18n quality failed: required_runtime_locales must be a non-empty list", file=sys.stderr)
        return 1

    canonical_locale = quality.get("canonical_locale", "en")
    canonical_entry = runtime.get(canonical_locale)
    if canonical_entry is None:
        print(f"i18n quality failed: canonical runtime locale missing: {canonical_locale}", file=sys.stderr)
        return 1
    canonical_root = ROOT / canonical_entry["path"]
    if not canonical_root.is_dir():
        print("i18n quality failed: canonical runtime resource root is missing", file=sys.stderr)
        return 1

    minimum = quality.get("quality_levels", {}).get("runtime_minimum", "A")
    allowed = {"A": 4, "B": 3, "C": 2, "D": 1, "F": 0}
    minimum_score = allowed.get(minimum, 4)
    rows: list[tuple[str, str, list[str], list[str], list[str]]] = []
    errors: list[str] = []

    for locale in required_locales:
        if locale not in runtime:
            errors.append(f"required runtime locale missing from catalog: {locale}")
            continue
        entry = runtime[locale]
        missing = resource_completeness(locale, entry, canonical_root)
        semantic = semantic_parity(locale, entry, vocabulary)
        consistency = runtime_documentation_consistency(locale, entry, docs)
        resource_ok = not missing
        semantic_ok = not semantic
        consistency_ok = not consistency
        current_grade = grade(resource_ok, semantic_ok, consistency_ok)
        rows.append((locale, current_grade, missing, semantic, consistency))
        if allowed[current_grade] < minimum_score:
            details = missing + semantic + consistency
            errors.append(f"{locale}: quality {current_grade} below runtime minimum {minimum}: " + "; ".join(details))

    if errors:
        print("i18n quality failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    counts = {grade_name: sum(1 for _, current, *_ in rows if current == grade_name) for grade_name in allowed}
    print("i18n quality OK")
    print(f"Runtime locales: {len(rows)}")
    print(f"Resource completeness: {sum(not missing for _, _, missing, _, _ in rows)}/{len(rows)}")
    print(f"Semantic parity:       {sum(not semantic for _, _, _, semantic, _ in rows)}/{len(rows)}")
    print(f"Runtime/doc consistency: {sum(not consistency for _, _, _, _, consistency in rows)}/{len(rows)}")
    print("Quality: " + ", ".join(f"{name}: {counts[name]}" for name in allowed))
    return 0


if __name__ == "__main__":
    raise SystemExit(validate())
