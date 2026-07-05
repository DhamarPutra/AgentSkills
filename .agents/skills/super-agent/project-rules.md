# Project Rules

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
