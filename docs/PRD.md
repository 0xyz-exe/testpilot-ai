# Product Requirements Document — TestPilot AI

**Version:** 1.0  
**Date:** 2026-10-16  
**Status:** Draft

## 1. Product Overview

**TestPilot AI** is a developer-first web testing platform combining Playwright automation with AI-assisted test creation and failure diagnosis.

### Problem Statement

Developers waste time:
- Writing repetitive browser test boilerplate
- Debugging flaky tests without sufficient context
- Reproducing failures that lack evidence
- Maintaining test suites as applications evolve
- Identifying root causes from vague error messages

### Solution

A local-first testing workspace that:
- Generates Playwright tests from natural language
- Executes tests in isolated browsers with full artifact capture
- Diagnoses failures using deterministic rules + optional AI
- Tracks test history, flakiness, and regressions
- Works without paid APIs (AI optional)

## 2. User Personas

### Primary: Full-Stack Developer
- Builds and maintains web applications
- Writes some tests but lacks QA automation depth
- Needs faster test authoring and better debugging evidence
- Values local development workflow
- Budget-conscious (prefers open-source, free-tier)

### Secondary: QA Engineer
- Writes comprehensive test suites
- Needs flaky-test analysis and regression tracking
- Integrates tests with CI pipelines
- Requires detailed failure diagnostics
- Values reproducibility and evidence

## 3. Core User Journey

**Goal:** Create, execute, and debug a web application test.

### Steps

1. **Create project**
   - Input: project name, authorized base URL(s)
   - Output: project workspace

2. **Create test suite**
   - Input: suite name, optional tags
   - Output: empty suite

3. **Generate test from requirement**
   - Input: natural language description ("verify login with valid credentials")
   - Output: draft Playwright test with steps, assertions, preconditions
   - User reviews generated code before approval

4. **Approve and save test**
   - Test moves from draft → approved
   - Stored with version metadata

5. **Execute test**
   - Backend spawns isolated Playwright worker
   - Browser runs against configured base URL
   - Captures: result, duration, screenshot (on failure), trace, console errors, network failures

6. **View result**
   - Status: PASSED | FAILED | TIMEOUT | ERROR
   - Artifacts: screenshot, trace file, logs
   - Execution metadata: browser version, timestamp, retry count

7. **Request diagnosis (on failure)**
   - System analyzes: error message, screenshot, console, network
   - Returns: likely cause, evidence references, suggested fix
   - Deterministic rules always available; AI enhances when configured

8. **Apply fix and retest**
   - User updates test or identifies app bug
   - Re-runs test
   - Compares new result with previous failure

9. **Review history**
   - Timeline of runs for this test
   - Pass/fail patterns
   - Duration trends
   - Flakiness indicators

## 4. Functional Requirements

### P0 — Core MVP (must work without AI)

#### Projects
- **F-001:** Create project with name + authorized URL list
- **F-002:** Edit project settings
- **F-003:** Delete project (cascade to suites/tests)
- **F-004:** List all projects

#### Test Suites
- **F-005:** Create suite within project
- **F-006:** Edit suite metadata
- **F-007:** Delete suite (cascade to tests)
- **F-008:** List suites per project

#### Test Cases
- **F-009:** Create test manually (title, steps, Playwright code)
- **F-010:** Edit test code and metadata
- **F-011:** Delete test
- **F-012:** Tag tests
- **F-013:** Search and filter tests
- **F-014:** View test version history

#### Test Execution
- **F-015:** Execute single test in Chromium
- **F-016:** Execute entire suite
- **F-017:** Capture test result: PASSED | FAILED | TIMEOUT | ERROR
- **F-018:** Capture duration
- **F-019:** Capture screenshot on failure
- **F-020:** Capture Playwright trace
- **F-021:** Capture sanitized console errors
- **F-022:** Retry failed tests (max 3 attempts)
- **F-023:** Cancel running test
- **F-024:** Enforce per-test timeout (default 30s, configurable up to 300s)
- **F-025:** Store execution metadata: browser version, timestamp, test code snapshot

#### Artifacts
- **F-026:** Store screenshots in project-scoped directory
- **F-027:** Store traces in project-scoped directory
- **F-028:** Authorize artifact access per project membership
- **F-029:** Redact sensitive headers/cookies from network logs

#### Test History
- **F-030:** List all runs for a test
- **F-031:** View detailed run: status, duration, error, artifacts
- **F-032:** Compare two runs (diff: status, duration, error message)
- **F-033:** Filter history by status, date range

#### Failure Diagnosis (deterministic rules)
- **F-034:** Detect selector errors
- **F-035:** Detect timeout errors
- **F-036:** Detect navigation failures
- **F-037:** Detect assertion failures
- **F-038:** Detect missing browser dependencies
- **F-039:** Return diagnosis: error type, evidence, recommended fix

#### Authentication & Authorization
- **F-040:** User registration and login
- **F-041:** Session management
- **F-042:** Enforce project-level access control
- **F-043:** Audit log for test executions and project changes

### P1 — AI-Assisted Features

#### Test Generation
- **F-044:** Generate Playwright test from natural language input
- **F-045:** Support provider abstraction (OpenAI-compatible, local models)
- **F-046:** Validate generated code schema (actions, selectors, assertions)
- **F-047:** Show generated test as draft (not auto-executed)
- **F-048:** Require explicit approval before execution
- **F-049:** Fallback to template-based generation when AI unavailable
- **F-050:** Handle provider errors gracefully (rate limit, timeout)

#### AI-Enhanced Diagnosis
- **F-051:** Enhance rule-based diagnosis with AI analysis
- **F-052:** Extract likely root cause from screenshot + logs
- **F-053:** Suggest test fixes or app changes
- **F-054:** Label AI-generated hypotheses clearly (vs. verified facts)

#### Provider Configuration
- **F-055:** Configure AI provider: API key, endpoint, model
- **F-056:** Test provider connection
- **F-057:** Store credentials server-side only
- **F-058:** Support local model endpoints (Ollama, LM Studio)

### P2 — Quality Intelligence

#### Flaky Test Detection
- **F-059:** Track pass/fail transitions per test
- **F-060:** Calculate flakiness score based on retry outcomes
- **F-061:** Mark test as flaky after 3+ inconsistent results
- **F-062:** Display flaky test report with evidence

#### Regression Analysis
- **F-063:** Compare test status before/after code change
- **F-064:** Detect newly failing tests
- **F-065:** Detect duration regressions (>50% slower)
- **F-066:** Generate regression report

#### Metrics and Reporting
- **F-067:** Project dashboard: total tests, pass rate, flaky count
- **F-068:** Execution timeline chart
- **F-069:** Duration distribution
- **F-070:** Failure breakdown by type
- **F-071:** Export test report (JSON, HTML)

#### CI Integration
- **F-072:** GitHub Actions example workflow
- **F-073:** API endpoint for triggered runs
- **F-074:** Webhook for run completion
- **F-075:** Exit with non-zero status when critical tests fail

## 5. Non-Functional Requirements

### Performance
- **NFR-001:** API response <500ms (p95) for CRUD operations
- **NFR-002:** Support 100 concurrent test executions (design target)
- **NFR-003:** Test history queries paginated (50 per page)

### Reliability
- **NFR-004:** Worker crash must not corrupt run state
- **NFR-005:** Failed test retries with exponential backoff
- **NFR-006:** Graceful degradation when AI provider unavailable

### Usability
- **NFR-007:** Dark and light theme support
- **NFR-008:** Responsive layout (desktop-first)
- **NFR-009:** Keyboard navigation for critical flows
- **NFR-010:** Accessible ARIA labels and semantic HTML
- **NFR-011:** Clear empty states for all lists
- **NFR-012:** Visible loading indicators for async operations

### Maintainability
- **NFR-013:** Modular architecture (separate execution, storage, API)
- **NFR-014:** Database migrations tracked
- **NFR-015:** Comprehensive error messages
- **NFR-016:** Logging for security events (auth, execution, access)

## 6. Security and Privacy Requirements

### Authentication & Authorization
- **SEC-001:** Passwords hashed with bcrypt (cost ≥12)
- **SEC-002:** Session tokens rotated on privilege change
- **SEC-003:** Enforce project membership for all resource access
- **SEC-004:** Audit trail for test executions and failures

### Test Execution Isolation
- **SEC-005:** Workers run in subprocess with timeout enforcement
- **SEC-006:** Workers cannot access host secrets or API database
- **SEC-007:** URL validation: allowlist, reject private/loopback/link-local by default
- **SEC-008:** Revalidate redirect destinations
- **SEC-009:** Enforce resource limits: CPU (where available), memory (where available), output size
- **SEC-010:** Clean up worker resources on completion or timeout

### Data Protection
- **SEC-011:** Redact passwords, tokens, cookies from stored artifacts
- **SEC-012:** Artifacts scoped per project
- **SEC-013:** No sensitive data in error messages or stack traces
- **SEC-014:** AI provider credentials stored server-side only
- **SEC-015:** Environment variables never exposed in UI or logs

### Input Validation
- **SEC-016:** Validate all request bodies with Pydantic/Zod
- **SEC-017:** Sanitize user-provided test code (reject unsafe imports, shell execution)
- **SEC-018:** Parameterized database queries (no raw SQL interpolation)
- **SEC-019:** Reject generated tests with disallowed Playwright APIs

### Rate Limiting & DoS Prevention
- **SEC-020:** Per-user rate limits: 100 test executions/hour
- **SEC-021:** Per-project concurrency limit: 10 parallel tests
- **SEC-022:** AI generation rate limit: 20 requests/hour/user

## 7. System Boundaries

### In Scope
- Web application testing with Playwright
- Test generation from English requirements
- Browser: Chromium (P0), Firefox/WebKit (P2)
- Local development workflow
- SQLite (local) and PostgreSQL (production-ready)
- Optional AI provider integration

### Out of Scope
- Mobile app testing
- Load/performance testing
- API-only testing (no browser)
- Real device testing
- Cross-browser screenshot comparison (visual regression)
- Hosted SaaS offering (self-hosted only for MVP)

## 8. Acceptance Criteria

### Milestone A: Core Platform
- [ ] User can create project, suite, test
- [ ] Manual test execution works in Chromium
- [ ] Screenshot captured on failure
- [ ] Test history persisted and viewable
- [ ] Unauthorized access blocked

### Milestone B: AI Features
- [ ] Test generated from natural language (when AI configured)
- [ ] Deterministic diagnosis works without AI
- [ ] AI diagnosis enhances failure analysis
- [ ] Generated tests require approval before execution

### Milestone C: Quality Intelligence
- [ ] Flaky tests detected after 3 inconsistent runs
- [ ] Regression comparison shows status/duration changes
- [ ] Dashboard displays test metrics
- [ ] GitHub Actions workflow example provided

### MVP Complete
- [ ] All P0 requirements implemented
- [ ] Security audit completed
- [ ] Automated tests cover critical flows
- [ ] Setup documented (Windows PowerShell + bash)
- [ ] Demo video or walkthrough created

## 9. Success Metrics

### Usage
- Time to create first test: <5 minutes
- Test execution feedback latency: <60 seconds (simple test)
- Diagnosis retrieval: <3 seconds

### Quality
- False positive diagnosis rate: <10%
- Test artifacts captured: 100% of failures
- Worker crash rate: <1%

### Adoption
- Developers write 3x more tests with AI generation (vs. manual)
- Test debugging time reduced by 50% (measured by time to fix)

## 10. Failure Handling

### Worker Failures
- **Timeout:** Kill process, mark test as TIMEOUT, capture partial artifacts
- **Crash:** Mark test as ERROR, log crash, preserve artifacts
- **OOM:** Enforce memory limit (when available), fail gracefully

### AI Failures
- **Rate limit:** Queue request with exponential backoff
- **Unavailable:** Fall back to template-based generation or rule-based diagnosis
- **Invalid output:** Validate schema, reject malformed responses, log error

### Database Failures
- **Connection loss:** Retry with exponential backoff (max 3)
- **Constraint violation:** Return 400 with clear error message
- **Migration failure:** Block startup, log error, require manual intervention

### Artifact Storage Failures
- **Disk full:** Fail test execution, alert user
- **Permission denied:** Fail execution, log error
- **Missing artifact:** Mark as unavailable, do not block report generation

## 11. Local Installation Scenario

### Prerequisites
- Python 3.11+
- Node.js 20+
- Git

### Setup Steps
1. Clone repository
2. Install backend: `pip install -r requirements.txt`
3. Install Playwright browsers: `playwright install chromium`
4. Initialize database: `python backend/init_db.py`
5. Start backend: `uvicorn backend.main:app --reload`
6. Install frontend: `npm install` (in frontend/)
7. Start frontend: `npm run dev`
8. Open http://localhost:3000
9. Register account
10. Create test project

### Demo Scenario
1. Create project "My App" with URL http://localhost:8080
2. Generate test: "verify homepage loads"
3. Review generated Playwright code
4. Approve test
5. Execute test
6. View result with screenshot
7. Intentionally break app (stop localhost:8080)
8. Re-run test → FAILED
9. View diagnosis: "Navigation timeout — target unreachable"
10. Restart app, verify test passes

## 12. Open Questions

1. **Multi-tenancy:** Single-user local mode or workspace teams?
   - **Decision:** Single-user for MVP, workspace support in P2
2. **Browser downloads:** Bundle browsers or require manual install?
   - **Decision:** Require manual `playwright install` (documented)
3. **Artifact retention:** Delete old artifacts automatically?
   - **Decision:** Keep last 100 runs per test (configurable)
4. **AI provider defaults:** Pre-configure any free providers?
   - **Decision:** No defaults; user provides API key or local endpoint

## 13. Out-of-Scope for MVP

- Visual regression testing
- Parallel test execution across multiple machines
- Test scheduling (cron-like)
- Email notifications
- Slack/Discord integrations
- Advanced test parameterization
- Data-driven testing (CSV input)
- Multi-language test generation (only English)
- Video recording (screenshots + traces sufficient)

---

**Next Steps:**
1. Review and approve PRD
2. Create UI/UX brief
3. Design architecture and threat model
4. Begin P0 implementation
