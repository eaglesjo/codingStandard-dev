# Multi-Agent AI Developer 2.0 Architecture

## 1. Purpose

AI Engineering Standard 2.0 extends the vendor-neutral AI Developer into a role-based multi-agent development system.

The goal is not to maximize the number of agents. The goal is to make development work auditable, bounded, recoverable, and independently verifiable.

The AI Developer remains the orchestrator. Specialist agents perform bounded work under explicit contracts and permissions.

## 2. Architecture

```text
                         AI Developer
                         Orchestrator
                              |
        +----------+----------+----------+-----------+
        |          |          |          |           |
        v          v          v          v           v
   File Picker  Planner    Editor    Validator   Reviewer
                                                
                         +-----------------------+
                         |
                         v
                  Research & Browser
```

The orchestrator owns task routing, dependency ordering, state transitions, retry decisions, approval boundaries, and durable recording.

Specialist agents MUST NOT arbitrarily invoke one another. Agent-to-agent coordination is mediated by the orchestrator.

## 3. Agents

### 3.1 AI Developer / Orchestrator

Responsibilities:

- interpret the user objective
- establish task scope and acceptance criteria
- select and sequence specialist agents
- enforce permission boundaries
- reconcile agent output with repository state
- decide whether work proceeds, loops back, or becomes blocked
- require evidence before completion claims
- record durable state and decisions

The orchestrator does not replace specialist expertise; it coordinates it.

### 3.2 File Picker Agent

Responsibilities:

- discover relevant files, directories, tests, configuration, and documentation
- trace direct and relevant indirect dependencies
- identify authoritative sources
- minimize unnecessary context loading
- return a bounded evidence set for the task

It MUST NOT modify repository content.

### 3.3 Planner Agent

Responsibilities:

- analyze requirements and current state
- decompose work into bounded actions
- identify dependencies, risks, and affected surfaces
- define implementation order
- define verification strategy and done criteria

It MUST NOT modify repository content.

Minimum plan output:

- objective
- targets
- method
- dependencies
- risks
- verification
- done criteria

### 3.4 Editor Agent

Responsibilities:

- implement approved code and documentation changes
- perform scoped refactoring
- add or update tests when required
- preserve existing architecture and project instructions
- report exactly what changed and what remains uncertain

The Editor MUST NOT self-certify final completion. Validation and review are separate responsibilities.

### 3.5 Validator Agent

Responsibilities:

- execute tests, lint, type checks, builds, and smoke tests as applicable
- inspect runtime behavior when required
- collect reproducible validation evidence
- distinguish implementation failures from environment failures
- report exact failed checks and likely owning scope

The Validator MUST NOT modify production source merely to make validation pass.

### 3.6 Reviewer Agent

Responsibilities:

- independently review requirements compliance
- inspect correctness and architecture
- identify security and regression risks
- assess maintainability and test coverage
- detect unnecessary or out-of-scope changes
- challenge unsupported completion claims

Default permission is read-only.

Review results:

- `PASS`
- `PASS_WITH_CONCERNS`
- `REQUEST_CHANGES`
- `BLOCKED`

A `REQUEST_CHANGES` result returns the task to the orchestrator for replanning or editor execution.

### 3.7 Research & Browser Agent

Responsibilities:

- research external technical information
- discover and compare authoritative sources
- verify source claims
- navigate websites when browser interaction is required
- perform bounded browser validation or website interaction
- return source-backed evidence separately from repository evidence

Research and browser capabilities are initially one agent boundary. They may be split later if independent scaling, permissions, or lifecycle requirements justify it.

## 4. Agent Contract

Every agent invocation uses a common conceptual contract.

### Input

```text
Task ID
Objective
Repository / workspace
Current durable state
Allowed scope
Available context
Constraints
Required evidence
```

### Output

```text
Status
Findings
Changes
Evidence
Risks
Blockers
Next action
```

Agent output MUST be machine-readable enough for the orchestrator to reason about state transitions, while remaining useful to a human reviewer.

## 5. Permission Model

| Agent | Read | Write | Execute | Web |
| --- | --- | --- | --- | --- |
| File Picker | yes | no | no | no |
| Planner | yes | no | no | no |
| Editor | yes | yes | bounded | no |
| Validator | yes | no | yes | no |
| Reviewer | yes | no | bounded | no |
| Research & Browser | bounded | no | bounded | yes |
| AI Developer | bounded | bounded | bounded | bounded |

Permissions are task-scoped, not global. A capability being available to an agent does not imply unrestricted access.

## 6. Lifecycle

```text
READY
  -> IN_PROGRESS
  -> PASS
  -> PASS_WITH_CONCERNS
  -> REQUEST_CHANGES
  -> BLOCKED
  -> FAILED
```

`REQUEST_CHANGES` is a controlled loop, not an implicit retry.

Retries MUST identify the cause of failure or uncertainty before re-execution. Blind repetition is prohibited.

## 7. Orchestration Protocol

Default development flow:

```text
User Request
    -> AI Developer
    -> File Picker
    -> Planner
    -> [Research & Browser when needed]
    -> Editor
    -> Validator
    -> Reviewer
    -> AI Developer decision
         |-> PASS -> Record
         |-> PASS_WITH_CONCERNS -> Record + explicit acceptance
         |-> REQUEST_CHANGES -> Planner/Editor loop
         |-> BLOCKED -> Record blocker and stop
```

The orchestrator may skip an agent when its responsibility is demonstrably unnecessary. Skipping MUST NOT bypass a required verification or review boundary.

## 8. State and Recovery

Development State Recovery is the persistence layer for multi-agent execution.

The durable recovery surface is:

```text
docs/development/state/CURRENT.md
docs/development/state/TASKS.md
docs/development/state/HISTORY.md
```

Future multi-agent state MAY include:

- active agent
- agent status
- task dependencies
- approval state
- validation evidence
- review findings
- retry count
- blocker reason

A fresh session MUST reconstruct execution from repository state, Git state, and durable evidence rather than conversation history.

## 9. Evidence Model

Completion requires evidence appropriate to the task.

Evidence categories include:

- repository inspection
- deterministic tests
- build output
- runtime smoke tests
- CI results
- review findings
- source-backed research evidence
- browser validation evidence

Agent claims are observations or recommendations until corroborated by the appropriate evidence source.

## 10. Failure Handling

When an agent fails:

1. preserve the failure evidence
2. classify the failure
3. identify the owning agent or task boundary
4. update durable state when material
5. replan if assumptions changed
6. retry only when a bounded corrective action exists

Environment failures MUST NOT be disguised as implementation success.

## 11. Design Principles

1. **Orchestration over agent proliferation** — add agents only when a clear responsibility or permission boundary exists.
2. **Skills over duplicated instructions** — agents reuse specialist Skills instead of copying procedures.
3. **Independent verification** — the agent that changes a surface does not provide the only completion judgment.
4. **Least privilege** — each agent receives only the capabilities required for its bounded task.
5. **Durable state** — material decisions and execution state survive chat/session interruption.
6. **Evidence before completion** — no completion claim without appropriate evidence.
7. **Vendor neutrality** — architecture is not coupled to a model provider or named AI persona.
8. **Bounded execution** — every invocation has an explicit scope and expected result.

## 12. V2 Implementation Order

Phase 1 — Contracts and orchestration:

- agent contract
- lifecycle/state model
- permission model
- orchestrator protocol
- durable state integration

Phase 2 — Core agents:

- File Picker
- Planner
- Editor
- Validator
- Reviewer

Phase 3 — Research & Browser:

- research/source verification
- browser navigation
- browser validation
- evidence integration

Phase 4 — Integration validation:

- documentation task
- bug-fix task
- feature task
- research-backed task
- validation failure and replan loop
- reviewer change-request loop
- fresh-session recovery

## 13. Non-Goals

2.0 does not require:

- one model per agent
- autonomous unrestricted agent-to-agent communication
- permanent parallel execution
- a separate agent for every Skill
- automatic public release

The architecture should remain useful even when all agents are backed by the same underlying model runtime.
