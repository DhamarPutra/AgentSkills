#!/usr/bin/env python3
"""
super-agent — Reset Generated Docs
====================================
Removes all generated .md files listed in list.md, resetting the
super-agent directory to a clean state.

Usage:
    python scripts/reset_docs.py           # Interactive confirm
    python scripts/reset_docs.py --force   # Skip confirmation

Use this before running generate_docs.py to ensure a completely fresh output.
"""
import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIST_FILE = os.path.join(SKILL_DIR, "list.md")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Reset generated docs")
    parser.add_argument("--force", action="store_true",
                        help="Skip confirmation prompt")
    args = parser.parse_args()

    if not os.path.exists(LIST_FILE):
        print("[ERROR] list.md not found. Nothing to reset.")
        sys.exit(1)

    with open(LIST_FILE, encoding="utf-8") as f:
        files = [l.strip() for l in f if l.strip() and not l.startswith("#")]

    existing = [f for f in files if os.path.exists(os.path.join(SKILL_DIR, f))]

    if not existing:
        print("Nothing to reset — no generated files found.")
        return

    print(f"\nFiles to delete ({len(existing)}):")
    for fname in existing:
        print(f"  - {fname}")

    if not args.force:
        confirm = input("\nDelete these files? [y/N] ").strip().lower()
        if confirm != "y":
            print("Aborted.")
            return

    deleted = 0
    for fname in existing:
        fpath = os.path.join(SKILL_DIR, fname)
        os.remove(fpath)
        print(f"  Deleted: {fname}")
        deleted += 1

    print(f"\nReset complete. {deleted} files deleted.")
    print("Run 'python generate_docs.py' to regenerate.\n")


if __name__ == "__main__":
    main()
