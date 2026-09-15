# Current Development State

This file is the durable handoff point for the active development task.

## Recovery contract

A new AI Developer session MUST treat repository state as authoritative and use this file to identify the last completed work and the next bounded action.

## Project

- Repository: `eaglesjo/codingStandard-dev`
- Canonical development branch: `main`
- Public release surface: `eaglesjo/AIEngineeringStandard`
- Released version: `2.0.0`

## Active task

- ID: `REAL-002`
- Title: Validate the complete 2.0 lifecycle on the real project `eaglesjo/codingStandard-dev`
- Status: `IN_PROGRESS`
- Acceptance contract: `docs/development/REAL-002.md`

## REAL-002 target boundary

The real-project target is explicitly `eaglesjo/codingStandard-dev` itself. This is a self-hosting validation of the AI Engineering Standard development system.

PetLM and every other unrelated repository are outside REAL-002 and MUST NOT be modified as part of this task.

## First bounded action

Execute the bounded maintenance task defined in `docs/development/REAL-002.md`: validate the repository's actual instructions and durable state, resolve the REAL-002 acceptance-boundary ambiguity, validate the resulting candidate, and record exact evidence for recovery.

## Latest completed task

`UPGRADE-001` — Validate 1.7 → 2.0 no-delete upgrade compatibility — is complete for its defined representative compatibility boundary.

Final validated candidate before durable-state documentation:

`93f97ea92960bd8565d59f8b096207584d21ac2f`

Fresh CI evidence:

- architecture validation run `34964212287`: PASS
- architecture job `104364722988`: PASS
- codingStandard validation run `34964212295`: PASS
- validation job `104364723251`: PASS

The validation job passed repository validation, environment contract tests, installer lifecycle tests, LLM CPU memory smoke tests, and Vision CPU memory smoke tests. The installer lifecycle test includes the direct v1.7-shaped upgrade regression, reconciliation, stale/obsolete legacy artifact preservation, manifest/state validation, all 20 Bash locales, and PowerShell integration on supported runners.

## UPGRADE-001 acceptance boundary

The accepted contract is:

- direct v1.7-shaped → v2 installation is allowed without mandatory uninstall
- project-owned content is preserved under explicit `merge`
- legacy managed blocks on desired v2 paths are replaced under explicit `merge`
- unknown legacy files are never silently deleted
- obsolete legacy artifacts outside the desired v2 surface remain `unknown-legacy` and survive the upgrade
- v2 manifest ownership is unique and every owned file exists
- post-upgrade state reports `installed: true`, `modified: 0`, `missing: 0`

The regression fixture is representative, not a byte-for-byte snapshot of every historical v1.7 installation. Historical ownership is never guessed when evidence is absent. The full acceptance evidence and boundary are frozen in `docs/development/upgrade/UPGRADE-001.md`.

## Release-quality finding already corrected in canonical main

The v2.0.0 public installer had exposed only five languages even though the public documentation and `i18n/languages.json` define 20 runtime/documentation locales. Canonical `main` was corrected to the full 20-locale catalog and installer integration tests were expanded to exercise all 20 locales. The already-published `v2.0.0` tag is not being rewritten.

Original fix commits:

- `89de08e16f4d2fc2ef475bd902d1adac8b5ea425` — installer locale alignment
- `7869f1db2771bec479e71be6bd6d485eefc2b577` — installer test coverage for all 20 locales

## Next bounded actions

1. Complete the REAL-002 bounded maintenance task and its acceptance evidence.
2. Build the AI Developer evaluation suite (`EVAL-003`).
3. Validate Multi-Agent Runtime execution (`MA-002`) when justified by the lifecycle acceptance criteria.
4. After those, design the deferred `MODEL-ROUTING` capability for the next version.

## Deferred to next version

- Provider/model adapters.
- Per-agent AI model assignment.
- Model routing policies and fallback selection.
- Provider/model-specific runtime coupling.

## Rules

- Never use chat history as the sole source of truth.
- Do not mark a task complete without repository or CI evidence.
- Keep agent boundaries role-based and vendor-neutral.
- Do not add agents merely to increase agent count.
- Do not force all nine agents into every task; route only the agents required by acceptance criteria.
- Prefer parallel read-only work and single-owner overlapping writes.
- Freeze the candidate revision before independent parallel validation.
- On failure, preserve evidence and repair the smallest responsible boundary instead of restarting the full pipeline.
- Preserve exact source identity and validation evidence across the dev/release boundary.
- 2.0 must remain vendor/model-neutral; AI provider/model mapping belongs to the next version.
- Review task-created branches after completion and delete branches with no remaining development or recovery value.
