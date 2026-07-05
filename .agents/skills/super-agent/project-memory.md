# Project Memory System

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
    '''
    1. Summarize raw episodes into key learnings
    2. Extract reusable heuristics ("User prefers concise explanations")
    3. Discard redundant or contradicted information
    4. Store distilled fact in Semantic tier
    5. Archive raw episodes (do not delete - needed for audits)
    '''
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
