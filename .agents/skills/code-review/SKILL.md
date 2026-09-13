---
name: code-review
description: Review changes for correctness, architecture, security, tests, maintainability, and release impact.
license: MIT
metadata:
  version: "0.1.0"
---

# Code Review

Review the diff, not just the final files.

Check in order:

1. Intended behavior and requirements.
2. Correctness and edge cases.
3. Architecture and dependency direction.
4. Security, secrets, permissions, and trust boundaries.
5. Error handling and failure behavior.
6. Test coverage and validation evidence.
7. Maintainability and unnecessary complexity.
8. Compatibility and release impact.

Prioritize actionable defects. Do not request cosmetic changes as blockers unless project rules require them.
