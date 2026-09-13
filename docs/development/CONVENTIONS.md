# codingStandard 2.0 Coding Conventions

This document is the common development-conventions template installed by the cross-platform installer.

## Instruction and execution model

Follow the repository root `AGENTS.md` and the applicable domain/platform instruction files. Treat `core/`, `domains/`, and `platform/` contracts as the source of execution guidance; do not introduce legacy `COMMON/`, `LLM/`, or `VISION/` execution paths.

Before coding, inspect the actual runtime environment and workload. Resolve resource settings from measured CPU, RAM, GPU/accelerator, VRAM, Python/runtime, and workload requirements. Run the applicable Memory Smoke Test before long-running training or inference workloads.

## Reproducibility and validation

Use validation metrics, Early Stopping where applicable, best-checkpoint handling, resume support, controlled ablation studies, and reproducibility/resource metadata for experiments. Keep validation deterministic where the contract requires it and record runtime evidence separately from static evidence.

## Dependency and platform discipline

Use the repository dependency-compatibility policy and resolver tests when changing dependency contracts. Keep installer behavior cross-platform and preserve the managed-file lifecycle: install, state, update, and uninstall must remain consistent with the installation manifest.

## Release discipline

Development changes are validated in `codingStandard-dev`. Only validated content is eligible for promotion to `AIEngineeringStandard`; a passing development CI run does not itself authorize public promotion or a release.
