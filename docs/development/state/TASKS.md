# Development Task Queue

This file records durable development tasks so a fresh AI Developer session can determine what remains without reconstructing chat history.

## Active

- [ ] `2.0-FINAL` — AI Engineering Standard 2.0 final quality and reproducibility hardening
  - [ ] Gap analysis: AI Code Quality & Verification
  - [ ] Gap analysis: AI/LLM Evaluation
  - [ ] Gap analysis: Observability & Provenance
  - [ ] Gap analysis: Data/Model Reproducibility
  - [ ] Define normative rules and machine-readable contracts where justified
  - [ ] Add executable validation for the accepted 2.0 additions
  - [ ] Integrate accepted validation into CI
  - [ ] Run full 2.0 validation and public-candidate audit
  - [ ] Promote exact validated source to `eaglesjo/AIEngineeringStandard`
  - [ ] Prepare release notes
  - [ ] Obtain explicit authorization before creating the v2.0.0 tag/release

## Deferred to next version

- [ ] `MODEL-ROUTING` — Multi-agent AI model/provider mapping
  - Provider/model adapters
  - Per-agent model assignment
  - Routing policies
  - Fallback selection
  - Model/provider provenance

## Completed reference

- `MA-001` — Multi-Agent AI Developer 2.0 Architecture — core architecture, agent contract, specialist surfaces, orchestration rules, and automated contract/E2E validation were implemented and merged.
- `DSR-001` — Development State Recovery v1 — completed and merged as PR #17.

Completed tasks remain in `HISTORY.md`; do not delete them from history merely because they are no longer active.
