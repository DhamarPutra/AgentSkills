# Agent Role Template

Use this template when adding a new agent role to the super-agent system.
Copy this file, rename it to `<your-agent-name>-agent.md`, and fill in
each section with the role-specific details.

---

## 1. Core Purpose

[One to two sentences: what unique responsibility does this agent have?
What problem would go unaddressed if this agent did not exist?]

---

## 2. Scope & Boundaries

**In Scope**:
- [Task type 1 this agent is responsible for]
- [Task type 2]

**Out of Scope**:
- [Explicit exclusions to prevent overlap with other agents]

---

## 3. Input & Output Contract

| Item | Schema | Description |
|------|--------|-------------|
| **Input** | `TaskMessage` | Standard task from Orchestrator with `success_criteria` |
| **Output** | `TaskResult` | Standard result with `status`, `result`, `metrics` |

### Input Payload Schema
```json
{
  "required_field": "string",
  "optional_field": "string | null"
}
```

### Output Payload Schema
```json
{
  "primary_output": "string",
  "metadata": {}
}
```

---

## 4. Workflow & Responsibilities

1. **Receive**: Accept task from Orchestrator. Validate input schema.
2. **Validate**: Check that all required context is present.
3. **Execute**: Perform the core responsibility.
4. **Validate Output**: Confirm output meets `success_criteria`.
5. **Return**: Send structured `TaskResult` back to Orchestrator.
6. **Error Handling**: On failure, return `AgentError` (never silent fail).

---

## 5. Interaction Patterns

```
Orchestrator
    │
    ▼ (task delegation)
[This Agent] ──► [Tools / Services this agent uses]
    │
    ▼ (result)
Orchestrator
```

**Dependencies** (agents this agent may interact with via Orchestrator):
- [Agent Name]: [Why / when]

---

## 6. Error Handling

```json
{
  "error_code": "ERR_[SPECIFIC_CODE]",
  "message": "Human-readable description",
  "retryable": true,
  "hitl_required": false
}
```

**When to escalate to HITL**:
- [Condition 1]
- [Condition 2]

---

## 7. Performance Requirements

| Metric | Target |
|--------|--------|
| Typical response time | < Xs |
| Timeout | Xs |
| Max token budget | N tokens |

---

## 8. Maintenance & Versioning

Update this document when:
- The agent's responsibilities change
- Input/output schemas are modified
- New tools or integrations are added
- A breaking change affects downstream agents

Tag breaking changes with `[BREAKING]` in the changelog entry.
