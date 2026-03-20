# Implementation plan

## Phase 1 - API MVP (done in this commit)
- FastAPI service + healthcheck
- Job CRUD endpoints
- Unit and integration tests for the API

## Phase 2 - Data layer
- Replace the in-memory repository with a SQLAlchemy or SQLModel implementation
- Alembic migrations
- Environment-based config (`DATABASE_URL`, `APP_ENV`)

## Phase 3 - Frontend MVP
- React + TypeScript UI
- Job list + create/edit form + status badges
- API client layer

## Phase 4 - Product quality
- Authentication and user scoping
- Filtering, sorting, and search
- Dashboard metrics (applications per week, response rate)
- Observability: structured logging + error tracking

## Phase 5 - Delivery
- Docker images
- CI pipeline
- Staging + production deployment
