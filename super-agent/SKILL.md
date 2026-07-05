---
name: super-agent
description: >
  Bootstraps a complete multi-agent system by generating all required
  architecture and role documentation files in one command. Use when a user
  asks to "initialize agent docs", "generate agent documentation", "setup
  super-agent", "bootstrap multi-agent system", or "generate all md files".
---

# Super-Agent — Multi-Agent System Bootstrap Skill

This skill enables any AI agent (Antigravity, Cursor, GitHub Copilot, Claude,
ChatGPT, etc.) to bootstrap a full multi-agent project documentation structure
with a single prompt or command.

---

## Trigger Keywords

This skill activates when the user says any of the following (or similar):
- "generate all docs"
- "initialize agent documentation"
- "setup super-agent"
- "bootstrap multi-agent system"
- "generate all md files"
- "run generate_docs"

---

## Core Instructions

When this skill is triggered, follow these steps **sequentially**:

### Step 1 — Read the File List
Read `list.md` in the current `super-agent/` directory to get the full list
of target documentation files to generate.

### Step 2 — Generate Each File
For each filename listed in `list.md`:
1. Check if the file already exists in `super-agent/`
2. If it does NOT exist (or `--overwrite` is requested): create it
3. Write rich, professional content based on the filename's implied role:
   - `*-agent.md` → Agent role specs (purpose, responsibilities, I/O, interactions)
   - `architecture.md` / `system-overview.md` → System-level design documents
   - `*-standard.md` → Coding/testing guidelines and conventions
   - `workflow.md` / `orchestrator.md` → Process and coordination flows
   - `deployment.md` / `roadmap.md` → Operational and planning documents
   - `project-rules.md` / `project-memory.md` → Team conventions and memory

### Step 3 — Confirm Completion
After all files are generated, output a summary table showing:
- ✅ Files created
- ⏭ Files skipped (already existed)
- ❌ Files that failed (if any)

---

## File Content Structure Template

Every generated file must follow this structure:

```markdown
# [Document Title]

[One-sentence description of this document's purpose]

---

## 1. Core Purpose
[What problem this solves or role this defines]

## 2. Specifications & Scope
[Rules, constraints, and boundaries]

## 3. Workflow & Responsibilities
- **Input**: What this role/component receives
- **Process**: What it does
- **Output**: What it produces

## 4. Interaction Patterns
[How this interacts with other agents or system components]

## 5. Maintenance & Versioning
[How to keep this document updated]
```

---

## Using the Generator Script

For automated (non-AI) execution, users can run the included Python script:

```bash
# Generate all files (skip existing)
python generate_docs.py

# Overwrite all existing files
python generate_docs.py --overwrite

# Preview without writing (dry run)
python generate_docs.py --dry-run
```

---

## References

For deeper context on the agent roles and system design, read:
- [`references/agents-overview.md`](references/agents-overview.md)
