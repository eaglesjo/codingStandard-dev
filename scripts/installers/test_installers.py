#!/usr/bin/env python3
"""Integration-test the cross-platform codingStandard installer lifecycle."""
from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PS1 = ROOT / "scripts" / "installers" / "install-domains.ps1"
SH = ROOT / "scripts" / "installers" / "install-domains.sh"
ENGINE = ROOT / "scripts" / "installers" / "installation.py"
RECONCILE = ROOT / "scripts" / "installers" / "reconcile_upgrade.py"
COMMON = [
    "AGENTS.md", "CLAUDE.md", "GEMINI.md", ".github/copilot-instructions.md",
    ".cursor/rules/coding-standard.mdc", ".windsurf/rules/coding-standard.md",
    ".clinerules/01-coding-standard.md", ".continue/rules/01-coding-standard.md",
    ".junie/AGENTS.md", ".amazonq/rules/coding-standard.md", "docs/development/CONVENTIONS.md", ".aider.conf.yml",
    "core/common/AGENT.md", "core/common/SKILL.md", "core/common/ENVIRONMENT.md", "core/common/environment.py", "core/common/experiment.py", "core/common/dependencies.py",
]
ML = [".github/instructions/ml.instructions.md", "domains/ml/AGENT.md", "domains/ml/SKILL.md", "domains/ml/ENVIRONMENT.md", "domains/ml/README.md"]
COLAB = ["platform/colab/AGENT.md", "platform/colab/SKILL.md"]
LOCALES = (
    "en", "ko", "fr", "es", "zh-CN", "ja", "ru", "tr", "de", "it",
    "pt", "ar", "hi", "id", "vi", "th", "nl", "pl", "sv", "uk",
)


def run(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=ROOT, check=check, text=True, capture_output=True)


def check(target: Path, paths: list[str]) -> None:
    missing = [p for p in paths if not (target / p).is_file()]
    if missing:
        raise AssertionError(f"missing installed files: {missing}")


def lifecycle(target: Path) -> None:
    manifest = target / ".codingstandard" / "installation.json"
    if not manifest.is_file():
        raise AssertionError("installation manifest missing")
    data = json.loads(manifest.read_text(encoding="utf-8"))
    assert data["schema_version"] == 1
    assert data["coding_standard_version"] == (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    assert data["language"] == "en"
    assert data["domain"] == "all"
    assert data["files"]

    state = run(["python3", str(ENGINE), "state", str(target)])
    assert "installed: true" in state.stdout
    assert "modified: 0" in state.stdout
    assert "missing: 0" in state.stdout

    removed = target / ML[0]
    removed.unlink()
    update = run(["bash", str(ROOT / "scripts/installers/update-domains.sh"), str(target), "--policy", "overwrite"])
    assert "Installed:" in update.stdout
    assert removed.is_file(), "update did not restore missing managed file"

    tracked = target / "AGENTS.md"
    tracked.write_text(tracked.read_text(encoding="utf-8") + "\nlocal change\n", encoding="utf-8")
    bad = run(["bash", str(ROOT / "scripts/installers/uninstall-domains.sh"), str(target)], check=False)
    assert bad.returncode == 2
    assert tracked.exists(), "modified file was removed without --force"
    assert manifest.exists(), "manifest disappeared after protected uninstall"

    forced = run(["bash", str(ROOT / "scripts/installers/uninstall-domains.sh"), str(target), "--force"])
    assert forced.returncode == 0
    assert not manifest.exists()
    assert not tracked.exists()


def legacy_v17_upgrade(target: Path) -> None:
    """Verify a representative v1.7 installation upgrades without uninstalling."""
    target.mkdir(parents=True, exist_ok=True)
    legacy_files = {
        "AGENTS.md": "# AGENTS.md\n\n# Project Agent Instructions\n\nThis file is the top-level entrypoint for AI coding agents.\n\n## Environment Contract\n\n- Inspect the real OS, Python/runtime, CPU, GPU/accelerator, VRAM, RAM, disk, and framework capabilities before resource-sensitive work.\n",
        "domains/ml/AGENT.md": "# ML Agent\n\n## Local ML Rule\n\nPreserve this project-specific ML workflow.\n",
        "domains/llm/AGENT.md": "# LLM Agent\n\n## Local LLM Rule\n\nPreserve this project-specific LLM workflow.\n",
        "domains/vision/AGENT.md": "# Vision Agent\n\n## Local Vision Rule\n\nPreserve this project-specific vision workflow.\n",
        "platform/colab/AGENT.md": "# Colab Agent\n\n## Local Colab Rule\n\nPreserve this project-specific Colab workflow.\n",
    }
    start = "<!-- BEGIN CODINGSTANDARD MANAGED BLOCK -->"
    end = "<!-- END CODINGSTANDARD MANAGED BLOCK -->"
    for rel, body in legacy_files.items():
        path = target / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"{body}\n{start}\nlegacy-v1.7-managed-content\n{end}\n", encoding="utf-8")

    legacy_only = target / "legacy-v1.7-only.md"
    legacy_only.write_text("legacy artifact that v2 does not manage\n", encoding="utf-8")
    stale_managed = target / "obsolete-v1.7-managed.md"
    stale_managed.write_text(
        f"# Obsolete v1.7 artifact\n\n{start}\nlegacy-v1.7-managed-content\n{end}\n",
        encoding="utf-8",
    )
    manifest = target / ".codingstandard" / "installation.json"
    assert not manifest.exists(), "v1.7 fixture must start without a v2 manifest"

    reconcile = run(["python3", str(RECONCILE), str(target), "--domain", "all"])
    reconciliation_path = target / ".codingstandard" / "upgrade-reconciliation.json"
    report = json.loads(reconciliation_path.read_text(encoding="utf-8"))
    assert "AGENTS.md" in report["categories"]["legacy-managed-candidate"]
    assert "domains/ml/AGENT.md" in report["categories"]["legacy-managed-candidate"]
    assert "legacy-v1.7-only.md" in report["categories"]["unknown-legacy"]
    assert "obsolete-v1.7-managed.md" in report["categories"]["unknown-legacy"]
    assert report["deletion_policy"] == "never-delete-unknown"
    assert "legacy-managed-candidate" in reconcile.stdout

    result = run(["python3", str(ENGINE), "install", str(target), "en", "all", "merge", "false"])
    assert result.returncode == 0
    assert manifest.is_file(), "v2 install did not establish installation state"

    for rel in legacy_files:
        text = (target / rel).read_text(encoding="utf-8")
        expected_local = "Project Agent Instructions" if rel == "AGENTS.md" else "Local"
        assert expected_local in text, f"local project content was lost: {rel}"
        assert "legacy-v1.7-managed-content" not in text, f"legacy managed block was not replaced: {rel}"
        assert "BEGIN CODINGSTANDARD MANAGED BLOCK" in text, f"v2 managed block missing: {rel}"
    assert legacy_only.is_file(), "upgrade deleted an unmanaged legacy file"
    assert stale_managed.is_file(), "upgrade deleted an obsolete legacy artifact"
    assert reconciliation_path.is_file(), "upgrade reconciliation evidence disappeared"

    data = json.loads(manifest.read_text(encoding="utf-8"))
    assert data["coding_standard_version"] == (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    assert data["language"] == "en"
    assert data["domain"] == "all"
    paths = [item["path"] for item in data["files"]]
    assert len(paths) == len(set(paths)), "installation manifest contains duplicate ownership entries"
    assert set(paths) >= set(COMMON + ML + COLAB)
    assert all((target / rel).is_file() for rel in paths), "manifest owns a missing file"
    post_state = run(["python3", str(ENGINE), "state", str(target)])
    assert "installed: true" in post_state.stdout
    assert "modified: 0" in post_state.stdout
    assert "missing: 0" in post_state.stdout


def test_upgrade_v17_to_v2() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / "v1.7-project"
        legacy_v17_upgrade(target)


def test_bash() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / "new-project"
        dry = run(["bash", str(SH), str(target), "en", "all", "overwrite", "true"])
        assert not target.exists() or not any(target.iterdir()), "bash dry-run modified target"
        assert "DRY-RUN" in dry.stdout
        run(["bash", str(SH), str(target), "en", "all", "overwrite", "false"])
        check(target, COMMON + ML + COLAB)
        lifecycle(target)
        for locale in LOCALES:
            locale_target = Path(tmp) / f"{locale}-project"
            result = run(["bash", str(SH), str(locale_target), locale, "common", "overwrite", "false"])
            check(locale_target, COMMON)
            assert f"language={locale}" in result.stdout


def test_powershell() -> None:
    executable = shutil.which("pwsh") or shutil.which("powershell")
    if not executable:
        return
    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / "new-project"
        run([executable, "-NoProfile", "-File", str(PS1), "-Target", str(target), "-Language", "ko", "-Domain", "all", "-Policy", "overwrite", "-DryRun"])
        assert not target.exists() or not any(target.iterdir()), "PowerShell dry-run modified target"
        run([executable, "-NoProfile", "-File", str(PS1), "-Target", str(target), "-Language", "ko", "-Domain", "ml", "-Policy", "overwrite"])
        check(target, COMMON + ML)
        state = run([executable, "-NoProfile", "-File", str(ROOT / "scripts/installers/state-domains.ps1"), "-Target", str(target)])
        assert "installed: true" in state.stdout
        for locale in LOCALES:
            locale_target = Path(tmp) / f"ps-{locale}-project"
            run([executable, "-NoProfile", "-File", str(PS1), "-Target", str(locale_target), "-Language", locale, "-Domain", "common", "-Policy", "overwrite"])
            check(locale_target, COMMON)


def main() -> int:
    test_upgrade_v17_to_v2()
    test_bash()
    test_powershell()
    print("installer lifecycle tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
