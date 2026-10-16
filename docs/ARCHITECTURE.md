# Architecture — TestPilot AI

**Version:** 1.0  
**Date:** 2026-10-16

## 1. System Overview

TestPilot AI is a web-based testing platform with three core subsystems:

1. **Web API** — REST API for project/test management
2. **Execution Engine** — Isolated Playwright workers
3. **AI Provider** — Optional test generation and diagnosis

```
┌─────────────────────────────────────────────────┐
│                  Frontend (Next.js)             │
│  React UI + API Client + Auth                   │
└──────────────────────┬──────────────────────────┘
                       │ HTTP/REST
┌──────────────────────▼──────────────────────────┐
│              Backend API (FastAPI)              │
│  Auth │ Projects │ Tests │ Runs │ Artifacts    │
└───┬──────────────┬──────────────┬───────────────┘
    │              │              │
    │         ┌────▼────┐    ┌────▼────┐
    │         │  Queue  │    │ AI Svc  │
    │         │ (async) │    │ (opt)   │
    │         └────┬────┘    └─────────┘
    │              │
┌───▼──────────────▼────────────────────┐
│         Execution Workers              │
│  Playwright subprocess • Isolated      │
│  Timeout • Resource limits • Cleanup   │
└────────────────┬───────────────────────┘
                 │
            ┌────▼────┐
            │ Browser │
            │Chromium │
            └─────────┘
```

## 2. Technology Stack

### Backend
- **Framework:** FastAPI 0.100+
- **Language:** Python 3.11+
- **Database:** SQLite (dev), PostgreSQL (prod)
- **ORM:** SQLAlchemy 2.0
- **Validation:** Pydantic v2
- **Testing:** pytest, pytest-asyncio
- **Browser:** Playwright 1.40+

### Frontend
- **Framework:** Next.js 14 (App Router)
- **Language:** TypeScript 5
- **UI:** React 18 + Tailwind CSS 3 + shadcn/ui
- **State:** React Query (TanStack Query)
- **Validation:** Zod
- **Testing:** Vitest + React Testing Library + Playwright

### Infrastructure
- **Queue:** Redis (if async execution needed; SQLite polling for MVP)
- **Storage:** Local filesystem (artifacts)
- **Web Server:** Uvicorn (dev), Gunicorn + Uvicorn workers (prod)

## 3. Module Architecture

### Backend Modules

```
backend/
├── main.py              # FastAPI app + CORS + middleware
├── config.py            # Settings (env vars)
├── database.py          # SQLAlchemy engine + session
├── models/              # SQLAlchemy models
│   ├── user.py
│   ├── project.py
│   ├── suite.py
│   ├── test.py
│   ├── run.py
│   └── artifact.py
├── schemas/             # Pydantic request/response schemas
│   ├── project.py
│   ├── test.py
│   └── run.py
├── routes/              # API route handlers
│   ├── auth.py
│   ├── projects.py
│   ├── suites.py
│   ├── tests.py
│   └── runs.py
├── services/            # Business logic
│   ├── auth.py
│   ├── project_service.py
│   ├── test_service.py
│   ├── execution_service.py  # Spawn workers
│   ├── artifact_service.py
│   ├── diagnosis_service.py  # Rule-based analysis
│   └── ai_service.py         # AI provider abstraction
├── workers/             # Execution engine
│   ├── playwright_worker.py  # Subprocess runner
│   ├── sandbox.py            # Isolation + limits
│   └── result_parser.py
├── security/            # Security utilities
│   ├── url_validator.py      # SSRF prevention
│   ├── input_sanitizer.py
│   └── rate_limiter.py
└── migrations/          # Alembic migrations
    └── versions/
```

### Frontend Modules

```
frontend/
├── app/                 # Next.js App Router
│   ├── layout.tsx
│   ├── page.tsx         # Projects dashboard
│   ├── projects/
│   │   └── [id]/
│   │       ├── page.tsx      # Project detail
│   │       └── tests/
│   │           └── [testId]/
│   │               └── page.tsx  # Test detail
│   ├── generate/
│   │   └── page.tsx     # AI test generator
│   └── settings/
│       └── page.tsx     # AI provider config
├── components/          # React components
│   ├── ui/              # shadcn/ui primitives
│   ├── project-card.tsx
│   ├── test-list.tsx
│   ├── test-detail.tsx
│   ├── diagnosis-panel.tsx
│   ├── code-editor.tsx
│   └── history-timeline.tsx
├── lib/
│   ├── api-client.ts    # Fetch wrapper + types
│   ├── auth.ts          # Auth context
│   └── utils.ts
├── hooks/
│   ├── use-projects.ts  # React Query hooks
│   └── use-tests.ts
└── types/
    └── api.ts           # TypeScript API types
```

## 4. Data Flow

### Test Execution Flow

1. **User triggers test run** (Frontend)
2. **API receives request** → validates auth + project ownership
3. **Execution service** creates `TestRun` record (status: PENDING)
4. **Worker spawned** as subprocess:
   - Timeout enforced (default 30s)
   - URL validated against project allowlist
   - Playwright script executed in isolated context
5. **Worker reports back**:
   - Updates `TestRun` (status: PASSED/FAILED/TIMEOUT)
   - Saves artifacts (screenshot, trace) to disk
   - Returns result to API
6. **Frontend polls** or receives SSE update
7. **User views result** with artifacts

### Test Generation Flow

1. **User submits requirement** (natural language)
2. **API validates** input length (<2000 chars)
3. **AI service**:
   - Checks provider availability
   - Sends prompt with schema constraints
   - Validates response against Pydantic schema
   - Falls back to template if AI unavailable
4. **Returns draft test** (not saved)
5. **User reviews and approves**
6. **Test saved** to suite

## 5. Security Architecture

### Authentication
- **Session-based** for MVP (HTTP-only cookies)
- JWT for API-only clients (P2)
- Password hashing: bcrypt (cost 12)

### Authorization
- **Project-level:** User must be project owner/member
- **Resource access:** All test/run/artifact queries check project membership
- **Audit trail:** Log all executions, failures, access

### Worker Isolation

**Subprocess sandboxing:**
```python
# Enforced limits
- Timeout: 30-300s (configurable)
- Memory: 512MB (via resource.setrlimit where available)
- CPU: 1 core affinity (where available)
- Network: Only allowlisted URLs
- Filesystem: Read-only except temp dir
```

**URL validation:**
```python
def validate_url(url: str, allowlist: List[str]) -> None:
    parsed = urlparse(url)
    
    # Reject private IPs
    if is_private_ip(parsed.hostname):
        raise ValueError("Private IP rejected")
    
    # Check allowlist
    if not any(url.startswith(allowed) for allowed in allowlist):
        raise ValueError("URL not in project allowlist")
    
    # Validate redirect destination (checked at runtime)
```

### Artifact Security
- Artifacts stored: `artifacts/<project_id>/<run_id>/`
- Access checked: user must own project
- Redaction: Remove `Authorization`, `Cookie`, `Set-Cookie` headers from traces
- Sensitive fields: Passwords, tokens scrubbed from screenshots (best-effort)

### Rate Limiting
- **Test execution:** 100 runs/hour per user
- **AI generation:** 20 requests/hour per user
- **Concurrent tests:** 10 per project

## 6. Database Design

See `DATABASE_DESIGN.md` for full schema.

**Key entities:**
- User (id, email, password_hash, created_at)
- Project (id, user_id, name, allowed_urls, settings)
- TestSuite (id, project_id, name)
- TestCase (id, suite_id, title, code, tags)
- TestRun (id, test_id, status, duration, error, browser_version, created_at)
- Artifact (id, run_id, type, path)

**Relationships:**
- User 1:N Project
- Project 1:N TestSuite
- TestSuite 1:N TestCase
- TestCase 1:N TestRun
- TestRun 1:N Artifact

## 7. API Design

See `API.md` for full endpoint spec.

**Core endpoints:**
- `POST /auth/register` — Create user
- `POST /auth/login` — Get session
- `GET /projects` — List projects
- `POST /projects` — Create project
- `GET /projects/:id/suites` — List suites
- `POST /projects/:id/tests/generate` — AI generation
- `POST /tests/:id/run` — Execute test
- `GET /runs/:id` — Get run result
- `GET /runs/:id/artifacts/:artifactId` — Download artifact

## 8. Deployment

### Development
```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate (Windows)
pip install -r requirements.txt
playwright install chromium
uvicorn main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

### Production (example)
```bash
# Backend
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app

# Frontend
npm run build
npm start
```

### Environment Variables
```bash
# Backend
DATABASE_URL=postgresql://user:pass@localhost/testpilot
SECRET_KEY=<random-secret>
ALLOWED_ORIGINS=http://localhost:3000
ARTIFACT_STORAGE_PATH=/var/testpilot/artifacts
AI_PROVIDER_TYPE=local  # or openai, anthropic
AI_ENDPOINT=http://localhost:11434

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 9. Scalability Considerations

### MVP (single server)
- SQLite database
- Synchronous worker execution
- Local filesystem artifacts
- Expected load: 1-10 users, <100 tests

### Future (horizontal scale)
- PostgreSQL with connection pooling
- Redis-backed job queue (Celery, RQ)
- S3-compatible artifact storage
- Worker pool (separate processes/machines)
- Load balancer (multiple API instances)

## 10. Observability

### Logging
- Structured JSON logs (stdlib `logging`)
- Levels: DEBUG (dev), INFO (prod)
- Logged events:
  - Auth attempts (success/failure)
  - Test executions (start/end/status)
  - Worker errors
  - Security violations (rejected URLs, rate limits)

### Metrics (P2)
- Test execution duration (histogram)
- Pass/fail rates
- Worker spawn time
- API response times

### Monitoring (P2)
- Health endpoint: `GET /health`
- Database connectivity check
- Playwright browser availability

## 11. Error Handling

### API Errors
```json
{
  "error": "ValidationError",
  "message": "Invalid project ID",
  "details": {"field": "project_id", "reason": "not_found"}
}
```

HTTP status codes:
- 400: Invalid input
- 401: Unauthenticated
- 403: Unauthorized (insufficient permissions)
- 404: Resource not found
- 429: Rate limit exceeded
- 500: Internal server error

### Worker Errors
- **Timeout:** Kill process, mark run as TIMEOUT
- **Crash:** Capture stderr, mark as ERROR
- **OOM:** Log event, mark as ERROR

## 12. Testing Strategy

### Backend Tests
- **Unit:** Services, validators, parsers
- **Integration:** API routes + database
- **E2E:** Full execution flow (mock browser)

### Frontend Tests
- **Unit:** Components (React Testing Library)
- **Integration:** Page flows (Playwright)

### Security Tests
- SSRF: Attempt private IPs, localhost, cloud metadata
- Auth: Test unauthorized access to all endpoints
- Input: Inject SQL, XSS, command injection

---

**Next:** Database design, API spec, threat model.
