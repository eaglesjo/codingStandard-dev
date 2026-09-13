# Development Task Queue

This file records durable development tasks so a fresh AI Developer session can determine what remains without reconstructing chat history.

## Active

- [ ] `MA-001` — Multi-Agent AI Developer 2.0 Architecture
  - [x] Define agent roles and boundaries
  - [x] Define AI Developer as orchestrator
  - [x] Define Agent Contract concept
  - [x] Define concrete Agent Contract schema and artifact format
  - [x] Define permission model
  - [x] Define lifecycle/state machine and orchestration protocol
  - [x] Define evidence and failure handling
  - [x] Define efficient real-development relay, parallelization, and context-economy rules
  - [x] Add architecture document
  - [x] Add machine-readable `agent-contract.schema.json`
  - [x] Map existing Skills to agents
  - [x] Implement core agent surfaces: File Picker and Planner
  - [x] Implement bounded coding/execution surfaces: Editor and Executor
  - [x] Implement Terminal Monitor and Reviewer
  - [x] Implement Debugger recovery loop
  - [x] Implement Research & Browser surface
  - [x] Define concrete Orchestrator control surface
  - [x] Define permission ceilings and lifecycle transition enforcement
  - [x] Add automated Agent Contract enforcement validation
  - [x] Add representative valid/invalid/failure-recovery fixtures
  - [x] Wire Agent Contract validation into architecture CI
  - [x] Implement contract-driven multi-agent E2E simulation
  - [ ] Verify CI execution and passing evidence on PR #18, including E2E simulation
  - [ ] Validate fresh-session recovery with multi-agent state
  - [ ] Merge architecture after required evidence

## Backlog

- [ ] Add automated checks for required recovery state fields.
- [ ] Add bounded stale-state detection for `CURRENT.md`.
- [ ] Evaluate controlled parallel execution only after sequential orchestration is proven.
- [ ] Evaluate whether Researcher and Browser should remain separate or share infrastructure after V2 integration evidence exists.

## Completed reference

- `DSR-001` — Development State Recovery v1 — completed and merged as PR #17.

Completed tasks remain in `HISTORY.md`; do not delete them from history merely because they are no longer active.
