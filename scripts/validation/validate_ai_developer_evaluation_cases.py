#!/usr/bin/env python3
"""Validate deterministic AI Developer EVAL-003 case specifications."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "tests/validation/fixtures/ai-developer-evaluation-cases.json"

ALLOWED_DIMENSIONS = {
    "repository_recovery",
    "scope_control",
    "planning_quality",
    "validation_evidence",
    "failure_diagnosis",
    "bounded_retry",
    "provenance",
    "development_continuity",
}

FORBIDDEN_PROVIDER_TERMS = {
    "openai",
    "anthropic",
    "google",
    "gemini",
    "claude",
    "gpt-",
    "llama",
}


def fail(message: str) -> None:
    print(f"AI Developer evaluation case validation failed: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> int:
    try:
        document = json.loads(FIXTURE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot read fixture: {exc}")

    if document.get("schema_version") != "2.0.0":
        fail("schema_version must be 2.0.0")
    if document.get("suite_id") != "EVAL-003":
        fail("suite_id must be EVAL-003")
    if document.get("method") != "deterministic_case_specification":
        fail("method must be deterministic_case_specification")
    if document.get("vendor_neutral") is not True:
        fail("vendor_neutral must be true")

    cases = document.get("cases")
    if not isinstance(cases, list) or not cases:
        fail("cases must be a non-empty array")

    ids: set[str] = set()
    dimensions: set[str] = set()
    serialized = json.dumps(document, ensure_ascii=False).lower()
    for term in FORBIDDEN_PROVIDER_TERMS:
        if term in serialized:
            fail(f"provider/model-specific term is forbidden: {term}")

    for case in cases:
        if not isinstance(case, dict):
            fail("each case must be an object")
        case_id = case.get("id")
        if not isinstance(case_id, str) or not case_id.strip() or case_id in ids:
            fail("case ids must be unique, non-empty strings")
        ids.add(case_id)

        dimension = case.get("dimension")
        if dimension not in ALLOWED_DIMENSIONS:
            fail(f"unsupported dimension for {case_id}: {dimension}")
        dimensions.add(dimension)

        if not isinstance(case.get("task"), str) or not case["task"].strip():
            fail(f"task is required for {case_id}")

        criteria = case.get("required_criteria")
        if not isinstance(criteria, list) or not criteria:
            fail(f"required_criteria must be non-empty for {case_id}")
        if len(criteria) != len(set(criteria)):
            fail(f"required_criteria must be unique for {case_id}")
        if not all(isinstance(item, str) and item.strip() for item in criteria):
            fail(f"required_criteria must contain non-empty strings for {case_id}")

    required_dimensions = ALLOWED_DIMENSIONS
    missing = required_dimensions - dimensions
    if missing:
        fail(f"missing required evaluation dimensions: {', '.join(sorted(missing))}")

    print(
        f"AI Developer evaluation case validation passed: "
        f"suite=EVAL-003 cases={len(cases)} dimensions={len(dimensions)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
