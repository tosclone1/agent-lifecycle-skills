# Publication checklist — agent-lifecycle-skills

This directory is a staging export. Follow these steps to publish it as a
new, standalone public repository.

Suggested GitHub repository description:

> Lifecycle-aware engineering skills for coding agents working on real software repositories.

## Checklist

1. Review `LICENSE` (Apache License 2.0).
2. Review `README.md` and `SOURCES.md` for accuracy.
3. Run validation from this directory:

   ```bash
   python scripts/agent_skills.py validate
   python scripts/agent_skills.py doctor
   python tests/test_export.py
   ```

   All commands must print PASS / ALL CHECKS PASSED.
4. Copy this directory's contents into a new empty working directory (or
   enter it directly). Do not copy any parent-repository `.git` directory.
5. Initialize a fresh Git repository:

   ```bash
   git init -b main
   git add -A
   ```

6. Make the initial commit:

   ```bash
   git commit -m "Initial public release"
   ```

7. Create a NEW public GitHub repository named `agent-lifecycle-skills`
   (empty — no README, license, or .gitignore template; those already exist
   here).
8. Connect the new remote:

   ```bash
   git remote add origin <new-repository-url>
   ```

9. Push main:

   ```bash
   git push -u origin main
   ```

10. Verify that the `validate` GitHub Actions workflow passes on the pushed
    commit.
11. Only after remote validation passes, create the first tag/release
    (suggested: `v0.1.0`, matching `VERSION`).
