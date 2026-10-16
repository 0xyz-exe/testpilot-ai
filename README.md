# TestPilot AI

AI-powered Playwright testing platform with failure diagnosis.

## Quick Start

### Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install fastapi uvicorn sqlalchemy pydantic pydantic-settings python-multipart passlib bcrypt
python -c "from database import init_db; init_db()"
python main.py
```

Backend: http://localhost:8000

### Test

```bash
curl http://localhost:8000/health
```

## Status

**Phase:** Milestone B (Core Implementation)

**Complete:**
- ✅ Requirements & architecture docs
- ✅ Database models
- ✅ Auth (register/login, bcrypt)
- ✅ Project CRUD routes
- ✅ URL validation & SSRF prevention

**Next:**
- Test execution worker
- Frontend React app
- Artifact storage

## Docs

- [PRD](docs/PRD.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Threat Model](docs/THREAT_MODEL.md)

## Note

Python 3.14 has limited package support. Use Python 3.11 or 3.12 for production.
