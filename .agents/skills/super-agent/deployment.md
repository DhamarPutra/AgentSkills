# Deployment Procedures

Step-by-step guide for staging and production deployments, pre-deploy
checklists, rollback procedures, and post-deploy verification.

---

## 1. Pre-Deploy Checklist

Complete ALL items before any production deployment:

### Code Quality
- [ ] All CI tests passing on main branch
- [ ] Code coverage ≥ 80% (unit), ≥ 60% (integration)
- [ ] Security scan clean (SAST + dependency audit)
- [ ] `validate_skill.py` passing

### Database
- [ ] All migration scripts tested against staging DB clone
- [ ] Rollback migration script tested and ready
- [ ] DB backup completed within last 4 hours

### Infrastructure
- [ ] Docker images tagged with semver (not `latest`)
- [ ] Kubernetes manifests reviewed for resource limits
- [ ] Secrets rotated if required by this release
- [ ] Load balancer health checks configured

### Communication
- [ ] Stakeholders notified of maintenance window
- [ ] On-call engineer designated for 2 hours post-deploy
- [ ] Rollback decision owner identified

---

## 2. Blue-Green Deployment Procedure

```
Step 1: Deploy new version to "Green" environment
        (runs alongside current "Blue" production)

Step 2: Run smoke tests against Green
        → Pass: proceed to step 3
        → Fail: debug in Green, Blue continues serving traffic

Step 3: Switch load balancer to route 5% traffic to Green (canary)
        → Monitor for 15 minutes (error rate, latency, business KPIs)
        → Error rate > 1%: switch back to Blue, investigate

Step 4: Gradually increase traffic: 5% → 25% → 50% → 100%
        → Monitor at each increment (15 min)

Step 5: Decommission Blue after 24 hours (keep as immediate rollback)
```

---

## 3. Rollback Runbook

**Trigger**: Error rate > 1% OR P95 latency increases > 20% post-deploy

```bash
# Immediate rollback (< 2 minutes)
# Step 1: Switch load balancer back to Blue
kubectl patch service api-gateway   -p '{"spec":{"selector":{"version":"blue"}}}'

# Step 2: Verify rollback is active
kubectl get endpoints api-gateway
curl https://api.example.com/health  # Should return 200

# Step 3: Notify team
echo "ROLLBACK COMPLETE: reverted to v$(cat .previous-version)"

# Step 4: Database rollback (if schema changed)
alembic downgrade -1
```

---

## 4. Post-Deploy Verification Checklist

Run within 30 minutes of production deployment:

- [ ] Health endpoint returns 200: `GET /health`
- [ ] Authentication flow working: login + token refresh
- [ ] Core agent endpoint responding: `POST /tasks`
- [ ] Database writes successful (create test record, verify, delete)
- [ ] Redis accessible (set/get test key)
- [ ] Error rate < 0.1% (last 15 min)
- [ ] P95 latency within 10% of pre-deploy baseline
- [ ] No new error types in logs

---

## 5. Incident Severity & Escalation

| P Level | Criteria | Response Time | Escalation |
|---------|----------|---------------|-----------|
| P0 | System down / data loss | Immediate | CTO + on-call |
| P1 | Critical feature broken | < 15 min | On-call + team lead |
| P2 | Significant degradation | < 1 hour | On-call |
| P3 | Minor issue | Next business day | Team backlog |
