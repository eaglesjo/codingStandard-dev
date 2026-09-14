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
  - `tests/validation/fixtures/ai-code-quality/valid.json`
  - `tests/validation/fixtures/ai-code-quality/invalid_not_all_pass.json`
  - `tests/validation/test_ai_code_quality.py`
  - architecture CI executes the AI code quality validator and focused tests.
- The quality contract requires evidence for scope, focused test, quality check, broader validation, and review before acceptance; accepted candidates must be clean revisions.
- This is intentionally a minimal vendor-neutral acceptance contract, not a new language-specific static-analysis framework.
- AI/LLM Evaluation minimal implementation added:
  - `core/validation/ai-evaluation.schema.json`
  - `scripts/validation/validate_ai_evaluation.py`
  - `tests/validation/fixtures/ai-evaluation/valid.json`
  - `tests/validation/fixtures/ai-evaluation/invalid_score.json`
  - `tests/validation/test_ai_evaluation.py`
  - architecture CI executes the evaluation validator and focused tests.
- The evaluation contract is deterministic and vendor-neutral: each case records input, expected criteria, criterion evidence, a derived 0..1 case score, and an acceptance threshold. The validator rejects score/evidence mismatches and acceptance below threshold.

## Evidence notes

- Existing `core/validation/conformance-evidence.schema.json` already provides runtime conformance evidence with repository/runtime identity, observations, checks, and evidence levels.
- Existing `core/common/experiment.py` already records experiment seed, config hash, model revision, dataset revision, environment profile, runtime config, and Git state.
- The new AI evaluation contract deliberately does not introduce a provider/model-specific judge or runtime dependency.
- Commit `4e93789f2e25fcfdd8fb88ac71ea87abc785b9d1` contains the latest CI integration; combined commit status currently reports no status entries, so CI execution has not yet been independently evidenced from that commit.

## Next bounded actions

1. Obtain CI evidence for the current AI Code Quality and AI/LLM Evaluation validators/tests; diagnose before retrying if any job fails.
2. Harden existing observability/provenance around cross-action traceability and acceptance.
3. Harden data/model reproducibility from metadata capture into enforceable integrity and acceptance checks.
4. Integrate accepted validation into CI and run the full 2.0 gate.
5. Freeze the validated candidate, independently audit the public candidate, and promote the exact validated source.
6. Prepare release notes; public tag/release creation remains a separate explicit authorization boundary.

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
