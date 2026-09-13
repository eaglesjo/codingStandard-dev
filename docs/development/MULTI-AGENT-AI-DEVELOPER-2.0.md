# Multi-Agent AI Developer 2.0 Architecture

## 1. Purpose

AI Engineering Standard 2.0 extends the vendor-neutral AI Developer into a role-based multi-agent development system.

The goal is not to maximize the number of agents. The goal is to make development work auditable, bounded, recoverable, efficient, and independently verifiable.

The AI Developer remains the orchestrator. Nine specialist agents perform bounded work under explicit contracts and permissions.

The nine agents are organized into three relay stages:

```text
Stage 1 — Analysis & Planning
  File Picker -> Planner -> Web Researcher (when required)

Stage 2 — Coding & Execution
  Editor -> Executor -> Terminal Monitor

Stage 3 — Validation & Visualization
  Reviewer -> Browser Agent -> Debugger (when required)
```

The arrows describe the default relay order, not a mandatory serial execution of every agent. The orchestrator may parallelize independent work, skip unnecessary agents, or loop back to the smallest owning agent when evidence requires it.

## 2. Architecture

```text
                         AI Developer
                         Orchestrator
                              |
             +----------------+----------------+
             |                |                |
             v                v                v
       Stage 1            Stage 2          Stage 3
       Analysis           Coding           Validation
       & Planning         & Execution      & Visualization
             |                |                |
   +---------+--------+   +---+------+---+   +---+------+------+
   |         |        |   |          |   |   |          |      |
   v         v        v   v          v   v   v          v      v
 File      Planner  Web  Editor   Executor TM  Reviewer Browser Debugger
 Picker            Researcher          Monitor            Agent
```

The orchestrator owns task routing, dependency ordering, parallelization decisions, state transitions, retry decisions, approval boundaries, and durable recording.

Specialist agents MUST NOT arbitrarily invoke one another. Agent-to-agent coordination is mediated by the orchestrator.

## 3. Nine Specialist Agents

### 3.1 Stage 1 — Analysis & Planning

#### File Picker Agent

Responsibilities:

- discover relevant files, directories, tests, configuration, and documentation
- trace direct and relevant indirect dependencies
- identify authoritative repository sources
- minimize unnecessary context loading
- return a bounded evidence set for the task

It MUST NOT modify repository content.

#### Planner Agent

Responsibilities:

- analyze the user objective and current state
- decompose work into bounded actions
- identify dependencies, risks, affected surfaces, and rollback considerations
- define implementation order
- identify work that can safely run in parallel
- define verification strategy and done criteria

It MUST NOT modify repository content.

Minimum plan output:

- objective
- targets
- assumptions
- dependencies
- execution graph
- risks
- verification
- done criteria
- rollback/recovery strategy

#### Web Researcher Agent

Responsibilities:

- research current external technical information
- discover authoritative documentation, API specifications, standards, and release information
- compare sources and detect conflicting claims
- provide source-backed implementation constraints
- separate external evidence from repository evidence

It SHOULD run in parallel with repository analysis when the task has independent external-information needs. It MUST NOT be invoked merely because web access is available.

### 3.2 Stage 2 — Coding & Execution

#### Editor Agent

Responsibilities:

- implement approved code and documentation changes
- perform scoped refactoring
- add or update tests when required
- preserve existing architecture and project instructions
- report exactly what changed and what remains uncertain

The Editor MUST NOT self-certify final completion.

#### Executor Agent

Responsibilities:

- prepare the declared development/runtime environment
- install or restore dependencies when authorized
- run build, test, migration, generation, packaging, or application commands
- manage bounded local or cloud execution tasks
- capture command, exit status, duration, and relevant artifacts
- distinguish setup failures from application failures

Execution MUST be reproducible and task-scoped. Installing arbitrary global software or changing persistent host configuration is prohibited unless explicitly authorized.

#### Terminal Monitor Agent

Responsibilities:

- observe long-running or interactive execution output
- detect crashes, hangs, repeated errors, warnings, resource exhaustion, and abnormal termination
- correlate runtime symptoms with the executing command and task
- trigger a bounded escalation to the orchestrator when intervention is required
- preserve relevant terminal evidence

Terminal Monitor is primarily observational. It MUST NOT silently edit source code or restart a failing workload indefinitely.

### 3.3 Stage 3 — Validation & Visualization

#### Reviewer Agent

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

A `REQUEST_CHANGES` result returns the task to the orchestrator for a bounded replan/edit cycle.

#### Browser Agent

Responsibilities:

- launch or connect to an approved browser environment
- validate web application navigation and critical user flows
- inspect rendered UI, layout, interaction, console errors, and network failures when relevant
- verify forms, buttons, links, and visible states
- capture reproducible browser evidence

Browser validation is required only for tasks whose acceptance criteria include browser-visible behavior. It MUST NOT be treated as a substitute for deterministic tests.

#### Debugger Agent

Responsibilities:

- analyze failures reported by Validator, Executor, Terminal Monitor, Reviewer, or Browser Agent
- isolate root cause and owning surface
- produce the smallest corrective change
- apply code/config/test fixes when authorized
- hand the result back to Executor/Validator for independent verification

Debugger is an exception-handling specialist, not a permanent final-stage editor. It MUST NOT declare success based only on symptom disappearance.

## 4. Agent Contract

Every agent invocation uses a common conceptual contract. The normative schema is defined in `docs/development/multi-agent/AGENT-CONTRACT.md`.

### Input

```text
Task ID
Objective
Repository / workspace
Current durable state
Agent role and version
Allowed scope
Permissions
Available context / evidence references
Constraints
Required evidence
Attempt number
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
Artifacts
```

Agent output MUST be machine-readable enough for the orchestrator to reason about state transitions, while remaining useful to a human reviewer.

## 5. Permission Model

| Agent | Read | Write | Execute | Web | Runtime Observe |
| --- | --- | --- | --- | --- | --- |
| File Picker | yes | no | no | no | no |
| Planner | yes | no | no | no | no |
| Web Researcher | bounded | no | bounded | yes | no |
| Editor | yes | yes | bounded | no | no |
| Executor | yes | bounded | yes | bounded | yes |
| Terminal Monitor | bounded | no | bounded | no | yes |
| Reviewer | yes | no | bounded | no | no |
| Browser Agent | bounded | no | bounded | yes | yes |
| Debugger | yes | yes | bounded | no | no |
| AI Developer | bounded | bounded | bounded | bounded | bounded |

Permissions are task-scoped, not global. A capability being available to an agent does not imply unrestricted access.

## 6. Relay Model and Efficient Real-Development Strategy

The relay is optimized around **handoff quality, parallel work, and early failure detection**, not around making every request pass through all nine agents.

### 6.1 Default relay

```text
User Request
    -> AI Developer
    -> File Picker
    -> Planner
    -> Web Researcher [if external facts are needed]
    -> Editor
    -> Executor
    -> Terminal Monitor [for long-running/interactive execution]
    -> Reviewer
    -> Browser Agent [for browser-visible acceptance criteria]
    -> AI Developer decision
         |-> PASS -> Record
         |-> PASS_WITH_CONCERNS -> explicit acceptance -> Record
         |-> REQUEST_CHANGES -> Planner -> Editor/Debugger -> Executor -> validation
         |-> BLOCKED -> Record blocker and stop
```

### 6.2 Dynamic routing

The orchestrator SHOULD select the smallest workflow that satisfies the task's evidence requirements.

Examples:

- documentation-only change: File Picker -> Planner -> Editor -> Reviewer
- isolated bug fix with tests: File Picker -> Planner -> Editor -> Executor -> Reviewer
- dependency/API change: File Picker + Web Researcher (parallel) -> Planner -> Editor -> Executor -> Reviewer
- web UI feature: File Picker + Web Researcher -> Planner -> Editor -> Executor -> Terminal Monitor -> Reviewer + Browser Agent
- runtime crash: File Picker -> Planner -> Executor/Terminal Monitor -> Debugger -> Executor -> Reviewer
- long-running job: Planner -> Editor -> Executor -> Terminal Monitor -> execution evidence -> Reviewer

A stage or agent MAY be skipped only when its responsibility is demonstrably unnecessary. Skipping an agent MUST NOT bypass a required acceptance criterion.

### 6.3 Parallelization rules

Parallel execution is allowed only when work units have no unresolved write dependency or when their outputs are read-only evidence.

Safe examples:

- File Picker repository scan || Web Researcher external research
- independent test suites || independent static checks
- Reviewer inspection || Browser Agent validation after the same immutable candidate state exists

Unsafe examples:

- two Editors modifying overlapping files
- Editor changing code while Reviewer reviews the same mutable worktree
- Debugger editing before failure evidence is captured

When parallel outputs conflict, the orchestrator reconciles them before the next write-capable step.

### 6.4 Context economy

To keep real development fast and reliable:

1. File Picker returns targeted file/evidence references rather than the entire repository.
2. Planner receives the minimum sufficient context plus durable state.
3. Agents pass artifacts and evidence references instead of repeating full outputs.
4. Executor records command-level evidence rather than dumping unlimited logs into agent context.
5. Terminal Monitor escalates only actionable anomalies.
6. Reviewer receives the final diff plus relevant plan, tests, and evidence—not every intermediate transcript.
7. Debugger receives the smallest reproducible failure package.

### 6.5 Quality gates

The orchestrator MUST enforce gates at stage boundaries:

```text
Stage 1 Gate:
  scope + targets + plan + required external evidence known

Stage 2 Gate:
  intended changes applied + execution evidence captured

Stage 3 Gate:
  acceptance criteria independently verified

Final Gate:
  no unresolved blocker + evidence sufficient for completion claim + durable state recorded
```

A failed gate sends the task to the smallest responsible corrective step instead of restarting the entire pipeline.

## 7. Lifecycle and State Machine

```text
READY
  -> ANALYZING
  -> PLANNING
  -> EDITING
  -> EXECUTING
  -> VALIDATING
  -> REVIEWING
  -> PASS

VALIDATING/REVIEWING
  -> REQUEST_CHANGES
  -> PLANNING

Any active state
  -> BLOCKED
  -> FAILED

FAILED/BLOCKED
  -> PLANNING only after a bounded recovery action is identified
```

`REQUEST_CHANGES` is a controlled loop, not an implicit retry.

Retries MUST identify the cause of failure or uncertainty before re-execution. Blind repetition is prohibited.

## 8. Orchestration Protocol

The orchestrator creates a task envelope, selects agents, enforces permissions, and records every material handoff.

Each handoff SHOULD contain:

```text
Task ID
Parent task / dependency
Current state
Objective
Input evidence references
Expected output
Allowed scope
Permissions
Attempt number
Timeout / stop condition
Success criteria
```

The receiving agent MUST return a contract-compliant result. The orchestrator validates that result before advancing the state.

Specialists MUST NOT create hidden side effects outside their declared scope.

## 9. State and Recovery

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
- stage
- task dependencies
- approval state
- validation evidence references
- review findings
- retry count
- blocker reason
- last successful handoff
- pending next action

A fresh session MUST reconstruct execution from repository state, Git state, and durable evidence rather than conversation history.

## 10. Evidence Model

Completion requires evidence appropriate to the task.

Evidence categories include:

- repository inspection
- deterministic tests
- build output
- execution output
- runtime smoke tests
- CI results
- review findings
- source-backed research evidence
- browser validation evidence
- screenshots or other visual artifacts where required

Agent claims are observations or recommendations until corroborated by the appropriate evidence source.

## 11. Failure Handling

When an agent fails:

1. preserve the failure evidence
2. classify the failure
3. identify the owning agent or task boundary
4. update durable state when material
5. replan if assumptions changed
6. retry only when a bounded corrective action exists

Failure routing SHOULD prefer the smallest responsible loop:

```text
Research conflict -> Web Researcher
Wrong file/scope -> File Picker / Planner
Implementation defect -> Editor or Debugger
Environment/command failure -> Executor
Runtime symptom -> Terminal Monitor -> Debugger
Requirement/quality issue -> Reviewer -> Planner/Editor
UI issue -> Browser Agent -> Debugger
```

Environment failures MUST NOT be disguised as implementation success.

## 12. Skills and Agent Boundaries

Agents are execution roles; Skills are reusable methods. Skills MUST NOT be copied into every agent definition.

Initial mapping:

| Agent | Existing / planned Skills |
| --- | --- |
| File Picker | `repository-analysis` |
| Planner | `repository-analysis` + future planning skill |
| Web Researcher | future research/browser skill |
| Editor | `implementation`, `debugging`, `testing-validation` |
| Executor | `testing-validation`, environment/runtime procedures |
| Terminal Monitor | runtime/debugging procedures |
| Reviewer | `code-review`, `testing-validation` |
| Browser Agent | future browser-validation skill |
| Debugger | `debugging`, `implementation`, `testing-validation` |
| AI Developer | `ai-developer`, `development-continuity` |

An agent may use multiple Skills. A Skill should be extended only when a recurring gap cannot be solved by task-specific orchestration.

## 13. Design Principles

1. **Orchestration over agent proliferation** — nine roles are justified by distinct responsibility or permission boundaries.
2. **Relay with dynamic routing** — the three stages provide a predictable default while allowing safe skips and loops.
3. **Skills over duplicated instructions** — agents reuse specialist Skills instead of copying procedures.
4. **Independent verification** — the agent that changes a surface does not provide the only completion judgment.
5. **Least privilege** — each agent receives only the capabilities required for its bounded task.
6. **Durable state** — material decisions and execution state survive chat/session interruption.
7. **Evidence before completion** — no completion claim without appropriate evidence.
8. **Vendor neutrality** — architecture is not coupled to a model provider or named AI persona.
9. **Bounded execution** — every invocation has explicit scope, stop conditions, and expected result.
10. **Failure-local recovery** — fix the smallest responsible boundary instead of restarting the full pipeline.
11. **Context economy** — pass references and artifacts, not unnecessary transcripts or whole repositories.
12. **Human approval for consequential actions** — destructive, external, or release-impacting operations require explicit authorization boundaries.

## 14. V2 Implementation Order

Phase 1 — Contracts and orchestration:

- agent contract schema and artifact format
- lifecycle/state model
- permission model
- orchestrator protocol
- durable state integration
- relay and routing rules

Phase 2 — Core agents:

- File Picker
- Planner
- Editor
- Executor
- Terminal Monitor
- Reviewer
- Debugger

Phase 3 — External and visual capabilities:

- Web Researcher
- Browser Agent
- research/source verification
- browser validation
- evidence integration

Phase 4 — Integration validation:

- documentation task
- bug-fix task
- feature task
- research-backed task
- browser UI task
- validation failure and replan loop
- reviewer change-request loop
- debugger recovery loop
- fresh-session recovery
- parallel execution safety

## 15. Non-Goals

2.0 does not require:

- one model per agent
- autonomous unrestricted agent-to-agent communication
- permanent parallel execution
- a separate agent for every Skill
- automatic public release
- all nine agents running for every request

The architecture should remain useful even when all agents are backed by the same underlying model runtime.
