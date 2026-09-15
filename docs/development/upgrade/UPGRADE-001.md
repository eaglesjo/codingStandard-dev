# UPGRADE-001 — v1.7 → v2 upgrade contract

## Scope

A v1.7 installation must be allowed to receive v2 without a mandatory pre-upgrade uninstall.

The upgrade path is evidence-driven and conservative. A missing v2 installation manifest means v2 cannot safely infer complete historical ownership.

## Ownership classes

Before the first v2 installation, the upgrade reconciliation step classifies existing files as:

- `known-v2-managed` — files already represented by a valid v2 installation manifest.
- `legacy-managed-candidate` — files in the desired v2 surface containing a codingStandard managed-block marker, but with no v2 ownership manifest proving current ownership.
- `project-owned` — files in the desired v2 surface that do not contain a codingStandard managed-block marker.
- `unknown-legacy` — existing files outside the desired v2 surface.

`legacy-managed-candidate` is intentionally a candidate classification, not proof of historical ownership. The system must not infer more than the evidence supports.

## Safety rules

1. **Never delete unknown legacy files during direct v1.7 → v2 installation.**
2. Existing managed-block candidates may be updated by an explicitly selected merge policy.
3. Project-owned files are subject to the normal explicit conflict policy (`ask`, `merge`, `overwrite`, `skip`).
4. A v2 manifest is established only after the installation completes.
5. Post-upgrade state must report `installed: true`, `modified: 0`, and `missing: 0` for the newly established v2 ownership set.
6. Unknown legacy files remain outside the v2 manifest unless a later explicit installation operation claims them.
7. Obsolete-file deletion is permitted only when prior v2 ownership evidence exists. The normal `update` lifecycle can therefore remove an obsolete file only when the v2 manifest proves that codingStandard previously owned it and the installed content is unchanged.
8. A stale legacy artifact that looks managed but is outside the desired v2 surface is still `unknown-legacy`; the presence of a managed-block marker does not authorize deletion.

## Evidence

`python3 scripts/installers/reconcile_upgrade.py <target> --domain all` writes:

`<target>/.codingstandard/upgrade-reconciliation.json`

The report records the classification and the explicit deletion policy `never-delete-unknown`.

The regression fixture explicitly includes both an unmanaged legacy artifact and an obsolete v1.7 artifact containing a legacy managed block. Both must survive the direct upgrade.

## Validation result

UPGRADE-001 is accepted for the supported compatibility boundary represented by the executable regression fixture.

Final candidate:

`93f97ea92960bd8565d59f8b096207584d21ac2f`

Fresh CI evidence:

- Architecture validation run `34964212287` — PASS
- `Validate architecture contract` job `104364722988` — PASS
- CodingStandard validation run `34964212295` — PASS
- `validate` job `104364723251` — PASS
- Installer integration test — PASS, including the direct v1.7-shaped upgrade regression, all 20 Bash locales, and PowerShell integration on supported runners
- Repository validation, environment contract, LLM CPU smoke test, and Vision CPU smoke test — PASS in the same validation job

The installer regression verifies all of the following on the reconciled fixture:

- v2 installation occurs directly without uninstalling first
- project-owned content is preserved
- legacy managed blocks on desired v2 paths are replaced under explicit `merge` policy
- unmanaged legacy files survive
- obsolete legacy files outside the desired v2 surface survive even when they contain a legacy managed-block marker
- reconciliation evidence survives the upgrade
- the v2 manifest has unique ownership entries and every owned file exists
- post-upgrade `state` reports `installed: true`, `modified: 0`, `missing: 0`

## Current validation boundary

The automated UPGRADE-001 regression uses a representative v1.7 installation fixture. It proves the ownership and safety contract for the represented legacy surface; it does not claim byte-for-byte compatibility with every historical v1.7 installation.

This boundary is intentional: historical v1.7 ownership cannot be safely inferred where no v2 ownership evidence exists, so unknown legacy files are preserved rather than guessed or deleted.
