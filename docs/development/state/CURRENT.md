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
- Goal: establish evidence-backed upgrade behavior from the released v1.7.0 installation to the released v2.0.0 installation without requiring a pre-upgrade uninstall.

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

## UPGRADE-001 initial evidence

The released public repository contains an actual `v1.7.0` tag.

The v1.7.0 installer surface was inspected from:

`eaglesjo/AIEngineeringStandard:v1.7.0/scripts/installers/install-domains.sh`

Observed v1.7 behavior includes:

- supported languages: `en`, `ko`;
- domains: `common`, `ml`, `llm`, `vision`, `colab`, `all`;
- conflict policies: `ask`, `merge`, `overwrite`, `skip`;
- managed-block merge behavior for existing files;
- no v2 installation-state/ownership reconciliation contract in the inspected installer.

This establishes a concrete v1.7 fixture source rather than a guessed legacy state.

## Next bounded actions

1. Capture the v1.7.0 installed file set for a reproducible upgrade fixture.
2. Compare the v1.7.0 installer surface with the v2.0.0 installer/state model and classify migration boundaries.
3. Execute v2.0.0 installation against the v1.7 fixture without uninstalling first.
4. Verify preservation of project-owned content and expected merge/overwrite behavior.
5. Detect and classify stale/obsolete v1.7 artifacts instead of silently deleting them.
6. Validate v2 installation state/ownership reconciliation after the upgrade.
7. Run post-upgrade validation and record exact evidence.
8. Add executable regression coverage and document the supported upgrade contract.

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
