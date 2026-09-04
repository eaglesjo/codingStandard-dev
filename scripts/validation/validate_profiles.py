from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROFILES = ROOT / "profiles"
REQUIRED_PROJECT_KEYS = {
    "id", "profile_version", "project_type", "architecture_profile",
    "policy_profile", "runtime", "delivery", "scalability",
}
REQUIRED_ARCH_KEYS = {
    "id", "profile_version", "project_type", "layers",
    "dependency_direction", "forbidden_dependencies", "boundaries",
    "scalability_profile",
}
REQUIRED_POLICY_KEYS = {
    "id", "profile_version", "scope", "rules", "inheritance",
}
FORBIDDEN_TEXT = ("password", "secret", "api_key", "token=", "/Users/", "/home/")
ID_RE = re.compile(r"[a-z0-9][a-z0-9-]*\Z")


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def load(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"invalid profile {path}: {exc}")
    if not isinstance(value, dict):
        fail(f"profile must be an object: {path}")
    return value


def check_keys(value: dict, required: set[str], path: Path) -> None:
    missing = sorted(required - value.keys())
    if missing:
        fail(f"missing keys in {path}: {', '.join(missing)}")


def check_id(value: dict, path: Path) -> None:
    if not isinstance(value.get("id"), str) or not ID_RE.fullmatch(value["id"]):
        fail(f"invalid profile id in {path}")
    if value.get("profile_version") != 1:
        fail(f"unsupported profile_version in {path}")


def check_project(path: Path, value: dict, architecture_ids: set[str], policy_ids: set[str]) -> None:
    check_keys(value, REQUIRED_PROJECT_KEYS, path)
    check_id(value, path)
    if value["architecture_profile"] not in architecture_ids:
        fail(f"unknown architecture_profile '{value['architecture_profile']}' in {path}")
    if value["policy_profile"] not in policy_ids:
        fail(f"unknown policy_profile '{value['policy_profile']}' in {path}")
    runtime = value["runtime"]
    if not isinstance(runtime, dict) or not {"os", "reference", "python"} <= runtime.keys():
        fail(f"runtime contract incomplete in {path}")
    oses = runtime.get("os")
    if not isinstance(oses, list) or not {"linux", "macos", "windows"} <= set(oses):
        fail(f"project profile must declare cross-platform support in {path}")
    if value["delivery"].get("validation_required") is not True:
        fail(f"delivery.validation_required must be true in {path}")


def check_architecture(path: Path, value: dict) -> None:
    check_keys(value, REQUIRED_ARCH_KEYS, path)
    check_id(value, path)
    layers = value["layers"]
    if not isinstance(layers, dict) or not layers:
        fail(f"architecture layers must be a non-empty object in {path}")
    allowed = set(layers)
    directions = value["dependency_direction"]
    forbidden = value["forbidden_dependencies"]
    if not isinstance(directions, list) or not isinstance(forbidden, list):
        fail(f"dependency contracts must be arrays in {path}")
    for edge in [*directions, *forbidden]:
        if not isinstance(edge, str) or " -> " not in edge:
            fail(f"invalid dependency edge in {path}: {edge!r}")
        source, target = edge.split(" -> ", 1)
        if source not in allowed or target not in allowed:
            fail(f"dependency edge references unknown layer in {path}: {edge}")
    overlap = set(directions) & set(forbidden)
    if overlap:
        fail(f"dependency edge is both allowed and forbidden in {path}: {sorted(overlap)[0]}")
    if not isinstance(value["boundaries"], list) or not value["boundaries"]:
        fail(f"architecture boundaries must be a non-empty array in {path}")


def check_policy(path: Path, value: dict) -> None:
    check_keys(value, REQUIRED_POLICY_KEYS, path)
    check_id(value, path)
    if value["scope"] != "repository":
        fail(f"repository policy must have scope=repository in {path}")
    if not isinstance(value["rules"], dict) or not value["rules"]:
        fail(f"policy rules must be a non-empty object in {path}")
    inheritance = value["inheritance"]
    required_inheritance = {
        "child_scopes_may_add_restrictions",
        "child_scopes_may_not_weaken_parent",
        "conflict_resolution",
    }
    if not isinstance(inheritance, dict) or not required_inheritance <= inheritance.keys():
        fail(f"policy inheritance contract incomplete in {path}")
    if inheritance["child_scopes_may_not_weaken_parent"] is not True:
        fail(f"policy inheritance must prevent weakening parent rules in {path}")
    if inheritance["conflict_resolution"] != "stricter-wins":
        fail(f"policy conflict resolution must be stricter-wins in {path}")


def check_sensitive_text(path: Path) -> None:
    text = path.read_text(encoding="utf-8").lower()
    for marker in FORBIDDEN_TEXT:
        if marker in text:
            fail(f"potential secret or machine-specific reference '{marker}' in {path}")


def main() -> None:
    if not PROFILES.is_dir():
        fail("profiles directory is missing")
    architecture_dir = PROFILES / "architecture"
    policy_dir = PROFILES / "policies"
    architecture_paths = sorted(architecture_dir.glob("*.json")) if architecture_dir.is_dir() else []
    policy_paths = sorted(policy_dir.glob("*.json")) if policy_dir.is_dir() else []
    project_paths = sorted(PROFILES.glob("project*.json"))
    if not architecture_paths:
        fail("no architecture profiles found")
    if not policy_paths:
        fail("no policy profiles found")
    if not project_paths:
        fail("no project profiles found")

    architecture_ids: set[str] = set()
    for path in architecture_paths:
        value = load(path)
        check_architecture(path, value)
        architecture_ids.add(value["id"])
        check_sensitive_text(path)

    policy_ids: set[str] = set()
    for path in policy_paths:
        value = load(path)
        check_policy(path, value)
        policy_ids.add(value["id"])
        check_sensitive_text(path)

    for path in project_paths:
        value = load(path)
        check_project(path, value, architecture_ids, policy_ids)
        check_sensitive_text(path)

    print(
        f"architecture profile validation passed "
        f"({len(architecture_paths)} architecture, {len(policy_paths)} policy, {len(project_paths)} project)"
    )


if __name__ == "__main__":
    main()
