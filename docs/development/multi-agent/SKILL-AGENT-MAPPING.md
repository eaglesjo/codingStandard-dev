# Skill-to-Agent Mapping

This document maps the current reusable Skills to the executable multi-agent surfaces. It is intentionally conservative: an agent may apply a Skill without inheriting capabilities that belong to another role.

## Current mapping

| Agent | Primary Skills | Capability boundary | Status |
| --- | --- | --- | --- |
| File Picker | `repository-analysis` | read-only discovery | implemented |
| Planner | `repository-analysis`, `implementation` | read-only planning | implemented |
| Web Researcher | future research/browser Skill | web research only | planned |
| Editor | `implementation`, `debugging`, `testing-validation` | bounded source writes | implemented |
| Executor | `testing-validation` + runtime/environment procedures | bounded execution | implemented |
| Terminal Monitor | `debugging` + runtime procedures | observe/escalate | implemented |
| Reviewer | `code-review`, `testing-validation` | read-only validation | implemented |
| Browser Agent | future browser-validation Skill | browser validation | planned |
| Debugger | `debugging`, `implementation`, `testing-validation` | bounded corrective changes | planned |
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

File Picker and Planner establish deterministic discovery-to-plan handoff. Editor adds bounded source writes, Executor adds bounded runtime verification, Terminal Monitor observes long-running or interactive execution, and Reviewer independently validates the candidate without modifying it.

## Missing Skills

Only create a new Skill when an existing Skill cannot express a recurring responsibility. Current candidates are:

1. research/browser procedures for Web Researcher
2. browser validation procedures for Browser Agent
3. a dedicated planning Skill only if Planner behavior becomes materially larger than repository-analysis + implementation guidance

Do not create Skills solely to mirror the agent count.
