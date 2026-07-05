# Multi-Agent Project Kickoff Checklist

Use this checklist at the start of every new software project built with
the super-agent multi-agent system. Based on industry research 2025-2026.

**Project**: _______________
**Date**: _______________
**Lead**: _______________

---

## Phase 1 — Goal Definition & Scope

- [ ] **Define Specific Outcome**: What does success look like in one sentence?
- [ ] **Validate Multi-Agent Necessity**: Can a single agent solve this? If yes, start simple.
- [ ] **Set Business KPIs**: Define measurable success metrics (not just technical).
- [ ] **Document Non-Goals**: Explicitly list what this system will NOT do.
- [ ] **Identify Stakeholders**: Who approves deployments? Who gets incident alerts?

---

## Phase 2 — Architecture Selection

- [ ] **Select Interaction Pattern**:
  - [ ] Hub-and-Spoke (recommended for most cases — best debuggability)
  - [ ] Hierarchical (for multi-tier domain expertise)
  - [ ] Flat Mesh (for high fault tolerance, high observability cost)

- [ ] **Define the Orchestrator**: Assign clear responsibility for task decomposition.
- [ ] **Establish Communication Protocol**: Confirm all agents will use the A2A schema in `agent-communication.md`.
- [ ] **Plan Memory Architecture**: Choose Centralized / Distributed / Hybrid.

---

## Phase 3 — Technical Readiness

- [ ] **Framework Selected**: LangGraph / CrewAI / AutoGen (see `references/framework-comparison.md`)
- [ ] **Infrastructure Ready**:
  - [ ] Redis available for short-term memory
  - [ ] PostgreSQL + pgvector for long-term memory and RAG
  - [ ] Docker + Kubernetes configured
  - [ ] CI/CD pipeline (GitHub Actions) configured
- [ ] **Observability Stack**: OpenTelemetry tracing + Grafana dashboard

---

## Phase 4 — Safety, Governance & Guardrails

- [ ] **HITL Gates Defined**: List every action that requires human approval.
- [ ] **Constraint Engineering**: Document hard limits per agent (token budget, tool access).
- [ ] **Rollback Procedures**: Every state-modifying action has a tested rollback.
- [ ] **Idempotency Verified**: Retrying any agent action does not produce duplicates.
- [ ] **RBAC Configured**: Agents have minimum required permissions only.

---

## Phase 5 — Testing Strategy

- [ ] **Test Pyramid Defined**: Unit (≥80%) + Integration (≥60%) + E2E (critical paths).
- [ ] **Chaos Test Scenarios**: At least 5 failure injection scenarios documented.
- [ ] **LLM Evaluation Rubric**: Defined for all non-deterministic outputs.
- [ ] **Continuous Eval Pipeline**: Automated evaluation in CI (not just one-off).

---

## Phase 6 — Team Readiness

- [ ] **On-Call Assigned**: Who owns the "off switch" in an incident?
- [ ] **Context Engineering Training**: Team understands dynamic context management.
- [ ] **Review Cycle**: Scheduled sprint review for agent performance.
- [ ] **Contribution Guidelines**: Contributors know how to add new agent roles.

---

## Quick Reference: Pattern Selection

| Architecture | Use When | Trade-off |
|---|---|---|
| **Hub-and-Spoke** | Default — centralized control needed | Lower adaptability |
| **Hierarchical** | Multi-domain expertise required | High design complexity |
| **Flat Mesh** | Fault tolerance is paramount | High observability cost |

---

**Checklist complete?** → Start with the Planner Agent and generate your `spec.md`.
