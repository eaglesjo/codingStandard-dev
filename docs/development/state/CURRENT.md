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

- ID: `UPGRADE-001`
- Title: Validate 1.7 → 2.0 no-delete upgrade compatibility
- Status: `IN_PROGRESS`
- Goal: establish evidence-backed upgrade behavior from the released v1.7.0 installation to the v2.x installation without requiring a pre-upgrade uninstall.

## Latest CI evidence

Ownership-reconciliation candidate `45d3b9a05eab8ace5c48b46bb094bb22502f30ae` passed both workflows:

- architecture validation run `34961720902`: PASS
- Windows installer validation run `34961720941`: PASS
- Windows PowerShell integration jobs: PASS

The ownership reconciliation regression is therefore validated by CI on the candidate.

## UPGRADE-001 evidence

The released public repository contains an actual `v1.7.0` tag. Its installer supports `en`/`ko`, the `common`/`ml`/`llm`/`vision`/`colab`/`all` domains, and `ask`/`merge`/`overwrite`/`skip` conflict policies. Its merge implementation uses coding-standard managed blocks for existing files.

A broader v1.7-shaped upgrade regression covers representative installed files from the common, ML, LLM, Vision, and Colab surfaces. The fixture also contains both a legacy-only unmanaged artifact and an obsolete v1.7 artifact containing a legacy managed block. The v2 installer is run directly with `merge` without uninstalling first. The test verifies v2 installation state, preservation/replacement behavior, preservation of both legacy artifacts, manifest ownership uniqueness, owned-file existence, reconciliation evidence preservation, and post-upgrade state reporting.

The fixture is representative compatibility coverage, not a complete byte-for-byte historical v1.7 installation snapshot. Do not claim full historical parity until the remaining migration surfaces are evidenced.

## Ownership reconciliation

Commit `42aecdf1f60bc82be189243ada5ea453da977069` adds `scripts/installers/reconcile_upgrade.py`.

Commit `4363109565f17e8926dffbd6b26b314639d3e052` extends the installer integration test to require reconciliation before direct upgrade.

Commit `3cea88ab37ec471472a34c71222450dc56c46561` adds the normative UPGRADE-001 contract at `docs/development/upgrade/UPGRADE-001.md`.

Commit `22683047a26065548c8f5abb4472fc1f0e735aad` adds an explicit stale/obsolete v1.7 artifact regression. A managed-looking file outside the desired v2 surface must remain `unknown-legacy` and must survive the direct upgrade.

Commit `5225ff23a9dff631fa2394d057e222872e7ce532` documents this safety boundary in the upgrade contract.

The reconciliation report classifies pre-v2 files as:

- `known-v2-managed`
- `legacy-managed-candidate`
- `project-owned`
- `unknown-legacy`

The report explicitly records `deletion_policy: never-delete-unknown`.

Important safety boundary: `legacy-managed-candidate` is only evidence that a desired v2 path contains a codingStandard managed-block marker. It is not treated as proof of complete historical ownership. Unknown legacy files are preserved and are never silently deleted during direct upgrade.

The reconciliation report is written to `.codingstandard/upgrade-reconciliation.json` before the v2 installation establishes its normal installation manifest.

## Release-quality finding already corrected in canonical main

The v2.0.0 public installer had exposed only five languages even though the public documentation and `i18n/languages.json` define 20 runtime/documentation locales. Canonical `main` was corrected to the full 20-locale catalog and installer integration tests were expanded to exercise all 20 locales. The already-published `v2.0.0` tag is not being rewritten.

Original fix commits:

- `89de08e16f4d2fc2ef475bd902d1adac8b5ea425` — installer locale alignment
- `7869f1db2771bec479e71be6bd6d485eefc2b577` — installer test coverage for all 20 locales

## Next bounded actions

1. Run fresh CI on the stale-artifact regression candidate.
2. If green, capture exact acceptance evidence.
3. Run post-upgrade `state` and repository validation on the reconciled fixture.
4. Document the supported upgrade contract boundaries and freeze the evidence.
5. Only then close UPGRADE-001.

## Next after UPGRADE-001

- Validate the complete 2.0 lifecycle on a real project.
- Build an AI Developer evaluation suite.
- Multi-Agent Runtime is a selectable execution layer with default `ON`; users can disable it, and the orchestrator may route only required agents.
- Then design the deferred `MODEL-ROUTING` capability for the next version.

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
