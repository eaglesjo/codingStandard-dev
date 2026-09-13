---
name: luna-chat-coder
description: Keep repository development reliable from chat by using the sandbox work container first, recovering exact GitHub state, and using bounded Actions missions when normal sandbox or GitHub paths are insufficient.
license: MIT
compatibility: Requires access to durable repository state. The fully specified ChatGPT Web path requires both the GitHub Plugin and the ChatGPT Codex Connector GitHub App for the target repository. GitHub Actions access is required only when an Actions mission is needed. Other Agent Skills hosts may use the core policy only to the extent that equivalent capabilities actually exist.
metadata:
  version: "0.1.2"
---

# Luna Chat Coder

Luna Chat Coder is a repository-development continuity and fallback policy for ordinary chat. Discover it early, keep it quiet on the normal path, and activate fallback mechanisms only when the normal sandbox or connected GitHub path becomes insufficient.

## Repository boundary: private → dev → release

This three-repository boundary is a **core invariant** and must not be weakened, bypassed, or silently changed:

```text
codingStandard-private  →  codingStandard-dev  →  AIEngineeringStandard
        Luna 활성화              개발/검증                 Release
```

- **`codingStandard-private`** is the **Luna activation and internal policy source**. Luna-specific skills, operating rules, continuity mechanisms, experiments, and internal development guidance belong here. Work performed here must preserve the boundary and must not be treated as a public release by itself.
- **`codingStandard-dev`** is the **development and validation repository**. Actual implementation, integration, testing, CI validation, and release-candidate preparation are developed and verified here.
- **`AIEngineeringStandard`** is the **release repository**. Only changes that have passed the required development/validation gates are promoted here for public release. It is the canonical public distribution/release surface.

### Non-negotiable flow

1. Activate or refine Luna behavior in `codingStandard-private`.
2. Develop and validate implementation in `codingStandard-dev`.
3. Promote only validated release-ready state to `AIEngineeringStandard`.
4. Never collapse these roles for convenience.
5. Never treat a private/Luna change as a release merely because it is committed.
6. Never use the release repository as the place to discover or develop unvalidated behavior.
7. When work crosses a repository boundary, preserve exact source identity, validation evidence, and provenance.

If a task appears to require crossing or collapsing these boundaries, stop and explicitly resolve the intended promotion path before making consequential changes.

## Core invariants

1. **Discover early, activate late.** Load this policy before repository work, but do not use Actions merely because the skill is present.
2. **Materialize exact source before editing.** Resolve the intended commit or PR-head SHA and establish a complete working tree for that exact state inside the sandbox before source edits, builds, tests, or debugging. Verify the materialized state matches the expected SHA.
3. **Sandbox first.** Prefer the sandbox work container for inspection, editing, building, testing, linting, formatting, services, and iterative debugging.
4. **Inventory before acquiring.** Inspect capabilities already present before installing, downloading, or dispatching a mission.
5. **The repository defines the engineering method.** Infer runtimes, services, databases, browsers, compilers, test tools, and versions from repository declarations and task requirements. Do not introduce substitutes merely because they are easier to run.
6. **GitHub holds exact durable truth.** Prefer commits, PR heads, branches/refs resolved to SHAs, and immutable artifacts over conversation reconstruction.
7. **Durable handoff is task-owned.** Use a branch, PR, issue, commit, or task-owned artifact when losing state would make recovery expensive or ambiguous.
8. **Assume concurrent actors.** Resolve mutable names to current immutable identity before consequential writes or cleanup; preserve unfamiliar state.
9. **Choose the simplest reliable exact path.** File writes, Git object operations, and patch/bundle missions are transport choices based on exactness, payload shape, file count, and reliability.
10. **Diagnose before retrying.** Inspect returned errors, failing steps, logs, and partial results before changing source or repeating an operation.
11. **The user's host computer is outside the workflow.** Do not require direct host access merely to unblock ordinary repository development.
12. **Evidence bounds completion claims.** Report only operations and checks that actually ran against the relevant state.

## Work in the sandbox first

Treat the sandbox work container as a disposable development workstation. Recover or materialize the exact target commit/PR-head there before editing. Read project instructions and repository declarations, inventory available tools, and perform the normal edit/build/test/debug loop in the sandbox whenever possible.

Do not silently weaken verification because setup is inconvenient. If the repository requires a real integration, prefer that integration over an easier substitute.

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

Preserve unfamiliar remote or sandbox state until ownership is understood.

## Completion and reporting

Source edits alone are not completion when executable behavior is part of the task. Run the applicable application/services, setup or migrations, build, tests, integration checks, and end-to-end checks required by the repository and task.

At completion, report what exact state changed, what checks actually ran and their results, any check that could not run and its blocker, and whether degraded remote mode was used.

## Project-specific priority

This repository's own engineering rules remain authoritative for architecture, coding standards, runtime configuration, domain behavior, validation, and release requirements. Luna supplies continuity, exact source recovery, transport, and fallback execution; it does not replace those rules.
