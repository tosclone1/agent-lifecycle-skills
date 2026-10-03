#!/usr/bin/env python3
"""Minimal validation tests for the agent-lifecycle-skills public export.

Run from the export root:

    python tests/test_export.py
"""
import importlib.util
import os
import re
import sys
import tempfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
FAILURES = []

# Internal identifiers that must never appear in the public export.
FORBIDDEN_PATTERNS = [
    r"tosclone",
    r"kpopmap",
    r"kcer",
    r"storeticket",
    r"fifteenfifty",
    r"shorts[- ]news",
    r"\bkpm\b",
    r"ahims",
    r"github\.com/tosclone1",
    r"[A-Za-z]:\\Users\\",
    r"AKIA[0-9A-Z]{16}",
    r"ghp_[A-Za-z0-9]{20,}",
    r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
]

SCAN_EXTENSIONS = {".md", ".py", ".yaml", ".yml", ".json", ".txt", ".ps1", ".cmd"}


def check(label, ok, detail=""):
    if ok:
        print(f"PASS: {label}")
    else:
        print(f"FAIL: {label} {detail}")
        FAILURES.append(label)


def load_cli():
    spec = importlib.util.spec_from_file_location(
        "agent_skills", ROOT / "scripts" / "agent_skills.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_required_files():
    required = [
        "README.md",
        "CONTRIBUTING.md",
        "SECURITY.md",
        "SOURCES.md",
        "VERSION",
        "scripts/agent_skills.py",
        "policies/greenfield.yaml",
        "policies/building.yaml",
        "policies/stabilizing.yaml",
        "policies/production.yaml",
        "policies/legacy.yaml",
        "profiles/example-web-app.yaml",
        "profiles/example-production-service.yaml",
        "profiles/templates/profile.yaml",
        "schemas/profile.schema.json",
        "schemas/policy.schema.json",
        ".github/workflows/validate.yml",
    ]
    missing = [r for r in required if not (ROOT / r).exists()]
    check("required files exist", not missing, f"missing: {missing}")
    check("LICENSE file exists", (ROOT / "LICENSE").exists())
    check(
        "license review placeholder removed",
        not (ROOT / "LICENSE-REVIEW-REQUIRED.md").exists(),
    )


def test_profiles_parse():
    schema = yaml.safe_load(
        (ROOT / "schemas" / "profile.schema.json").read_text(encoding="utf-8")
    )
    lifecycles = set(
        schema["properties"]["project"]["properties"]["lifecycle"]["enum"]
    )
    for profile_path in sorted((ROOT / "profiles").glob("*.yaml")):
        try:
            profile = yaml.safe_load(profile_path.read_text(encoding="utf-8"))
            ok = (
                isinstance(profile, dict)
                and profile.get("schema_version") == 1
                and profile["project"]["lifecycle"] in lifecycles
                and isinstance(profile["skills"].get("include"), list)
                and isinstance(profile["skills"].get("exclude"), list)
            )
        except Exception as exc:  # noqa: BLE001
            ok = False
            print(f"  profile error: {profile_path.name}: {exc}")
        check(f"profile parses: {profile_path.name}", ok)


def test_policy_references():
    cli = load_cli()
    skills = cli.all_skills()
    for policy_path in sorted((ROOT / "policies").glob("*.yaml")):
        policy = yaml.safe_load(policy_path.read_text(encoding="utf-8"))
        refs = set(policy.get("required", [])) | set(policy.get("preferred", []))
        unknown = refs - skills
        check(
            f"policy references valid: {policy_path.name}",
            not unknown,
            f"unknown: {sorted(unknown)}",
        )

def test_resolution():
    cli = load_cli()
    for profile_path in sorted((ROOT / "profiles").glob("*.yaml")):
        profile, policy, selected = cli.resolve(profile_path)
        excluded = set(profile["skills"].get("exclude", []))
        expected_globals = cli.GLOBAL_SKILLS - excluded
        check(
            f"resolution includes global skills: {profile_path.name}",
            expected_globals <= set(selected),
            f"missing: {sorted(expected_globals - set(selected))}",
        )
        check(
            f"resolution excludes excluded skills: {profile_path.name}",
            not (excluded & set(selected)),
        )
        check(
            f"resolution includes policy required: {profile_path.name}",
            set(policy.get("required", [])) - excluded <= set(selected),
        )


# Deterministic expected resolution for each lifecycle, pinned to the current
# intentional behavior. With a minimal synthetic profile (no include, no
# exclude) the resolver selects: GLOBAL_SKILLS + policy required + policy
# preferred. These are explicit literals on purpose (not recomputed): if a
# lifecycle policy or the resolver changes, this test fails so the drift is
# reviewed deliberately. Update a set here only when the change is intended.
EXPECTED_LIFECYCLE_RESOLUTION = {
    "greenfield": {
        "change-planner",
        "code-review",
        "continuity-reviewer",
        "handoff",
        "reconstruct-system",
    },
    "building": {
        "change-planner",
        "code-review",
        "continuity-reviewer",
        "diagnosing-bugs",
        "handoff",
        "regression-guard",
    },
    "stabilizing": {
        "change-planner",
        "code-review",
        "continuity-reviewer",
        "deployment-safety",
        "diagnosing-bugs",
        "handoff",
        "production-validation",
        "regression-guard",
    },
    "production": {
        "change-planner",
        "code-review",
        "continuity-reviewer",
        "deployment-safety",
        "diagnosing-bugs",
        "handoff",
        "production-validation",
        "reconstruct-system",
        "regression-guard",
    },
    "legacy": {
        "change-planner",
        "code-review",
        "continuity-reviewer",
        "diagnosing-bugs",
        "handoff",
        "production-validation",
        "reconstruct-system",
        "regression-guard",
    },
}


def _minimal_profile(lifecycle, include=(), exclude=()):
    """Build a completely synthetic profile for regression testing."""
    return {
        "schema_version": 1,
        "project": {
            "id": "fixture-" + lifecycle,
            "name": "Fixture " + lifecycle.capitalize(),
            "lifecycle": lifecycle,
        },
        "skills": {"include": list(include), "exclude": list(exclude)},
    }


def test_lifecycle_regression_fixtures():
    """Pin the exact resolved skill set for every lifecycle so that an
    unintended lifecycle-policy or resolver change fails CI. Uses only
    synthetic, in-memory profiles (no private/internal data)."""
    cli = load_cli()
    known = cli.all_skills()
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        for lc, expected in EXPECTED_LIFECYCLE_RESOLUTION.items():
            check(
                f"fixture {lc}: pinned skills all known",
                expected <= known,
                f"unknown: {sorted(expected - known)}",
            )
            profile = _minimal_profile(lc)
            path = tmp / (lc + ".profile.yaml")
            path.write_text(yaml.safe_dump(profile), encoding="utf-8")
            resolved_profile, _policy, selected = cli.resolve(path)
            check(
                f"fixture {lc}: lifecycle selected",
                resolved_profile["project"]["lifecycle"] == lc,
            )
            got = set(selected)
            missing = expected - got
            extra = got - expected
            check(
                f"fixture {lc}: resolved set == pinned ({len(expected)} skills)",
                got == expected,
                f"missing={sorted(missing)} extra={sorted(extra)}",
            )
        # Exclusion is respected: drop a preferred skill from production.
        lc, excluded_skill = "production", "reconstruct-system"
        expected_minus = EXPECTED_LIFECYCLE_RESOLUTION[lc] - {excluded_skill}
        profile = _minimal_profile(lc, exclude=[excluded_skill])
        path = tmp / (lc + "-exclude.profile.yaml")
        path.write_text(yaml.safe_dump(profile), encoding="utf-8")
        _rp, _po, selected = cli.resolve(path)
        got = set(selected)
        check(
            f"fixture {lc}: exclusion removes {excluded_skill}",
            excluded_skill not in got and got == expected_minus,
            f"got={sorted(got)} expected={sorted(expected_minus)}",
        )


def test_activation_preserves_unmanaged():
    cli = load_cli()
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        target = tmp / "codex_home" / "skills"
        target.mkdir(parents=True)
        os.environ["CODEX_HOME"] = str(tmp / "codex_home")
        try:
            # Pre-existing unrelated skill that must survive activation.
            (target / "user-skill").mkdir()
            (target / "user-skill" / "SKILL.md").write_text(
                "---\nname: user-skill\ndescription: user managed\n---\n",
                encoding="utf-8",
            )
            profile_path = ROOT / "profiles" / "example-web-app.yaml"
            cli.activate(profile_path)
            check(
                "activation preserves unmanaged skills",
                (target / "user-skill" / "SKILL.md").exists(),
            )
            manifest = target / cli.MANIFEST_NAME
            managed = set(manifest.read_text(encoding="utf-8").splitlines())
            check("activation wrote manifest", "user-skill" not in managed)
            # Second activation: managed skills get replaced without error.
            cli.activate(profile_path)
            check(
                "re-activation succeeds",
                (target / "user-skill" / "SKILL.md").exists(),
            )
        finally:
            os.environ.pop("CODEX_HOME", None)


def test_activation_manifest_scoped_cleanup():
    """A skill this pack previously installed must be removed from the target
    once it falls out of the resolved set, while unmanaged user skills are left
    alone (manifest-scoped cleanup; exercises shutil.rmtree across platforms).
    """
    cli = load_cli()
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        target = tmp / "codex_home" / "skills"
        target.mkdir(parents=True)
        os.environ["CODEX_HOME"] = str(tmp / "codex_home")
        try:
            (target / "user-skill").mkdir()
            (target / "user-skill" / "SKILL.md").write_text(
                "---\nname: user-skill\ndescription: user managed\n---\n",
                encoding="utf-8",
            )
            # production profile resolves reconstruct-system; building does not.
            with_skill = ROOT / "profiles" / "example-production-service.yaml"
            without_skill = ROOT / "profiles" / "example-web-app.yaml"

            cli.activate(with_skill)
            managed = set(
                (target / cli.MANIFEST_NAME).read_text(encoding="utf-8")
                .splitlines()
            )
            check(
                "cleanup: installed skill recorded in manifest",
                "reconstruct-system" in managed,
            )
            check(
                "cleanup: installed skill directory present",
                (target / "reconstruct-system" / "SKILL.md").exists(),
            )

            cli.activate(without_skill)
            managed = set(
                (target / cli.MANIFEST_NAME).read_text(encoding="utf-8")
                .splitlines()
            )
            check(
                "cleanup: deselected skill removed from manifest",
                "reconstruct-system" not in managed,
            )
            check(
                "cleanup: deselected skill directory removed from target",
                not (target / "reconstruct-system").exists(),
            )
            check(
                "cleanup: unmanaged user skill survives deselection",
                (target / "user-skill" / "SKILL.md").exists(),
            )
        finally:
            os.environ.pop("CODEX_HOME", None)


def test_forbidden_identifiers():
    hits = []
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in SCAN_EXTENSIONS:
            continue
        if path.name == "test_export.py":
            continue  # the forbidden list lives here
        rel = path.relative_to(ROOT)
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for pattern in FORBIDDEN_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                hits.append(f"{rel}: /{pattern}/")
    check("no forbidden internal identifiers", not hits, "\n  " + "\n  ".join(hits))


def test_no_env_files():
    env_files = [
        p for p in ROOT.rglob("*") if p.is_file() and p.name.startswith(".env")
    ]
    check("no .env files", not env_files, f"found: {env_files}")


def main():
    os.chdir(ROOT)
    test_required_files()
    test_profiles_parse()
    test_policy_references()
    test_resolution()
    test_lifecycle_regression_fixtures()
    test_activation_preserves_unmanaged()
    test_activation_manifest_scoped_cleanup()
    test_forbidden_identifiers()
    test_no_env_files()
    if FAILURES:
        print(f"\nFAILED: {len(FAILURES)} check(s)")
        sys.exit(1)
    print("\nALL CHECKS PASSED")


if __name__ == "__main__":
    main()

