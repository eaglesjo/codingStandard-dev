# Skill-to-Agent Mapping

This document maps the current reusable Skills to the executable multi-agent surfaces. It is intentionally conservative: an agent may apply a Skill without inheriting capabilities that belong to another role.

## Current mapping

| Agent | Primary Skills | Capability boundary | Status |
| --- | --- | --- | --- |
| File Picker | `repository-analysis` | read-only discovery | implemented |
| Planner | `repository-analysis`, `implementation` | read-only planning | implemented |
| Web Researcher | external research procedures | web research only | implemented |
| Editor | `implementation`, `debugging`, `testing-validation` | bounded source writes | implemented |
| Executor | `testing-validation` + runtime/environment procedures | bounded execution | implemented |
| Terminal Monitor | `debugging` + runtime procedures | observe/escalate | implemented |
| Reviewer | `code-review`, `testing-validation` | read-only validation | implemented |
| Browser Agent | browser validation procedures | browser validation | implemented |
| Debugger | `debugging`, `implementation`, `testing-validation` | bounded corrective changes | implemented |
| AI Developer / Orchestrator | `ai-developer`, `development-continuity` | orchestration/state transition | orchestrator surface planned |

## Boundary rule

Skill reuse is procedural reuse, not permission inheritance. The Agent Contract remains authoritative for effective capabilities, scope, evidence, and state transitions.

## First executable loop

```text
File Picker
  -> Planner
  -> Editor
  -> Executor
  -> Terminal Monitor [when runtime monitoring is needed]
  -> Reviewer
  -> AI Developer decision
```

## Failure recovery loop

```text
Executor / Terminal Monitor
  -> failure evidence
  -> Debugger
  -> bounded corrective change
  -> Executor
  -> Terminal Monitor [when needed]
  -> Reviewer
  -> AI Developer decision
```

## External research / browser loop

```text
File Picker + Web Researcher [parallel when independent]
          ↓
       Planner
          ↓
       Editor
          ↓
       Executor
          ↓
 Reviewer + Browser Agent [parallel when independent]
          ↓
 AI Developer decision
```

Web Researcher and Browser Agent are both read-only with respect to repository source. They do not inherit Editor, Executor, or publication permissions.

## Missing Skills

Do not create Skills solely to mirror the agent count. The current agent surfaces use existing procedural guidance where sufficient; dedicated reusable Skills should be introduced only after repeated workflows demonstrate a real gap.
