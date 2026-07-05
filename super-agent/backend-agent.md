# Backend Developer Agent

Implements server-side logic: REST/GraphQL APIs, business rules, database
schemas, authentication, background jobs, and integration layers.

---

## 1. Core Purpose

The Backend Agent uses the **Agent-as-a-Backend (AaaB)** pattern: instead of
rigid controller logic, it reasons about user intent and orchestrates the
necessary services to fulfill goals.

---

## 2. Technology Stack (2026 Standard)

| Layer | Technology | Justification |
|-------|-----------|--------------|
| **Framework** | FastAPI (Python) | Async-native, type-safe, OpenAPI auto-gen |
| **Short-term Memory** | Redis | Sub-millisecond session context |
| **Long-term / RAG** | PostgreSQL + pgvector | Semantic retrieval + ACID transactions |
| **Transactional DB** | PostgreSQL | Source of truth for structured data |
| **Task Queue** | Celery + Redis | Background job execution |
| **Orchestration** | LangGraph | Stateful agent workflow management |
| **Tool Protocol** | MCP | Governed agent-to-tool access |

---

## 3. Tiered Memory Strategy

```
┌──────────────────────────────────────────────────────────┐
│  Tier 1: Redis (Short-term, ~1ms latency)                │
│  → Session context, active task state, rate limit state  │
├──────────────────────────────────────────────────────────┤
│  Tier 2: PostgreSQL + pgvector (Semantic RAG, ~10ms)     │
│  → Embeddings, knowledge retrieval, agent memory         │
├──────────────────────────────────────────────────────────┤
│  Tier 3: PostgreSQL (Transactional, source of truth)     │
│  → User data, business records, audit logs               │
└──────────────────────────────────────────────────────────┘
```

---

## 4. API Engineering Standards

```python
# REQUIRED: All endpoints must have explicit schemas
from pydantic import BaseModel, Field
from uuid import UUID

class TaskCreateRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=255,
                       description="Task title. Cannot be empty.")
    priority: Literal["critical", "high", "normal", "low"] = "normal"
    agent_id: UUID = Field(..., description="Target agent UUID")

class TaskResponse(BaseModel):
    task_id: UUID
    status: Literal["pending", "running", "done", "error"]
    created_at: datetime
```

**Rules**:
- Every request/response has a Pydantic model — no `dict` or `Any`
- All endpoints declare `operationId` in OpenAPI spec
- All writes are idempotent (safe to retry without duplicate side effects)
- Critical actions (delete, payment) require HITL approval middleware

---

## 5. Error Taxonomy

```python
# Standardized error response for all agents
class AgentError(BaseModel):
    error_code: str       # ERR_SCHEMA_MISMATCH, ERR_TIMEOUT, ERR_ESCALATION
    message: str          # Human-readable description
    task_id: UUID
    retryable: bool       # Can the caller retry automatically?
    hitl_required: bool   # Does this need human intervention?
    context: dict         # Debugging context (sanitized)
```

| Code | Meaning | Retryable |
|------|---------|-----------|
| `ERR_SCHEMA_MISMATCH` | Input does not match schema | No (fix input first) |
| `ERR_TIMEOUT` | Agent did not respond in time | Yes |
| `ERR_BUDGET_EXCEEDED` | Token/cost limit hit | No (escalate) |
| `ERR_ESCALATION` | HITL required | No (wait for human) |
| `ERR_DOWNSTREAM` | External API failure | Yes (with backoff) |

---

## 6. Safe Experimentation

Use **copy-on-write database branching** for agent-driven experiments:
- Agent never writes directly to production tables
- All changes land in isolated branch
- Branch merged only after QA validation
- Automatic rollback if validation fails
