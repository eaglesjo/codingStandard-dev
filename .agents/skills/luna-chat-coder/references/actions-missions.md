# Actions Missions

Use an Actions mission when the normal sandbox or connected GitHub path cannot safely or efficiently provide a capability, exact transport, or bounded execution step required by the repository task.

## Mission types

- **supply mission**: obtain or prepare an external input the sandbox cannot obtain directly;
- **transport mission**: carry an exact patch, bundle, archive, or deterministic payload when direct GitHub writes are inefficient, constrained, or unreliable;
- **degraded execution mission**: perform a bounded edit/build/test/verification step while the sandbox itself is unavailable or insufficient.

## Mission contract

Before dispatch, define:

- source identity: repository plus expected commit or PR-head SHA;
- purpose: the capability gap, transport need, or bounded execution step;
- inputs: exact files, patch/bundle, lockfiles, versions, parameters, or other required state;
- operations: explicit commands or workflow steps;
- outputs: artifact, logs, checksum, generated input, test result, commit, or other durable result;
- integrity: checksums and provenance when bytes cross the sandbox/runner boundary;
- permissions: minimum workflow and repository permissions required;
- terminal state: what makes the mission complete and what temporary state can eventually be removed.

If the expected source SHA no longer matches, stop and deliberately recover/rebase rather than applying an exact payload to the wrong source.

## Supply mission

Use a supply mission when the sandbox can perform the engineering work but cannot obtain a required external input. Acquire only what the task requires, derive versions from repository declarations, record provenance, checksum the returned payload, and verify platform compatibility before consuming it. Return to the sandbox for editing, building, testing, and debugging whenever possible.

## Exact source transport

Patch or bundle transport is a first-class option, not a punishment after every API mechanism fails. Consider it when many files change, repeated writes create partial-update risk, binary/rename/mode/history semantics matter, connector limits apply, or API errors persist after diagnosis.

For a binary-safe patch:

```bash
git diff --binary > change.patch
sha256sum change.patch
git apply --check change.patch
git apply change.patch
git diff --check
```

Bind the payload to the expected base SHA and run repository-defined verification after applying it. Use a Git bundle when preserving Git objects or history is more useful than a patch or source archive.

## Degraded remote mode

Enter degraded remote mode only when the sandbox work container itself is unavailable or cannot sustain the task because of a hard platform constraint. Continue through bounded missions, persist reusable progress as commits/branches/exact payloads/artifacts, inspect logs/results before each next step, and return to the sandbox when practical. Tell the user when this mode was used and report the actual remote checks performed.

## Diagnose failures before retrying

Inspect the run conclusion, failing jobs/steps, logs, artifacts, commits, refs, and partial results before changing source or re-running. Distinguish repository/test failure, workflow defect, permission/authentication failure, quota/platform limit, stale source identity, and transient service failure when possible. Without evidence of transience, do not repeatedly re-run an unchanged mission.

## Task ownership and cleanup

Use collision-resistant task-owned names for independent missions. Keep task branches, workflow definitions, transport/supply artifacts, and logs while they have debugging, review, handoff, or recovery value. Do not delete unfamiliar state. After a durable result supersedes temporary state and ownership is clear, clean up task-owned temporary objects. Cleanup should be idempotent and recovery-aware.

## Security

Keep credentials and unrelated runner state out of artifacts. Use minimum workflow permissions. Verify provenance of downloaded executables and native inputs. Keep large caches, SDKs, and toolchains out of source history unless the repository explicitly adopts them.
