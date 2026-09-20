---
name: deployment-safety
description: Plan and execute production changes with explicit blast radius, rollout, and rollback.
metadata:
  pack: agent-lifecycle-skills
  version: 1.0.0
---

# Deployment Safety

Before deployment record:
- exact artifact/commit
- affected services/data
- blast radius
- migration order
- preconditions
- rollback/fallback
- post-deploy checks

Prefer reversible, incremental rollout. Do not combine unrelated changes in a risky production deployment.
