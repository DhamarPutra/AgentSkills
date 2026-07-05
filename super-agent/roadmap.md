# Product Roadmap

Short-term (current sprint), mid-term (next quarter), and long-term vision
for the super-agent multi-agent system.

---

## 1. Current Sprint (Q3 2026)

| Milestone | Features | Success Metric | Status |
|-----------|----------|----------------|--------|
| **Foundation Complete** | All 21 docs generated, scripts/ and assets/ added | CI passing ✅ | In Progress |
| **Content Quality** | All docs have production-grade content | 0 placeholder text | In Progress |
| **Publish Ready** | README, LICENSE, CONTRIBUTING.md | Stars on GitHub | Pending |

---

## 2. Next Quarter (Q4 2026)

| Milestone | Features | Success Metric |
|-----------|----------|----------------|
| **Agent Templates** | Python starter templates for each agent role | Community adoption |
| **Interactive Generator** | CLI wizard for custom list.md | 100+ clones/month |
| **Multi-language Support** | TypeScript/JS generate_docs equivalent | 20+ contributors |
| **Integration Guides** | Cursor, Copilot, Claude Code setup guides | Compatibility matrix |

---

## 3. Long-term Vision (2027+)

| Vision | Description |
|--------|-------------|
| **Skill Marketplace** | Community-contributed skills with quality ratings |
| **Auto-update Engine** | Skills auto-update from authoritative sources (OWASP, etc.) |
| **Agent Interop Standard** | Formal spec for cross-platform skill compatibility |
| **Visual Skill Builder** | GUI for creating skills without editing markdown |

---

## 4. Technical Debt Backlog

| Item | Priority | Effort | Notes |
|------|----------|--------|-------|
| Improve generate_docs.py test coverage | Medium | Small | Add unit tests |
| Add YAML schema validation for list.md | Medium | Small | Prevent malformed entries |
| Internationalize all docs (EN + ID) | Low | Large | Start with README only |

---

## 5. Research Backlog

Areas to explore for future skill versions:

- [ ] Integration with LangGraph memory checkpointing examples
- [ ] Automated skill health monitoring (skill drift detection)
- [ ] Fine-tuned models for each agent role specialization
- [ ] Formal verification of agent communication protocols

---

*Last updated: 2026-07-05*
