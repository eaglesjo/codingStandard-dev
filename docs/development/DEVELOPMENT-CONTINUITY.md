# Development Continuity Rules

This document is the durable handoff point for continuing development after a chat, session, context, or execution environment is interrupted.

## Purpose

When work resumes, read this document before making new changes. The goal is to preserve decisions, reduce repeated discussion, and prevent accidental reintroduction of retired architecture or unnecessary cleanup.

## Canonical development surfaces

- `codingStandard-dev` is the canonical development, Luna activation, and validation surface.
- `AIEngineeringStandard` is the public release surface. Only validated release-ready state is promoted there.
- `luna-chat-coder` remains an independent standalone template/reference and is not a runtime prerequisite for this repository.
- `codingStandard-private` is retired. Do not restore it as a source of truth, runtime prerequisite, or hidden dependency.

## Luna role

Luna is both a continuity/fallback capability and a first-class development Skill. The developer persona is defined by `.agents/skills/luna-developer/SKILL.md`; specialist capabilities are selected per task.

Use Luna to:

- preserve task state and durable handoff information;
- prefer exact GitHub state when recovering from context or sandbox loss;
- keep task ownership and cleanup explicit;
- diagnose failures before retrying;
- make completion claims only from available evidence; and
- operate with bounded permissions and explicit provenance.

The intended feedback loop is:

```text
Use Luna for real development
        -> observe gaps or failure modes
        -> improve the smallest owning Skill/rule
        -> validate the improvement
        -> use the improved Luna in subsequent development
```

## Luna Developer Profile v1

Default persona:

> Senior AI Software Engineer + Architect.

Default behavior:

- understand the repository before changing it;
- respect existing architecture and project instructions;
- prefer the smallest correct change;
- distinguish facts, observations, assumptions, and decisions;
- investigate uncertainty instead of guessing;
- diagnose failures before retrying;
- treat validation evidence as part of implementation; and
- record material decisions for future recovery.

Core specialist Skills introduced with v1:

- `repository-analysis`
- `implementation`
- `debugging`
- `testing-validation`
- `code-review`
- `git-release`

These Skills are modular. Do not load every specialist Skill for every task; select the minimum relevant set.

## Documentation rule

Any material project decision, architecture decision, workflow change, cleanup rule, or Luna operating rule that is likely to matter when work resumes must be recorded here or in the more specific normative document that owns the rule.

Do not rely on chat history as the sole source of truth.

When a rule changes:

1. update the owning document;
2. record the reason and affected scope when the change is non-obvious;
3. validate the affected behavior;
4. commit the documentation and implementation changes together when practical; and
5. use the resulting Git revision as the durable handoff reference.

## Branch hygiene rule

Do not delete branches merely because they are old.

Before deleting a branch, determine:

1. whether its commits are already represented in the target `main` branch;
2. whether it contains unique work that may still be useful;
3. whether an open PR or follow-up task depends on it; and
4. whether deletion would make recovery or historical tracing harder.

Delete only branches with no remaining development or recovery value.

Current audit decisions:

- `AIEngineeringStandard/release/2.0.0-rc.1`: deletion candidate; it is fully behind `main` with no unique commits.
- `AIEngineeringStandard/promote/2.0-dependency-compatibility`: preserve; it contains unique dependency-compatibility work.
- `AIEngineeringStandard/audit/ai-engineering-standard-2.0-gap`: preserve; it contains unique conformance/audit work.
- `codingStandard-dev/chore/luna-runtime-cleanup`: merged cleanup branch; deletion candidate.
- `codingStandard-dev/fix/2.0-release-promotion-boundary`: merged cleanup branch with no unique commits; deletion candidate.

These are decisions as of the current development revision. Re-audit before deleting if the repository state has changed.

## Promotion boundary

The intended flow is:

```text
codingStandard-dev
  -> develop / validate
  -> promote exact validated source
  -> AIEngineeringStandard public main
  -> independent release authorization
  -> tag / GitHub Release when explicitly authorized
```

Promotion does not itself authorize a public release.

## Current known state

- `codingStandard-dev/main` currently contains the integrated Luna policy and the release-promotion boundary.
- The promotion workflow uses `actions/checkout@v5`.
- Public promotion intentionally excludes `.github/workflows/`, `.agents/`, `AGENTS.md`, and other development-only surfaces according to the workflow export rules.
- `codingStandard-private` references and `actions/checkout@v4` references were audited and found absent from the current repositories at the time of this document update.

## Resume procedure

When starting a new session:

1. Read `AGENTS.md`.
2. Read this document.
3. Read `.agents/skills/luna-chat-coder/SKILL.md` when the task involves substantial chat/sandbox development.
4. Read `.agents/skills/luna-developer/SKILL.md` for ordinary software development.
5. Inspect the current Git revision and working tree.
6. Check the relevant PR/branch state before continuing an interrupted task.
7. Reconcile any difference between this document and the actual repository state before acting.
8. Record new material decisions before ending the work session.

The repository state is authoritative when it conflicts with stale notes; update this document after resolving the discrepancy.
