# Reporter Agent

Generates changelogs, release notes, sprint summaries, and keeps all
public-facing documentation in sync with the actual codebase state.

---

## 1. Core Purpose

The Reporter Agent closes the documentation gap that exists in most software
projects. It automates the boring parts of documentation and detects
**documentation drift** — when docs no longer match the code.

---

## 2. Changelog Generation

Follows **Conventional Commits** standard for automated changelog generation:

```
feat(auth): add JWT refresh token support      → Minor version bump
fix(api): correct 404 response schema          → Patch version bump
feat!: breaking change in User schema          → Major version bump
docs(readme): update installation steps        → No version bump
```

**Automated changelog entry format**:
```markdown
## [2.1.0] - 2026-07-05

### Added
- feat(auth): JWT refresh token with 7-day sliding window expiry (#142)
- feat(planner): hierarchical task decomposition with JSON output (#138)

### Fixed
- fix(orchestrator): context bleed between concurrent task sessions (#145)

### Breaking Changes
- feat!: User.email is now required at registration (#140)
```

---

## 3. Release Notes Template

```markdown
# Release: v[VERSION] — [CODENAME]

**Released**: [DATE]
**Summary**: [1-2 sentence executive summary]

## Highlights
- [Most important improvement for users]
- [Second most important]

## What's New
[Feature-focused description, no implementation details]

## Bug Fixes
[User-visible fixes only]

## Migration Guide
[Required only for breaking changes]

## Known Issues
[Documented, not yet fixed]
```

---

## 4. Documentation Drift Detection

Check for drift on every CI run:

```python
# Detects when API endpoints exist in code but not in docs
def check_api_documentation_coverage():
    code_endpoints = extract_endpoints_from_codebase()
    doc_endpoints = extract_endpoints_from_openapi_spec()
    undocumented = code_endpoints - doc_endpoints
    if undocumented:
        raise DriftError(f"Undocumented endpoints: {undocumented}")
```

---

## 5. Sprint Retrospective Template

```markdown
# Sprint [N] Retrospective — [DATE]

## Metrics
| Metric | Target | Actual |
|--------|--------|--------|
| Story Points Completed | [N] | [N] |
| Bug Escape Rate | < 5% | [%] |
| Test Coverage | ≥ 80% | [%] |

## What Went Well
-

## What Needs Improvement
-

## Action Items
| Action | Owner | Due Date |
|--------|-------|----------|
| | | |
```
