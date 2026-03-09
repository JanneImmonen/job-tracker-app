# Implementation plan

## Phase 1 — API MVP (done in this commit)
- FastAPI service + healthcheck
- Job CRUD endpointit
- Yksikkötestit / integraatiotestit API:lle

## Phase 2 — Data layer
- Vaihdetaan in-memory repository SQLAlchemy/SQLModel-toteutukseen
- Alembic migraatiot
- Environment-based config (`DATABASE_URL`, `APP_ENV`)

## Phase 3 — Frontend MVP
- React + TypeScript UI
- Job list + create/edit form + status badges
- API client kerros

## Phase 4 — Product quality
- Auth ja user scoping
- Filtering/sorting/search
- Dashboard metrics (applications per week, response rate)
- Observability: structured logging + error tracking

## Phase 5 — Delivery
- Docker images
- CI pipeline
- Staging + production deployment
