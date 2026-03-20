# Job Tracker App

Job Tracker App is a backend MVP for tracking job applications and the progress of each opportunity through the hiring pipeline.

## Goal

Build an application that helps users stay organized during a job search by supporting:
- storing job opportunities with core details such as company, role, status, and notes
- tracking application stages from `saved` to `applied`, `interview`, `offer`, or `rejected`
- expanding later into dashboards, reminders, and analytics

## Current Scope

- `backend/`: FastAPI-based REST API MVP with SQLite persistence
- `docs/implementation-plan.md`: step-by-step roadmap for the next phases

## Quickstart

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
PYTHONPATH=backend pytest backend/tests
uvicorn app.main:app --app-dir backend --reload
```

The API will be available at `http://127.0.0.1:8000`.
Interactive API documentation is available at `http://127.0.0.1:8000/docs`.

By default, the API stores data in `backend/data/job_tracker.db`.
You can override the database location with `DATABASE_URL=sqlite:////absolute/path/to/job_tracker.db`.

## Available Endpoints

- `GET /health`
- `GET /api/jobs`
- `POST /api/jobs`
- `GET /api/jobs/{job_id}`
- `PATCH /api/jobs/{job_id}`
- `DELETE /api/jobs/{job_id}`

## Current Architecture

- FastAPI application with a small, focused CRUD API
- Pydantic schemas for request and response validation
- SQLite-backed repository with local file persistence
- Environment-based configuration via `DATABASE_URL` and `APP_ENV`
- API tests covering CRUD, persistence, and validation rules

## Next Steps

1. Add SQLAlchemy and Alembic migrations for a more scalable data layer
2. Introduce authentication and user scoping
3. Build a React + TypeScript frontend
4. Add filtering, sorting, and search for the jobs list
5. Add CI for linting, testing, and builds
6. Prepare deployment for staging and production
