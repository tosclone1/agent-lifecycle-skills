---
name: regression-guard
description: Identify and lock down behavior that must remain true across a change.
metadata:
  pack: agent-lifecycle-skills
  version: 1.0.0
---

# Regression Guard

Before implementation, enumerate:
- must remain true
- must not change
- known-good behaviors
- compatibility boundaries
- operational invariants
- fallback behavior

Prefer executable regression checks where possible.

After implementation, verify every listed invariant explicitly. A passing new-feature test does not prove absence of regression.
