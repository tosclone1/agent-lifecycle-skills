# Security Policy

## Reporting a vulnerability

If you discover a security issue — including accidentally committed
credentials, tokens, or private information — please report it privately
via GitHub's private vulnerability reporting (Security > Advisories) rather
than opening a public issue.

Please do not disclose the issue publicly until it has been addressed.

## Scope notes

This repository is a local skill pack: markdown skill definitions, YAML
policies/profiles, and a small Python CLI that copies skill directories into
an agent's skill folder. It has no network service, telemetry, or hosted
component.

- The CLI (`scripts/agent_skills.py`) copies files only within the local
  machine and never transmits data.
- It deletes only skill directories it previously recorded in its own
  manifest; unrelated user-managed skills are left untouched.
- Never commit secrets, credentials, or internal operational details to
  this repository.
