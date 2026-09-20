# Contributing

Thanks for your interest in contributing.

## Ground rules

- **No private information.** Never commit internal project names, customer
  names, private repository names, real hostnames, domains, absolute local
  paths, credentials, or operational details. Skills in this pack are
  generic; project-specific facts belong in the consuming project's own
  profile, `AGENTS.md`, `CONTEXT.md`, and ADRs.
- **Keep skills generic.** A skill should describe a reusable engineering
  practice, not one organization's system.
- **Small, focused changes.** Open an issue before adding a new skill or
  changing the resolution model.

## Development setup

Requires Python 3.10+ and PyYAML:

```bash
pip install pyyaml
```

## Validation

Run before submitting a change:

```bash
python scripts/agent_skills.py validate
python tests/test_export.py
```

The test suite checks, among other things, that no forbidden internal
identifiers appear anywhere in the export. Additions to that list are
welcome.

## Skill format

Each skill lives in `skills/<name>/SKILL.md` with YAML frontmatter:

```markdown
---
name: <name>
description: <one sentence>
metadata:
  pack: agent-lifecycle-skills
  version: 0.1.0
---
```

The frontmatter `name` must match the directory name, and `description` is
required. Keep the body concise and practice-oriented.

## License

This project is licensed under the Apache License 2.0 (see `LICENSE`). By
contributing, you agree that your contributions are licensed under the
Apache License 2.0.
