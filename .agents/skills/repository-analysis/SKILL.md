---
name: repository-analysis
description: Inspect repository structure, instructions, runtime, dependencies, and validation paths before implementation.
license: MIT
metadata:
  version: "0.1.0"
---

# Repository Analysis

Use before substantial implementation.

1. Read project and task instructions.
2. Identify the relevant modules, entrypoints, configuration, tests, and scripts.
3. Detect runtime and dependency versions from repository declarations.
4. Trace the current behavior and its callers before editing.
5. Identify security, compatibility, and platform constraints.
6. State the smallest meaningful change surface.
7. Record important uncertainty instead of silently assuming.

Do not infer runtime conformance from file presence alone.
