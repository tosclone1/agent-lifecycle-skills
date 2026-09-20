---
name: production-validation
description: Prove that a change works in the real operational path, not only in code or tests.
metadata:
  pack: agent-lifecycle-skills
  version: 1.0.0
---

# Production Validation

Code PASS is not Production PASS.

Validate as applicable:
1. unit/static checks
2. integration checks
3. runtime path exercised
4. scheduler/event actually fired
5. external provider returned expected result
6. state persisted correctly
7. subsequent cycle remains healthy
8. fallback/rollback remains valid
9. observable evidence is captured

Never treat configuration presence as proof of execution.
