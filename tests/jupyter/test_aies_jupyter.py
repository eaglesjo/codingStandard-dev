from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "plugins" / "jupyter-notebook" / "aies_jupyter.py"


def load_module():
    spec = importlib.util.spec_from_file_location("aies_jupyter_test_module", MODULE_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_plugin_manifest_is_agent_plugins_1_0():
    manifest = json.loads(
        (ROOT / "plugins" / "jupyter-notebook" / "plugin.json").read_text(encoding="utf-8")
    )
    assert manifest["$schema"] == "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
    assert manifest["name"] == "ai-engineering-standard-jupyter"


def test_profile_detects_standard_root():
    module = load_module()
    original = os.getcwd()
    try:
        os.chdir(ROOT)
        data = module.profile()
    finally:
        os.chdir(original)
    assert data["standard_root"] == str(ROOT)
    assert data["standard_version"] == (ROOT / "VERSION").read_text(encoding="utf-8").strip()


def test_plugin_skill_exists():
    skill = ROOT / "plugins" / "jupyter-notebook" / "skills" / "jupyter-engineering" / "SKILL.md"
    assert skill.is_file()
    assert "name: jupyter-engineering" in skill.read_text(encoding="utf-8")
