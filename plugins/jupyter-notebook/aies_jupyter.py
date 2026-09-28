"""AIEngineeringStandard Jupyter/IPython runtime adapter."""
from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from IPython.core.magic import Magics, line_magic, magics_class


def _find_standard_root(start: Path) -> Path | None:
    explicit = os.environ.get("AIENGINEERINGSTANDARD_ROOT")
    if explicit:
        root = Path(explicit).expanduser().resolve()
        if (root / "VERSION").is_file() and (root / "scripts" / "validation" / "validate.py").is_file():
            return root
    for candidate in (start, *start.parents):
        if (candidate / "VERSION").is_file() and (candidate / "scripts" / "validation" / "validate.py").is_file():
            return candidate
    return None


def profile() -> dict[str, Any]:
    cwd = Path.cwd()
    report: dict[str, Any] = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version.split()[0],
        "executable": sys.executable,
        "os": platform.system(),
        "architecture": platform.machine(),
        "cwd": str(cwd),
        "jupyter": False,
        "colab": False,
        "accelerator": "none",
    }
    try:
        from IPython import get_ipython
        report["jupyter"] = get_ipython() is not None
    except Exception:
        pass
    try:
        import google.colab  # type: ignore  # noqa: F401
        report["colab"] = True
    except Exception:
        report["colab"] = bool(os.environ.get("COLAB_RELEASE_TAG"))
    try:
        import psutil
        report["ram_gb"] = round(psutil.virtual_memory().total / 1024**3, 2)
        report["disk_free_gb"] = round(shutil.disk_usage(cwd).free / 1024**3, 2)
    except Exception:
        report["ram_gb"] = None
        report["disk_free_gb"] = None
    try:
        import torch
        report["torch"] = torch.__version__
        if torch.cuda.is_available():
            report["accelerator"] = f"cuda:{torch.cuda.get_device_name(0)}"
        elif getattr(torch.backends, "mps", None) is not None and torch.backends.mps.is_available():
            report["accelerator"] = "mps"
    except Exception:
        report["torch"] = None
    standard_root = _find_standard_root(cwd)
    report["standard_root"] = str(standard_root) if standard_root else None
    report["standard_version"] = (
        (standard_root / "VERSION").read_text(encoding="utf-8").strip()
        if standard_root else None
    )
    return report


def _run_validation(root: Path) -> int:
    command = [sys.executable, str(root / "scripts" / "validation" / "validate.py")]
    return subprocess.run(command, cwd=str(root), check=False).returncode


@magics_class
class AIESMagics(Magics):
    @line_magic
    def aies(self, line: str = "") -> None:
        parser = argparse.ArgumentParser(prog="%aies", add_help=False)
        parser.add_argument("command", nargs="?", default="help")
        args = parser.parse_args(line.split())

        if args.command == "help":
            print("AIEngineeringStandard Jupyter adapter")
            print("  %aies status   show standard + runtime status")
            print("  %aies profile  print the measured notebook runtime profile")
            print("  %aies validate run the standard validation entrypoint")
            print("  %aies report   write .codingstandard/jupyter-runtime.json")
            return

        if args.command in {"status", "profile", "report"}:
            data = profile()
            if args.command == "status":
                print(json.dumps({
                    "jupyter": data["jupyter"],
                    "colab": data["colab"],
                    "python": data["python"],
                    "accelerator": data["accelerator"],
                    "standard_root": data["standard_root"],
                    "standard_version": data["standard_version"],
                }, indent=2))
            elif args.command == "profile":
                print(json.dumps(data, indent=2))
            else:
                root = Path(".codingstandard")
                root.mkdir(parents=True, exist_ok=True)
                path = root / "jupyter-runtime.json"
                path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
                print(f"Runtime report: {path}")
            return

        if args.command == "validate":
            root = _find_standard_root(Path.cwd())
            if root is None:
                raise RuntimeError("AIEngineeringStandard root not found. Set AIENGINEERINGSTANDARD_ROOT.")
            rc = _run_validation(root)
            if rc:
                raise RuntimeError(f"AIEngineeringStandard validation failed with exit code {rc}")
            print("AIEngineeringStandard validation passed")
            return

        raise ValueError(f"Unknown %aies command: {args.command}")


def load_ipython_extension(ipython: Any) -> None:
    ipython.register_magics(AIESMagics)


def unload_ipython_extension(ipython: Any) -> None:
    return None
