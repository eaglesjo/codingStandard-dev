#!/usr/bin/env python3
"""Classify pre-v2 installation files without deleting anything."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from installation import collect_files

MANIFEST_DIR = ".codingstandard"
START_MARKERS = (
    "<!-- BEGIN CODINGSTANDARD MANAGED BLOCK -->",
    "# BEGIN CODINGSTANDARD MANAGED BLOCK",
)


def classify(target: Path, desired: set[str]) -> dict[str, list[str]]:
    result = {
        "known-v2-managed": [],
        "legacy-managed-candidate": [],
        "project-owned": [],
        "unknown-legacy": [],
    }
    for path in sorted(target.rglob("*")):
        if not path.is_file():
            continue
        rel = str(path.relative_to(target))
        if rel.startswith(f"{MANIFEST_DIR}/"):
            continue
        if rel in desired:
            text = path.read_text(encoding="utf-8", errors="replace")
            if any(marker in text for marker in START_MARKERS):
                result["legacy-managed-candidate"].append(rel)
            else:
                result["project-owned"].append(rel)
        else:
            result["unknown-legacy"].append(rel)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target")
    parser.add_argument("--domain", default="all")
    parser.add_argument("--output")
    args = parser.parse_args()

    target = Path(args.target).resolve()
    if not target.is_dir():
        raise SystemExit(f"Target does not exist: {target}")
    root = Path(__file__).resolve().parents[2]
    desired = set(collect_files(root, args.domain))
    categories = classify(target, desired)
    report = {
        "schema_version": 1,
        "mode": "pre-v2-upgrade",
        "domain": args.domain,
        "target": str(target),
        "deletion_policy": "never-delete-unknown",
        "categories": categories,
    }
    output = Path(args.output).resolve() if args.output else target / MANIFEST_DIR / "upgrade-reconciliation.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
