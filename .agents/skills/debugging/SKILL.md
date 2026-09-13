---
name: debugging
description: Diagnose software failures systematically before changing code or retrying execution.
license: MIT
metadata:
  version: "0.1.0"
---

# Debugging

1. Capture the exact failure, command, revision, and environment when relevant.
2. Reproduce the failure if practical.
3. Separate symptom from root-cause hypotheses.
4. Inspect logs, stack traces, state, and recent changes.
5. Test the highest-value hypothesis with the smallest experiment.
6. Change the smallest owning component.
7. Re-run the failing check, then run focused regression coverage.
8. Record root cause, fix, and remaining uncertainty.

Never perform blind repeated retries.
