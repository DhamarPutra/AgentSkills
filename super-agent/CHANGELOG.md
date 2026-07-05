# Changelog

All notable changes to this skill are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.0.0] - 2026-07-05

### Added
- **Overpower content**: All 21 generated `.md` files now contain
  production-grade, research-backed content instead of placeholder boilerplate
- `AGENTS.md`: Repo-wide behavioral guardrails for all compatible AI agents
- `scripts/validate_skill.py`: Automated health check for skill integrity
- `scripts/reset_docs.py`: Reset generated docs to clean state
- `assets/agent-role-template.md`: Blank template for creating new agent roles
- `assets/system-doc-template.md`: Blank template for system documentation
- `assets/project-kickoff.md`: Full multi-agent project kickoff checklist
- `references/communication-spec.md`: Complete A2A communication protocol
- `references/guardrails.md`: Behavioral constraints and safety patterns
- `references/framework-comparison.md`: LangGraph vs CrewAI vs AutoGen guide
- `CHANGELOG.md`: This file

### Changed
- `generate_docs.py` v2.0: Complete rewrite with rich CONTENT registry
  supporting all 21 agent documentation files with substantive content
- `SKILL.md`: Rewritten with universal instructions, progressive disclosure,
  negative triggers, and explicit platform compatibility declarations
- `README.md`: Updated with badges, enhanced quick start, and complete
  directory structure diagram
- `references/agents-overview.md`: Enhanced with design principles and
  communication contract schema

### Research Sources
Content based on: Anthropic, LangGraph, OWASP Agentic Top 10 (2026),
MITRE ATLAS, MLflow, Redis, Temporal, Mem0, Google ADK, GitHub Engineering Blog

---

## [1.0.0] - 2026-07-05

### Added
- Initial release with 21 auto-generated documentation files (boilerplate)
- `generate_docs.py` v1.0 with `--overwrite` and `--dry-run` flags
- `SKILL.md` with basic orchestration instructions
- `README.md` with quick start guide
- MIT `LICENSE`
- Root `AgentSkills/README.md`
