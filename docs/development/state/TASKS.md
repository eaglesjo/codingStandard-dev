# Development Task Queue

This file records durable development tasks so a fresh AI Developer session can determine what remains without reconstructing chat history.

## Active

- [ ] `DSR-001` — Development State Recovery v1
  - [x] Define `CURRENT.md`
  - [x] Define `TASKS.md`
  - [x] Define `HISTORY.md`
  - [x] Add AI Developer session-recovery procedure
  - [x] Update project agent entrypoint
  - [x] Update continuity rules
  - [ ] Validate the complete recovery contract
  - [ ] Record validation evidence
  - [ ] Open integration PR

## Backlog

- [ ] Add an explicit repository-identity/discovery contract if runtime behavior requires it.
- [ ] Add automated checks for required recovery files and mandatory fields.
- [ ] Define a bounded stale-state detection rule for `CURRENT.md`.

## Completed reference

Completed tasks remain in `HISTORY.md`; do not delete them from history merely because they are no longer active.
