# Repository Structure

Canonical directory layout, naming conventions, file ownership, and
branching strategy for the multi-agent system project.

---

## 1. Root Directory Layout

```
project-root/
├── .agents/                    ← Agent skill configurations
│   └── skills/
│       └── super-agent/        ← This skill
├── .github/
│   └── workflows/              ← CI/CD pipelines
├── src/
│   ├── orchestrator/           ← Orchestrator service
│   ├── agents/                 ← Individual agent implementations
│   │   ├── planner/
│   │   ├── architect/
│   │   ├── backend/
│   │   ├── frontend/
│   │   ├── qa/
│   │   ├── debug/
│   │   ├── security/
│   │   ├── devops/
│   │   └── reporter/
│   ├── shared/                 ← Shared schemas, utilities, base classes
│   │   ├── schemas/            ← Pydantic models (task, result, error)
│   │   ├── memory/             ← Memory layer implementations
│   │   └── mcp/                ← MCP client utilities
│   └── api/                    ← External-facing FastAPI app
├── tests/
│   ├── unit/                   ← Unit tests (mirrors src/ structure)
│   ├── integration/            ← API + agent integration tests
│   ├── e2e/                    ← End-to-end critical path tests
│   └── chaos/                  ← Chaos injection tests
├── infra/
│   ├── docker/                 ← Dockerfiles per service
│   ├── k8s/                    ← Kubernetes manifests
│   └── terraform/              ← Infrastructure as Code
├── docs/
│   ├── adr/                    ← Architecture Decision Records
│   ├── api/                    ← Generated OpenAPI docs
│   └── runbooks/               ← Operational runbooks
├── scripts/                    ← Dev & ops utility scripts
├── AGENTS.md                   ← Agent behavioral guidelines
├── CHANGELOG.md                ← Version history
└── README.md                   ← Project overview
```

---

## 2. Naming Conventions

| Type | Convention | Example |
|------|-----------|---------|
| Python files | `snake_case.py` | `task_scheduler.py` |
| Python classes | `PascalCase` | `OrchestratorAgent` |
| Python functions | `snake_case()` | `delegate_task()` |
| Python constants | `UPPER_SNAKE_CASE` | `MAX_RETRIES = 3` |
| Test files | `test_<module>.py` | `test_orchestrator.py` |
| Test functions | `test_<unit>_<scenario>_<expected>` | see Testing Standard |
| K8s manifests | `<resource>-<name>.yaml` | `deploy-backend-agent.yaml` |
| Docker images | `super-agent/<service>:<semver>` | `super-agent/backend:2.1.0` |
| ADR files | `ADR-<NNN>-<title>.md` | `ADR-001-hub-spoke-pattern.md` |

---

## 3. File Ownership

| Directory | Owner | Review Required By |
|-----------|-------|--------------------|
| `src/orchestrator/` | Backend Lead | Architect Agent |
| `src/agents/*/` | Respective Agent | QA Agent |
| `src/shared/schemas/` | Architect Agent | All agents |
| `infra/` | DevOps Agent | Security Agent |
| `tests/` | QA Agent | All agents |
| `docs/adr/` | Architect Agent | Tech Lead |
