# Agent Communication Protocol

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
