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
- AI Code Quality & Verification implementation added:
  - `core/validation/ai-code-quality.schema.json`
  - `scripts/validation/validate_ai_code_quality.py`
  - positive/negative fixtures and focused tests
  - architecture CI executes the validator and focused tests.
- AI/LLM Evaluation minimal implementation added:
  - `core/validation/ai-evaluation.schema.json`
  - `scripts/validation/validate_ai_evaluation.py`
  - positive/negative fixtures and focused tests
  - architecture CI executes the validator and focused tests.
- The evaluation contract is deterministic and vendor-neutral: each case records input, expected criteria, criterion evidence, a derived 0..1 case score, and an acceptance threshold. The validator rejects score/evidence mismatches and acceptance below threshold.
- Observability/Provenance hardening added:
  - `core/validation/conformance-evidence.schema.json` now requires trace identity (`action_id`) and supports `parent_action_id` plus unique `evidence_id`.
  - `core/validation/evidence-provenance-policy.md` now defines cross-action traceability and forbids silent reuse of unrelated action/revision evidence.

## Evidence notes

- Existing conformance evidence already carries repository/runtime identity, observations, checks, and evidence levels; the hardening extends that same system rather than introducing a second provenance system. fileciteturn510file0
- Existing `core/common/experiment.py` already records standard version, experiment ID, variant, seed, config hash/config, model revision, dataset revision, environment profile, runtime config, and Git state. fileciteturn523file0
- The new AI evaluation contract deliberately does not introduce a provider/model-specific judge or runtime dependency.
- Commit `4e93789f2e25fcfdd8fb88ac71ea87abc785b9d1` contains the CI integration for the quality/evaluation validators and focused tests; combined status at that point had no status entries, so CI execution was not independently evidenced then.
- Provenance hardening commits: `6054259ac3be61881ea16209d8a1f0cec56cf881`, `b9ed1b980f5e2af853cc4be5ed7e0e5097475cdf`.

## Next bounded actions

1. Obtain fresh CI evidence for the latest main revision and diagnose before retrying if any job fails.
2. Harden data/model reproducibility from metadata capture into enforceable artifact identity and deterministic acceptance checks.
3. Add cross-area acceptance validation and integrate the final 2.0 gate.
4. Freeze the validated candidate, independently audit the public candidate, and promote the exact validated source.
5. Prepare release notes; public tag/release creation remains a separate explicit authorization boundary.

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
