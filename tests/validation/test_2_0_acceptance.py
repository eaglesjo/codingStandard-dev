#!/usr/bin/env python3
"""Focused tests for the final cross-area 2.0 acceptance boundary."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VALIDATOR = ROOT / "scripts/validation/validate_2_0_acceptance.py"
FIXTURES = ROOT / "tests/validation/fixtures/2.0-acceptance"


def run_fixture(name: str) -> subprocess.CompletedProcess[str]:
    document = json.loads((FIXTURES / name).read_text(encoding="utf-8"))
    code = f"import json; exec(open({str(VALIDATOR)!r}, encoding='utf-8').read()); validate(json.loads({json.dumps(json.dumps(document))}))"
    # Keep the fixture payload out of the validator's CLI surface while exercising the same contract.
    code = f"import json; exec(open({str(VALIDATOR)!r}, encoding='utf-8').read()); validate({json.dumps(document)})"
    return subprocess.run([sys.executable, "-c", code], cwd=ROOT, text=True, capture_output=True)


def test_valid_candidate_is_accepted() -> None:
    result = run_fixture("valid.json")
    assert result.returncode == 0, result.stderr


def test_revision_mismatch_is_rejected() -> None:
    result = run_fixture("invalid_revision.json")
    assert result.returncode != 0
    assert "provenance revision does not match candidate" in result.stderr


if __name__ == "__main__":
    test_valid_candidate_is_accepted()
    test_revision_mismatch_is_rejected()
    print("2.0 cross-area acceptance focused tests passed")
