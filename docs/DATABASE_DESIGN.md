# Database Design — TestPilot AI

**Version:** 1.0  
**Date:** 2026-10-16

## Schema

### users
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_users_email ON users(email);
```

### projects
```sql
CREATE TABLE projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    name VARCHAR(255) NOT NULL,
    allowed_urls TEXT NOT NULL,  -- JSON array
    settings TEXT,               -- JSON config
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
CREATE INDEX idx_projects_user ON projects(user_id);
```

### test_suites
```sql
CREATE TABLE test_suites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
);
CREATE INDEX idx_suites_project ON test_suites(project_id);
```

### test_cases
```sql
CREATE TABLE test_cases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    suite_id INTEGER NOT NULL,
    title VARCHAR(255) NOT NULL,
    code TEXT NOT NULL,  -- Playwright test code
    tags TEXT,           -- JSON array
    status VARCHAR(50) DEFAULT 'draft',  -- draft, approved
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (suite_id) REFERENCES test_suites(id) ON DELETE CASCADE
);
CREATE INDEX idx_tests_suite ON test_cases(suite_id);
CREATE INDEX idx_tests_status ON test_cases(status);
```

### test_runs
```sql
CREATE TABLE test_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    test_id INTEGER NOT NULL,
    status VARCHAR(50) NOT NULL,  -- PENDING, RUNNING, PASSED, FAILED, TIMEOUT, ERROR
    duration_ms INTEGER,
    error_message TEXT,
    browser_version VARCHAR(100),
    playwright_version VARCHAR(50),
    retry_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    FOREIGN KEY (test_id) REFERENCES test_cases(id) ON DELETE CASCADE
);
CREATE INDEX idx_runs_test ON test_runs(test_id);
CREATE INDEX idx_runs_status ON test_runs(status);
CREATE INDEX idx_runs_created ON test_runs(created_at DESC);
```

### artifacts
```sql
CREATE TABLE artifacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id INTEGER NOT NULL,
    type VARCHAR(50) NOT NULL,  -- screenshot, trace, console_log, network_log
    file_path VARCHAR(500) NOT NULL,
    file_size INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (run_id) REFERENCES test_runs(id) ON DELETE CASCADE
);
CREATE INDEX idx_artifacts_run ON artifacts(run_id);
CREATE INDEX idx_artifacts_type ON artifacts(type);
```

### diagnoses
```sql
CREATE TABLE diagnoses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id INTEGER NOT NULL,
    cause VARCHAR(255),
    evidence TEXT,       -- JSON array of evidence items
    recommended_fix TEXT,
    confidence VARCHAR(50),  -- high, medium, low
    ai_enhanced BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (run_id) REFERENCES test_runs(id) ON DELETE CASCADE
);
CREATE INDEX idx_diagnoses_run ON diagnoses(run_id);
```

### audit_events
```sql
CREATE TABLE audit_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    event_type VARCHAR(100) NOT NULL,  -- login, test_run, project_create, etc.
    resource_type VARCHAR(50),
    resource_id INTEGER,
    details TEXT,  -- JSON
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);
CREATE INDEX idx_audit_user ON audit_events(user_id);
CREATE INDEX idx_audit_type ON audit_events(event_type);
CREATE INDEX idx_audit_created ON audit_events(created_at DESC);
```

## Relationships

```
users (1) ──→ (N) projects
projects (1) ──→ (N) test_suites
test_suites (1) ──→ (N) test_cases
test_cases (1) ──→ (N) test_runs
test_runs (1) ──→ (N) artifacts
test_runs (1) ──→ (1) diagnoses
users (1) ──→ (N) audit_events
```

## Data Constraints

- `users.email`: Valid email format, unique
- `projects.allowed_urls`: Non-empty JSON array of valid URLs
- `test_cases.code`: Non-empty Playwright test
- `test_runs.status`: Enum: PENDING | RUNNING | PASSED | FAILED | TIMEOUT | ERROR
- `artifacts.type`: Enum: screenshot | trace | console_log | network_log

## Migrations

Use Alembic for schema versioning:

```bash
alembic init migrations
alembic revision --autogenerate -m "Initial schema"
alembic upgrade head
```

## Example Queries

### Get test pass rate for project
```sql
SELECT 
    COUNT(*) FILTER (WHERE tr.status = 'PASSED') * 100.0 / COUNT(*) as pass_rate
FROM test_runs tr
JOIN test_cases tc ON tr.test_id = tc.id
JOIN test_suites ts ON tc.suite_id = ts.id
WHERE ts.project_id = ?;
```

### Detect flaky tests (inconsistent results)
```sql
SELECT tc.id, tc.title, 
       COUNT(DISTINCT tr.status) as status_count
FROM test_cases tc
JOIN test_runs tr ON tr.test_id = tc.id
WHERE tr.created_at > datetime('now', '-7 days')
GROUP BY tc.id
HAVING status_count > 1;
```

### Get recent runs with artifacts
```sql
SELECT tr.*, a.type, a.file_path
FROM test_runs tr
LEFT JOIN artifacts a ON a.run_id = tr.id
WHERE tr.test_id = ?
ORDER BY tr.created_at DESC
LIMIT 10;
```
