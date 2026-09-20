# agent-lifecycle-skills

Lifecycle-aware engineering skills for coding agents working on real software repositories.

## What

A small, local skill pack for coding agents (e.g. Codex-style agents and
other agents that read markdown skill definitions from a skills directory).
Each skill is a concise `SKILL.md` describing a disciplined engineering
practice. A small Python CLI resolves which skills apply to a given project
and installs them into the agent's skills directory.

## Why

Most coding-agent examples focus on greenfield generation. Real repositories
are different: they contain prior decisions, validated behavior, production
constraints, regressions that already happened once, and sunk implementation
cost. An agent that ignores that history tends to rewrite what already works.

This pack encodes a different default posture:

- **Reconstruct before changing.** Build an evidence-based model of the
  existing system before proposing modifications.
- **Preserve validated decisions and sunk cost.** Prior decisions were made
  for reasons; understand them before superseding them.
- **Evaluate regression risk.** Enumerate what must remain true, then verify
  it after the change.
- **Change production systems safely.** Explicit blast radius, rollout, and
  rollback; code/test success alone is not production success.

The optimization order for any change is:

```
REUSE -> MODIFY -> ADD -> REPLACE
```

REPLACE requires explicit justification showing why reuse, modification, or
addition is insufficient. Do not redesign the system unless necessary.

## How

Active skills for a project are resolved as:

```
Global practices
+ Lifecycle policy
+ Project profile
+ Task-specific skills
- Exclusions
```

### Lifecycle model

Every project declares one lifecycle stage, which loads a matching policy:

| Stage | Posture |
|---|---|
| `greenfield` | Exploration allowed; no existing behavior to preserve |
| `building` | Prefer reuse; regression checks required |
| `stabilizing` | Runtime evidence required; architecture frozen |
| `production` | Full safety posture; no speculative refactoring |
| `legacy` | Reconstruct and mine the system before touching it |

### Included skills

- **continuity-reviewer** -- reconstruct history and constraints before changing anything
- **reconstruct-system** -- reverse-engineer an existing system from code, config, tests, and runtime evidence
- **change-planner** -- define the smallest safe implementation delta (REUSE/MODIFY/ADD/REPLACE)
- **code-review** -- review diffs on three axes: standards, spec, continuity
- **diagnosing-bugs** -- evidence-first diagnosis with falsifiable hypotheses
- **regression-guard** -- enumerate and verify invariants that must remain true
- **deployment-safety** -- plan production changes with blast radius and rollback
- **production-validation** -- prove the change works in the real operational path
- **handoff** -- compact, evidence-based handoff between agents or sessions

Shared reference material (`shared/`) covers change classification,
continuity principles, evidence policy, production safety, and review
severity.

### Example profiles

Two synthetic example profiles are included under `profiles/`:

- `example-web-app.yaml` -- a project in the `building` stage
- `example-production-service.yaml` -- a project in the `production` stage

They exist only to demonstrate resolution and activation; copy
`profiles/templates/profile.yaml` as the starting point for a real project.


## Quick Start (5-10 minutes)

Requires Python 3.10+ and PyYAML.

```bash
pip install pyyaml

# 1. Check the pack itself (run from the repository root)
python scripts/agent_skills.py doctor
python scripts/agent_skills.py validate

# 2. Try resolution against an example profile in a scratch directory
mkdir /tmp/demo && cd /tmp/demo
mkdir .agent-skills
cp /path/to/agent-lifecycle-skills/profiles/example-production-service.yaml .agent-skills/profile.yaml

# 3. See which skills resolve
python /path/to/agent-lifecycle-skills/scripts/agent_skills.py resolve .

# 4. Install the resolved skills for your agent
python /path/to/agent-lifecycle-skills/scripts/agent_skills.py activate .
```

(On Windows, substitute an appropriate scratch path for `/tmp/demo`.)

`activate` copies the resolved skills as real directories under
`$CODEX_HOME/skills` (default `~/.codex/skills`). Only skills recorded in the
pack's own manifest are ever replaced on re-activation; unrelated
user-managed skills are left untouched. Real directories are used instead of
symlinks for reliable discovery across environments.

To configure your own project, copy `profiles/templates/profile.yaml` to
`.agent-skills/profile.yaml` in the project, set its lifecycle stage, and
re-run `activate`.

## Commands

```bash
python scripts/agent_skills.py doctor      # environment check
python scripts/agent_skills.py validate    # skill/policy integrity check
python scripts/agent_skills.py resolve .   # show resolved skills for a project
python scripts/agent_skills.py activate .  # install resolved skills
python scripts/agent_skills.py status      # alias for doctor
```

## Using the skills with a coding agent

The skills are plain markdown; any agent that can read skill definitions can
use them. Two generic patterns:

- **Installed discovery** (above): `activate` places skills where the agent
  discovers them automatically.
- **Manual prompting**: paste or reference a skill file (e.g.
  `skills/continuity-reviewer/SKILL.md`) at the start of a task.

For agents that follow the `CODEX_HOME` convention (for example,
Codex-style agents that read skills from `~/.codex/skills`), `activate`
installs to that location and the skills are picked up on the next session.
Set `CODEX_HOME` only if your installation uses a non-default location.
Other agents can point at the same directory or use manual prompting.

For project-specific invariants, keep them in the project itself
(`AGENTS.md`, `CONTEXT.md`, `docs/adr/`), not in this shared pack. This
pack must never contain project secrets or operational facts.

## Limitations

- Designed for local filesystems with Python 3.10+; it has been exercised on
  Windows and POSIX-style paths, but unusual setups may need adjustment.
- Skill *discovery* depends on your agent's conventions; if your agent does
  not read `$CODEX_HOME/skills`, use the manual prompting pattern.
- No hosted service, registry, telemetry, or UI; this is a local tool by
  design.
- No performance, security, or compatibility guarantees are made. See
  `SECURITY.md` for reporting issues.

## Repository layout

```
skills/     SKILL.md definitions (the pack content)
policies/   lifecycle policies (greenfield..legacy)
profiles/   synthetic example profiles + template
schemas/    JSON schemas for profiles and policies
shared/     shared reference docs (change classes, evidence policy, ...)
scripts/    agent_skills.py -- resolve/validate/activate CLI
tests/      export validation tests
.github/    CI workflow
```

## Contributing

See `CONTRIBUTING.md`. Run `python scripts/agent_skills.py validate` and
`python tests/test_export.py` before submitting changes.

## License

Apache License 2.0. See `LICENSE`.

## Provenance

See `SOURCES.md`: this is original work conceptually informed by public
skill collections (MIT and Apache-2.0 sources, plus GPL-3.0 material used as
conceptual inspiration only with no copied implementation).

