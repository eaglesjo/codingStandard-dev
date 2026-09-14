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

## Next bounded actions

1. Complete repository-backed gap analysis for AI Code Quality & Verification, AI/LLM Evaluation, Observability & Provenance, and Data/Model Reproducibility.
2. Decide which gaps are release-relevant and define the smallest normative/machine-readable additions.
3. Implement executable validation for accepted additions and integrate it into CI.
4. Run full 2.0 validation and independent public-candidate audit.
5. Promote the exact validated source to `eaglesjo/AIEngineeringStandard`.
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
