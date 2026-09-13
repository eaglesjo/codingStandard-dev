---
name: testing-validation
description: Validate software changes from focused checks to the repository's broader validation gate.
license: MIT
metadata:
  version: "0.1.0"
---

# Testing and Validation

1. Identify the behavior changed and its smallest meaningful check.
2. Run the focused check first.
3. Validate failure paths and relevant boundaries, not only the happy path.
4. Run the broader project gate when the change warrants it.
5. Capture runtime version and repository revision when required for conformance evidence.
6. Distinguish passed, failed, skipped, and blocked checks.
7. Do not convert a skipped or blocked check into a completion claim.
8. Preserve reproducible evidence without secrets or unnecessary environment data.
