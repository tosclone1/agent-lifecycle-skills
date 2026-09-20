---
name: reconstruct-system
description: Reverse-engineer an existing system from code, configuration, tests, runtime evidence, and operations.
metadata:
  pack: agent-lifecycle-skills
  version: 1.0.0
---

# Reconstruct System

Build an evidence-based model before proposing changes.

## Inspect
- entry points
- configuration and environment
- data/state flow
- schedulers and background jobs
- external dependencies
- persistence
- tests
- deployment/runtime
- monitoring/logging
- fallback and rollback paths

Trace one real end-to-end path. Record contradictions between docs, code, config, and runtime.

## Deliverable
Produce a compact system map with:
- components
- control flow
- state boundaries
- external boundaries
- operational invariants
- unknowns

Never infer unseen behavior when evidence can be inspected.
