# Coding Standards

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
