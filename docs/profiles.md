# Project profiles

A project profile tells the resolver which skills to apply to *your*
repository. It is a small YAML file that you keep in your own project — never in
this shared pack.

## Where the resolver looks

The resolver searches for `.agent-skills/profile.yaml`, starting at the path you
pass to `resolve`/`activate` (or the current directory) and walking up its
parent directories. So a profile lives at:

```
<your-project>/.agent-skills/profile.yaml
```

## Required vs optional fields

Only three parts of a profile affect resolution; the rest are optional metadata
that the resolver ignores:

| Field                  | Required         | Affects resolution?         |
|------------------------|------------------|-----------------------------|
| `schema_version`       | yes (must be `1`)| no                          |
| `project.id`           | yes (string)     | no (project identifier)      |
| `project.name`         | yes (string)     | no (display name)            |
| `project.lifecycle`    | yes (enum)       | **yes** — selects the policy |
| `skills.include`       | yes (list)       | **yes** — adds skills        |
| `skills.exclude`       | yes (list)       | **yes** — removes skills     |
| `skill_pack.*`         | no               | no (metadata)                |
| `context.*`            | no               | no (metadata)                |

`skills.include` and `skills.exclude` must both be present, even if empty
(`[]`). Unknown top-level or nested fields are allowed but ignored.

## Choosing a lifecycle

Set `project.lifecycle` to the stage that best matches the repository. Each value
loads a matching policy (`policies/<lifecycle>.yaml`):

- `greenfield` — new work; exploration is allowed, nothing exists yet to preserve.
- `building` — active development; prefer reuse, regression checks required.
- `stabilizing` — nearing stable; runtime evidence required, architecture frozen.
- `production` — running in production; full safety posture, no speculative refactoring.
- `legacy` — inherited or opaque code; reconstruct and mine it before touching it.

The policy files are the source of truth; this is a summary for selection.

## How skills are selected

For a given profile, the resolver computes:

```
selected =
    global skills
  + lifecycle policy (required + preferred)
  + skills.include
  - skills.exclude
```

- The four global skills are always present unless excluded: `continuity-reviewer`,
  `change-planner`, `code-review`, and `handoff`.
- Exclusions are applied **after** the union, so `skills.exclude` can remove a
  global skill or a lifecycle skill.
- Every included skill must exist in the pack. If `skills.include` names a skill
  that does not exist, `resolve`/`activate` fails with `Unknown skills: [...]`.
  Excluding a name that is not otherwise selected is a no-op.

## Create a profile safely

Start from the template:

```bash
cp profiles/templates/profile.yaml .agent-skills/profile.yaml
```

Then edit it:

1. Set `project.lifecycle` to the best-fitting stage.
2. List skills you always want in `skills.include` (they must exist in the pack).
3. List skills that do not apply in `skills.exclude`.
4. Keep `project.id` and `project.name` as identifiers for your project.

Validate and inspect before activating:

```bash
python scripts/agent_skills.py validate
python scripts/agent_skills.py resolve .
```

Review the resolved skill set, then install it only if it looks right:

```bash
python scripts/agent_skills.py activate .
```

## Example (synthetic)

A `stabilizing` project that always wants `diagnosing-bugs` and never wants the
global `handoff` skill:

```yaml
schema_version: 1
project:
  id: example-svc
  name: Example Service
  lifecycle: stabilizing
skills:
  include:
    - diagnosing-bugs
  exclude:
    - handoff
```

`resolve` selects the stabilizing policy skills plus `diagnosing-bugs`, minus
`handoff`. (All examples here are synthetic; replace `id`/`name` with your own.)
