# Development Task Queue

This file records durable development tasks so a fresh AI Developer session can determine what remains without reconstructing chat history.

## Active

- [ ] `EVAL-003` — Build an AI Developer evaluation suite
  - representative development tasks
  - deterministic case/fixture coverage
  - failure-mode coverage
  - validation/evidence completeness
  - unnecessary-change detection
  - bounded-retry behavior
  - fresh-session continuity

- [ ] `MA-002` — Validate multi-agent runtime execution
  - preserve vendor/model-neutral contracts
  - execute representative agent routes
  - validate permissions and handoffs at runtime
  - validate failure routing and evidence

## Deferred to next version

- [ ] `MODEL-ROUTING` — Multi-agent AI model/provider mapping
  - Provider/model adapters
  - Per-agent model assignment
  - Routing policies
  - Fallback selection
  - Model/provider provenance

## Completed

- [x] `REAL-002` — Validate the complete 2.0 lifecycle on the real project `eaglesjo/codingStandard-dev`
  - Explicit self-hosting target; no unrelated repository changes
  - Resolved the missing acceptance-boundary ambiguity
  - Recorded the bounded execution contract and durable recovery requirements
  - Final validated candidate `28434d9d75c337438465934d12359a162aa54f69`
  - Architecture validation run `34976603912` / job `104405785663` passed
  - codingStandard validation run `34976603907` / job `104405786815` passed
  - Windows installer validation run `34976603809` / jobs `104405785762`, `104405785963` passed
  - Fresh-session recovery reconstructed the task from repository state without chat history
  - Acceptance evidence is recorded in `docs/development/state/CURRENT.md` and `HISTORY.md`

- [x] `UPGRADE-001` — Validate 1.7 → 2.0 no-delete upgrade compatibility
  - Verified the released `v1.7.0` installer surface and its managed-block/conflict-policy behavior
  - Added representative direct-upgrade regression coverage without pre-upgrade uninstall
  - Added ownership reconciliation with conservative `unknown-legacy` classification
  - Enforced `never-delete-unknown` safety policy
  - Added stale/obsolete legacy artifact regression
  - Verified project-owned content preservation and managed-block replacement under explicit `merge`
  - Verified v2 manifest ownership uniqueness and owned-file existence
  - Verified post-upgrade `state`: `installed: true`, `modified: 0`, `missing: 0`
  - Fresh architecture and repository/installer validation passed on candidate `93f97ea92960bd8565d59f8b096207584d21ac2f`
  - Acceptance boundary: representative v1.7 compatibility surface, not byte-for-byte parity with every historical installation

- [x] `2.0-FINAL` — AI Engineering Standard 2.0 final quality and reproducibility hardening
  - AI Code Quality & Verification contract and executable validation
  - AI/LLM Evaluation contract and executable validation
  - Observability/Provenance hardening
  - Data/Model Reproducibility contract and executable validation
  - Cross-area 2.0 acceptance gate
  - 20-locale README/documentation quality re-review
  - Public-boundary validation hardening
  - Fresh `Validate codingStandard` validation for final candidate
  - Fresh Windows Installer Validation for final candidate
  - Exact-source public promotion
  - `AIEngineeringStandard` v2.0.0 release

- [x] `MA-001` — Multi-Agent AI Developer 2.0 Architecture — core architecture, agent contract, specialist surfaces, orchestration rules, and automated contract/E2E validation were implemented and merged.
- [x] `DSR-001` — Development State Recovery v1 — completed and merged as PR #17.

Completed tasks remain in `HISTORY.md`; do not delete them from history merely because they are no longer active.
