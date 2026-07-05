# Testing Standards

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
