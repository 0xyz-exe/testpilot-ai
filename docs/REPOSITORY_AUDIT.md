# Repository Audit — TestPilot AI

**Date:** 2026-10-16  
**Status:** Greenfield project — no existing code

## 1. Current Architecture

None. Fresh repository.

## 2. Existing Functionality

None verified.

## 3. Reusable Components

None.

## 4. Known Bugs and Technical Debt

N/A — no code exists.

## 5. Security and Reliability Risks

N/A — implementation phase will address:
- SSRF through user-controlled test URLs
- Arbitrary code execution via test generation
- Secret leakage in traces/screenshots
- Resource exhaustion from unbounded browser execution
- Privilege escalation through test workers

## 6. Missing Functionality

Everything. Core requirements:
- Project/suite/test CRUD
- Playwright execution engine with isolation
- Test artifact storage (screenshots, traces)
- AI-assisted test generation (optional, with deterministic fallback)
- Failure diagnosis
- Test history and reporting
- Authentication and authorization
- Security controls (URL validation, resource limits, sandboxing)

## 7. Recommended Implementation Sequence

**P0 — Core MVP (no AI required):**
1. Backend API: FastAPI + SQLite + Pydantic validation
2. Database schema: projects, suites, tests, runs, artifacts
3. Playwright worker: isolated subprocess, timeout enforcement, screenshot capture
4. Frontend: Next.js + React + TypeScript + shadcn/ui
5. Auth: simple API key or session-based (JWT later)
6. Basic CRUD screens: projects, tests, run history

**P1 — AI Features:**
7. Provider abstraction (OpenAI-compatible, local model support)
8. Test generation from natural language
9. Rule-based failure diagnosis (always available)
10. AI-enhanced diagnosis (when provider configured)

**P2 — Quality Intelligence:**
11. Flaky test detection
12. Regression comparison
13. Coverage metrics
14. CI integration example

**Security baseline (applies to all phases):**
- URL allowlist with redirect validation
- Worker sandboxing (subprocess, timeout, resource limits)
- Input validation on all endpoints
- Artifact access authorization
- Secret redaction in logs/traces
- Rate limiting and quotas

## Next Steps

1. Create PRD
2. Define UI/UX requirements
3. Design architecture and threat model
4. Implement P0 features with security controls
5. Add tests as features land
6. Document setup and demo scenario
