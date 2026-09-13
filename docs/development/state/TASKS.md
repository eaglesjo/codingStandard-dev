# Development Task Queue

This file records durable development tasks so a fresh AI Developer session can determine what remains without reconstructing chat history.

## Active

- [ ] `MA-001` — Multi-Agent AI Developer 2.0 Architecture
  - [x] Define agent roles and boundaries
  - [x] Define AI Developer as orchestrator
  - [x] Define Agent Contract concept
  - [x] Define permission model
  - [x] Define lifecycle and orchestration protocol
  - [x] Define evidence and failure handling
  - [x] Add architecture document
  - [ ] Define concrete Agent Contract schema
  - [ ] Define orchestrator state machine
  - [ ] Map existing Skills to agents
  - [ ] Implement core agent surfaces
  - [ ] Implement Research & Browser surface
  - [ ] Validate end-to-end multi-agent flows
  - [ ] Validate fresh-session recovery with multi-agent state
  - [ ] Open integration PR

## Backlog

- [ ] Add automated checks for required recovery state fields.
- [ ] Add bounded stale-state detection for `CURRENT.md`.
- [ ] Evaluate whether Research and Browser should split into separate agents after V2 integration evidence exists.
- [ ] Evaluate controlled parallel execution only after sequential orchestration is proven.

## Completed reference

- `DSR-001` — Development State Recovery v1 — completed and merged as PR #17.

Completed tasks remain in `HISTORY.md`; do not delete them from history merely because they are no longer active.
