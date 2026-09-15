# REAL-002 — Real-project 2.0 lifecycle validation

## Purpose

`REAL-002` validates that the AI Engineering Standard 2.0 development system can be used for an actual software-development task without relying on chat-only coordination.

This task is a **self-hosting validation**: the real project under test is `eaglesjo/codingStandard-dev`, the canonical development repository for the standard itself.

This is intentional. A real-project target must not be selected arbitrarily from an unrelated user repository. The project must be explicitly identified by the durable task definition before execution begins.

## Why codingStandard-dev is the target

`codingStandard-dev` is itself a real, continuously maintained software project. It contains:

- project instructions and engineering rules;
- portable AI Developer Skills;
- implementation and validation code;
- CI workflows;
- reproducibility/provenance contracts;
- release-boundary rules; and
- durable development-state recovery.

The repository therefore exercises the same development system that REAL-002 is intended to validate.

## Scope

REAL-002 validates one bounded development lifecycle, not every possible project or every possible AI runtime.

The lifecycle under test is:

```text
Discover
  → Detect
  → Measure
  → Resolve
  → Smoke Test
  → Lock
  → Implement
  → Validate
  → Record
```

and the AI Developer coordination loop is:

```text
Understand → Plan → Implement → Verify → Record
```

## Bounded real task

The first REAL-002 task is to resolve the missing acceptance boundary that previously allowed the real-project target to be selected ambiguously.

The task must:

1. inspect the repository's actual instructions and durable state;
2. identify the smallest owning documentation/state boundary;
3. define and record the REAL-002 acceptance contract;
4. make only the necessary repository changes;
5. run the applicable validation gates against the resulting candidate;
6. preserve exact source identity and evidence; and
7. leave durable state sufficient for a fresh session to resume without chat history.

This is a real maintenance task in the canonical project, not a synthetic fixture and not an external-project modification.

## Required capabilities

### 1. Repository discovery

Evidence must show that the AI Developer recovered:

- repository identity;
- current revision;
- `AGENTS.md`;
- relevant Skills;
- Development Continuity rules;
- `CURRENT.md`;
- `TASKS.md`;
- relevant 2.0 conformance/provenance contracts.

### 2. Planning

The plan must identify:

- the actual problem;
- the smallest owning files;
- acceptance criteria;
- validation commands/gates;
- evidence to retain.

### 3. Implementation

Only the files required by the acceptance contract may be changed. No unrelated repository cleanup is part of REAL-002.

### 4. Execution

The resulting candidate must be exercised through the repository's applicable validation path. Static file presence alone is not runtime conformance evidence.

### 5. Validation

At minimum, the candidate must receive:

- focused validation of the changed contract;
- the broader repository/architecture validation gate required by the project;
- exact candidate SHA capture.

If an agent-runtime capability is explicitly exercised, its evidence must follow the 2.0 conformance protocol and runtime-conformance rules. Unsupported or unobservable capabilities remain `UNTESTED` rather than being inferred as PASS.

### 6. Provenance

The acceptance record must identify:

- candidate commit SHA;
- task/scenario identifier;
- runtime/agent identity when runtime execution occurs;
- validation runs and results;
- relevant evidence references;
- final acceptance decision.

### 7. Recovery

The lifecycle must be recoverable from repository state after an interruption. A fresh session must be able to identify the first incomplete bounded action from durable state alone.

## Multi-agent boundary

REAL-002 validates the **AI Developer orchestration contract**, but it does not require all nine specialist agents to execute.

The orchestrator may use only the minimum required Skills/agents for the bounded task. Actual nine-agent runtime validation remains `MA-002`.

This prevents REAL-002 from becoming an accidental duplicate of the separate Multi-Agent Runtime task.

## Runtime conformance boundary

The existing 2.0 runtime-conformance protocol remains authoritative. Runtime claims require objective evidence; model output or static repository presence is not sufficient. The current Codex P0 path intentionally leaves capabilities without trustworthy runtime telemetry as `UNTESTED`.

REAL-002 therefore may establish lifecycle integration without falsely claiming full runtime conformance for every agent capability.

## Acceptance criteria

REAL-002 is `PASS` only when all of the following are true:

- [ ] target project is explicitly `eaglesjo/codingStandard-dev`;
- [ ] no unrelated repository is modified as part of REAL-002;
- [ ] repository instructions and relevant Skills were actually used;
- [ ] a bounded real development task was completed;
- [ ] focused validation passed;
- [ ] broader required validation passed;
- [ ] exact candidate SHA is recorded;
- [ ] provenance/evidence is recorded;
- [ ] durable state records the completed action and next action;
- [ ] a fresh-session recovery check can reconstruct the state without chat history;
- [ ] no runtime capability is marked PASS without objective evidence.

## Non-goals

REAL-002 does not:

- validate every AI provider;
- select a production model for each agent;
- implement model/provider routing;
- require all nine specialist agents to run;
- rewrite the already-published `v2.0.0` public tag;
- modify PetLM or any other unrelated project.

## Completion evidence

The final acceptance record belongs in the durable development state and must reference the exact candidate SHA and validation evidence. This document defines the boundary; it does not itself constitute execution evidence.
