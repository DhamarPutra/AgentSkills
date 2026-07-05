# 🤖 Super-Agent

**Bootstrap a complete multi-agent system in one command.**

`super-agent` is an AI agent skill that automatically generates the full documentation structure for a professional multi-agent software system — 21 Markdown files covering roles, architecture, workflows, standards, and more — in a single prompt or Python command.

---

## ✨ What It Does

Run one command → get a fully scaffolded multi-agent documentation system:

```
super-agent/
├── system-overview.md       ← High-level system design
├── architecture.md          ← Component & tech stack design
├── orchestrator.md          ← Orchestrator agent role
├── planner-agent.md         ← Planner agent role
├── architect-agent.md       ← Architect agent role
├── backend-agent.md         ← Backend developer agent role
├── frontend-agent.md        ← Frontend developer agent role
├── qa-agent.md              ← QA & testing agent role
├── debug-agent.md           ← Debug agent role
├── security-agent.md        ← Security agent role
├── devops-agent.md          ← DevOps & infra agent role
├── reporter-agent.md        ← Reporter agent role
├── agent-communication.md   ← Inter-agent communication protocol
├── project-memory.md        ← Memory & state management
├── workflow.md              ← End-to-end pipeline flow
├── project-rules.md         ← Team rules & conventions
├── repository-structure.md  ← Folder layout guidelines
├── coding-standard.md       ← Code style & linting rules
├── testing-standard.md      ← Testing requirements & coverage
├── deployment.md            ← Deployment & rollback procedures
└── roadmap.md               ← Product milestones & roadmap
```

---

## 🚀 Quick Start

### Option A — Using an AI Agent (Recommended)

If you're using an AI coding agent (Antigravity, Cursor, GitHub Copilot, etc.):

1. Copy the `super-agent/` folder into your `.agents/skills/` directory (or equivalent skill directory for your agent tool).
2. Open a chat with your AI agent and type:

```
generate all docs from list.md
```

The agent will automatically read `list.md` and generate all files with professional content.

---

### Option B — Using Python Script

No AI agent needed. Just run the generator script directly:

```bash
# Clone or download this repo
git clone https://github.com/DhamarPutra/AgentSkills.git
cd AgentSkills/super-agent

# Generate all documentation files (skips existing files)
python generate_docs.py

# Overwrite all existing files
python generate_docs.py --overwrite

# Preview what would be generated (no files written)
python generate_docs.py --dry-run
```

**Requirements**: Python 3.6+ (no extra packages needed)

---

## 🤖 Supported AI Agents

This skill is designed to be **universal** and works with any AI agent or coding assistant:

| Agent Tool | Skill Directory |
|---|---|
| Antigravity IDE | `.agents/skills/super-agent/` |
| Cursor | `.cursor/rules/` (adapt SKILL.md as a rule) |
| GitHub Copilot | `.github/copilot-instructions.md` (adapt) |
| Claude Projects | Add SKILL.md as project knowledge |
| ChatGPT | Use SKILL.md as a custom instruction |

---

## 📋 Customizing the File List

Edit [`list.md`](list.md) to add, remove, or rename files before generating:

```
# list.md
project-rules.md
system-overview.md
architecture.md
my-custom-agent.md    ← add your own!
...
```

Then run `python generate_docs.py` again.

---

## 🗂 Agent Roles Overview

| Agent | Responsibility |
|---|---|
| **Orchestrator** | Routes tasks, manages state, coordinates all agents |
| **Planner** | Breaks down requirements, proposes implementation plans |
| **Architect** | Designs component structure, API contracts, data models |
| **Backend** | Implements APIs, business logic, database schemas |
| **Frontend** | Builds UI, manages state, handles responsive design |
| **QA** | Writes & runs tests, validates requirements |
| **Debug** | Analyzes errors, traces bugs, proposes hotfixes |
| **Security** | Audits vulnerabilities, validates CSP & auth flows |
| **DevOps** | Manages CI/CD, Docker, cloud infra, environments |
| **Reporter** | Writes release notes, keeps documentation updated |

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Add new agent role templates
- Improve the boilerplate content quality
- Add support for other languages (JS, Go, etc.)
- Submit a PR or open an issue

---

## 📄 License

MIT License — see [LICENSE](../LICENSE) for details.

---

Made with ❤️ by [DhamarPutra](https://github.com/DhamarPutra)
