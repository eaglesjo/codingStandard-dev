# REAL-002 — Bounded Execution Plan

## Target

`eaglesjo/codingStandard-dev` on `main`.

This is a self-hosting validation. No unrelated repository is part of REAL-002.

## Starting evidence

- Repository default branch: `main`.
- Existing architecture validation evidence: workflow job `104364722988` passed all architecture, multi-agent, AI code quality, AI evaluation, reproducibility, and cross-area 2.0 acceptance steps.
- Existing codingStandard validation evidence: workflow job `104364723251` passed architecture contract, repository validation, environment contract, installer tests, LLM CPU smoke test, and Vision CPU smoke test.
- These existing runs are baseline evidence only; they do not constitute REAL-002 completion.

## Bounded task

Use the canonical repository to validate the AI Developer development lifecycle against one real maintenance task: establish and record the REAL-002 acceptance boundary and execution contract in durable state.

The task is intentionally documentation/state oriented. It tests repository discovery, planning, minimal implementation, focused validation, broader validation, provenance capture, and fresh-session recovery without introducing unrelated product code.

## Execution sequence

1. Discover repository instructions, AI Developer Skill, Development Continuity Skill, `CURRENT.md`, `TASKS.md`, `HISTORY.md`, and relevant 2.0 contracts.
2. Confirm the target and candidate starting revision from Git state.
3. Implement only the files required to make the REAL-002 boundary durable and unambiguous.
4. Validate the changed documentation/state contract with focused checks.
5. Run the broader repository validation gate required by the project.
6. Capture exact candidate SHA and validation run/job evidence.
7. Update durable state with the completed bounded action, evidence, and next action.
8. Perform a fresh-session recovery check using repository state only; do not use chat history as evidence.
9. Record the final REAL-002 acceptance decision.

## Acceptance gates

REAL-002 may be marked PASS only if:

- the target remains exactly `eaglesjo/codingStandard-dev`;
- no unrelated repository is modified;
- only bounded owning files are changed;
- focused validation passes;
- broader required validation passes;
- exact candidate SHA is captured;
- evidence/provenance identifies the task and validation runs;
- durable state identifies the completed action and next action;
- a fresh session can reconstruct the state without chat history;
- no unsupported runtime capability is inferred as PASS.

## Failure/recovery rule

If a validation gate fails, preserve the failure evidence, identify the smallest responsible boundary, make the smallest repair, and rerun only the necessary validation before the broader gate. Do not perform unrelated cleanup.

## Non-goals

- No PetLM changes.
- No other repository changes.
- No public `v2.0.0` tag rewrite.
- No provider/model routing implementation.
- No requirement to execute all nine specialist agents.
