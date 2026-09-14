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
- AI Code Quality & Verification implementation added with contract, positive/negative fixtures, focused tests, and CI validation.
- AI/LLM Evaluation implementation added with deterministic vendor-neutral contract, positive/negative fixtures, focused tests, and CI validation.
- Observability/Provenance hardening added:
  - conformance evidence requires trace identity (`action_id`) and supports `parent_action_id` plus unique `evidence_id`.
  - provenance policy defines cross-action traceability and forbids silent reuse of unrelated action/revision evidence.
- Data/Model Reproducibility implementation added:
  - `core/validation/reproducibility.schema.json`
  - `scripts/validation/validate_reproducibility.py`
  - positive/negative fixtures and focused tests
  - architecture CI validation.
- Reproducibility acceptance requires experiment identity (experiment/variant/seed/config hash/Git revision/clean state) plus immutable SHA-256 identities for recorded artifacts. A `REPRODUCIBLE` result cannot be accepted from a dirty revision.
- Cross-area 2.0 acceptance implementation added:
  - `core/validation/2.0-acceptance.schema.json`
  - `scripts/validation/validate_2_0_acceptance.py`
  - positive/mismatch fixtures and focused tests
  - architecture CI now executes the final cross-area acceptance gate.
- The cross-area gate binds code quality, deterministic evaluation, provenance, and reproducibility evidence to one clean candidate revision before overall `ACCEPTED` status is possible.

## Locale quality re-review

A full second-pass review of all 20 documentation locales was completed on the canonical `main` branch.

- English canonical README was reconciled with the public release boundary; retired internal repository references were removed.
- All 19 non-English README locales were reworked for natural-language quality, terminology, grammar, consistency, and current public repository paths.
- All locale READMEs now point to `https://github.com/eaglesjo/AIEngineeringStandard.git` in their installation examples.
- Installation and validation examples were normalized to the public repository layout.
- Locale-specific wording was corrected rather than merely reported, including runtime/localization terminology in German, Italian, Portuguese, Polish, Swedish, Ukrainian, and other locales.
- `i18n/README.md` was reconciled with the 2.0 localization quality contract; stale `v1.16` references were removed.
- `i18n/languages.json` remains the catalog source for the 20 documentation/runtime locales.
- Repository searches after the review found no `codingStandard-private`, `codingStandard.git`, or `v1.16` references in the canonical repository.
- Canonical README and INSTALL validation commands now use the explicit public path `./AIEngineeringStandard/...`, matching the documented clone layout.

## Public-boundary validation

- `scripts/validation/validate.py` was made aware of the public export boundary in commit `394fbda51c0e71b12f294c73696a3f64770f754d` so public validation does not require development-only `AGENTS.md` or `.github/workflows/windows-install-test.yml`.
- The validator explicitly reports that Windows workflow evidence is validated in `codingStandard-dev` CI when running against the public export.
- This boundary fix and the locale/documentation changes require fresh CI before the next promotion.

## Evidence notes

- Existing `core/common/experiment.py` already records standard version, experiment ID, variant, seed, config hash/config, model revision, dataset revision, environment profile, runtime config, and Git state.
- The new reproducibility contract turns that metadata foundation into an explicit evidence/acceptance boundary rather than treating metadata emission alone as proof.
- The new AI evaluation contract deliberately does not introduce a provider/model-specific judge or runtime dependency.
- CI includes quality, evaluation, reproducibility, and cross-area acceptance validators/tests in `.github/workflows/validate-architecture.yml`.
- Fresh full CI evidence is available for candidate `60d5fb7801d10ec239a9a66b88265eaa1bb4f4d0`:
  - `Validate codingStandard` run `34814381117` completed `success`.
  - Windows installer validation run `34814381091` completed successfully for the same candidate.
- That evidence predates the later public-boundary validator fix and the second locale/documentation review, so it is not sufficient for the current release candidate.
- The latest documentation/localization commits are on `main`; the latest recorded commit in this handoff sequence is the locale-quality state update itself. No fresh workflow evidence is currently associated with that final state yet.

## Next bounded actions

1. Run fresh `Validate codingStandard` and the Windows installer validation against the post-review `main` candidate.
2. If CI exposes any localization, validation-boundary, or documentation-path defect, fix it at the smallest owning file and repeat only the necessary validation.
3. Freeze the first fully green post-review candidate SHA.
4. Manually dispatch `.github/workflows/promote-release.yml` with that exact SHA; the GitHub connector does not provide workflow-dispatch capability.
5. Verify public `AIEngineeringStandard/main` content and re-run the public audit: no retired/internal references, no generated artifacts, no secrets, correct `VERSION=2.0.0`, 20-locale consistency, and working documented validation paths.
6. Record promotion evidence before any separate public tag/release authorization.

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
