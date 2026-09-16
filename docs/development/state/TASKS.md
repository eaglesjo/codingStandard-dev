# Development Task Queue

This file records durable development tasks so a fresh AI Developer session can determine what remains without reconstructing chat history.

## Active

None. The repository is intentionally held at the AI Engineering Standard 2.0 release-era baseline pending a new development instruction.

## Discarded after the 2.0 baseline

- [discarded] `EVAL-003` — Build an AI Developer evaluation suite
  - All post-baseline implementation, fixtures, validators, runner changes, and tests were discarded.

- [discarded] `MA-002` — Validate multi-agent runtime execution
  - All post-baseline runtime-conformance implementation and related state changes were discarded.

## Deferred to next version

- [ ] `MODEL-ROUTING` — Multi-agent AI model/provider mapping
  - Provider/model adapters
  - Per-agent model assignment
  - Routing policies
  - Fallback selection
  - Model/provider provenance

## Completed at the 2.0 baseline

- [x] `REAL-002` — Validate the complete 2.0 lifecycle on the real project `eaglesjo/codingStandard-dev`
  - Explicit self-hosting target; no unrelated repository changes
  - Resolved the missing acceptance-boundary ambiguity
  - Recorded the bounded execution contract and durable recovery requirements
  - Validated candidate `8bf6df7c9322fabd08e39c1bd36a6d18f74d83a8`
  - Focused contract/recovery checks passed
  - Architecture validation run `34972844488` / job `104393094798` passed
  - codingStandard validation run `34972844585` / job `104393095466` passed
  - Windows installer validation run `34972844593` / jobs `104393095165`, `104393095696` passed
  - Fresh-session recovery reconstructed the task from repository state without chat history
  - Acceptance evidence is recorded in `docs/development/state/CURRENT.md`

- [x] `UPGRADE-001` — Validate 1.7 → 2.0 no-delete upgrade compatibility
- [x] `2.0-FINAL` — AI Engineering Standard 2.0 final quality and reproducibility hardening
- [x] `MA-001` — Multi-Agent AI Developer 2.0 Architecture
- [x] `DSR-001` — Development State Recovery v1

Completed tasks remain in `HISTORY.md`; do not delete them from history merely because they are no longer active.
