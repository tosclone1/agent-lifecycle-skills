---
name: continuity-reviewer
description: Preserve project history before proposing or making changes.
metadata:
  pack: agent-lifecycle-skills
  version: 1.0.0
---

# Continuity Reviewer

Use this before modifying any existing or in-progress system.

## Workflow
1. Reconstruct the current state.
2. Inventory existing assets and interfaces.
3. Identify prior decisions and their reasons.
4. Identify validated behavior and known-good evidence.
5. Identify sunk implementation and operational cost.
6. State the exact current problem.
7. Evaluate **Reuse → Modify → Add → Replace**, in that order.
8. Choose the smallest safe change.

## Output
Always state: Current state, preserved invariants, affected surfaces, reuse candidates, chosen change class, and risks.

## Guardrails
- Do not redesign merely because a cleaner design exists.
- Do not replace validated infrastructure without explicit evidence that modification is insufficient.
- Distinguish observed facts from assumptions.
