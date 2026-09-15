# Development History

This file records material development state transitions that are useful when a future session resumes work.

## 2026-09-15

- Completed `REAL-002` — validate the complete AI Engineering Standard 2.0 lifecycle on the real project `eaglesjo/codingStandard-dev` using self-hosting validation.
- Resolved the acceptance-boundary ambiguity that had previously allowed an unrelated repository to be selected as the real-project target.
- Frozen target boundary: `eaglesjo/codingStandard-dev`; PetLM and every other unrelated repository are excluded from REAL-002.
- Defined the bounded execution contract in `docs/development/REAL-002.md` and `docs/development/REAL-002-EXECUTION-PLAN.md`.
- Validated candidate `8bf6df7c9322fabd08e39c1bd36a6d18f74d83a8` with focused repository-state/contract checks and the broader validation gates below.
- Architecture validation run `34972844488` passed with job `104393094798`, including profile validation, multi-agent contract/fixtures/E2E, AI code quality, AI evaluation, reproducibility, and cross-area 2.0 acceptance checks.
- codingStandard validation run `34972844585` passed with job `104393095466`, including repository validation, environment contract, installer tests, LLM CPU smoke, and Vision CPU smoke.
- Windows installer validation run `34972844593` passed with jobs `104393095165` and `104393095696`.
- Fresh-session recovery was validated from repository state only: repository identity/current revision, project instructions, AI Developer Skill, Development Continuity Skill, `CURRENT.md`, `TASKS.md`, REAL-002 acceptance contract, execution plan, exact candidate SHA, and validation evidence were sufficient without chat history.
- Advanced durable state to `EVAL-003` after REAL-002 acceptance.

- Completed `UPGRADE-001` — validate `v1.7.0` → `v2.x` no-delete upgrade compatibility for the defined representative compatibility boundary.
- Added and validated ownership reconciliation with conservative classes: `known-v2-managed`, `legacy-managed-candidate`, `project-owned`, and `unknown-legacy`.
- Enforced `deletion_policy: never-delete-unknown` for direct upgrade reconciliation.
- Added executable regression coverage proving direct upgrade without uninstall, preservation of project-owned content, managed-block replacement under explicit `merge`, preservation of unmanaged legacy artifacts, preservation of obsolete legacy managed-looking artifacts outside the desired v2 surface, unique v2 manifest ownership, owned-file existence, and post-upgrade `state` of `installed: true`, `modified: 0`, `missing: 0`.
- Fresh architecture validation run `34964212287` passed with job `104364722988`.
- Fresh codingStandard validation run `34964212295` passed with job `104364723251`, including repository validation, environment contract, installer lifecycle tests, LLM CPU smoke test, and Vision CPU smoke test.
- The accepted boundary is explicitly representative rather than byte-for-byte compatibility with every historical v1.7 installation; historical ownership is never guessed where evidence is absent.
- Froze the acceptance evidence in `docs/development/upgrade/UPGRADE-001.md` and advanced the durable state to `REAL-002`.

- Reconciled durable development state with the actual released repository state.
- Completed `2.0-FINAL` in the durable task queue because the validated source `6fed7b85f162611e6f5aa16dc857905b597b56ea` was promoted to `eaglesjo/AIEngineeringStandard` and released as `v2.0.0`.
- Started `UPGRADE-001` — validate `v1.7.0` → `v2.0.0` no-delete upgrade compatibility.
- Verified that the public distribution contains a real `v1.7.0` release and inspected its legacy installer surface before designing the upgrade fixture.
- The v1.7.0 Bash installer supports `en|ko`, domains `common|ml|llm|vision|colab|all`, conflict policies `ask|merge|overwrite|skip`, and managed-block merging, but does not expose the v2 installation-state/ownership reconciliation contract seen in the v2 public installer documentation.

## 2026-09-14

- PR #18 candidate `23efd3a60bd51a8e00d354291ddfaffc36d75a90` passed the architecture workflow run `34790623343`.
- Architecture job `103814028876` executed and passed multi-agent contract validation, multi-agent fixture validation, and contract-driven multi-agent E2E simulation.
- Fresh-session recovery was validated from durable repository state: exact PR head, `CURRENT.md`, `TASKS.md`, `HISTORY.md`, Development Continuity Skill, recovery procedure, PR metadata, and CI evidence were sufficient to reconstruct MA-001 without chat history.
- Updated durable state to leave PR #18 as the only remaining MA-001 merge gate.

## 2026-09-13

- PR #16 established the vendor-neutral `ai-developer` and `development-continuity` namespaces and was merged into `main`.
- Started `DSR-001` — Development State Recovery v1.
- Added `CURRENT.md`, `TASKS.md`, and `HISTORY.md` as durable state surfaces.
- The intended recovery model is repository-state recovery, not chat-history recovery.
- Session recovery must reconcile durable notes with actual Git/PR state before acting.
- PR #17 merged Development State Recovery v1 into `main` as `5ee47990419419a351afd3a92a5c538320660319`.
- PR #17 head `c36c6ef0694f2738868db6f97787439234017801` passed Windows installer validation, architecture profile validation, and codingStandard validation.
- Completed `DSR-001`.
- Started `MA-001` — Multi-Agent AI Developer 2.0 Architecture.
- Established AI Developer as orchestrator with File Picker, Planner, Editor, Validator, Reviewer, and Research & Browser specialist boundaries.
- Added `docs/development/MULTI-AGENT-AI-DEVELOPER-2.0.md` defining the initial contract, permissions, lifecycle, orchestration, evidence, recovery, and implementation order.

Completed tasks remain in history even after their active queue entry is closed.
