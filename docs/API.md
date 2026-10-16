# API Specification — TestPilot AI

**Version:** 1.0  
**Base URL:** `http://localhost:8000/api/v1`

## Authentication

All endpoints except `/auth/*` require authentication.

**Session-based:** Include session cookie in requests.  
**Headers:** `Content-Type: application/json`

---

## Auth Endpoints

### POST /auth/register
Create new user account.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "email": "user@example.com",
  "created_at": "2026-10-16T19:00:00Z"
}
```

**Errors:**
- `400`: Email already registered
- `422`: Validation error (invalid email, weak password)

---

### POST /auth/login
Start authenticated session.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Response:** `200 OK`
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com"
  }
}
```
Sets HTTP-only session cookie.

**Errors:**
- `401`: Invalid credentials

---

### POST /auth/logout
End session.

**Response:** `204 No Content`

---

## Project Endpoints

### GET /projects
List user's projects.

**Response:** `200 OK`
```json
{
  "projects": [
    {
      "id": 1,
      "name": "My App",
      "test_count": 45,
      "pass_rate": 89.5,
      "last_run_at": "2026-10-16T19:30:00Z"
    }
  ]
}
```

---

### POST /projects
Create project.

**Request:**
```json
{
  "name": "My App",
  "allowed_urls": ["http://localhost:3000", "https://staging.myapp.com"]
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "name": "My App",
  "allowed_urls": ["http://localhost:3000"],
  "settings": {},
  "created_at": "2026-10-16T19:00:00Z"
}
```

**Errors:**
- `400`: Invalid URL format
- `422`: Validation error

---

### GET /projects/:id
Get project details.

**Response:** `200 OK`
```json
{
  "id": 1,
  "name": "My App",
  "allowed_urls": ["http://localhost:3000"],
  "settings": {"timeout": 30, "retries": 3},
  "created_at": "2026-10-16T19:00:00Z"
}
```

**Errors:**
- `403`: Not project owner
- `404`: Project not found

---

### PATCH /projects/:id
Update project.

**Request:**
```json
{
  "name": "My App (Updated)",
  "allowed_urls": ["http://localhost:3000", "https://prod.myapp.com"]
}
```

**Response:** `200 OK` (updated project)

---

### DELETE /projects/:id
Delete project (cascades to suites, tests, runs).

**Response:** `204 No Content`

---

## Test Suite Endpoints

### GET /projects/:id/suites
List suites in project.

**Response:** `200 OK`
```json
{
  "suites": [
    {
      "id": 1,
      "project_id": 1,
      "name": "Authentication",
      "test_count": 8,
      "created_at": "2026-10-16T19:00:00Z"
    }
  ]
}
```

---

### POST /projects/:id/suites
Create test suite.

**Request:**
```json
{
  "name": "Authentication",
  "description": "Login, logout, registration tests"
}
```

**Response:** `201 Created`

---

## Test Case Endpoints

### GET /suites/:id/tests
List tests in suite.

**Response:** `200 OK`
```json
{
  "tests": [
    {
      "id": 1,
      "suite_id": 1,
      "title": "Login with valid credentials",
      "status": "approved",
      "tags": ["auth", "critical"],
      "last_run": {
        "status": "PASSED",
        "duration_ms": 2800,
        "created_at": "2026-10-16T19:30:00Z"
      }
    }
  ]
}
```

---

### POST /suites/:id/tests
Create test manually.

**Request:**
```json
{
  "title": "Login with valid credentials",
  "code": "test('login', async ({page}) => { /* ... */ });",
  "tags": ["auth", "critical"]
}
```

**Response:** `201 Created`

---

### GET /tests/:id
Get test details.

**Response:** `200 OK`
```json
{
  "id": 1,
  "suite_id": 1,
  "title": "Login with valid credentials",
  "code": "test('login', async ({page}) => { /* ... */ });",
  "tags": ["auth"],
  "status": "approved",
  "created_at": "2026-10-16T19:00:00Z"
}
```

---

### PATCH /tests/:id
Update test.

**Request:**
```json
{
  "code": "test('login', async ({page}) => { /* updated */ });",
  "status": "approved"
}
```

**Response:** `200 OK`

---

### DELETE /tests/:id
Delete test.

**Response:** `204 No Content`

---

## Test Generation

### POST /projects/:id/tests/generate
Generate test from natural language.

**Request:**
```json
{
  "requirement": "Verify that a user can sign in with valid credentials",
  "suite_id": 1
}
```

**Response:** `200 OK`
```json
{
  "title": "User login with valid credentials",
  "code": "test('user login', async ({page}) => {\n  await page.goto('/login');\n  // ...\n});",
  "preconditions": "User account must exist",
  "assumptions": ["Login form at /login", "Email and password fields present"],
  "ai_provider": "local"
}
```

**Errors:**
- `503`: AI provider unavailable (returns template-based fallback)
- `429`: Rate limit exceeded

---

## Test Execution

### POST /tests/:id/run
Execute test.

**Request:**
```json
{
  "retry_on_failure": true
}
```

**Response:** `202 Accepted`
```json
{
  "run_id": 42,
  "status": "PENDING"
}
```

**Errors:**
- `403`: Test not approved
- `429`: Rate limit exceeded

---

### GET /runs/:id
Get test run result.

**Response:** `200 OK`
```json
{
  "id": 42,
  "test_id": 1,
  "status": "FAILED",
  "duration_ms": 3200,
  "error_message": "Timeout 30000ms exceeded waiting for selector \"button[type=submit]\"",
  "browser_version": "Chromium 130.0.6723.58",
  "retry_count": 1,
  "created_at": "2026-10-16T19:30:00Z",
  "completed_at": "2026-10-16T19:30:03Z",
  "artifacts": [
    {
      "id": 1,
      "type": "screenshot",
      "file_path": "artifacts/1/42/screenshot.png",
      "file_size": 45678
    },
    {
      "id": 2,
      "type": "trace",
      "file_path": "artifacts/1/42/trace.zip"
    }
  ]
}
```

---

### GET /runs/:id/artifacts/:artifactId
Download artifact.

**Response:** `200 OK`  
**Content-Type:** `image/png` | `application/zip` | `text/plain`

**Errors:**
- `403`: Not authorized for this artifact
- `404`: Artifact not found

---

## Test History

### GET /tests/:id/runs
List historical runs for test.

**Query params:**
- `status`: Filter by status (PASSED, FAILED, etc.)
- `limit`: Max results (default 50)
- `offset`: Pagination offset

**Response:** `200 OK`
```json
{
  "runs": [
    {
      "id": 42,
      "status": "FAILED",
      "duration_ms": 3200,
      "created_at": "2026-10-16T19:30:00Z"
    },
    {
      "id": 41,
      "status": "PASSED",
      "duration_ms": 2800,
      "created_at": "2026-10-16T18:15:00Z"
    }
  ],
  "total": 156
}
```

---

## Failure Diagnosis

### POST /runs/:id/diagnose
Generate failure diagnosis.

**Response:** `200 OK`
```json
{
  "cause": "Selector timeout — button not found",
  "evidence": [
    "Error: Timeout waiting for selector \"button[type=submit]\"",
    "Screenshot: Button missing from DOM",
    "Console: No JavaScript errors"
  ],
  "recommended_fix": "Update selector to match current DOM:\n- await page.click('button[type=submit]')\n+ await page.click('button.submit-btn')",
  "confidence": "high",
  "ai_enhanced": false
}
```

---

## Flaky Tests

### GET /projects/:id/flaky-tests
List flaky tests in project.

**Response:** `200 OK`
```json
{
  "flaky_tests": [
    {
      "test_id": 5,
      "title": "Remove product from cart",
      "flakiness_rate": 0.4,
      "recent_runs": "PASS,FAIL,PASS,FAIL,PASS"
    }
  ]
}
```

---

## Error Responses

All errors return:
```json
{
  "error": "ErrorType",
  "message": "Human-readable message",
  "details": {}
}
```

**Status codes:**
- `400` Bad Request
- `401` Unauthorized
- `403` Forbidden
- `404` Not Found
- `422` Validation Error
- `429` Rate Limit Exceeded
- `500` Internal Server Error
- `503` Service Unavailable
