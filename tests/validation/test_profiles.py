from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class ProfileContractTests(unittest.TestCase):
    def test_project_profile_is_repository_standard(self) -> None:
        value = json.loads((ROOT / "profiles" / "project.json").read_text(encoding="utf-8"))
        self.assertEqual(value["profile_version"], 1)
        self.assertEqual(value["project_type"], "developer-standard")
        self.assertEqual(value["architecture_profile"], "repository-standard")
        self.assertEqual(value["policy_profile"], "repository-default")
        self.assertEqual(set(value["runtime"]["os"]), {"linux", "macos", "windows"})

    def test_repository_standard_dependency_contract(self) -> None:
        value = json.loads(
            (ROOT / "profiles" / "architecture" / "repository-standard.json").read_text(encoding="utf-8")
        )
        self.assertIn("interface -> domain", value["dependency_direction"])
        self.assertIn("domain -> interface", value["forbidden_dependencies"])
        self.assertNotIn("domain -> interface", value["dependency_direction"])

    def test_repository_policy_prevents_weakening(self) -> None:
        value = json.loads(
            (ROOT / "profiles" / "policies" / "repository-default.json").read_text(encoding="utf-8")
        )
        self.assertEqual(value["scope"], "repository")
        self.assertTrue(value["inheritance"]["child_scopes_may_not_weaken_parent"])
        self.assertEqual(value["inheritance"]["conflict_resolution"], "stricter-wins")

    def test_validator_passes(self) -> None:
        proc = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "validation" / "validate_profiles.py")],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("validation passed", proc.stdout)


if __name__ == "__main__":
    unittest.main()
