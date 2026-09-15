#!/usr/bin/env python3
"""Run deterministic EVAL-003 cases from explicit criterion evidence."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CASES = ROOT / "tests/validation/fixtures/ai-developer-evaluation-cases.json"


def fail(message: str) -> None:
    print(f"EVAL-003 evaluation failed: {message}", file=sys.stderr)
    raise SystemExit(1)


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot read {path}: {exc}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--candidate-revision", required=True)
    args = parser.parse_args()

    case_spec = load_json(CASES)
    evidence = load_json(args.evidence)
    results = evidence.get("cases")
    if not isinstance(results, list):
        fail("evidence.cases must be an array")

    by_id = {item.get("id"): item for item in results if isinstance(item, dict)}
    if len(by_id) != len(results):
        fail("evidence case ids must be unique")

    output_cases = []
    total_score = 0.0

    for case in case_spec["cases"]:
        case_id = case["id"]
        item = by_id.get(case_id)
        if item is None:
            fail(f"missing evidence for {case_id}")

        criterion_results = item.get("criteria")
        if not isinstance(criterion_results, dict):
            fail(f"criteria must be an object for {case_id}")

        expected = case["required_criteria"]
        missing = [criterion for criterion in expected if criterion not in criterion_results]
        if missing:
            fail(f"missing criteria for {case_id}: {', '.join(missing)}")

        normalized = []
        for criterion in expected:
            result = criterion_results[criterion]
            if not isinstance(result, dict):
                fail(f"criterion evidence must be an object: {case_id}/{criterion}")
            status = result.get("status")
            if status not in {"PASS", "FAIL"}:
                fail(f"criterion status must be PASS or FAIL: {case_id}/{criterion}")
            evidence_text = result.get("evidence")
            if not isinstance(evidence_text, str) or not evidence_text.strip():
                fail(f"criterion evidence text is required: {case_id}/{criterion}")
            normalized.append({"criterion": criterion, "status": status, "evidence": evidence_text})

        score = sum(1 for item in normalized if item["status"] == "PASS") / len(normalized)
        acceptance = "ACCEPTED" if score == 1.0 else "REJECTED"
        total_score += score
        output_cases.append(
            {
                "id": case_id,
                "dimension": case["dimension"],
                "score": round(score, 6),
                "acceptance": acceptance,
                "criteria": normalized,
            }
        )

    mean_score = total_score / len(output_cases)
    accepted = all(item["acceptance"] == "ACCEPTED" for item in output_cases)
    output = {
        "schema_version": "2.0.0",
        "suite_id": "EVAL-003",
        "method": "deterministic_case_evaluation",
        "deterministic": True,
        "vendor_neutral": True,
        "candidate_revision": args.candidate_revision,
        "cases": output_cases,
        "overall": {
            "acceptance": "ACCEPTED" if accepted else "REJECTED",
            "mean_score": round(mean_score, 6),
            "basis": "All required criteria must PASS for every representative case.",
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"EVAL-003 evaluation complete: cases={len(output_cases)} mean_score={mean_score:.6f} acceptance={output['overall']['acceptance']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
