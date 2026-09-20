---
name: diagnosing-bugs
description: Diagnose hard bugs using a red-capable feedback loop before hypotheses.
metadata:
  pack: agent-lifecycle-skills
  version: 1.0.0
---

# Diagnosing Bugs

No red-capable feedback loop, no diagnosis.

## Phases
1. Build a fast, deterministic signal that catches the user's exact symptom.
2. Reproduce and minimize.
3. Generate 3–5 falsifiable, ranked hypotheses.
4. Instrument one prediction at a time.
5. Convert the minimized repro into a regression test at the correct seam.
6. Apply the smallest fix.
7. Re-run the original loop and remove temporary instrumentation.

Redact secrets from all logs and artifacts.

Do not recommend waiting, retrying, or redesigning as a substitute for evidence.
