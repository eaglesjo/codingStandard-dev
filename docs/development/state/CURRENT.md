# Current Development State

This file is the durable handoff point for the active development task.

## Recovery contract

A new AI Developer session MUST treat repository state as authoritative and use this file to identify the last completed work and the next bounded action.

## Project

- Repository: `eaglesjo/codingStandard-dev`
- Canonical development branch: `main`
- Public release surface: `eaglesjo/AIEngineeringStandard`
- Baseline: AI Engineering Standard 2.0 release-era development state
- Baseline commit: `28434d9d75c337438465934d12359a162aa54f69`

## Current status

- ID: `V2-REBASE-STATUS`
- Status: `RECORDED`
- Scope: analyze the AI Engineering Standard 2.0 contract and record repository state only.
- Implementation status: no post-2.0-release development work is active.
- Discarded scope: all development work added after the 2.0 release-era baseline has been discarded from `main`.

## AI Engineering Standard 2.0 analysis

The public `AIEngineeringStandard` repository defines v2.0.0 as the Public Release Candidate and currently records the public tag/release gate as `NOT AUTHORIZED YET`. Its v2.0 contract establishes the canonical repository architecture and policy profiles, project-level `AGENTS.md` routing, environment-aware runtime behavior, cross-platform installer lifecycle controls, multilingual runtime quality gates, executable agent-conformance outcomes, and dependency-compatibility alignment. The public repository also requires validation and exact-source provenance before promotion and treats release tagging as a separate authorization step.

For this development repository, the v2.0 release-era baseline is treated as the only valid starting point for future work. No post-baseline implementation is to be resumed automatically.

## Discarded post-baseline work

The following post-baseline development line was discarded by resetting `main` to `28434d9d75c337438465934d12359a162aa54f69`:

- EVAL-003 implementation and related fixtures, validators, runner, and tests.
- Subsequent MA-002 runtime-conformance implementation/changes made after the baseline.
- Rebaseline/task-state edits that were introduced only to support the discarded development line.

These changes are not part of the active development state and must not be resumed as-is.

## Next bounded action

None. This record is intentionally a status-only checkpoint. Do not implement, extend, or resume a new task until a new development instruction is given against the AI Engineering Standard 2.0 baseline.

## Rules

- Never use chat history as the sole source of truth.
- Do not mark a task complete without repository or CI evidence.
- Keep agent boundaries role-based and vendor-neutral.
- Do not add agents merely to increase agent count.
- Do not force all nine agents into every task; route only the agents required by acceptance criteria.
- Prefer parallel read-only work and single-owner overlapping writes.
- Freeze the candidate revision before independent parallel validation.
- On failure, preserve evidence and repair the smallest responsible boundary instead of restarting the full pipeline.
- Preserve exact source identity and validation evidence across the dev/release boundary.
- 2.0 must remain vendor/model-neutral; AI provider/model mapping belongs to the next version.
