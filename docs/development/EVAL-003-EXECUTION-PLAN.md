# EVAL-003 — AI Developer Evaluation Suite Execution Plan

## Target

`eaglesjo/codingStandard-dev` on `main`.

EVAL-003 is the next bounded task after REAL-002. It evaluates the AI Developer development behavior itself; it does not select a provider or model.

## Purpose

Build a deterministic, vendor-neutral evaluation suite that measures whether AI Developer follows the repository's engineering lifecycle and produces evidence-backed development outcomes.

The evaluation must test behavior, not prose quality and not model brand/model identity.

## Evaluation dimensions

1. **Repository recovery**
   - identifies the correct repository/revision;
   - reads the required project instructions and durable state;
   - reconciles stale notes with Git state.

2. **Scope control**
   - identifies the requested target correctly;
   - avoids unrelated repository changes;
   - avoids unnecessary cleanup or speculative refactors.

3. **Planning quality**
   - identifies the smallest owning files;
   - defines acceptance criteria before implementation;
   - defines focused and broader validation.

4. **Implementation discipline**
   - makes the smallest correct change;
   - preserves existing architecture/contracts;
   - respects write ownership and permissions.

5. **Validation and evidence**
   - runs the relevant validation;
   - distinguishes execution from success;
   - records exact revision and validation evidence;
   - never claims PASS without objective evidence.

6. **Failure diagnosis and bounded retry**
   - diagnoses a failure before retrying;
   - repairs the smallest responsible boundary;
   - does not restart unrelated work.

7. **Unnecessary-change detection**
   - detects and rejects changes outside task scope;
   - preserves unrelated user/project content.

8. **Development continuity**
   - records material decisions in durable state;
   - leaves a clear next bounded action;
   - supports fresh-session recovery without chat history.

## Initial representative cases

The first suite should contain at least these deterministic cases:

- `EVAL-003-RECOVERY-001` — recover a task from repository state after simulated context loss.
- `EVAL-003-SCOPE-001` — perform a bounded documentation fix while rejecting unrelated repository cleanup.
- `EVAL-003-PLAN-001` — identify owning files and acceptance criteria before implementation.
- `EVAL-003-VALIDATION-001` — distinguish a successful command from a passing validation result.
- `EVAL-003-FAILURE-001` — diagnose a bounded validation failure and repair only the responsible boundary.
- `EVAL-003-RETRY-001` — perform one justified bounded retry instead of restarting the full lifecycle.
- `EVAL-003-EVIDENCE-001` — produce exact revision, run/job, and acceptance evidence.
- `EVAL-003-CONTINUITY-001` — leave durable state sufficient for a fresh session to resume.

## Evidence model

Use the existing deterministic `ai-evaluation` contract:

- `schema_version = 2.0.0`;
- deterministic method only;
- every criterion has PASS/FAIL plus evidence;
- case score is derived from criterion results;
- overall acceptance is threshold-based.

Do not introduce provider-specific judge APIs into the normative contract.

## Acceptance boundary

EVAL-003 is complete only when:

- representative cases are defined;
- each case has objective pass/fail criteria;
- fixtures are deterministic and reproducible;
- evaluator output conforms to `core/validation/ai-evaluation.schema.json`;
- validator coverage rejects score/evidence inconsistencies;
- unnecessary-change and bounded-retry behavior are explicitly measured;
- validation/evidence completeness is measured;
- focused tests pass;
- broader architecture/repository validation passes;
- exact candidate SHA and evidence are recorded in durable state;
- a fresh session can resume the next bounded action from repository state alone.

## Non-goals

- No provider/model selection.
- No model routing.
- No vendor-specific runtime dependency.
- No requirement to execute all nine specialist agents.
- No changes to PetLM or unrelated repositories.
- No public `v2.0.0` rewrite.

## Failure/recovery rule

If a case or validator fails, preserve the failure evidence, identify the smallest owning contract/fixture/validator boundary, repair only that boundary, rerun focused validation, then rerun the broader gate.
