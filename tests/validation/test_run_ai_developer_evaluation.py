from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RUNNER = ROOT / "scripts/validation/run_ai_developer_evaluation.py"
FIXTURE = ROOT / "tests/validation/fixtures/ai-developer-evaluation-cases.json"


def test_eval_003_runner_requires_explicit_self_report_opt_in() -> None:
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    case = fixture["cases"][0]
    markers = " ".join(f"CRITERION {item}: objective evidence" for item in case["required_criteria"])
    command = [
        sys.executable,
        str(RUNNER),
        "--fixture",
        str(FIXTURE),
        "--case",
        case["id"],
        "--command",
        f"{sys.executable} -c \"print('{markers}')\"",
    ]

    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, check=False)
    assert result.returncode != 0
    document = json.loads(result.stdout)
    measured = document["cases"][0]
    assert measured["result"] == "PARTIAL"
    assert measured["measurement_mode"] == "self_report_only"
    assert all(item["status"] == "SELF_REPORTED" for item in measured["criteria"])


def test_eval_003_runner_can_explicitly_measure_deterministic_self_report_fixture() -> None:
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    case = fixture["cases"][0]
    markers = " ".join(f"CRITERION {item}: objective evidence" for item in case["required_criteria"])
    command = [
        sys.executable,
        str(RUNNER),
        "--fixture",
        str(FIXTURE),
        "--case",
        case["id"],
        "--allow-self-report",
        "--command",
        f"{sys.executable} -c \"print('{markers}')\"",
    ]

    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, check=False)
    assert result.returncode == 0, result.stderr
    document = json.loads(result.stdout)
    measured = document["cases"][0]
    assert measured["result"] == "PASS"
    assert measured["measurement_mode"] == "self_report_allowed"
    assert measured["observed_criteria"] == measured["total_criteria"]
