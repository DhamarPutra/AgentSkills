# Orchestrator Agent

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
