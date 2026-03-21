# Job Tracker App

Job Tracker App is a backend MVP for tracking job applications and the progress of each opportunity through the hiring pipeline.

## Goal

Build an application that helps users stay organized during a job search by supporting:
- storing job opportunities with core details such as company, role, status, and notes
- tracking application stages from `saved` to `applied`, `interview`, `offer`, or `rejected`
- expanding later into dashboards, reminders, and analytics

## Current Scope

- `backend/`: FastAPI-based REST API MVP with SQLite persistence
- `frontend/`: React + TypeScript dashboard MVP powered by Vite
- `docs/implementation-plan.md`: step-by-step roadmap for the next phases

## Quickstart

This project targets Python `3.12.x` and includes a pinned `.python-version` for local tooling such as `pyenv`.

Backend:
```bash
python3 -m venv .venv
source .venv/bin/activate
python --version
pip install -r backend/requirements.txt
ruff check .
ruff format --check .
DATABASE_URL=sqlite:////tmp/job-tracker-local.db PYTHONPATH=backend pytest -p no:cacheprovider backend/tests
uvicorn app.main:app --app-dir backend --reload
```

Make sure `python --version` reports Python `3.12.x` before installing dependencies.

Frontend:
```bash
cd frontend
node --version
npm install
npm run build
npm run dev
```

The frontend expects the API at `http://127.0.0.1:8000` by default.
You can override it with `VITE_API_BASE_URL` or copy `frontend/.env.example` to a local `.env`.
Make sure `node --version` reports at least `v22.12.0`.

The API will be available at `http://127.0.0.1:8000`.
Interactive API documentation is available at `http://127.0.0.1:8000/docs`.
The frontend dev server runs at `http://127.0.0.1:5173`.

By default, the API stores data in `backend/data/job_tracker.db`.
You can override the database location with `DATABASE_URL=sqlite:////absolute/path/to/job_tracker.db`.

## Available Endpoints

- `GET /health`
- `GET /api/jobs`
- `GET /api/jobs?status=applied&company=open&q=engineer&sort_by=company&order=asc`
- `POST /api/jobs`
- `GET /api/jobs/{job_id}`
- `PATCH /api/jobs/{job_id}`
- `DELETE /api/jobs/{job_id}`

## Current Architecture

- FastAPI backend with a small, focused CRUD API
- React + TypeScript frontend for job management
- Pydantic schemas for request and response validation
- SQLite-backed repository with local file persistence
- Queryable job list with filtering, search, and sorting
- Environment-based configuration via `DATABASE_URL` and `APP_ENV`
- Ruff linting and formatting checks
- API tests covering CRUD, persistence, and validation rules
- Vite-powered frontend build pipeline

## Next Steps

1. Add SQLAlchemy and Alembic migrations for a more scalable data layer
2. Introduce authentication and user scoping
3. Add delete actions and richer job detail views in the frontend
4. Add pagination and richer dashboard metrics
5. Add pre-commit hooks for local quality checks
6. Prepare deployment for staging and production
