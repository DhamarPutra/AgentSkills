# DevOps & Infrastructure Agent

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
