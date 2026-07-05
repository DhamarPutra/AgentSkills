# Agent Roles — Overview

This document provides a quick reference for all agent roles in the
`super-agent` multi-agent system framework.

---

## Role Summary Table

| Agent | File | Core Responsibility |
|-------|------|---------------------|
| **Orchestrator** | `orchestrator.md` | Central coordinator. Routes all tasks, manages state, synthesizes agent outputs. |
| **Planner** | `planner-agent.md` | Breaks down user goals into structured implementation plans with clear acceptance criteria. |
| **Architect** | `architect-agent.md` | Designs component boundaries, API contracts, data models, and technology choices. |
| **Backend** | `backend-agent.md` | Implements server-side APIs, business logic, database schemas, and auth flows. |
| **Frontend** | `frontend-agent.md` | Builds UI components, manages client state, implements responsive layouts. |
| **QA** | `qa-agent.md` | Writes and runs tests, validates requirements, reports defects. |
| **Debug** | `debug-agent.md` | Traces runtime errors to root causes, proposes targeted hotfixes. |
| **Security** | `security-agent.md` | Audits for OWASP vulnerabilities, enforces CSP, validates access control. |
| **DevOps** | `devops-agent.md` | Manages CI/CD, Docker, cloud infra, secrets, and deployment automation. |
| **Reporter** | `reporter-agent.md` | Generates changelogs, release notes, and keeps documentation in sync. |

---

## Task Delegation Flow

```
User Prompt
    │
    ▼
Orchestrator ──► Planner (create plan)
    │
    ├──► Architect (design structure)
    │
    ├──► Backend Agent (implement API/logic)
    ├──► Frontend Agent (implement UI)
    │
    ├──► QA Agent (test & validate)
    ├──► Debug Agent (fix failures)
    ├──► Security Agent (audit)
    │
    ├──► DevOps Agent (deploy)
    │
    └──► Reporter Agent (document & report)
```

---

## Communication Contract

All inter-agent messages follow this JSON schema:

```json
{
  "task_id": "uuid-v4",
  "from": "orchestrator",
  "to": "backend-agent",
  "type": "TASK",
  "payload": { },
  "priority": "high | normal | low",
  "timestamp": "ISO-8601"
}
```

Response schema:

```json
{
  "task_id": "uuid-v4",
  "from": "backend-agent",
  "to": "orchestrator",
  "type": "RESULT",
  "status": "success | error | partial",
  "result": { },
  "errors": [],
  "timestamp": "ISO-8601"
}
```

---

## Design Principles

1. **Single Responsibility**: Each agent does exactly one thing well.
2. **Loose Coupling**: Agents communicate only via the Orchestrator; no direct agent-to-agent calls.
3. **Fail Gracefully**: Every agent must handle errors and return structured error responses.
4. **Stateless Execution**: Agents do not hold persistent state between tasks — state lives in `project-memory`.
5. **Interchangeable**: Any agent can be swapped for a different implementation as long as it adheres to the communication contract.
