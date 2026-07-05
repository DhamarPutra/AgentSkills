# System Workflow

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
