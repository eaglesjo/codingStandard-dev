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

- ID: `EVAL-003`
- Title: Build an AI Developer evaluation suite
- Status: `IN_PROGRESS`
- Execution plan: `docs/development/EVAL-003-EXECUTION-PLAN.md`

## Completed task: REAL-002

- Status: `PASS`
- Target: `eaglesjo/codingStandard-dev` itself
- No unrelated repository was modified.
- Final validated candidate: `28434d9d75c337438465934d12359a162aa54f69`
- Architecture validation run `34976603912` / job `104405785663`: PASS
- codingStandard validation run `34976603907` / job `104405786815`: PASS
- Windows installer validation run `34976603809` / jobs `104405785762`, `104405785963`: PASS
- Fresh-session recovery was demonstrated from repository state without chat history.
- Durable completion record is in `docs/development/state/HISTORY.md`.

## EVAL-003 next bounded action

Build the first deterministic case/fixture set for AI Developer behavior, starting with repository recovery and scope-control cases. Use the existing `ai-evaluation` schema and validator; do not introduce provider/model-specific judging.

Initial case dimensions:

1. repository recovery;
2. scope control;
3. planning quality;
4. implementation discipline;
5. validation/evidence completeness;
6. failure diagnosis;
7. bounded retry;
8. unnecessary-change detection;
9. development continuity.

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
