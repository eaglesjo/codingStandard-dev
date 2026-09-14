# Current Development State

This file is the durable handoff point for the active development task.

## Recovery contract

A new AI Developer session MUST treat repository state as authoritative and use this file to identify the last completed work and the next bounded action.

## Project

- Repository: `eaglesjo/codingStandard-dev`
- Canonical development branch: `main`
- Public release surface: `eaglesjo/AIEngineeringStandard`

## Active task

- ID: `2.0-FINAL`
- Title: AI Engineering Standard 2.0 final quality and reproducibility hardening
- Status: `IN_PROGRESS`
- Goal: complete the 2.0 quality, evaluation, observability/provenance, and data/model reproducibility foundations without coupling agents to specific AI providers or models.

## Current implementation

- Repository-backed gap analysis completed and recorded in `docs/development/2.0-FINAL-GAP-MATRIX.md`.
- AI Code Quality & Verification first implementation added:
  - `core/validation/ai-code-quality.schema.json`
  - `scripts/validation/validate_ai_code_quality.py`
  - architecture CI now executes the AI code quality contract validator.
- The quality contract requires evidence for scope, focused test, quality check, broader validation, and review before acceptance; accepted candidates must be clean revisions.
- This is intentionally a minimal vendor-neutral acceptance contract, not a new language-specific static-analysis framework.

## Evidence notes

- Existing `core/validation/conformance-evidence.schema.json` already provides runtime conformance evidence with repository/runtime identity, observations, checks, and evidence levels.
- Existing `core/common/experiment.py` already records experiment seed, config hash, model revision, dataset revision, environment profile, runtime config, and Git state.
- These existing foundations will be hardened rather than duplicated.

## Next bounded actions

1. Add focused positive/negative fixtures or tests for the AI Code Quality contract and run the validator.
2. Implement the minimal vendor-neutral AI/LLM Evaluation contract, fixtures, and deterministic scorer/acceptance validation.
3. Harden existing observability/provenance around cross-action traceability and acceptance.
4. Harden data/model reproducibility from metadata capture into enforceable integrity and acceptance checks.
5. Integrate accepted validation into CI and run the full 2.0 gate.
6. Freeze the validated candidate, independently audit the public candidate, and promote the exact validated source.
7. Prepare release notes; public tag/release creation remains a separate explicit authorization boundary.

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
