# Job Tracker App

Tämä repository sisältää **teknisesti hyvän lähtöpohjan** job-tracker-sovellukselle.

## Tavoite
Rakentaa sovellus, jolla työnhaku pysyy hallinnassa:
- työpaikkojen tallennus (company, role, status, muistiinpanot)
- hakuprosessin vaiheet (saved → applied → interview → offer/rejected)
- myöhemmin: dashboard, reminderit, analytiikka

## Nykyinen sisältö
- `backend/`: FastAPI-pohjainen REST API (MVP)
- `docs/implementation-plan.md`: vaiheittainen toteutussuunnitelma

## Quickstart
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
PYTHONPATH=backend pytest backend/tests
uvicorn app.main:app --app-dir backend --reload
```

API on tällöin osoitteessa `http://127.0.0.1:8000`.

## Ensimmäiset endpointit
- `GET /health`
- `GET /api/jobs`
- `POST /api/jobs`
- `GET /api/jobs/{job_id}`
- `PATCH /api/jobs/{job_id}`
- `DELETE /api/jobs/{job_id}`

## Seuraavat askeleet
1. Persistenssi SQLite/PostgreSQL + Alembic-migraatiot
2. Auth (esim. Clerk/Supabase Auth/JWT)
3. Frontend (React + TypeScript)
4. CI (lint + testit + build)
5. Deploy (Render/Fly/Vercel + managed DB)
