# Development Continuity Rules

This document is the durable handoff point for continuing development after a chat, session, context, or execution environment is interrupted.

## Purpose

When work resumes, read this document before making new changes. The goal is to preserve decisions, reduce repeated discussion, and prevent accidental reintroduction of retired architecture or unnecessary cleanup.

## Canonical development surfaces

- `codingStandard-dev` is the canonical development and validation surface.
- `AIEngineeringStandard` is the public release surface. Only validated release-ready state is promoted there.
- `codingStandard-private` is retired. Do not restore it as a source of truth, runtime prerequisite, or hidden dependency.

## AI Developer role

The default development persona is defined by `.agents/skills/ai-developer/SKILL.md`; specialist capabilities are selected per task.

Use the development system to:

- preserve task state and durable handoff information;
- prefer exact GitHub state when recovering from context or sandbox loss;
- keep task ownership and cleanup explicit;
- diagnose failures before retrying;
- make completion claims only from available evidence; and
- operate with bounded permissions and explicit provenance.

The intended feedback loop is:

```text
Use AI Developer for real development
        -> observe gaps or failure modes
        -> improve the smallest owning Skill/rule
        -> validate the improvement
        -> use the improved system in subsequent development
```

## AI Developer Profile v1

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

Continuity/fallback capabilities are provided by `.agents/skills/development-continuity/`.

These Skills are modular. Do not load every specialist Skill for every task; select the minimum relevant set.

## Naming rule

The development system is vendor- and model-neutral. Do not use a product, model, or personal project codename as the normative developer persona or Skill namespace.

Use role/capability names such as `ai-developer` and `development-continuity` instead.

Historical commits and external repositories may retain old names for traceability, but active repository behavior and documentation must use the neutral names.

## Durable development state

Development continuity is state recovery, not chat transcript recovery.

The canonical state surfaces are:

- `docs/development/state/CURRENT.md` — immediate active task, repository/branch references, blockers, evidence, and next action.
- `docs/development/state/TASKS.md` — active and queued tasks.
- `docs/development/state/HISTORY.md` — durable record of material state transitions.

A fresh session should load these files after the project instructions and continuity Skill, then reconcile them with actual Git/PR state. Git state is authoritative when a state file is stale.

Persist decisions, task status, repository revisions, PR references, validation evidence, blockers, and next actions. Do not persist conversational transcripts merely for continuity.

Before ending a development session, update the state when material progress occurred. A task is not complete until its validation evidence is recorded.

## Documentation rule

Any material project decision, architecture decision, workflow change, cleanup rule, or development operating rule that is likely to matter when work resumes must be recorded here or in the more specific normative document that owns the rule.

Do not rely on chat history as the sole source of truth.

When a rule changes:

1. update the owning document;
2. record the reason and affected scope when the change is non-obvious;
3. validate the affected behavior;
4. commit the documentation and implementation changes together when practical; and
5. use the resulting Git revision as the durable handoff reference.

## Version-boundary decision: AI model mapping

The multi-agent architecture in 2.0 remains vendor- and model-neutral. Individual agents MUST NOT be coupled to a specific AI provider or model in the 2.0 release scope.

Actual model/provider mapping, provider adapters, routing policies, and fallback selection are deferred to the next version. 2.0 may preserve abstraction points needed for future integration, but must not introduce provider-specific runtime coupling merely to anticipate that feature.

Rationale: keep the 2.0 release focused on the development system, agent contracts, validation, reproducibility, recovery, and quality foundations; add model selection/routing as a separate versioned capability after those foundations are validated.

## Branch hygiene rule

Temporary task branches are disposable working resources, not permanent project assets.

When a task requires a new branch:

1. create it from the appropriate base revision;
2. use it only for the bounded task;
3. merge or otherwise incorporate any work that is intentionally retained;
4. after the task is complete, determine whether the branch has any remaining development, recovery, or review value; and
5. delete the task branch when it is no longer needed.

After each completed task, proactively review branches created for that task. Do not leave temporary branches behind merely because they were once useful.

Before deleting a branch, determine:

1. whether its commits are already represented in the target `main` branch;
2. whether it contains unique work that may still be useful;
3. whether an open PR or follow-up task depends on it; and
4. whether deletion would make recovery or historical tracing harder.

Delete only branches with no remaining development or recovery value. Preserve long-lived branches only when their purpose is explicit and documented.

The default operating rule is therefore:

```text
Task branch created
      -> task completed
      -> retained work merged/recorded
      -> dependency/recovery check
      -> branch no longer needed
      -> delete branch
```

Do not delete `main` or any branch that is still required by an active PR, release process, recovery path, or explicitly retained work.

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

## Resume procedure

When starting a new session:

1. Identify the repository and current revision.
2. Read `AGENTS.md`.
3. Read this document.
4. Read `.agents/skills/development-continuity/SKILL.md` when the task involves substantial chat/sandbox development.
5. Read `.agents/skills/ai-developer/SKILL.md` for ordinary software development.
6. Read `docs/development/state/CURRENT.md` and `TASKS.md` when present.
7. Inspect the current Git revision, working tree, branch, and relevant PR state.
8. Reconcile any difference between durable notes and actual repository state.
9. Resume from the first incomplete bounded action.
10. Record new material decisions and validation evidence before ending the session.
11. Review task-created branches and delete those that are no longer needed.

The repository state is authoritative when it conflicts with stale notes; update the durable state after resolving the discrepancy.
