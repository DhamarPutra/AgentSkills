# AGENTS.md — Super-Agent Behavioral Guidelines

This file defines repo-wide behavioral rules for ALL AI agents operating
within this project. It is automatically loaded by compatible agent tools
(Antigravity IDE, Cursor, Claude Code, etc.) as high-priority instructions.

---

## Hard Rules (Cannot Be Overridden)

1. **Read SKILL.md first**: Before executing any task, read `SKILL.md` in its
   entirety to understand the skill's scope and trigger conditions.

2. **No irreversible actions without confirmation**: Never delete files, push
   to remote, or overwrite production data without explicit user confirmation.

3. **Dry-run before overwrite**: When using `generate_docs.py`, prefer
   `--dry-run` first to preview changes before `--overwrite`.

4. **Preserve user content**: Never overwrite files that contain substantive
   user-written content (detected by checking if content differs from the
   boilerplate template).

5. **No network requests**: This skill operates entirely locally. Do not make
   external API calls, fetch URLs, or install packages.

---

## Safe Defaults

- When ambiguous, **ask for clarification** rather than guessing.
- When generating content, **use the CONTENT registry** in `generate_docs.py`
  — do not invent schemas that conflict with documented standards.
- When modifying `list.md`, **validate** that all entries have a corresponding
  content template in `generate_docs.py` before saving.

---

## Escalation Policy (HITL Triggers)

Stop and ask the user when:
- The task would modify files outside the `super-agent/` directory
- The task would delete more than 3 files at once
- The task output conflicts with an existing Architecture Decision Record
- A validation check fails and the fix is non-obvious

---

## Output Contract

All agent outputs for this skill must:
- Be Markdown-formatted with proper heading hierarchy
- Include section numbers (## 1. Title, ## 2. Title)
- Not contain placeholder text like "Describe the main objective..."
- Pass `validate_skill.py` checks before being considered complete
