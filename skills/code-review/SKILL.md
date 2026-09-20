---
name: code-review
description: Review changes against standards, specification, and continuity.
metadata:
  pack: agent-lifecycle-skills
  version: 1.0.0
---

# Code Review

Review the diff from a fixed point on three separate axes.

## 1. Standards
Does the change follow repository rules and avoid clear maintainability smells?

## 2. Spec
Does it implement the requested behavior without missing requirements or scope creep?

## 3. Continuity
Does it preserve validated behavior, prior decisions, compatibility boundaries, and production invariants?

Do not merge the axes into one score. Report evidence and severity per finding.
