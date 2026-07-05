#!/usr/bin/env python3
"""
super-agent — Overpower Documentation Generator v2.0
=====================================================
Generates all multi-agent system documentation files listed in list.md
with rich, production-grade, research-backed content.

Usage:
    python generate_docs.py              # Generate missing files only
    python generate_docs.py --overwrite  # Overwrite all existing files
    python generate_docs.py --dry-run    # Preview without writing any files

Requirements: Python 3.6+ (no extra packages)
Sources: Anthropic, LangGraph, CrewAI, OWASP 2026, MLflow, Redis, Temporal, Mem0
"""

import os
import sys
import argparse
from datetime import date

# Force UTF-8 output (fixes emoji on Windows terminals)
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LIST_FILE = os.path.join(BASE_DIR, "list.md")
TODAY = date.today().strftime("%Y-%m-%d")

# ─────────────────────────────────────────────────────────────────────────────
# CONTENT REGISTRY — Rich, research-backed content for all 21 files
# ─────────────────────────────────────────────────────────────────────────────

CONTENT = {}

# ─── 1. ORCHESTRATOR ─────────────────────────────────────────────────────────
CONTENT["orchestrator.md"] = """# Orchestrator Agent

The central conductor of the multi-agent system. Receives all incoming tasks,
decomposes them into sub-tasks, delegates to specialized agents, tracks
progress, and synthesizes final results.

---

## 1. Core Purpose

The Orchestrator implements the **Hub-and-Spoke pattern** — the industry
standard for production multi-agent systems due to superior debuggability and
operational maturity over flat-mesh architectures.

```
              ┌─────────────────────────────────────┐
              │            ORCHESTRATOR              │
              │   (Goal Decomposition + Governance)  │
              └──┬────┬────┬────┬────┬────┬────┬───┘
                 │    │    │    │    │    │    │
              Planner │  Backend│   QA  Debug Security
                  Architect Frontend  DevOps Reporter
```

---

## 2. State Machine Lifecycle

The Orchestrator maintains an explicit state model. Never rely on LLM
context alone for state tracking.

```
IDLE ──► RECEIVING ──► PLANNING ──► DELEGATING ──► MONITORING
  ▲                                                      │
  └──────────────── DONE ◄──── SYNTHESIZING ◄───────────┘
                      │
              ERROR ──► ESCALATING (HITL)
```

| State | Description | Next States |
|-------|-------------|-------------|
| `IDLE` | Waiting for task | `RECEIVING` |
| `RECEIVING` | Parsing & validating input | `PLANNING`, `ERROR` |
| `PLANNING` | Breaking task into sub-tasks | `DELEGATING` |
| `DELEGATING` | Assigning tasks to agents | `MONITORING` |
| `MONITORING` | Tracking agent progress | `SYNTHESIZING`, `ERROR` |
| `SYNTHESIZING` | Merging agent outputs | `DONE` |
| `ESCALATING` | Awaiting human-in-the-loop | `DELEGATING`, `DONE` |

---

## 3. Memory Architecture

Use **Anchored Iterative Summarization** to prevent context drift.
Keep a fixed core context block + summarize historical data as session grows.

| Memory Type | Storage | TTL | Purpose |
|-------------|---------|-----|---------|
| **Short-term** | In-memory / Redis | Session | Current task context |
| **Working** | Redis | Task lifecycle | Active sub-task state |
| **Long-term** | PostgreSQL | Permanent | Project history, preferences |
| **Episodic** | Vector DB | Configurable | Raw event history |
| **Semantic** | pgvector / Mem0 | Permanent | Distilled facts & conclusions |

---

## 4. Task Delegation Protocol

Every task delegated to a sub-agent must follow this schema:

```json
{
  "task_id": "uuid-v4",
  "parent_task_id": "uuid-v4 | null",
  "from": "orchestrator",
  "to": "backend-agent",
  "type": "TASK | QUERY | CANCEL",
  "priority": "critical | high | normal | low",
  "payload": {},
  "success_criteria": "Explicit, measurable definition of done",
  "timeout_ms": 30000,
  "max_retries": 3,
  "hitl_required": false,
  "timestamp": "ISO-8601"
}
```

**Key principle**: Always provide explicit `success_criteria`. Agents do not
possess human common sense; ambiguity leads to incorrect outputs.

---

## 5. Governance & Guardrails

- **Cost limits**: Track token consumption per task chain. Hard-stop at budget.
- **HITL checkpoints**: Escalate when confidence < 0.75 or action is irreversible.
- **Retry policy**: Max 3 retries with exponential backoff (1s, 4s, 16s).
- **Isolation**: Never pass full conversation history to sub-agents. Inject only
  task-relevant context (context isolation principle).

---

## 6. Observability Requirements

Log every orchestration decision with:
- `trace_id` — unique per user request
- `span_id` — unique per agent interaction
- `decision_reason` — WHY this agent was chosen
- `token_cost` — tokens consumed in this hop
- `latency_ms` — execution time

---

## 7. Anti-Patterns to Avoid

| Anti-Pattern | Risk | Fix |
|---|---|---|
| Passing full chat history to sub-agents | Context overflow, performance degradation | Use context isolation |
| Relying on LLM for state tracking | Non-deterministic state | Use explicit state machines |
| Infinite retry loops | Runaway cost | Hard-stop at max_retries |
| No HITL for irreversible actions | Catastrophic failures | Add approval gates |
"""

# ─── 2. PLANNER AGENT ────────────────────────────────────────────────────────
CONTENT["planner-agent.md"] = """# Planner Agent

Translates high-level user goals into structured, verifiable implementation
plans. The Planner is the first agent activated after the Orchestrator
receives a task, and its output drives the entire execution chain.

---

## 1. Core Purpose

The Planner implements **Spec-Driven Development**: every task begins with a
machine-readable specification (`spec.md` artifact) that serves as the single
source of truth for all downstream agents.

---

## 2. Planning Architecture

Choose the right pattern based on task predictability:

| Pattern | When to Use | Mechanism |
|---------|-------------|-----------|
| **Plan-and-Execute** | Stable, linear workflows | Full roadmap before any action |
| **ReAct (Reasoning+Acting)** | Open-ended, high-uncertainty | Reason → Act → Observe loop |
| **Hybrid** | Complex projects (default) | Plan milestones, ReAct within each |

### ReAct Loop Diagram
```
GOAL
  │
  ▼
[THINK] What do I know? What's missing?
  │
  ▼
[ACT] Execute smallest verifiable step
  │
  ▼
[OBSERVE] Did it meet success criteria?
  │
  ├──► YES → Next step
  └──► NO  → [REPLAN] Adjust and retry
```

---

## 3. Hierarchical Decomposition

Break every goal into exactly two levels:

```
Level 1 — Milestones (5-7 max, business-level)
  └── Level 2 — Atomic Tasks (independently executable)
        └── Success Criteria (machine-parseable JSON)
```

### Atomic Task Schema

```json
{
  "task_id": "T-001",
  "milestone": "M-01: Setup Backend",
  "description": "Create User authentication endpoint",
  "agent": "backend-agent",
  "inputs": ["database schema", "API spec"],
  "outputs": ["POST /auth/login endpoint", "JWT token response"],
  "success_criteria": {
    "test_passes": ["test_login_valid_credentials", "test_login_invalid_returns_401"],
    "response_schema": "LoginResponse",
    "latency_p95_ms": 200
  },
  "dependencies": [],
  "estimated_tokens": 2000
}
```

---

## 4. Spec.md Format

Every plan must produce a `spec.md` artifact:

```markdown
# Spec: [Project Name]

## Goal
[Single sentence: what success looks like for the user]

## Constraints
- Budget: [token limit]
- Timeline: [deadline or sprint]
- Out of scope: [explicit exclusions]

## Milestones
| ID | Name | Agent | Estimated Effort |
|----|------|-------|-----------------|
| M-01 | ... | ... | ... |

## Acceptance Criteria
- [ ] Criterion 1 (measurable)
- [ ] Criterion 2 (testable)
```

---

## 5. Replanning Triggers

The Planner MUST replan when:
- A sub-task fails after max_retries
- Environment state changes significantly mid-execution
- Actual token cost exceeds estimate by >50%
- QA agent flags a critical defect in milestone output

---

## 6. Self-Correction Loop

```
Monitor milestone completion
    │
    ▼
Success criteria met? ──► YES ──► Mark complete, advance
    │
    NO
    │
    ▼
Root cause: plan ambiguity OR external failure?
    │
    ├── Plan ambiguity → Rewrite affected atomic tasks
    └── External failure → Escalate to Orchestrator (HITL)
```
"""

# ─── 3. ARCHITECT AGENT ──────────────────────────────────────────────────────
CONTENT["architect-agent.md"] = """# Architect Agent

Translates implementation plans into high-level system designs: component
boundaries, API contracts, data models, technology choices, and integration
patterns. The Architect's output is the blueprint all developer agents follow.

---

## 1. Core Purpose

The Architect ensures the system is built on solid engineering foundations
before a single line of code is written. All design decisions are documented
as **Architecture Decision Records (ADRs)**.

---

## 2. Core Design Patterns (2025-2026)

Apply the appropriate pattern per task type:

| Pattern | Mechanism | Best For |
|---------|-----------|----------|
| **ReAct** | Reason → Act → Observe loop | Exploratory design tasks |
| **Reflection** | Agent critiques its own output | Design reviews & refactoring |
| **Planning** | Hierarchical decomposition | Large system design |
| **Coordinator/Router** | Routes to specialized agents | Multi-domain systems |
| **Agent-as-Tool** | Sub-agents as stateless tools | Modular, composable systems |
| **Agentic RAG** | Memory-enhanced retrieval | Knowledge-intensive design |

---

## 3. Hexagonal Architecture (Default)

Isolate business logic from infrastructure to enable LLM provider swaps
and database migrations without breaking core reasoning.

```
┌─────────────────────────────────────────────┐
│               CORE DOMAIN                   │
│         (Business Logic / Use Cases)        │
├──────────────┬──────────────────────────────┤
│  INPUT PORTS │        OUTPUT PORTS          │
│  (API, CLI,  │  (DB, LLM Provider, Email,   │
│   Events)    │   External APIs)             │
└──────────────┴──────────────────────────────┘
```

---

## 4. API Contract Standards (Agent-Ready)

Traditional APIs are insufficient for autonomous agents. All APIs must be
**schema-first with rigid definitions**:

```yaml
# OpenAPI 3.1 — Agent-Ready Standard
paths:
  /tasks/{id}:
    get:
      operationId: getTaskById        # Required: unique, descriptive
      description: |                   # Required: explicit, no ambiguity
        Returns a single task by ID.
        Returns 404 if task does not exist.
        Never returns partial data.
      parameters:
        - name: id
          schema:
            type: string
            format: uuid               # Required: use formats, not just types
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Task'
```

**Agent Contract** — every API endpoint must declare:
```json
{
  "resource_budget": { "max_calls_per_minute": 60, "max_tokens": 4000 },
  "temporal_constraints": { "timeout_ms": 5000, "idempotent": true },
  "success_criteria": "Returns Task object with all required fields populated"
}
```

---

## 5. Model Context Protocol (MCP)

Use MCP as the standard for connecting agents to data sources and tools.
Provides governed, standardized agent-to-tool discovery:

```
Agent ──► MCP Client ──► MCP Server ──► Tool / Database / API
```

- All tool access goes through MCP — never direct, unrestricted access
- MCP Server enforces RBAC, field-level masking, rate limits
- Agents discover available tools via MCP, not hardcoded registries

---

## 6. Architecture Decision Record (ADR) Template

```markdown
# ADR-001: [Decision Title]

## Status: Proposed | Accepted | Deprecated

## Context
[Why is this decision needed? What problem does it solve?]

## Decision
[What was decided?]

## Consequences
### Positive
- [Benefit 1]

### Negative / Trade-offs
- [Trade-off 1]

## Alternatives Considered
- [Option A] — rejected because [reason]
```
"""

# ─── 4. BACKEND AGENT ────────────────────────────────────────────────────────
CONTENT["backend-agent.md"] = """# Backend Developer Agent

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
"""

# ─── 5. FRONTEND AGENT ───────────────────────────────────────────────────────
CONTENT["frontend-agent.md"] = """# Frontend Developer Agent

Builds user-facing interfaces: UI components, client-side state management,
responsive layouts, accessibility compliance, and performance optimization.

---

## 1. Core Purpose

The Frontend Agent implements **Component-Driven Development (CDD)**:
build and test components in isolation before assembling pages.

---

## 2. Component Development Workflow

```
Design Token System
    │
    ▼
Atomic Components (Button, Input, Badge)
    │
    ▼
Molecule Components (Form, Card, Modal)
    │
    ▼
Organism Components (Header, Sidebar, Dashboard)
    │
    ▼
Page Templates
    │
    ▼
Integration with Backend Agent APIs
```

---

## 3. State Management Strategy

| State Type | Solution | Example |
|------------|----------|---------|
| **Server state** | React Query / TanStack Query | API data, cache |
| **UI state** | useState / useReducer | Modal open, tab selection |
| **Global state** | Zustand / Jotai | Auth, theme, notifications |
| **URL state** | Search params | Filters, pagination |
| **Form state** | React Hook Form | Form inputs, validation |

**Agentic UI patterns**:
- **Optimistic updates**: Apply change immediately, revert on error
- **Skeleton loaders**: Show structure while data loads
- **Error boundaries**: Graceful degradation per component, not full-page crash
- **Streaming UI**: Show partial results as agent generates them

---

## 4. Performance Budget

| Metric | Target | Measurement |
|--------|--------|-------------|
| **LCP** (Largest Contentful Paint) | < 2.5s | Chrome DevTools |
| **FID** (First Input Delay) | < 100ms | Web Vitals |
| **CLS** (Cumulative Layout Shift) | < 0.1 | Web Vitals |
| **Bundle size (initial)** | < 200KB gzipped | Bundler analysis |
| **Time to Interactive** | < 3.5s | Lighthouse |

---

## 5. Accessibility Checklist (WCAG 2.2)

- [ ] All interactive elements keyboard-navigable
- [ ] Focus indicators visible (min 3:1 contrast ratio)
- [ ] All images have descriptive `alt` text
- [ ] Color is never the only means of conveying information
- [ ] Form fields have associated `<label>` elements
- [ ] Error messages are programmatically associated with fields
- [ ] Heading hierarchy is correct (h1 → h2 → h3, no skips)
- [ ] Touch targets minimum 44×44px on mobile

---

## 6. Responsive Breakpoint System

```css
/* Standard breakpoints */
--bp-xs:  480px;   /* Small phones */
--bp-sm:  640px;   /* Large phones */
--bp-md:  768px;   /* Tablets */
--bp-lg:  1024px;  /* Laptops */
--bp-xl:  1280px;  /* Desktops */
--bp-2xl: 1536px;  /* Large monitors */
```

**Mobile-first rule**: All styles default to mobile, use `min-width` queries.
"""

# ─── 6. QA AGENT ─────────────────────────────────────────────────────────────
CONTENT["qa-agent.md"] = """# QA & Testing Agent

Validates functional requirements through automated testing, validates agent
outputs with LLM-as-a-Judge, and ensures system reliability via chaos testing.

---

## 1. Core Purpose

The QA Agent implements a **4-tier testing pyramid** and uses
**end-state evaluation** (not turn-by-turn) for non-deterministic agent output.

---

## 2. Testing Pyramid

```
         ┌───────────────┐
         │  Chaos Tests  │  ← Agent coordination stability
         ├───────────────┤
         │  E2E Tests    │  ← Critical user journeys
         ├───────────────┤
         │  Integration  │  ← Agent-to-agent, API contracts
         ├───────────────┤
         │  Unit Tests   │  ← Individual functions, schemas
         └───────────────┘
```

| Tier | Coverage Target | Tools | CI Gate |
|------|----------------|-------|---------|
| Unit | ≥ 80% | pytest, jest | Block PR if < 80% |
| Integration | ≥ 60% | pytest, Postman | Block PR if < 60% |
| E2E | Critical paths | Playwright, Cypress | Block deploy if fails |
| Chaos | Key coordination | Custom injection | Weekly scheduled run |

---

## 3. LLM-as-a-Judge Framework

For non-deterministic agent output that cannot be validated with assertions:

```python
# Rubric-based evaluation schema
evaluation_rubric = {
    "factual_accuracy": {
        "weight": 0.35,
        "criteria": "All factual claims are verifiable and correct"
    },
    "instruction_following": {
        "weight": 0.30,
        "criteria": "Output addresses all requirements in the task spec"
    },
    "completeness": {
        "weight": 0.20,
        "criteria": "No required sections are missing"
    },
    "format_compliance": {
        "weight": 0.15,
        "criteria": "Output matches the declared output schema"
    }
}
# Score < 0.75 triggers automatic rerun. Score < 0.50 escalates to HITL.
```

---

## 4. Chaos Testing Protocol

Inject controlled failures to test MAS coordination stability:

| Injection Type | Target | Expected Behavior |
|----------------|--------|-------------------|
| Agent timeout | Any sub-agent | Orchestrator retries with backoff |
| Malformed output | Any agent response | Schema validator rejects, logs error |
| Memory poisoning | Shared context | Agents detect anomaly, request re-fetch |
| Cascading failure | 2+ agents fail simultaneously | System isolates, escalates to HITL |

**Run frequency**: Weekly in staging, before every major release.

---

## 5. Test Naming Convention

```
test_<unit>_<scenario>_<expected_outcome>

Examples:
test_login_valid_credentials_returns_200
test_login_invalid_password_returns_401
test_orchestrator_timeout_triggers_retry
test_planner_ambiguous_goal_requests_clarification
```

---

## 6. CI Integration

```yaml
# Required CI gates (block PR if failing)
- run: pytest tests/unit/ --cov=src --cov-fail-under=80
- run: pytest tests/integration/ --cov=src --cov-fail-under=60
- run: playwright test --project=chromium tests/e2e/critical/
```
"""

# ─── 7. DEBUG AGENT ──────────────────────────────────────────────────────────
CONTENT["debug-agent.md"] = """# Debug Agent

Investigates runtime errors, traces failures across agent chains, identifies
root causes, and proposes targeted hotfixes with rollback procedures.

---

## 1. Core Purpose

The Debug Agent specializes in **distributed tracing** and **silent failure
detection** — finding errors that cause incorrect outputs without throwing
exceptions (the hardest class of bugs in multi-agent systems).

---

## 2. Root Cause Analysis (RCA) Methodology

For every P0/P1 incident, apply this sequence:

```
1. CONTAIN     → Isolate the failing agent. Prevent cascading damage.
2. REPRODUCE   → Recreate the failure in a sandbox environment.
3. TRACE       → Follow the full execution trace (trace_id across all agents).
4. HYPOTHESIZE → Generate 3-5 candidate root causes (5 Whys + Fishbone).
5. VALIDATE    → Test each hypothesis against trace evidence.
6. FIX         → Implement targeted hotfix. Write regression test first.
7. VERIFY      → Run full test suite. Confirm fix in staging.
8. DOCUMENT    → Update incident log and post-mortem.
```

---

## 3. Incident Severity Matrix

| Level | Definition | Response Time | Action |
|-------|-----------|--------------|--------|
| **P0** | System down, data loss | < 15 min | Immediate HITL + rollback |
| **P1** | Critical feature broken | < 1 hour | Debug Agent activated |
| **P2** | Significant degradation | < 4 hours | Scheduled fix in next sprint |
| **P3** | Minor issue / cosmetic | < 1 week | Backlog |

---

## 4. Distributed Tracing

Every agent interaction generates a trace span:

```json
{
  "trace_id": "global-uuid-per-user-request",
  "span_id": "uuid-per-agent-hop",
  "parent_span_id": "uuid-of-calling-agent",
  "agent": "backend-agent",
  "operation": "createUser",
  "status": "error",
  "error_code": "ERR_SCHEMA_MISMATCH",
  "duration_ms": 142,
  "timestamp": "ISO-8601"
}
```

To reconstruct a failure: filter all spans by `trace_id`, sort by
`timestamp`, identify where `status: error` first appears.

---

## 5. Silent Failure Detection

The hardest failures: API returns 200 but output is corrupt or incorrect.

Detection patterns:
- **Schema drift**: Output structure changed without updating contract
- **Semantic corruption**: Values plausible but factually wrong (hallucination)
- **Context bleed**: Agent received wrong task context (isolation failure)
- **Partial completion**: Agent stopped mid-task without error signal

Detection method: Validate all agent outputs against declared schema
AND run LLM-as-a-Judge score. Score < 0.50 = silent failure alert.

---

## 6. Hotfix Classification

```
P0 Hotfix:  Direct patch → deploy to production (bypasses normal pipeline)
             Must include: regression test, rollback plan, incident report
P1 Hotfix:  Feature branch → expedited review → staging → production
P2+ Fix:    Normal sprint process
```
"""

# ─── 8. SECURITY AGENT ───────────────────────────────────────────────────────
CONTENT["security-agent.md"] = """# Security Agent

Audits the system for vulnerabilities using OWASP Agentic Top 10 (2026),
validates access controls, enforces CSP headers, and runs continuous
automated red teaming integrated into CI/CD.

---

## 1. Core Purpose

Traditional application security is insufficient for multi-agent systems.
The Security Agent applies the **OWASP Top 10 for Agentic Applications (2026)**
alongside classical OWASP LLM Top 10 and MITRE ATLAS.

---

## 2. OWASP Agentic Top 10 (2026)

| # | Risk | MAS-Specific Threat |
|---|------|---------------------|
| A01 | **Agent Goal Hijacking** | Attacker redirects agent's objective via crafted input |
| A02 | **Privilege Escalation via Delegation** | Low-privilege agent tricks high-privilege agent |
| A03 | **Tool Misuse** | Agent calls tools outside its authorized scope |
| A04 | **Memory Poisoning** | Shared context store is corrupted, affecting all agents |
| A05 | **Tool-Call Hijacking** | Malicious tool descriptions redirect agent actions |
| A06 | **Prompt Injection Propagation** | Injection spreads across agent chain |
| A07 | **Sensitive Information Disclosure** | Agent leaks PII/credentials in inter-agent messages |
| A08 | **Insecure Agent Supply Chain** | Compromised sub-agent or tool dependency |
| A09 | **Audit Log Bypass** | Agent actions not captured in audit trail |
| A10 | **Resource Exhaustion** | Agent enters infinite loop, exhausts compute/budget |

---

## 3. Tiered Enforcement Architecture

```
┌──────────────────────────────────────────────┐
│  INPUT LAYER                                 │
│  • Rate limiting & authentication            │
│  • Prompt injection detection                │
│  • Input schema validation                   │
├──────────────────────────────────────────────┤
│  ORCHESTRATION LAYER                         │
│  • Tool access RBAC (MCP enforcement)        │
│  • Agent scope constraints                   │
│  • HITL gates for high-risk operations       │
├──────────────────────────────────────────────┤
│  OUTPUT LAYER                                │
│  • Output schema validation                  │
│  • PII scrubbing before cross-agent relay    │
│  • Safety policy compliance check            │
└──────────────────────────────────────────────┘
```

---

## 4. Security Audit Checklist

### Per Agent
- [ ] Principle of least privilege: agent only accesses tools it needs
- [ ] Memory isolation: private context not shared without explicit permission
- [ ] All tool outputs treated as untrusted input (sanitized before re-use)
- [ ] HITL gate for every irreversible action (file delete, DB write, send email)
- [ ] Max token budget enforced to prevent resource exhaustion

### Per System
- [ ] Content Security Policy (CSP) header: `default-src 'self'; script-src 'self'`
- [ ] All agent-to-agent messages cryptographically signed
- [ ] Audit log captures: agent, action, timestamp, user context, trace_id
- [ ] Red team schedule: automated in CI + quarterly manual exercise

---

## 5. Architectural Red Teaming

Focus on **inter-agent injection chains**, not just single-agent attacks:

```
Attack Scenario: Retrieval → Execution Escalation
1. Inject malicious payload into document retrieved by Retrieval Agent
2. Retrieval Agent embeds payload in context sent to Execution Agent
3. Execution Agent interprets payload as trusted instruction
4. Unauthorized file deletion or data exfiltration occurs

Defense: Sanitize ALL retrieved content before injection into agent context
```

---

## 6. Compliance Mapping

| Requirement | Framework | Control |
|-------------|-----------|---------|
| Prompt Injection prevention | OWASP LLM01 | Input validation + sandboxing |
| Access control enforcement | OWASP A01:2021 | MCP RBAC |
| Audit trail | EU AI Act Art. 13 | Immutable trace logs |
| Data minimization | GDPR Art. 5 | Context isolation, PII scrubbing |
| Vulnerability management | MITRE ATLAS | Continuous red teaming in CI |
"""

# ─── 9. DEVOPS AGENT ─────────────────────────────────────────────────────────
CONTENT["devops-agent.md"] = """# DevOps & Infrastructure Agent

Manages CI/CD pipelines, Docker containerization, Kubernetes orchestration,
Infrastructure as Code, environment configuration, and deployment automation.

---

## 1. Core Purpose

The DevOps Agent implements the **Observe-Reason-Act** cycle for CI/CD:
observe system state → reason about optimal action → execute with approval gate.

---

## 2. CI/CD Pipeline Architecture

```
Code Push
    │
    ▼
┌─────────────────────────────────────────────┐
│  CI Stage: Validate                         │
│  • Lint (ruff, eslint)                      │
│  • Type check (mypy)                        │
│  • Unit tests (coverage gate: 80%)          │
│  • Security scan (SAST)                     │
│  • validate_skill.py                        │
├─────────────────────────────────────────────┤
│  CI Stage: Build                            │
│  • Docker build + push to registry         │
│  • Integration tests                        │
│  • E2E tests (critical paths)               │
├─────────────────────────────────────────────┤
│  CD Stage: Staging Deploy (auto)            │
│  • Blue-green deployment to staging         │
│  • Smoke tests                              │
│  • Performance benchmark vs baseline        │
├─────────────────────────────────────────────┤
│  CD Stage: Production Deploy (HITL gate)    │
│  • Human approval required ◄────────────── │
│  • Canary release (5% → 25% → 100%)        │
│  • Post-deploy verification                 │
└─────────────────────────────────────────────┘
```

---

## 2. GitOps Workflow

```
Developer pushes to feature branch
    │
    ▼
PR opened → CI validates
    │
    ▼
Merge to main → ArgoCD detects Git state change
    │
    ▼
ArgoCD syncs Kubernetes cluster to match desired state in Git
    │
    ▼
Cluster state = Git state (always)
```

**Rule**: The Git repository is the single source of truth for cluster state.
No manual `kubectl apply` in production. All changes go through Git.

---

## 3. Docker Standards

```dockerfile
# Required: multi-stage build for minimal attack surface
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.12-slim AS runtime
WORKDIR /app
# Run as non-root user (security requirement)
RUN useradd -r -u 1001 agentuser
COPY --from=builder /usr/local/lib/python3.12 /usr/local/lib/python3.12
COPY . .
USER agentuser
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0"]
```

---

## 4. Kubernetes RBAC for Agents

**Hard rule**: Agents NEVER get `cluster-admin`. Use minimal RBAC.

```yaml
# Example: Backend Agent ServiceAccount
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: backend-agent-role
  namespace: production
rules:
- apiGroups: [""]
  resources: ["configmaps", "secrets"]
  verbs: ["get", "list"]        # Read-only on secrets
- apiGroups: ["apps"]
  resources: ["deployments"]
  verbs: ["get", "list", "watch"]  # No create/delete
```

---

## 5. Canary Release Procedure

```
Step 1: Deploy new version to 5% of traffic
Step 2: Monitor error rate & latency for 15 minutes
    → Error rate > 1% or p95 latency up > 20%: ROLLBACK
    → Metrics healthy: advance to step 3
Step 3: 25% traffic → monitor 15 min → advance or rollback
Step 4: 100% traffic → full deployment complete
Step 5: Run post-deploy verification checklist
```
"""

# ─── 10. REPORTER AGENT ──────────────────────────────────────────────────────
CONTENT["reporter-agent.md"] = """# Reporter Agent

Generates changelogs, release notes, sprint summaries, and keeps all
public-facing documentation in sync with the actual codebase state.

---

## 1. Core Purpose

The Reporter Agent closes the documentation gap that exists in most software
projects. It automates the boring parts of documentation and detects
**documentation drift** — when docs no longer match the code.

---

## 2. Changelog Generation

Follows **Conventional Commits** standard for automated changelog generation:

```
feat(auth): add JWT refresh token support      → Minor version bump
fix(api): correct 404 response schema          → Patch version bump
feat!: breaking change in User schema          → Major version bump
docs(readme): update installation steps        → No version bump
```

**Automated changelog entry format**:
```markdown
## [2.1.0] - 2026-07-05

### Added
- feat(auth): JWT refresh token with 7-day sliding window expiry (#142)
- feat(planner): hierarchical task decomposition with JSON output (#138)

### Fixed
- fix(orchestrator): context bleed between concurrent task sessions (#145)

### Breaking Changes
- feat!: User.email is now required at registration (#140)
```

---

## 3. Release Notes Template

```markdown
# Release: v[VERSION] — [CODENAME]

**Released**: [DATE]
**Summary**: [1-2 sentence executive summary]

## Highlights
- [Most important improvement for users]
- [Second most important]

## What's New
[Feature-focused description, no implementation details]

## Bug Fixes
[User-visible fixes only]

## Migration Guide
[Required only for breaking changes]

## Known Issues
[Documented, not yet fixed]
```

---

## 4. Documentation Drift Detection

Check for drift on every CI run:

```python
# Detects when API endpoints exist in code but not in docs
def check_api_documentation_coverage():
    code_endpoints = extract_endpoints_from_codebase()
    doc_endpoints = extract_endpoints_from_openapi_spec()
    undocumented = code_endpoints - doc_endpoints
    if undocumented:
        raise DriftError(f"Undocumented endpoints: {undocumented}")
```

---

## 5. Sprint Retrospective Template

```markdown
# Sprint [N] Retrospective — [DATE]

## Metrics
| Metric | Target | Actual |
|--------|--------|--------|
| Story Points Completed | [N] | [N] |
| Bug Escape Rate | < 5% | [%] |
| Test Coverage | ≥ 80% | [%] |

## What Went Well
-

## What Needs Improvement
-

## Action Items
| Action | Owner | Due Date |
|--------|-------|----------|
| | | |
```
"""

# ─── 11. AGENT COMMUNICATION ─────────────────────────────────────────────────
CONTENT["agent-communication.md"] = """# Agent Communication Protocol

Defines how agents exchange messages: payload schemas, event types, error
codes, retry policies, and security requirements for all inter-agent
communication.

---

## 1. Core Principles

1. **Loose coupling**: Agents communicate ONLY via Orchestrator — no direct peer-to-peer calls
2. **Schema-first**: Every message validated against JSON schema before processing
3. **Idempotent**: Every message can be safely redelivered without duplicate effects
4. **Traceable**: Every message carries `trace_id` and `span_id`

---

## 2. Task Message Schema

```json
{
  "$schema": "https://super-agent/schemas/v2/task-message.json",
  "task_id": "uuid-v4",
  "parent_task_id": "uuid-v4 | null",
  "trace_id": "uuid-v4",
  "span_id": "uuid-v4",
  "from": "orchestrator | planner-agent | architect-agent | ...",
  "to": "backend-agent | frontend-agent | ...",
  "type": "TASK",
  "priority": "critical | high | normal | low",
  "payload": {},
  "success_criteria": "Explicit, measurable string",
  "context": {
    "relevant_history": [],
    "project_id": "uuid-v4",
    "sprint_id": "string | null"
  },
  "constraints": {
    "timeout_ms": 30000,
    "max_retries": 3,
    "token_budget": 4000
  },
  "hitl_required": false,
  "timestamp": "ISO-8601"
}
```

---

## 3. Result Message Schema

```json
{
  "task_id": "uuid-v4",
  "trace_id": "uuid-v4",
  "span_id": "uuid-v4",
  "from": "backend-agent",
  "to": "orchestrator",
  "type": "RESULT",
  "status": "success | error | partial | escalated",
  "result": {},
  "confidence": 0.95,
  "tokens_used": 1250,
  "duration_ms": 3420,
  "errors": [],
  "timestamp": "ISO-8601"
}
```

---

## 4. Error Code Taxonomy

| Code | Category | Retryable | Action |
|------|----------|-----------|--------|
| `ERR_SCHEMA_MISMATCH` | Input | No | Fix input schema |
| `ERR_TIMEOUT` | Infrastructure | Yes | Retry with backoff |
| `ERR_BUDGET_EXCEEDED` | Resource | No | Escalate to HITL |
| `ERR_ESCALATION` | Governance | No | Await human approval |
| `ERR_DOWNSTREAM` | External | Yes | Retry with backoff |
| `ERR_CONTEXT_BLEED` | Security | No | Reset context, retry |
| `ERR_MEMORY_CORRUPT` | Memory | No | Re-fetch from source |
| `ERR_AGENT_UNAVAILABLE` | Infrastructure | Yes | Route to backup agent |

---

## 5. Retry Policy

```
Attempt 1: Immediate
Attempt 2: +1 second delay
Attempt 3: +4 seconds delay
Attempt 4: +16 seconds delay (final)
Max total wait: ~21 seconds
After max retries: ERR_ESCALATION → HITL
```

**Jitter**: Add ±20% random jitter to prevent thundering herd on simultaneous failures.

---

## 6. Context Isolation Protocol

To prevent **context bleed** (agent A's context corrupting agent B):

- Each agent receives only task-relevant context, never full conversation history
- Context passed per-task, not per-session
- Shared memory accessed via explicit read operation, not automatic injection
- All cross-agent context transfers logged with `span_id` for auditability
"""

# ─── 12. PROJECT MEMORY ──────────────────────────────────────────────────────
CONTENT["project-memory.md"] = """# Project Memory System

Specifies how agents share, persist, and retrieve state across tasks,
sessions, and long-running workflows. Implements the Hybrid Memory Architecture.

---

## 1. Core Architecture: Hybrid Pattern

The industry-standard approach for production MAS (2026):

```
┌─────────────────────────────────────────────────────┐
│                 HYBRID MEMORY                       │
├──────────────────────┬──────────────────────────────┤
│  PRIVATE MEMORY      │  SHARED GLOBAL STORE         │
│  (per-agent)         │  (curated, access-controlled)│
│  • Task-specific     │  • Project facts              │
│  • Local reasoning   │  • User preferences           │
│  • Not shared        │  • Completed task summaries  │
└──────────────────────┴──────────────────────────────┘
```

---

## 2. Tiered Memory Taxonomy

| Tier | Type | Storage | TTL | Content |
|------|------|---------|-----|---------|
| **Episodic** | Raw event history | PostgreSQL | Configurable | Full trace logs, raw outputs |
| **Semantic** | Distilled facts | pgvector / Mem0 | Permanent | Conclusions, heuristics |
| **Procedural** | Encoded skills | SKILL.md files | Version-controlled | Agent behaviors |
| **Working** | Active task context | Redis | Task lifecycle | Current task state |
| **Short-term** | Session context | Redis | Session TTL | Conversation history |

---

## 3. Reflective Consolidation

Agents periodically review history to extract patterns and "forget" noise:

```python
# Consolidation trigger: every 20 tasks or at session end
def consolidate_memory(agent_id: str, episodes: list[Episode]) -> SemanticFact:
    \'\'\'
    1. Summarize raw episodes into key learnings
    2. Extract reusable heuristics ("User prefers concise explanations")
    3. Discard redundant or contradicted information
    4. Store distilled fact in Semantic tier
    5. Archive raw episodes (do not delete - needed for audits)
    \'\'\'
```

---

## 4. LangGraph Checkpointing

For long-running workflows that must survive infrastructure failures:

```python
from langgraph.checkpoint.postgres import PostgresSaver

# Checkpoint every state transition
checkpointer = PostgresSaver.from_conn_string(DATABASE_URL)
graph = workflow.compile(checkpointer=checkpointer)

# Resume interrupted workflow
result = graph.invoke(
    input=None,  # Resume from checkpoint
    config={"configurable": {"thread_id": "workflow-uuid"}}
)
```

**Rule**: Any workflow longer than 30 seconds MUST use checkpointing.

---

## 5. Access Control Model

Memory access follows the principle of least privilege:

```
User ──► Agent A: can read User's own memory only
Agent A ──► Agent B: can share task-specific context only (not full memory)
Orchestrator: can read all agent memories (audit/debug only)
External: no access to any agent memory
```

---

## 6. Memory Hygiene Rules

- Sensitive data (PII, credentials) NEVER stored in agent memory
- All memory writes logged with `agent_id`, `timestamp`, `operation`
- Memory entries older than TTL automatically purged (configurable)
- Poisoning detection: validate memory entries against expected schema on read
"""

# ─── 13. WORKFLOW ─────────────────────────────────────────────────────────────
CONTENT["workflow.md"] = """# System Workflow

End-to-end pipeline from user request intake through planning, implementation,
testing, deployment, and reporting. Includes HITL checkpoints and error paths.

---

## 1. High-Level Pipeline

```
User Request
    │
    ▼
┌──────────────┐
│ Orchestrator │ ── validates input schema
│ (RECEIVING)  │ ── initializes trace_id
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   Planner    │ ── decomposes goal into spec.md
│   Agent      │ ── generates atomic task list
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Architect   │ ── designs system structure
│    Agent     │ ── produces ADRs + API contracts
└──────┬───────┘
       │ (parallel execution)
       ├──────────────────┬─────────────────┐
       ▼                  ▼                 ▼
┌─────────────┐  ┌───────────────┐  ┌──────────────┐
│   Backend   │  │   Frontend    │  │   Security   │
│    Agent    │  │     Agent     │  │    Agent     │
└──────┬──────┘  └───────┬───────┘  └──────┬───────┘
       └──────────────────┴─────────────────┘
                          │
                          ▼
               ┌──────────────────┐
               │    QA Agent      │ ── runs all test tiers
               └──────┬───────────┘
                      │
          ┌───────────┴───────────┐
          │ pass?                 │ fail?
          ▼                       ▼
  ┌──────────────┐       ┌─────────────────┐
  │ DevOps Agent │       │   Debug Agent   │
  │  (Staging)   │       │ (RCA + Hotfix)  │
  └──────┬───────┘       └────────┬────────┘
         │                        │ (loop back to QA)
  HITL GATE ◄───────────────────── │
  (Human approval)
         │
         ▼
  ┌──────────────┐
  │ DevOps Agent │ ── canary release
  │ (Production) │ ── post-deploy verify
  └──────┬───────┘
         │
         ▼
  ┌──────────────┐
  │   Reporter   │ ── changelog, release notes
  │    Agent     │ ── docs sync
  └──────────────┘
```

---

## 2. HITL Checkpoint Policy

Human approval is REQUIRED before:
- Deploying to production
- Any database schema migration
- Deleting data (any volume)
- Exceeding defined token/cost budget
- Any action flagged by Security Agent as high-risk

---

## 3. Parallel vs Sequential Execution

| Phase | Execution | Rationale |
|-------|-----------|-----------|
| Planner → Architect | Sequential | Architect needs full plan |
| Backend + Frontend + Security | Parallel | Independent workstreams |
| QA | Sequential (after builders) | Needs completed output |
| Debug (if needed) | Sequential | Blocking for QA |
| DevOps Staging | Sequential (after QA pass) | Gate-dependent |
| HITL Review | Sequential | Mandatory human step |
| DevOps Production | Sequential (after HITL) | Gate-dependent |
| Reporter | Parallel (post-deploy) | Non-blocking |

---

## 4. SLA & Timeout Matrix

| Stage | Timeout | Action if Exceeded |
|-------|---------|-------------------|
| Planning | 60s | Replan with simpler decomposition |
| Architecture | 120s | Escalate to HITL |
| Backend/Frontend | 300s | Debug Agent activated |
| QA | 600s | CI fails, notify DevOps |
| DevOps Deploy | 180s | Auto-rollback |
| Post-deploy verify | 60s | Rollback if verify fails |
"""

# ─── 14. PROJECT RULES ────────────────────────────────────────────────────────
CONTENT["project-rules.md"] = """# Project Rules

Foundational rules that govern all agents and contributors working in this
system. These are non-negotiable constraints, not guidelines.

---

## 1. The 10 Hard Rules

These rules CANNOT be violated under any circumstances:

1. **Single Responsibility**: Each agent does exactly one thing. No agent
   handles tasks outside its defined scope.

2. **Explicit State Contracts**: All shared data objects use typed schemas
   (Pydantic models). No untyped `dict` or `Any` in agent interfaces.

3. **Context Isolation**: Agents never receive full conversation history.
   Each receives only task-relevant context.

4. **HITL for Irreversible Actions**: No irreversible action (delete, deploy,
   send) executes without explicit human approval.

5. **Schema-First APIs**: Every API endpoint has an OpenAPI definition before
   any implementation begins.

6. **Test Before Merge**: No code merges to main without passing unit tests
   (≥80% coverage) and integration tests (≥60% coverage).

7. **Immutable Audit Logs**: Every agent action is logged with trace_id,
   timestamp, and agent identity. Logs cannot be modified or deleted.

8. **No Direct Agent-to-Agent Calls**: All inter-agent communication goes
   through the Orchestrator. No peer-to-peer shortcuts.

9. **Fail Safe, Not Silent**: Agents must return structured error responses.
   Silent failures (returning empty/incorrect output without error) are
   treated as P1 incidents.

10. **Budget Enforcement**: Every task has a token budget. Agents stop and
    escalate when budget is reached. No unlimited execution.

---

## 2. Code Review Checklist

Apply to all PRs (human or AI-generated):

- [ ] Single responsibility maintained?
- [ ] All inputs/outputs have typed schemas?
- [ ] New endpoints added to OpenAPI spec?
- [ ] Unit tests cover new code (≥80%)?
- [ ] No hardcoded secrets or credentials?
- [ ] Error handling returns structured `AgentError`?
- [ ] Logging added with `trace_id`?
- [ ] Documentation updated?

---

## 3. Naming Conventions

```
Files:          kebab-case.py           agent-communication.md
Classes:        PascalCase              OrchestratorAgent
Functions:      snake_case              delegate_task()
Variables:      snake_case              task_payload
Constants:      UPPER_SNAKE_CASE        MAX_RETRIES = 3
Test functions: test_<unit>_<scenario>_<expected>
```

**Rule**: Names must be distinctive and grep-safe. Never use single-letter
variables or abbreviations that require context to interpret.

---

## 4. Branching Strategy

```
main        → Production-ready code. Protected. Requires PR + review.
staging     → Pre-production. Auto-deployed. CI gates enforced.
feat/*      → Feature branches. Merged to main via PR.
fix/*       → Bug fix branches. Expedited review for P0/P1.
chore/*     → Maintenance. No functional changes.
```
"""

# ─── 15. SYSTEM OVERVIEW ──────────────────────────────────────────────────────
CONTENT["system-overview.md"] = """# System Overview

High-level description of the multi-agent system: its goals, capabilities,
technology stack, design philosophy, and architectural decisions.

---

## 1. What This System Does

A production-grade multi-agent software engineering system that autonomously
plans, implements, tests, deploys, and documents software — with human
oversight at critical decision points.

**Core value**: Reduce time from user goal to production-ready software
by 60-80% through intelligent agent delegation while maintaining high
quality standards and full auditability.

---

## 2. System Capabilities

| Capability | Description | Agent |
|------------|-------------|-------|
| **Goal Analysis** | Parse vague goals into structured specs | Planner |
| **System Design** | Architecture, APIs, data models | Architect |
| **Backend Development** | REST APIs, business logic, DB schemas | Backend |
| **Frontend Development** | UI components, state management | Frontend |
| **Automated Testing** | Unit, integration, E2E, chaos tests | QA |
| **Bug Investigation** | RCA, distributed tracing, hotfixes | Debug |
| **Security Auditing** | OWASP compliance, red teaming | Security |
| **Infrastructure** | CI/CD, Docker, Kubernetes, GitOps | DevOps |
| **Documentation** | Changelogs, release notes, drift detection | Reporter |

---

## 3. Technology Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| **Orchestration** | LangGraph | Stateful graphs, checkpointing, HITL |
| **Backend API** | FastAPI | Async, type-safe, OpenAPI auto-gen |
| **Agent Memory** | Redis + pgvector + PostgreSQL | Tiered: fast → semantic → durable |
| **Tool Protocol** | MCP | Governed agent-to-tool access |
| **Containers** | Docker + Kubernetes | Isolation, scalability, GitOps |
| **CI/CD** | GitHub Actions + ArgoCD | Automated pipeline + GitOps sync |
| **Observability** | OpenTelemetry + Grafana | Distributed tracing |
| **Testing** | pytest + Playwright + LangSmith | Full test stack |

---

## 4. Architecture Decision Records

Key decisions made during system design:

| ADR | Decision | Rationale |
|-----|----------|-----------|
| ADR-001 | Hub-and-Spoke over Flat Mesh | Superior debuggability in production |
| ADR-002 | LangGraph over CrewAI | Explicit state machines + checkpointing |
| ADR-003 | FastAPI over Flask | Native async + Pydantic + OpenAPI |
| ADR-004 | Hybrid Memory Architecture | Balance consistency vs scalability |
| ADR-005 | MCP for tool access | Standardized governance |

---

## 5. Scalability Principles

- Start with 3-5 agents; add new agents only based on measured performance gaps
- Each agent is independently scalable (containerized, stateless reasoning)
- State lives externally (Redis/PostgreSQL) — never inside agent process
- Add agents when: coordination overhead < productivity gain from specialization
"""

# ─── 16. ARCHITECTURE ─────────────────────────────────────────────────────────
CONTENT["architecture.md"] = """# System Architecture

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
"""

# ─── 17. REPOSITORY STRUCTURE ─────────────────────────────────────────────────
CONTENT["repository-structure.md"] = """# Repository Structure

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
"""

# ─── 18. CODING STANDARDS ─────────────────────────────────────────────────────
CONTENT["coding-standard.md"] = """# Coding Standards

Style guidelines, naming conventions, linting configuration, and quality
gates for all code in this project. Optimized for both human readability
and AI agent code navigation.

---

## 1. Agent-Centric Clean Code Principles (2026)

Clean code in multi-agent systems prioritizes **machine readability** alongside
human readability:

1. **Distinctiveness**: Names must be unique and grep-safe. Agents navigate
   codebases via text search — ambiguous names cause incorrect retrieval.

2. **Explicit over Implicit**: Type hints on every function. No inference.
   Agents use type signatures to understand intent without reading bodies.

3. **State Contracts**: All shared data objects use Pydantic models.
   Never pass raw `dict` between modules or agents.

4. **Single Exit Point**: Functions have one return path where possible.
   Multiple early returns confuse agent code generation.

5. **Self-Documenting Interfaces**: Function names + type hints should make
   intent clear without needing docstrings for routine functions.

---

## 2. Python Standards

```python
# REQUIRED: All function signatures fully typed
def delegate_task(
    task: TaskMessage,
    target_agent: AgentIdentifier,
    timeout_ms: int = 30_000,
) -> TaskResult:
    '''
    Delegates a task to the specified agent.

    Args:
        task: Fully validated TaskMessage with success_criteria
        target_agent: Enum identifying the target agent
        timeout_ms: Hard timeout in milliseconds (default: 30s)

    Returns:
        TaskResult with status, result payload, and metrics

    Raises:
        AgentTimeoutError: If agent does not respond within timeout_ms
        SchemaValidationError: If task payload fails schema validation
    '''
```

---

## 3. Linting Stack

```toml
# pyproject.toml — required configuration
[tool.ruff]
line-length = 88
select = ["E", "F", "I", "N", "UP", "S", "ANN"]
# E: pycodestyle errors
# F: pyflakes
# I: isort
# N: naming conventions
# UP: pyupgrade
# S: bandit security
# ANN: type annotation enforcement

[tool.mypy]
strict = true
disallow_any_untyped_defs = true
disallow_incomplete_defs = true

[tool.ruff.per-file-ignores]
"tests/**" = ["S101"]  # Allow assert in tests
```

---

## 4. Pre-Commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: ruff-lint
        name: Ruff Lint
        entry: ruff check --fix
        language: system
        types: [python]

      - id: mypy-check
        name: MyPy Type Check
        entry: mypy
        language: system
        types: [python]

      - id: pytest-fast
        name: Fast Unit Tests
        entry: pytest tests/unit/ -q --tb=short
        language: system
```

---

## 5. Anti-Patterns (Strictly Prohibited)

| Anti-Pattern | Example | Correct Approach |
|---|---|---|
| Magic numbers | `if retries > 3:` | `if retries > MAX_RETRIES:` |
| Untyped function | `def process(data):` | `def process(data: TaskMessage) -> Result:` |
| Raw dict in API | `return {"status": "ok"}` | `return StatusResponse(status="ok")` |
| Print debugging | `print(result)` | `logger.info("result", extra={"result": result})` |
| Broad except | `except Exception:` | `except AgentTimeoutError, SchemaValidationError:` |
| Inline comments explaining HOW | `# loop 3 times` | Use variable names to self-document |
"""

# ─── 19. TESTING STANDARDS ────────────────────────────────────────────────────
CONTENT["testing-standard.md"] = """# Testing Standards

Requirements for unit tests, integration tests, E2E tests, chaos testing,
and LLM evaluation. Defines coverage thresholds and CI gates.

---

## 1. Coverage Matrix

| Tier | Minimum Coverage | CI Action if Below | Measurement Tool |
|------|-----------------|-------------------|-----------------|
| Unit | 80% | Block PR | pytest-cov |
| Integration | 60% | Block PR | pytest-cov |
| E2E | Critical paths | Block deploy | Playwright |
| Chaos | Defined scenarios | Weekly report | Custom |
| LLM Eval | Score ≥ 0.75 | Block task completion | LangSmith / custom |

---

## 2. Test Naming Convention

```
test_<unit>_<scenario>_<expected_outcome>

Unit      = the thing being tested (module/function/class)
Scenario  = the specific condition or input
Expected  = the expected behavior or result

Examples:
  test_orchestrator_timeout_triggers_retry
  test_planner_ambiguous_goal_requests_clarification
  test_backend_agent_invalid_schema_returns_422
  test_security_injection_attempt_blocked
```

---

## 3. Unit Test Requirements

```python
# REQUIRED structure for all unit tests
class TestOrchestratorDelegation:
    '''Tests for Orchestrator task delegation logic.'''

    def test_delegate_task_valid_input_returns_task_id(
        self, orchestrator: Orchestrator, mock_planner: MockAgent
    ):
        # Arrange
        task = TaskMessage(
            task_id=uuid4(),
            to="planner-agent",
            payload={"goal": "Build login feature"},
            success_criteria="Returns spec.md with milestones"
        )

        # Act
        result = orchestrator.delegate_task(task, AgentIdentifier.PLANNER)

        # Assert
        assert result.status == "success"
        assert result.task_id == task.task_id
        mock_planner.receive.assert_called_once_with(task)

    def test_delegate_task_timeout_raises_agent_timeout_error(self, ...):
        ...
```

---

## 4. Integration Test Requirements

```python
# Integration tests use real services (Docker Compose test environment)
@pytest.mark.integration
class TestAgentCommunicationProtocol:

    def test_orchestrator_to_planner_valid_task_returns_spec(self, client):
        response = client.post("/tasks", json={
            "goal": "Add user authentication",
            "priority": "high"
        })
        assert response.status_code == 202
        task = response.json()
        # Poll for completion (or use WebSocket for real-time)
        result = wait_for_task(task["task_id"], timeout=30)
        assert result["status"] == "success"
        assert "spec.md" in result["result"]
```

---

## 5. Chaos Test Scenarios

| Scenario | Injection Method | Expected System Behavior |
|----------|-----------------|-------------------------|
| Agent timeout | Delay response by 60s | Orchestrator retries 3x, then HITL |
| Malformed output | Return wrong schema | Schema validator rejects, error logged |
| Memory poisoning | Corrupt Redis key | Agent re-fetches from source, logs alert |
| Budget exhaustion | Consume max tokens | Hard stop, ERR_BUDGET_EXCEEDED returned |
| Cascade failure | Kill 2 agents simultaneously | Remaining agents complete, HITL escalation |

---

## 6. LLM Evaluation Rubric

```python
# Applied to all non-deterministic agent outputs
EVALUATION_RUBRIC = {
    "factual_accuracy":      {"weight": 0.35, "pass_threshold": 0.8},
    "instruction_following": {"weight": 0.30, "pass_threshold": 0.9},
    "completeness":          {"weight": 0.20, "pass_threshold": 0.7},
    "format_compliance":     {"weight": 0.15, "pass_threshold": 1.0},
}
# Weighted average < 0.75: task rerun automatically
# Weighted average < 0.50: escalate to HITL
```
"""

# ─── 20. DEPLOYMENT ──────────────────────────────────────────────────────────
CONTENT["deployment.md"] = """# Deployment Procedures

Step-by-step guide for staging and production deployments, pre-deploy
checklists, rollback procedures, and post-deploy verification.

---

## 1. Pre-Deploy Checklist

Complete ALL items before any production deployment:

### Code Quality
- [ ] All CI tests passing on main branch
- [ ] Code coverage ≥ 80% (unit), ≥ 60% (integration)
- [ ] Security scan clean (SAST + dependency audit)
- [ ] `validate_skill.py` passing

### Database
- [ ] All migration scripts tested against staging DB clone
- [ ] Rollback migration script tested and ready
- [ ] DB backup completed within last 4 hours

### Infrastructure
- [ ] Docker images tagged with semver (not `latest`)
- [ ] Kubernetes manifests reviewed for resource limits
- [ ] Secrets rotated if required by this release
- [ ] Load balancer health checks configured

### Communication
- [ ] Stakeholders notified of maintenance window
- [ ] On-call engineer designated for 2 hours post-deploy
- [ ] Rollback decision owner identified

---

## 2. Blue-Green Deployment Procedure

```
Step 1: Deploy new version to "Green" environment
        (runs alongside current "Blue" production)

Step 2: Run smoke tests against Green
        → Pass: proceed to step 3
        → Fail: debug in Green, Blue continues serving traffic

Step 3: Switch load balancer to route 5% traffic to Green (canary)
        → Monitor for 15 minutes (error rate, latency, business KPIs)
        → Error rate > 1%: switch back to Blue, investigate

Step 4: Gradually increase traffic: 5% → 25% → 50% → 100%
        → Monitor at each increment (15 min)

Step 5: Decommission Blue after 24 hours (keep as immediate rollback)
```

---

## 3. Rollback Runbook

**Trigger**: Error rate > 1% OR P95 latency increases > 20% post-deploy

```bash
# Immediate rollback (< 2 minutes)
# Step 1: Switch load balancer back to Blue
kubectl patch service api-gateway \
  -p '{"spec":{"selector":{"version":"blue"}}}'

# Step 2: Verify rollback is active
kubectl get endpoints api-gateway
curl https://api.example.com/health  # Should return 200

# Step 3: Notify team
echo "ROLLBACK COMPLETE: reverted to v$(cat .previous-version)"

# Step 4: Database rollback (if schema changed)
alembic downgrade -1
```

---

## 4. Post-Deploy Verification Checklist

Run within 30 minutes of production deployment:

- [ ] Health endpoint returns 200: `GET /health`
- [ ] Authentication flow working: login + token refresh
- [ ] Core agent endpoint responding: `POST /tasks`
- [ ] Database writes successful (create test record, verify, delete)
- [ ] Redis accessible (set/get test key)
- [ ] Error rate < 0.1% (last 15 min)
- [ ] P95 latency within 10% of pre-deploy baseline
- [ ] No new error types in logs

---

## 5. Incident Severity & Escalation

| P Level | Criteria | Response Time | Escalation |
|---------|----------|---------------|-----------|
| P0 | System down / data loss | Immediate | CTO + on-call |
| P1 | Critical feature broken | < 15 min | On-call + team lead |
| P2 | Significant degradation | < 1 hour | On-call |
| P3 | Minor issue | Next business day | Team backlog |
"""

# ─── 21. ROADMAP ─────────────────────────────────────────────────────────────
CONTENT["roadmap.md"] = f"""# Product Roadmap

Short-term (current sprint), mid-term (next quarter), and long-term vision
for the super-agent multi-agent system.

---

## 1. Current Sprint (Q3 2026)

| Milestone | Features | Success Metric | Status |
|-----------|----------|----------------|--------|
| **Foundation Complete** | All 21 docs generated, scripts/ and assets/ added | CI passing ✅ | In Progress |
| **Content Quality** | All docs have production-grade content | 0 placeholder text | In Progress |
| **Publish Ready** | README, LICENSE, CONTRIBUTING.md | Stars on GitHub | Pending |

---

## 2. Next Quarter (Q4 2026)

| Milestone | Features | Success Metric |
|-----------|----------|----------------|
| **Agent Templates** | Python starter templates for each agent role | Community adoption |
| **Interactive Generator** | CLI wizard for custom list.md | 100+ clones/month |
| **Multi-language Support** | TypeScript/JS generate_docs equivalent | 20+ contributors |
| **Integration Guides** | Cursor, Copilot, Claude Code setup guides | Compatibility matrix |

---

## 3. Long-term Vision (2027+)

| Vision | Description |
|--------|-------------|
| **Skill Marketplace** | Community-contributed skills with quality ratings |
| **Auto-update Engine** | Skills auto-update from authoritative sources (OWASP, etc.) |
| **Agent Interop Standard** | Formal spec for cross-platform skill compatibility |
| **Visual Skill Builder** | GUI for creating skills without editing markdown |

---

## 4. Technical Debt Backlog

| Item | Priority | Effort | Notes |
|------|----------|--------|-------|
| Improve generate_docs.py test coverage | Medium | Small | Add unit tests |
| Add YAML schema validation for list.md | Medium | Small | Prevent malformed entries |
| Internationalize all docs (EN + ID) | Low | Large | Start with README only |

---

## 5. Research Backlog

Areas to explore for future skill versions:

- [ ] Integration with LangGraph memory checkpointing examples
- [ ] Automated skill health monitoring (skill drift detection)
- [ ] Fine-tuned models for each agent role specialization
- [ ] Formal verification of agent communication protocols

---

*Last updated: {TODAY}*
"""

# ─────────────────────────────────────────────────────────────────────────────
# GENERATOR ENGINE
# ─────────────────────────────────────────────────────────────────────────────

def read_list(list_file: str) -> list:
    if not os.path.exists(list_file):
        print(f"[ERROR] {list_file} not found.")
        sys.exit(1)
    files = []
    with open(list_file, "r", encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()
            if stripped and not stripped.startswith("#"):
                files.append(stripped)
    return files


def generate(files: list, overwrite: bool, dry_run: bool):
    created, skipped, failed = [], [], []
    mode = "[DRY RUN] " if dry_run else ""
    print(f"\n{mode}Starting generation of {len(files)} files...\n")

    for filename in files:
        filepath = os.path.join(BASE_DIR, filename)

        if os.path.exists(filepath) and not overwrite:
            print(f"  ⏭  Skipped (exists): {filename}")
            skipped.append(filename)
            continue

        content = CONTENT.get(filename)
        if not content:
            # Fallback for any file not in registry
            title = filename.replace(".md", "").replace("-", " ").title()
            content = f"# {title}\n\n*Documentation for {title} in the super-agent system.*\n"

        if dry_run:
            lines = content.strip().count("\n") + 1
            print(f"  📄 Would create: {filename} ({lines} lines)")
            created.append(filename)
            continue

        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content.strip() + "\n")
            print(f"  ✅ Created: {filename}")
            created.append(filename)
        except Exception as e:
            print(f"  ❌ Failed: {filename} — {e}")
            failed.append(filename)

    print(f"\n{'─' * 52}")
    print(f"  ✅ {'Would create' if dry_run else 'Created'} : {len(created)} files")
    print(f"  ⏭  Skipped         : {len(skipped)} files")
    if failed:
        print(f"  ❌ Failed          : {len(failed)} files")
    print(f"{'─' * 52}")
    if not dry_run and not failed:
        print("\n🎉 All done! Your overpower multi-agent documentation is ready.\n")


def main():
    parser = argparse.ArgumentParser(
        description="super-agent Overpower Documentation Generator v2.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument("--overwrite", action="store_true",
                        help="Overwrite existing files")
    parser.add_argument("--dry-run", action="store_true",
                        help="Preview without writing files")
    args = parser.parse_args()
    files = read_list(LIST_FILE)
    generate(files, overwrite=args.overwrite, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
