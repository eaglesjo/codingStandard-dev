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

## Main integration

- Multi-Agent AI Developer 2.0 architecture was merged into `main` as PR #18, commit `df654a8fc73dfbd1c100c06b359c6086bc3d7e42`.
- Pre-merge architecture CI evidence: run `34790623343`, job `103814028876`, all validation steps passed including multi-agent contract, fixtures, and E2E simulation.
- Public promotion workflow run `34806455593` successfully promoted the then-validated candidate to `eaglesjo/AIEngineeringStandard`.
- Release-candidate audit found and corrected obsolete `Luna` terminology and generated Python cache artifacts on the public surface.
- Durable decision: actual AI provider/model mapping for individual agents is deferred to the next version; 2.0 remains vendor- and model-neutral.

## Completed foundation

- Nine bounded specialist agents and the AI Developer orchestrator.
- Three-stage relay: Analysis & Planning, Coding & Execution, Validation & Visualization.
- Normative Agent Contract and machine-readable schema.
- Skill-to-Agent mapping with conservative capability boundaries.
- Concrete Orchestrator control surface, permission ceilings, dispatch/acceptance gates, retry discipline, and lifecycle state authority.
- Automated Agent Contract validation, representative fixtures, contract-driven E2E simulation, and architecture CI integration.
- Development continuity and durable state recovery.
- Environment detection, reproducibility, dependency, training, LLM/Vision, installer, validation, and release-provenance foundations already present in the 2.0 architecture.

## Gap analysis result

The repository-backed analysis is recorded in `docs/development/2.0-FINAL-GAP-MATRIX.md`.

- AI Code Quality & Verification: **PARTIAL** — executable validation and review/testing procedures exist, but no dedicated AI-code quality/acceptance contract exists.
- AI/LLM Evaluation: **MISSING / PARTIAL FOUNDATION** — conformance validation exists, but no dedicated vendor-neutral LLM evaluation contract/scoring gate exists.
- Observability & Provenance: **IMPLEMENTED FOUNDATION / PARTIAL** — runtime evidence schema and provenance policy exist; cross-action observability/acceptance hardening remains.
- Data/Model Reproducibility: **PARTIAL** — experiment metadata captures seed, config hash, model revision, dataset revision, environment and Git state; enforceable artifact identity/reproducibility acceptance remains.

## Next bounded actions

1. Implement the smallest AI Code Quality & Verification contract and deterministic validation path.
2. Implement the minimal vendor-neutral AI/LLM Evaluation contract, fixtures, and scoring/acceptance validation.
3. Harden existing observability/provenance rather than creating a duplicate provenance system.
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
