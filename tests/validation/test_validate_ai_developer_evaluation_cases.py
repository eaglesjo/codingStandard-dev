from __future__ import annotations

import runpy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts/validation/validate_ai_developer_evaluation_cases.py"


def test_eval_003_case_specification_validator_passes() -> None:
    namespace = runpy.run_path(str(SCRIPT), run_name="eval_003_case_validator")
    assert namespace["main"]() == 0
