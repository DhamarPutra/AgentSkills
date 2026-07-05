#!/usr/bin/env python3
"""
super-agent — Skill Validator
=============================
Checks the health of the super-agent skill installation.

Usage: python scripts/validate_skill.py

Exit code 0 = all checks passed
Exit code 1 = one or more checks failed
"""
import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIST_FILE = os.path.join(SKILL_DIR, "list.md")

REQUIRED_FILES = [
    "SKILL.md",
    "list.md",
    "generate_docs.py",
    "README.md",
    "AGENTS.md",
    "CHANGELOG.md",
]

PLACEHOLDER_STRINGS = [
    "Describe the main objective",
    "Describe the most important rule",
    "Step-by-step instructions or reference examples",
]


def check(label: str, passed: bool, detail: str = ""):
    icon = "[PASS]" if passed else "[FAIL]"
    msg = f"  {icon} {label}"
    if detail and not passed:
        msg += f"\n         {detail}"
    print(msg)
    return passed


def run_checks() -> bool:
    all_passed = True
    print("\nsuper-agent Skill Validator\n" + "=" * 40)

    # 1. Required files exist
    print("\n[1] Required files")
    for fname in REQUIRED_FILES:
        fpath = os.path.join(SKILL_DIR, fname)
        ok = os.path.exists(fpath)
        all_passed &= check(f"{fname} exists", ok,
                            f"Missing: {fpath}")

    # 2. SKILL.md has valid frontmatter
    print("\n[2] SKILL.md frontmatter")
    skill_path = os.path.join(SKILL_DIR, "SKILL.md")
    if os.path.exists(skill_path):
        with open(skill_path, encoding="utf-8") as f:
            content = f.read()
        has_name = "name:" in content
        has_desc = "description:" in content
        all_passed &= check("Has 'name:' field", has_name)
        all_passed &= check("Has 'description:' field", has_desc)
    else:
        all_passed = False

    # 3. list.md has content
    print("\n[3] list.md validity")
    if os.path.exists(LIST_FILE):
        with open(LIST_FILE, encoding="utf-8") as f:
            lines = [l.strip() for l in f if l.strip() and not l.startswith("#")]
        all_passed &= check(f"list.md has {len(lines)} entries", len(lines) > 0)
        md_files = [l for l in lines if l.endswith(".md")]
        all_passed &= check("All entries are .md files",
                            len(md_files) == len(lines),
                            "Non-.md entries found in list.md")

        # 4. Check generated files exist and have content
        print("\n[4] Generated files")
        empty_count = 0
        placeholder_count = 0
        for fname in lines:
            fpath = os.path.join(SKILL_DIR, fname)
            if not os.path.exists(fpath):
                all_passed &= check(f"{fname} exists", False, "Run: python generate_docs.py")
                empty_count += 1
                continue
            with open(fpath, encoding="utf-8") as f:
                file_content = f.read()
            is_empty = len(file_content.strip()) < 50
            has_placeholder = any(p in file_content for p in PLACEHOLDER_STRINGS)
            if is_empty:
                empty_count += 1
            if has_placeholder:
                placeholder_count += 1

        all_passed &= check(
            f"All {len(lines)} files exist",
            empty_count == 0,
            f"{empty_count} missing files. Run: python generate_docs.py"
        )
        all_passed &= check(
            "No placeholder content detected",
            placeholder_count == 0,
            f"{placeholder_count} files still have placeholder text. Run: python generate_docs.py --overwrite"
        )

    # Summary
    print("\n" + "=" * 40)
    if all_passed:
        print("Result: ALL CHECKS PASSED")
        print("Skill is healthy and ready to use.\n")
    else:
        print("Result: SOME CHECKS FAILED")
        print("Fix the issues above and run again.\n")

    return all_passed


if __name__ == "__main__":
    sys.exit(0 if run_checks() else 1)
