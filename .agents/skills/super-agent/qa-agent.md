# QA & Testing Agent

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
