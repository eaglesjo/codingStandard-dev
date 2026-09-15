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

Candidate `48be3dea5b1bfb20602d053178287ff5d1926c7d` was validated by fresh `Validate codingStandard` run `34933418917`.

Result:
- architecture validation: PASS
- repository validation: PASS
- environment contract: PASS
- installer test: FAIL

Failure boundary was the PowerShell wrapper locale contract, not the v1.7 upgrade regression. The installer integration test reached the PowerShell all-lifecycle section and failed on locale `fr` because `scripts/installers/install-domains.ps1` still had a stale five-locale `ValidateSet` (`en`, `ko`, `zh-CN`, `ja`, `ru`). The underlying Python installer already accepts all 20 locales.

This is a real installer parity defect exposed by the expanded 20-locale regression coverage. It is unrelated to the upgrade fixture itself.

Windows installer validation also ran for the same candidate and must be rechecked against the corrected wrapper candidate.

## Current correction

Fixed `scripts/installers/install-domains.ps1` in:

`c0c1734e76d0eab4d8ca5a1ec497e539d130dad8` — `fix(installer): align PowerShell locale contract with 20 locales`

The PowerShell `ValidateSet` now matches the canonical 20-locale runtime catalog:

`en`, `ko`, `fr`, `es`, `zh-CN`, `ja`, `ru`, `tr`, `de`, `it`, `pt`, `ar`, `hi`, `id`, `vi`, `th`, `nl`, `pl`, `sv`, `uk`.

## UPGRADE-001 evidence

The released public repository contains an actual `v1.7.0` tag. Its installer supports `en`/`ko`, the `common`/`ml`/`llm`/`vision`/`colab`/`all` domains, and `ask`/`merge`/`overwrite`/`skip` conflict policies. Its merge implementation uses coding-standard managed blocks for existing files.

A broader v1.7-shaped upgrade regression covers representative installed files from the common, ML, LLM, Vision, and Colab surfaces. The fixture also contains a legacy-only unmanaged artifact. The v2 installer is run directly with `merge` without uninstalling first. The test verifies v2 installation state, preservation/replacement behavior, unmanaged artifact preservation, manifest ownership uniqueness, owned-file existence, and post-upgrade state reporting.

The fixture is representative compatibility coverage, not a complete byte-for-byte historical v1.7 installation snapshot. Do not claim full historical parity until the remaining migration surfaces are evidenced.

## Release-quality finding already corrected in canonical main

The v2.0.0 public installer had exposed only five languages even though the public documentation and `i18n/languages.json` define 20 runtime/documentation locales. Canonical `main` was corrected to the full 20-locale catalog and installer integration tests were expanded to exercise all 20 locales. The already-published `v2.0.0` tag is not being rewritten.

Original fix commits:

- `89de08e16f4d2fc2ef475bd902d1adac8b5ea425` — installer locale alignment
- `7869f1db2771bec479e71be6bd6d485eefc2b577` — installer test coverage for all 20 locales

## Next bounded actions

1. Validate corrected candidate `c0c1734e76d0eab4d8ca5a1ec497e539d130dad8` in fresh `Validate codingStandard` and Windows installer CI.
2. If green, capture exact green evidence and freeze the candidate.
3. Add stale/obsolete v1.7 artifact classification coverage; do not silently delete unmanaged files.
4. Complete installation-state and ownership reconciliation evidence after direct upgrade.
5. Run post-upgrade validation and record exact evidence.
6. Document the supported upgrade contract and its boundaries.

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
