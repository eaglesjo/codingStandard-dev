# Agent Contract

## 1. Purpose

This document defines the normative handoff contract for the nine specialist agents and the AI Developer orchestrator.

The contract separates task intent, permissions, evidence, and agent results so agents can be replaced, retried, parallelized, or resumed without relying on conversation history.

## 2. Contract Rules

1. Every invocation has a unique `invocation_id` and a stable `task_id`.
2. Every invocation declares one agent role and its allowed capabilities.
3. Agents MUST stay inside `allowed_scope` and MUST NOT infer broader authority.
4. Outputs MUST identify evidence and uncertainty separately.
5. A successful agent result does not imply task completion.
6. Only the orchestrator may advance global task state.
7. Retries MUST increment `attempt` and identify the corrective reason.
8. Artifacts SHOULD be referenced by durable identifiers rather than copied into every handoff.

## 3. Canonical Envelope

The following JSON shape is the canonical logical representation. It is implementation-neutral; a runtime may serialize it as JSON, YAML, or another validated transport format.

```json
{
  "contract_version": "1.0",
  "invocation_id": "INV-0001",
  "task_id": "MA-001",
  "parent_invocation_id": null,
  "agent": { "role": "planner", "version": "1.0" },
  "stage": "analysis_planning",
  "state": "PLANNING",
  "attempt": 1,
  "objective": "Define the implementation plan for the requested change.",
  "workspace": {
    "repository": "eaglesjo/codingStandard-dev",
    "ref": "feat/multi-agent-ai-developer-v2"
  },
  "allowed_scope": {
    "paths": ["docs/development/"],
    "operations": ["read"]
  },
  "permissions": {
    "read": true,
    "write": false,
    "execute": false,
    "web": false,
    "runtime_observe": false
  },
  "context": {
    "durable_state_refs": [],
    "evidence_refs": [],
    "input_artifact_refs": []
  },
  "constraints": [],
  "required_evidence": ["plan", "affected_files", "verification_strategy"],
  "stop_conditions": ["scope ambiguity", "missing required evidence"],
  "result": {
    "status": "PASS",
    "findings": [],
    "changes": [],
    "evidence": [],
    "risks": [],
    "blockers": [],
    "artifacts": [],
    "next_action": "editor"
  }
}
```

## 4. Field Semantics

| Field | Required | Meaning |
| --- | --- | --- |
| `contract_version` | yes | Contract version, independent of agent version |
| `invocation_id` | yes | Unique identifier for one agent invocation |
| `task_id` | yes | Durable task identity shared across the workflow |
| `parent_invocation_id` | no | Immediate predecessor handoff, if any |
| `agent.role` | yes | One defined agent role |
| `agent.version` | yes | Version of the role implementation/contract |
| `stage` | yes | `analysis_planning`, `coding_execution`, or `validation_visualization` |
| `state` | yes | Orchestrator-controlled lifecycle state |
| `attempt` | yes | 1-based invocation attempt count |
| `objective` | yes | Bounded objective for this invocation |
| `workspace` | yes | Repository/workspace and exact ref when relevant |
| `allowed_scope` | yes | Explicit paths/resources and permitted operations |
| `permissions` | yes | Effective capabilities for this invocation |
| `context` | yes | References to durable state, evidence, and artifacts |
| `constraints` | yes | Task-specific restrictions |
| `required_evidence` | yes | Evidence required before invocation acceptance |
| `stop_conditions` | yes | Conditions that require stopping/escalation |
| `result` | yes | Agent outcome envelope |

## 5. Canonical Agent Roles

```text
file_picker
planner
web_researcher
editor
executor
terminal_monitor
reviewer
browser_agent
debugger
orchestrator
```

Display names may be localized. Role identifiers MUST remain stable and vendor-neutral.

## 6. Result Status

Agent result status is intentionally narrower than the global lifecycle:

```text
PASS
PASS_WITH_CONCERNS
REQUEST_CHANGES
BLOCKED
FAILED
```

- `PASS`: bounded work completed and required evidence is present.
- `PASS_WITH_CONCERNS`: usable result with explicitly documented concerns.
- `REQUEST_CHANGES`: another bounded corrective action is required.
- `BLOCKED`: progress requires an external decision, resource, or authorization.
- `FAILED`: the invocation could not complete because of an execution or agent failure.

The orchestrator converts agent results into global state transitions. Agents MUST NOT directly mutate global task state.

## 7. Evidence Format

Each evidence item SHOULD contain:

```json
{
  "id": "E-0001",
  "type": "test_result",
  "source": "executor",
  "reference": "artifact-or-log-id",
  "claim": "Targeted test suite passed.",
  "strength": "direct",
  "timestamp": "2026-09-13T00:00:00Z"
}
```

Recommended evidence types:

- `repository_inspection`
- `plan`
- `research_source`
- `diff`
- `test_result`
- `build_result`
- `runtime_result`
- `terminal_observation`
- `review`
- `browser_result`
- `artifact`
- `ci_result`

Evidence strength:

- `direct` — directly observed from an authoritative source
- `derived` — computed from direct observations
- `reported` — supplied by another agent but not independently verified

Completion claims SHOULD rely on `direct` evidence wherever practical.

## 8. Changes Format

Write-capable agents SHOULD report changes as bounded records:

```json
{
  "path": "src/example.py",
  "operation": "modify",
  "summary": "Fix null handling in the parser.",
  "scope": "parser input validation",
  "verification_required": true
}
```

The orchestrator SHOULD reconcile these records with the actual Git diff before accepting the invocation.

## 9. Failure and Retry Contract

A retry is valid only when all of the following are known:

```text
failure evidence
failure classification
owning boundary
corrective action
new stop condition
```

Example:

```text
Executor failed
  -> capture exit code/log
  -> classify missing dependency
  -> authorize dependency installation
  -> retry Executor with attempt=2
```

A retry MUST NOT simply repeat the previous invocation with the same inputs when no cause has changed.

## 10. Handoff Efficiency

To minimize latency and context consumption:

- pass references to large logs/artifacts rather than full contents
- pass only the diff and relevant files to Reviewer
- pass only the minimal reproducible failure package to Debugger
- allow read-only research and repository discovery to run concurrently
- freeze the candidate revision before parallel validation
- keep write operations single-owner per overlapping scope
- terminate monitoring when success/failure stop conditions are met

## 11. Security and Authorization

The contract is not an authorization bypass. A runtime MUST enforce permissions independently of agent instructions.

In particular:

- secrets MUST NOT be included in ordinary context unless explicitly required and protected
- destructive commands require an explicit authorization boundary
- external side effects require declared scope and authorization
- release/publication operations remain outside ordinary Editor/Executor authority
- browser sessions MUST use task-scoped credentials or safe test identities when credentials are required

## 12. Validation Requirements

The contract implementation should eventually be validated by automated checks for:

- required fields
- valid role identifiers
- valid lifecycle/status values
- permission consistency
- scope presence for write/execute operations
- attempt numbering
- evidence references
- prohibition of undeclared capabilities
- deterministic serialization/parsing

The schema may evolve, but compatibility changes MUST be versioned through `contract_version` and recorded in development state.
