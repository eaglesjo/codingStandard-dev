---
name: git-release
description: Manage development branches, commits, promotion boundaries, and release evidence safely.
license: MIT
metadata:
  version: "0.1.0"
---

# Git and Release

- Resolve mutable refs to exact SHAs before consequential operations.
- Keep task-owned work on an explicit branch or PR.
- Inspect existing changes before modifying or cleaning them.
- Use focused commits with clear intent.
- Never delete old branches without checking unique work, open dependencies, and recovery value.
- Promotion to `AIEngineeringStandard` is not release authorization.
- Preserve exact source SHA, validation evidence, and provenance across promotion.
- Never expose credentials, tokens, or secrets in commits, logs, or evidence.
