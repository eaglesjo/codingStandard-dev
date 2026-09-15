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

## 2.0 release state

AI Engineering Standard 2.0 final quality/reproducibility hardening is complete and the public v2.0.0 release is already published.

Validated 2.0 source revision:

`6fed7b85f162611e6f5aa16dc857905b597b56ea`

The public distribution was promoted from that exact validated source and released as `v2.0.0`.

The completed 2.0 scope includes:

- AI Code Quality & Verification contract and executable validation.
- AI/LLM Evaluation contract and executable validation.
- Observability/Provenance hardening with trace identity and evidence provenance.
- Data/Model Reproducibility contract and executable validation.
- Cross-area 2.0 acceptance binding the four areas to one clean candidate revision.
- 20-locale documentation/runtime quality validation and README re-review.
- Public-boundary validation hardening.
- Fresh coding-standard and Windows installer validation for the final candidate.
- Exact-source public promotion and v2.0.0 release.

## UPGRADE-001 evidence

The released public repository contains an actual `v1.7.0` tag.

The v1.7.0 installer surface was inspected from:

`eaglesjo/AIEngineeringStandard:v1.7.0/scripts/installers/install-domains.sh`

Observed v1.7 behavior includes:

- supported languages: `en`, `ko`;
- domains: `common`, `ml`, `llm`, `vision`, `colab`, `all`;
- conflict policies: `ask`, `merge`, `overwrite`, `skip`;
- managed-block merge behavior for existing files;
- no v2 installation-state/ownership reconciliation contract in the inspected installer.

A regression test was added to exercise a representative v1.7-shaped project with no v2 manifest, local project-owned rules, and an unmanaged legacy artifact. The v2 installer is then run directly with `merge` without uninstalling first and the test verifies that local content and unmanaged legacy content survive while a v2 installation manifest is established.

Upgrade regression commits:

- `0187e360466d003186e9002655e7c49c4d09de53` — initial v1.7 → v2 regression test
- `de0a036e6057458f87ff6b326a1e610f5c75d42b` — remove obsolete `_probe_v13` installer artifact
- `aca6807f9b62f5055bfdc9706bee941d6bbfadf7` — fix regression fixture target creation

The first CI attempt exposed only a test-fixture defect (`FileNotFoundError` because the temporary legacy target directory was not created). That defect was corrected in `aca6807f...` and a fresh validation run is currently in progress for that exact SHA.

## Release-quality finding already corrected in canonical main

The v2.0.0 public installer had exposed only five languages (`en`, `ko`, `zh-CN`, `ja`, `ru`) even though the public documentation and `i18n/languages.json` define 20 runtime/documentation locales.

Canonical `main` was corrected to the full 20-locale catalog and installer integration tests were expanded to exercise all 20 locales. The already-published `v2.0.0` tag is not being rewritten.

Original fix commits:

- `89de08e16f4d2fc2ef475bd902d1adac8b5ea425` — installer locale alignment
- `7869f1db2771bec479e71be6bd6d485eefc2b577` — installer test coverage for all 20 locales

## Next bounded actions

1. Finish fresh CI validation for `aca6807f9b62f5055bfdc9706bee941d6bbfadf7`.
2. If green, capture the exact green evidence and freeze that candidate.
3. Strengthen the v1.7 fixture toward a broader installed-file snapshot where practical; do not claim full historical parity from the current representative fixture alone.
4. Validate upgrade preservation/merge behavior across representative common and domain files.
5. Detect and classify stale/obsolete v1.7 artifacts instead of silently deleting them.
6. Validate installation state/ownership reconciliation after the upgrade.
7. Run post-upgrade validation and record exact evidence.
8. Document the supported upgrade contract.

## Next after UPGRADE-001

- Validate the complete 2.0 lifecycle on a real project.
- Build an AI Developer evaluation suite.
- Validate multi-agent runtime execution.
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
