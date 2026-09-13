---
name: development-continuity
description: Keep repository development reliable from chat by using the sandbox first, recovering exact GitHub state, and using bounded Actions only when normal paths are insufficient.
license: MIT
compatibility: Requires access to durable repository state. The fully specified ChatGPT Web path requires GitHub and sandbox capabilities; Actions access is required only when an Actions mission is needed. Other Agent Skills hosts may use the policy only to the extent that equivalent capabilities exist.
metadata:
  version: "0.3.0"
---

# Development Continuity

Development Continuity is the repository-development continuity and fallback policy for ordinary chat. Discover it early, keep it quiet on the normal path, and activate fallback mechanisms only when the normal sandbox or connected GitHub path becomes insufficient.

## Repository role

`codingStandard-dev` is the canonical development and validation repository for the Coding Standard ecosystem.

```text
codingStandard-dev  →  AIEngineeringStandard
   development/validation   public release
```

- `codingStandard-dev` is the source of truth for active development behavior, engineering integration, implementation, testing, CI validation, and release-candidate preparation.
- `AIEngineeringStandard` is the public release repository. Only changes that have passed the required development and validation gates are promoted there.
- `codingStandard-private` is retired from the active development flow. Do not require it for activation, development, validation, or ordinary repository work.

### Non-negotiable flow

1. Develop and validate behavior in `codingStandard-dev`.
2. Promote only validated release-ready state to `AIEngineeringStandard`.
3. Never treat a development commit as a public release merely because it is committed.
4. Never use the release repository as the place to discover or develop unvalidated behavior.
5. When work crosses the dev/release boundary, preserve exact source identity, validation evidence, and provenance.

## Core invariants

1. **Discover early, activate late.** Load this policy before repository work, but do not use Actions merely because the Skill is present.
2. **Materialize exact source before editing.** Resolve the intended commit or PR-head SHA and establish a complete working tree for that exact state before source edits, builds, tests, or debugging. Verify the materialized state matches the expected SHA.
3. **Sandbox first.** Prefer the sandbox work container for inspection, editing, building, testing, linting, formatting, services, and iterative debugging.
4. **Inventory before acquiring.** Inspect capabilities already present before installing, downloading, or dispatching a mission.
5. **The repository defines the engineering method.** Infer runtimes, services, databases, browsers, compilers, test tools, and versions from repository declarations and task requirements.
6. **GitHub holds exact durable truth.** Prefer commits, PR heads, branches/refs resolved to SHAs, and immutable artifacts over conversation reconstruction.
7. **Durable handoff is task-owned.** Use a branch, PR, issue, commit, or task-owned artifact when losing state would make recovery expensive or ambiguous.
8. **Assume concurrent actors.** Resolve mutable names to current immutable identity before consequential writes or cleanup; preserve unfamiliar state.
9. **Choose the simplest reliable exact path.** File writes, Git object operations, and patch/bundle missions are transport choices based on exactness, payload shape, file count, and reliability.
10. **Diagnose before retrying.** Inspect returned errors, failing steps, logs, and partial results before changing source or repeating an operation.
11. **The user's host computer is outside the workflow.** Do not require direct host access merely to unblock ordinary repository development.
12. **Evidence bounds completion claims.** Report only operations and checks that actually ran against the relevant state.

## Work in the sandbox first

Treat the sandbox work container as a disposable development workstation. Recover or materialize the exact target commit/PR-head there before editing. Read project instructions and repository declarations, inventory available tools, and perform the normal edit/build/test/debug loop in the sandbox whenever possible.

## Actions missions

Use GitHub Actions only when the normal sandbox or connected GitHub path cannot safely or efficiently provide a required capability, exact transport, or bounded execution step.

Typical roles are:

- **supply mission:** obtain or prepare an external input the sandbox cannot obtain directly;
- **transport mission:** carry an exact patch, bundle, archive, or deterministic payload when direct writes are inefficient or constrained;
- **degraded execution mission:** perform a bounded edit/build/test/verification step while the sandbox itself is unavailable or insufficient.

Every mission should have an exact source identity, narrow purpose, explicit inputs/operations/outputs, integrity checks where bytes cross boundaries, minimum permissions, and a clear terminal state. Read `references/actions-missions.md` before dispatching a mission.

Do not use Actions merely because it exists. Diagnose failures before retrying. An unchanged retry is appropriate only when evidence supports a transient failure; repeated blind retries are prohibited.

## Publish exact changes

Choose the lowest-overhead path that remains exact and reliable:

- connected file operations for small textual changes;
- native Git blob/tree/commit/ref operations for substantial multi-file state;
- exact patch/bundle transport for large or complex diffs, binary/mode/rename semantics, connector limits, or persistent write instability.

Capture the expected base SHA before substantial publication. If the base moved, deliberately recover, rebase, merge, or recreate the payload. Never reconstruct a substantial verified change from prose when exact bytes are available.

## Recovery

After chat/sandbox reset or source-identity ambiguity, read `references/recovery.md`. Prefer recovery in this order:

```text
commit / PR head
    > immutable Git or Actions artifact
    > surviving sandbox working tree
    > conversation reconstruction
```

Preserve unfamiliar remote or sandbox changes until ownership is understood.

## Completion and reporting

Source edits alone are not completion when executable behavior is part of the task. Run the applicable application/services, setup or migrations, build, tests, integration checks, and end-to-end checks required by the repository and task.

At completion, report what exact state changed, what checks actually ran and their results, any check that could not run and its blocker, and whether degraded remote mode was used.

## Project-specific priority

The repository's own engineering rules remain authoritative for architecture, coding standards, runtime configuration, domain behavior, validation, and release requirements. Development Continuity supplies continuity, exact source recovery, transport, and fallback execution; it does not replace those rules.
