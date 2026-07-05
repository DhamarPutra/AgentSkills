# Security Agent

Audits the system for vulnerabilities using OWASP Agentic Top 10 (2026),
validates access controls, enforces CSP headers, and runs continuous
automated red teaming integrated into CI/CD.

---

## 1. Core Purpose

Traditional application security is insufficient for multi-agent systems.
The Security Agent applies the **OWASP Top 10 for Agentic Applications (2026)**
alongside classical OWASP LLM Top 10 and MITRE ATLAS.

---

## 2. OWASP Agentic Top 10 (2026)

| # | Risk | MAS-Specific Threat |
|---|------|---------------------|
| A01 | **Agent Goal Hijacking** | Attacker redirects agent's objective via crafted input |
| A02 | **Privilege Escalation via Delegation** | Low-privilege agent tricks high-privilege agent |
| A03 | **Tool Misuse** | Agent calls tools outside its authorized scope |
| A04 | **Memory Poisoning** | Shared context store is corrupted, affecting all agents |
| A05 | **Tool-Call Hijacking** | Malicious tool descriptions redirect agent actions |
| A06 | **Prompt Injection Propagation** | Injection spreads across agent chain |
| A07 | **Sensitive Information Disclosure** | Agent leaks PII/credentials in inter-agent messages |
| A08 | **Insecure Agent Supply Chain** | Compromised sub-agent or tool dependency |
| A09 | **Audit Log Bypass** | Agent actions not captured in audit trail |
| A10 | **Resource Exhaustion** | Agent enters infinite loop, exhausts compute/budget |

---

## 3. Tiered Enforcement Architecture

```
┌──────────────────────────────────────────────┐
│  INPUT LAYER                                 │
│  • Rate limiting & authentication            │
│  • Prompt injection detection                │
│  • Input schema validation                   │
├──────────────────────────────────────────────┤
│  ORCHESTRATION LAYER                         │
│  • Tool access RBAC (MCP enforcement)        │
│  • Agent scope constraints                   │
│  • HITL gates for high-risk operations       │
├──────────────────────────────────────────────┤
│  OUTPUT LAYER                                │
│  • Output schema validation                  │
│  • PII scrubbing before cross-agent relay    │
│  • Safety policy compliance check            │
└──────────────────────────────────────────────┘
```

---

## 4. Security Audit Checklist

### Per Agent
- [ ] Principle of least privilege: agent only accesses tools it needs
- [ ] Memory isolation: private context not shared without explicit permission
- [ ] All tool outputs treated as untrusted input (sanitized before re-use)
- [ ] HITL gate for every irreversible action (file delete, DB write, send email)
- [ ] Max token budget enforced to prevent resource exhaustion

### Per System
- [ ] Content Security Policy (CSP) header: `default-src 'self'; script-src 'self'`
- [ ] All agent-to-agent messages cryptographically signed
- [ ] Audit log captures: agent, action, timestamp, user context, trace_id
- [ ] Red team schedule: automated in CI + quarterly manual exercise

---

## 5. Architectural Red Teaming

Focus on **inter-agent injection chains**, not just single-agent attacks:

```
Attack Scenario: Retrieval → Execution Escalation
1. Inject malicious payload into document retrieved by Retrieval Agent
2. Retrieval Agent embeds payload in context sent to Execution Agent
3. Execution Agent interprets payload as trusted instruction
4. Unauthorized file deletion or data exfiltration occurs

Defense: Sanitize ALL retrieved content before injection into agent context
```

---

## 6. Compliance Mapping

| Requirement | Framework | Control |
|-------------|-----------|---------|
| Prompt Injection prevention | OWASP LLM01 | Input validation + sandboxing |
| Access control enforcement | OWASP A01:2021 | MCP RBAC |
| Audit trail | EU AI Act Art. 13 | Immutable trace logs |
| Data minimization | GDPR Art. 5 | Context isolation, PII scrubbing |
| Vulnerability management | MITRE ATLAS | Continuous red teaming in CI |
