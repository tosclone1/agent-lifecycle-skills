---
name: change-planner
description: Define the smallest safe implementation delta after continuity review.
metadata:
  pack: agent-lifecycle-skills
  version: 1.0.0
---

# Change Planner

Convert a requested outcome into the smallest safe implementation plan.

## Sequence
Current state → Desired delta → Affected surfaces → Reuse candidates → Minimal change set → Risks → Verification.

Classify the change as:
- REUSE
- MODIFY
- ADD
- REPLACE

REPLACE requires explicit justification showing why reuse/modify/add are insufficient.

List files/modules likely to change only after system reconstruction.
