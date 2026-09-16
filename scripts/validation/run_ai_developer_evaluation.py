#!/usr/bin/env python3
"""Run deterministic EVAL-003 cases against a configured agent runtime."""
from __future__ import annotations

import argparse
import json
import os
import shlex
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_FIXTURE = ROOT / "tests/validation/fixtures/ai-developer-evaluation-cases.json"


def now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def git_snapshot() -> dict:
    def run(*args: str) -> str:
        try:
            result = subprocess.run(
                ["git", *args], cwd=ROOT, capture_output=True, text=True, timeout=10, check=False
            )
            return (result.stdout or "").strip()
        except (OSError, subprocess.TimeoutExpired):
            return ""

    return {
        "revision": run("rev-parse", "HEAD"),
        "branch": run("branch", "--show-current"),
        "status_porcelain": run("status", "--porcelain=v1"),
        "diff_stat": run("diff", "--stat"),
    }


def load_fixture(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"ERROR: cannot read EVAL-003 fixture {path}: {exc}") from exc
    if not isinstance(value, dict) or value.get("suite_id") != "EVAL-003":
        raise SystemExit("ERROR: fixture is not an EVAL-003 suite")
    return value


def run_case(case: dict, command_template: str, timeout: int, allow_self_report: bool) -> dict:
    prompt = str(case["task"])
    criteria = [str(item) for item in case["required_criteria"]]
    evidence_instruction = (
        "\n\nReturn a machine-readable completion record containing one line for every required criterion. "
        "Each line must begin exactly with 'CRITERION <criterion_id>:' followed by concise objective evidence. "
        "Do not claim PASS merely because a command was executed; distinguish execution from validation. "
        "If a criterion cannot be objectively established, write 'NOT_OBSERVED'."
    )
    prompt = prompt + evidence_instruction + "\nRequired criteria:\n" + "\n".join(f"- {item}" for item in criteria)
    command = shlex.split(command_template.replace("{prompt}", prompt))
    if not command:
        raise SystemExit("ERROR: --command must not be empty")

    env = os.environ.copy()
    env["AIENGINEERINGSTANDARD_EVAL_003"] = "1"
    before = git_snapshot()
    started = now()
    try:
        proc = subprocess.run(
            command, cwd=ROOT, capture_output=True, text=True, timeout=timeout, check=False, env=env
        )
        stdout = proc.stdout or ""
        stderr = proc.stderr or ""
        timed_out = False
        exit_code = proc.returncode
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout if isinstance(exc.stdout, str) else ""
        stderr = exc.stderr if isinstance(exc.stderr, str) else ""
        timed_out = True
        exit_code = None
    except OSError as exc:
        stdout, stderr = "", str(exc)
        timed_out = False
        exit_code = None
    after = git_snapshot()

    output = stdout + "\n" + stderr
    folded = output.casefold()
    criterion_results = []
    for criterion in criteria:
        marker = f"criterion {criterion}:".casefold()
        observed = marker in folded
        not_observed = f"criterion {criterion}: not_observed".casefold() in folded
        criterion_results.append({
            "id": criterion,
            "observed": observed and not not_observed,
            "status": "SELF_REPORTED" if observed and not not_observed else "NOT_OBSERVED",
        })

    observed_count = sum(item["observed"] for item in criterion_results)
    if timed_out:
        result = "FAIL"
    elif observed_count == len(criteria) and exit_code == 0 and allow_self_report:
        result = "PASS"
    elif observed_count > 0:
        result = "PARTIAL"
    else:
        result = "FAIL"

    return {
        "id": case["id"],
        "dimension": case["dimension"],
        "result": result,
        "measurement_mode": "self_report_allowed" if allow_self_report else "self_report_only",
        "exit_code": exit_code,
        "timed_out": timed_out,
        "criteria": criterion_results,
        "observed_criteria": observed_count,
        "total_criteria": len(criteria),
        "repository_before": before,
        "repository_after": after,
        "repository_state_changed": before != after,
        "started_at": started,
        "finished_at": now(),
        "stdout_excerpt": stdout[-12000:],
        "stderr_excerpt": stderr[-4000:],
    }


def overall(results: list[dict]) -> str:
    states = {item["result"] for item in results}
    if not results or states == {"UNTESTED"}:
        return "UNTESTED"
    if "FAIL" in states:
        return "FAIL"
    if "PARTIAL" in states or "UNTESTED" in states:
        return "PARTIAL"
    return "PASS"


def main() -> int:
    parser = argparse.ArgumentParser(description="Run EVAL-003 against a configured agent runtime.")
    parser.add_argument("--fixture", default=str(DEFAULT_FIXTURE))
    parser.add_argument("--command", required=True, help="Runtime command template; use {prompt} as the prompt placeholder")
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--output", help="Write machine-readable evaluation evidence to this path")
    parser.add_argument("--case", action="append", dest="case_ids", help="Run only the named case; may be repeated")
    parser.add_argument(
        "--allow-self-report",
        action="store_true",
        help="Allow complete self-reported criterion markers to produce PASS; without this flag they cannot prove PASS.",
    )
    args = parser.parse_args()
    if args.timeout < 1 or args.timeout > 900:
        raise SystemExit("ERROR: --timeout must be between 1 and 900 seconds")

    suite = load_fixture(Path(args.fixture))
    cases = suite["cases"]
    if args.case_ids:
        wanted = set(args.case_ids)
        cases = [case for case in cases if case.get("id") in wanted]
        missing = wanted - {case.get("id") for case in cases}
        if missing:
            raise SystemExit(f"ERROR: unknown EVAL-003 case(s): {sorted(missing)}")

    results = [run_case(case, args.command, args.timeout, args.allow_self_report) for case in cases]
    document = {
        "schema_version": "2.0.0",
        "suite_id": "EVAL-003",
        "method": "deterministic_runtime_measurement",
        "vendor_neutral": True,
        "measurement_boundary": (
            "self_report_criterion_markers_only; objective repository-state assertions are not yet implemented"
        ),
        "started_at": results[0]["started_at"] if results else now(),
        "finished_at": results[-1]["finished_at"] if results else now(),
        "result": overall(results),
        "cases": results,
    }
    text = json.dumps(document, ensure_ascii=False, indent=2) + "\n"
    print(text, end="")
    if args.output:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text, encoding="utf-8")
        print(f"EVAL-003 evidence written: {output}")
    return 0 if document["result"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
