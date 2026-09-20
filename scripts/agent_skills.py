#!/usr/bin/env python3
from pathlib import Path
import argparse, os, shutil, sys, yaml

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
POLICIES = ROOT / "policies"
GLOBAL_SKILLS = {"continuity-reviewer", "change-planner", "code-review", "handoff"}
MANIFEST_NAME = ".agent-lifecycle-skills-manifest"
PROFILE_DIR = ".agent-skills"


def all_skills():
    return {p.name for p in SKILLS.iterdir() if (p / "SKILL.md").exists()}


def find_profile(project=None):
    start = Path(project or os.getcwd()).resolve()
    for p in [start, *start.parents]:
        candidate = p / PROFILE_DIR / "profile.yaml"
        if candidate.exists():
            return candidate
    raise SystemExit(f"No {PROFILE_DIR}/profile.yaml found.")


def load_yaml(p):
    return yaml.safe_load(Path(p).read_text(encoding="utf-8"))


def resolve(profile_path):
    profile = load_yaml(profile_path)
    lc = profile["project"]["lifecycle"]
    policy = load_yaml(POLICIES / f"{lc}.yaml")
    selected = (
        GLOBAL_SKILLS
        | set(policy.get("required", []))
        | set(policy.get("preferred", []))
        | set(profile["skills"].get("include", []))
    )
    selected -= set(profile["skills"].get("exclude", []))
    unknown = selected - all_skills()
    if unknown:
        raise SystemExit(f"Unknown skills: {sorted(unknown)}")
    return profile, policy, sorted(selected)


def codex_home():
    return Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))


def target_dir():
    # Coding agents that follow the CODEX_HOME convention look for user skills
    # under $CODEX_HOME/skills.
    return codex_home() / "skills"


def _remove_managed_skill(path):
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.exists():
        shutil.rmtree(path)


def activate(profile_path):
    profile, policy, selected = resolve(profile_path)
    target = target_dir()
    target.mkdir(parents=True, exist_ok=True)
    manifest = target / MANIFEST_NAME
    old = set(manifest.read_text(encoding="utf-8").splitlines()) if manifest.exists() else set()

    # Only paths recorded in our manifest are managed/deleted. Other user skills are untouched.
    for name in old:
        _remove_managed_skill(target / name)

    # Use real directories rather than symlinks. This is more reliable across
    # agent skill-discovery behavior that may not follow symlink roots.
    for name in selected:
        src = (SKILLS / name).resolve()
        dst = target / name
        if dst.exists() and name not in old:
            raise SystemExit(
                f"Refusing to overwrite unmanaged skill: {dst}. "
                "Move/remove it or rename the pack skill first."
            )
        shutil.copytree(src, dst)

    manifest.write_text("\n".join(selected) + "\n", encoding="utf-8")
    print(
        f"Activated {len(selected)} skills for "
        f"{profile['project']['id']} ({profile['project']['lifecycle']})"
    )
    print("Target:", target)
    for s in selected:
        print(" -", s)


def doctor():
    problems = []
    if not SKILLS.exists():
        problems.append("skills directory missing")
    try:
        import yaml as _yaml  # noqa: F401
    except Exception:
        problems.append("PyYAML unavailable (install with: python -m pip install pyyaml)")

    print("Skill pack:", ROOT)
    print("Skill home:", codex_home())
    print("Skill target:", target_dir())
    print("Skills:", len(all_skills()))
    if problems:
        print("FAIL")
        for x in problems:
            print(" -", x)
        raise SystemExit(1)
    print("PASS")


def validate():
    bad = []
    seen_names = set()
    for p in SKILLS.iterdir():
        f = p / "SKILL.md"
        if not f.exists():
            continue
        txt = f.read_text(encoding="utf-8")
        if not txt.startswith("---\n"):
            bad.append(f"{p.name}: missing YAML frontmatter")
            continue
        front = txt.split("---", 2)[1]
        meta = yaml.safe_load(front) or {}
        name = meta.get("name")
        desc = meta.get("description")
        if name != p.name:
            bad.append(f"{p.name}: frontmatter name mismatch ({name!r})")
        if not desc:
            bad.append(f"{p.name}: missing description")
        if name in seen_names:
            bad.append(f"{p.name}: duplicate skill name")
        seen_names.add(name)
    count = len(all_skills())
    if count == 0:
        bad.append("no skills found")
    for policy_path in POLICIES.glob("*.yaml"):
        policy = load_yaml(policy_path)
        refs = set(policy.get("required", [])) | set(policy.get("preferred", []))
        unknown = refs - all_skills()
        if unknown:
            bad.append(f"{policy_path.name}: unknown skills {sorted(unknown)}")
    if bad:
        print("FAIL")
        for item in bad:
            print(" -", item)
        raise SystemExit(1)
    print(f"PASS: {count} skills valid")


def main():
    ap = argparse.ArgumentParser(prog="agent-skills")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for x in ["doctor", "validate", "status"]:
        sub.add_parser(x)
    a = sub.add_parser("resolve")
    a.add_argument("project", nargs="?")
    a = sub.add_parser("activate")
    a.add_argument("project", nargs="?")
    args = ap.parse_args()

    if args.cmd == "doctor":
        doctor()
    elif args.cmd == "validate":
        validate()
    elif args.cmd == "status":
        doctor()
    elif args.cmd == "resolve":
        pf = find_profile(args.project)
        pr, po, ss = resolve(pf)
        print(pr["project"]["id"], pr["project"]["lifecycle"])
        for x in ss:
            print(" -", x)
    elif args.cmd == "activate":
        activate(find_profile(args.project))


if __name__ == "__main__":
    main()
