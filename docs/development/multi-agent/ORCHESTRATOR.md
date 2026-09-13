# AI Developer Orchestrator Control Model

## Purpose

The Orchestrator is the control plane for bounded multi-agent development. It does not replace the Agent Contract; it enforces the contract and converts specialist results into global task-state decisions.

## Dispatch gate

An invocation may start only when all of these are true:

1. The `contract_version`, `task_id`, and `invocation_id` are valid.
2. The role is one of the canonical roles.
3. The workspace/ref is explicit when repository work is involved.
4. `allowed_scope` is explicit.
5. Effective permissions are within the role ceiling and task authorization.
6. Write or execute authority has explicit scope.
7. Required evidence and stop conditions are declared.
8. The invocation attempt is consistent with its parent/retry lineage.
9. Required predecessor evidence is available.

Invalid dispatch is rejected before the specialist starts.

## Acceptance gate

A specialist result is accepted only when:

- its result status is valid;
- required evidence is present;
- evidence is traceable to durable artifacts or direct observations;
- reported changes match the actual candidate diff where writes occurred;
- no capability outside the contract was used;
- the next action is compatible with the current state;
- retry requirements are satisfied when `attempt > 1`.

Acceptance of an invocation is not equivalent to completion of the global task.

## Permission ceiling

Role defaults are ceilings:

| Role | Read | Write | Execute | Web | Runtime observe |
| --- | --- | --- | --- | --- | --- |
| file_picker | yes | no | no | no | no |
| planner | yes | no | no | no | no |
| web_researcher | yes | no | no | yes | no |
| editor | yes | yes | no | no | no |
| executor | yes | no | yes | no | no |
| terminal_monitor | yes | no | no | no | yes |
| reviewer | yes | no | no | no | no |
| browser_agent | yes | no | no | yes | yes |
| debugger | yes | yes | no | no | no |
| orchestrator | yes | no | no | no | no |

A task may reduce a ceiling for an invocation. It may not silently expand a role's ceiling.

## Global state authority

Only the Orchestrator advances global lifecycle state:

```text
READY -> ANALYZING -> PLANNING -> EDITING -> EXECUTING
                                      |             |
                                      v             v
                                REQUEST_CHANGES <- FAILED
                                      |
                                      v
                                  VALIDATING -> REVIEWING -> PASS
                                      |
                                      +-> BLOCKED
```

`REQUEST_CHANGES` returns to a bounded planning/correction step. `FAILED` and `BLOCKED` preserve evidence and stop the active chain until a new bounded action is identified.

## Parallelization

Parallel work is permitted only when:

- scopes do not overlap for writes;
- outputs do not depend on one another;
- each invocation has an independent stop condition;
- the candidate revision is frozen before parallel validation.

Typical safe parallel pairings are File Picker + Web Researcher and Reviewer + Browser Agent when their acceptance criteria are independent.

## Retry discipline

A retry requires a failure package containing evidence, classification, owning boundary, corrective action, and a new stop condition. `attempt` increments. Repeating the same invocation with unchanged inputs is not a valid retry.

## Security boundary

The Orchestrator is not an authorization bypass. Secrets, destructive commands, persistent host configuration, external side effects, publication, and release operations require their own explicit authorization boundaries.
