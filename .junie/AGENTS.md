# Junie Agent Rules

Follow the project coding standard in `AGENTS.md` and the applicable domain `AGENT.md`, `SKILL.md`, and `ENVIRONMENT.md` files.

Before implementation, inspect and measure the actual execution environment and resolve runtime settings from measured CPU, RAM, disk, accelerator, VRAM, Python/runtime, and workload capabilities.

For ML/LLM work, apply the domain lifecycle, validation metrics, Early Stopping where meaningful, best-checkpoint and resume behavior, controlled ablations, reproducibility, and resource tracking.

Do not infer capabilities from the IDE or agent client. Keep credentials and sensitive artifacts out of source control.
