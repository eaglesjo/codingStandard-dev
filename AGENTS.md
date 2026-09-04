# AGENTS.md

# Project Agent Instructions

This file is the top-level entrypoint for AI coding agents.

## Instruction Order

1. Inspect the active machine-readable project, architecture, and policy profiles under `profiles/` before implementation changes.
2. Apply `COMMON/AGENT.md`, `COMMON/SKILL.md`, and `COMMON/ENVIRONMENT.md`.
3. Detect which domain resources are installed and relevant:
   - `LLM/` for language-model, NLP, RAG, fine-tuning, and text-model work.
   - `VISION/` for image, video, OCR, detection, segmentation, generation, and VLM work.
4. Apply the matching domain `AGENT.md`, `SKILL.md`, and `ENVIRONMENT.md`.
5. Apply task-specific Skills under the selected domain.
6. Read the project's existing README, dependency files, lock files, tests, and security constraints.

## Architecture Profile Contract

The machine-readable profiles under `profiles/` are the canonical architecture and policy contract for repository changes.

- Resolve `profiles/project.json` first to determine the active project, runtime, delivery, and scalability profile.
- Resolve the referenced architecture profile under `profiles/architecture/` and policy profile under `profiles/policies/` before changing implementation structure or repository-wide rules.
- Child or task-specific policies may add restrictions but must not weaken repository-level policy; conflicts resolve by `stricter-wins`.
- Keep implementation dependencies aligned with the declared architecture dependency direction and forbidden dependency list.
- When architecture or policy changes are proposed, update the machine-readable profile and its validation/tests together with the human-facing documentation.
- Validate the profiles with `python3 scripts/validation/validate_profiles.py` before considering architecture work complete.

## Environment Contract

- Inspect the real OS, Python/runtime, CPU, GPU/accelerator, VRAM, RAM, disk, and framework capabilities before resource-sensitive work.
- Use the installed environment profiler as the source of truth when available.
- Resolve a conservative runtime configuration, run a workload-appropriate Memory Smoke Test, then lock the validated configuration.
- Do not hard-code a named machine as a prerequisite.
- After environment validation, remove unused execution branches and obsolete code from application/notebook paths unless multi-platform support is intentional.

## Training Contract

- Long-running training uses validation, Early Stopping where meaningful, best Checkpoint, and Resume.
- Experiments define a baseline, controlled variants, seeds, metrics, and resource tracking.
- Record reproducibility metadata including coding-standard version, Git state, environment profile, configuration, model/dataset revisions, and resource usage.
- Use staged recovery for OOM or resource failures; do not repeat the same failing configuration indefinitely.

## Clean Execution Contract

```text
Discover
  ↓
Inspect active profiles
  ↓
Detect installed domains
  ↓
Measure environment
  ↓
Resolve runtime
  ↓
Smoke Test
  ↓
Lock
  ↓
Apply domain/task Skills
  ↓
Implement / Train / Infer
  ↓
Validate
  ↓
Record
```

The final project should keep only the rules and execution paths that are relevant to the installed domains and actual workload.
