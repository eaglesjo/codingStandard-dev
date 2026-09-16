from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RUNNER = ROOT / "scripts/validation/run_ai_developer_evaluation.py"
FIXTURE = ROOT / "tests/validation/fixtures/ai-developer-evaluation-cases.json"


def test_eval_003_runner_measures_all_criteria_with_deterministic_runtime() -> None:
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
    assert result.returncode == 0, result.stderr
    document = json.loads(result.stdout)
    measured = document["cases"][0]
    assert measured["result"] == "PASS"
    assert measured["observed_criteria"] == measured["total_criteria"]
