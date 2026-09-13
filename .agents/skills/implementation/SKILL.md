---
name: implementation
description: Implement a planned change with minimal scope while preserving architecture and reproducibility.
license: MIT
metadata:
  version: "0.1.0"
---

# Implementation

1. Confirm the intended base state and change boundary.
2. Follow existing patterns before introducing new abstractions.
3. Keep domain logic in modules; keep orchestration thin.
4. Avoid unrelated cleanup and opportunistic refactors.
5. Preserve configuration, provenance, permissions, and deterministic paths.
6. Add or update focused tests with behavior changes.
7. Run the smallest meaningful verification before broader validation.
8. Report exactly what changed and what remains unverified.
