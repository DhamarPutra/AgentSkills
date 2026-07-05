# System Architecture

Detailed structural design: component boundaries, data flows, technology
choices, integration patterns, failure domains, and blast radius analysis.

---

## 1. Component Architecture

```
                          ┌─────────────────────────────────────┐
                          │         EXTERNAL INTERFACE          │
                          │   (REST API / CLI / WebSocket)      │
                          └───────────────┬─────────────────────┘
                                          │
                          ┌───────────────▼─────────────────────┐
                          │           ORCHESTRATOR              │
                          │     (LangGraph State Machine)       │
                          └──┬────┬────┬────┬────┬────┬────┬───┘
                             │    │    │    │    │    │    │
             ┌───────────────┘    │    │    │    │    │    └────────────────┐
             │             ┌──────┘    │    │    └──────┐                  │
             ▼             ▼           ▼    ▼           ▼                  ▼
        ┌─────────┐ ┌──────────┐ ┌───────┐ ┌───────┐ ┌──────────┐ ┌──────────┐
        │Planner  │ │Architect │ │Backend│ │Frontend│ │ QA/Debug │ │ DevOps/  │
        │ Agent   │ │  Agent   │ │ Agent │ │ Agent  │ │  Agents  │ │ Reporter │
        └────┬────┘ └────┬─────┘ └───┬───┘ └───┬────┘ └────┬─────┘ └────┬─────┘
             │           │           │          │           │            │
             └───────────┴───────────┴──────────┴───────────┴────────────┘
                                           │
                          ┌────────────────▼────────────────────┐
                          │            MCP LAYER                │
                          │    (Governed Tool Access Gateway)   │
                          └──┬─────────┬──────────┬────────────┘
                             │         │          │
                        ┌────▼────┐ ┌──▼──┐ ┌────▼────┐
                        │  Redis  │ │ PG  │ │ Docker  │
                        │(Memory) │ │(DB) │ │  K8s    │
                        └─────────┘ └─────┘ └─────────┘
```

---

## 2. Data Flow: Task Execution

```
1. User sends goal via API
2. Orchestrator creates Task (trace_id assigned)
3. Orchestrator → Planner: "decompose this goal"
4. Planner returns: spec.md + atomic task list
5. Orchestrator → Architect: "design system for this spec"
6. Architect returns: ADRs + API schemas
7. Orchestrator → Backend + Frontend (parallel): "implement"
8. Agents write to isolated DB branches
9. QA Agent validates all outputs
10. QA pass → DevOps deploys to staging
11. HITL gate → human approves production
12. DevOps: canary → 100% production
13. Reporter: generates changelog
14. Orchestrator: closes task, writes to project memory
```

---

## 3. Failure Domains & Blast Radius

| Failure | Affected Components | Blast Radius | Recovery |
|---------|---------------------|--------------|----------|
| Redis down | Working memory, sessions | High — active tasks fail | Failover to replica |
| PostgreSQL down | Long-term memory, API data | Critical | Backup restore |
| Single agent crash | That agent's tasks | Low — Orchestrator retries | Auto-restart in K8s |
| Orchestrator crash | All in-flight tasks | High | LangGraph checkpoint resume |
| Full cluster down | Everything | Critical | DR procedure |

---

## 4. Integration Boundaries

| Integration | Type | Protocol | Auth |
|-------------|------|----------|------|
| External User | Synchronous | REST + WebSocket | JWT |
| Agent-to-Agent | Via Orchestrator | Internal JSON | Service account |
| Agent-to-Tools | Via MCP | MCP protocol | RBAC token |
| Agent-to-DB | Direct (scoped) | SQL/Redis | Minimal privilege role |
| CI/CD | Event-driven | GitHub webhooks | Deploy key |
