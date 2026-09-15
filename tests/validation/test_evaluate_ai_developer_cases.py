from __future__ import annotations

import json
import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts/validation/evaluate_ai_developer_cases.py"
EVIDENCE = ROOT / "tests/validation/fixtures/ai-developer-evaluation-evidence.sample.json"


def test_eval_003_deterministic_evaluator_accepts_complete_sample(tmp_path: Path) -> None:
    namespace = runpy.run_path(str(SCRIPT), run_name="eval_003_runner")
    output = tmp_path / "result.json"

    import sys

    original = sys.argv
    try:
        sys.argv = [
            str(SCRIPT),
            "--evidence",
            str(EVIDENCE),
            "--output",
            str(output),
            "--candidate-revision",
            "deadbeef" * 5,
        ]
        assert namespace["main"]() == 0
    finally:
        sys.argv = original

    result = json.loads(output.read_text(encoding="utf-8"))
    assert result["suite_id"] == "EVAL-003"
    assert result["deterministic"] is True
    assert result["overall"]["acceptance"] == "ACCEPTED"
    assert result["overall"]["mean_score"] == 1.0
    assert len(result["cases"]) == 8


def test_eval_003_rejects_missing_criterion(tmp_path: Path) -> None:
    namespace = runpy.run_path(str(SCRIPT), run_name="eval_003_runner_missing")
    evidence = json.loads(EVIDENCE.read_text(encoding="utf-8"))
    del evidence["cases"][0]["criteria"]["read_durable_state"]
    bad = tmp_path / "bad.json"
    bad.write_text(json.dumps(evidence), encoding="utf-8")
    output = tmp_path / "result.json"

    import sys

    original = sys.argv
    try:
        sys.argv = [
            str(SCRIPT),
            "--evidence",
            str(bad),
            "--output",
            str(output),
            "--candidate-revision",
            "deadbeef" * 5,
        ]
        try:
            namespace["main"]()
        except SystemExit as exc:
            assert exc.code == 1
        else:
            raise AssertionError("expected evaluator failure")
    finally:
        sys.argv = original
