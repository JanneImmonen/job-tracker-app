from fastapi.encoders import jsonable_encoder
from fastapi import FastAPI, HTTPException, Request, Response, status
from pydantic import ValidationError
from typing import Optional

from .config import load_config
from .repository import JobRepository
from .schemas import JobCreate, JobRead, JobUpdate


def create_app(repository: Optional[JobRepository] = None) -> FastAPI:
    app = FastAPI(title="Job Tracker API", version="0.2.0")
    if repository is None:
        config = load_config()
        repository = JobRepository(config.database_path)
    app.state.repo = repository

    def get_repository(request: Request) -> JobRepository:
        return request.app.state.repo

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/api/jobs", response_model=list[JobRead])
    def list_jobs(request: Request) -> list[JobRead]:
        return get_repository(request).list()

    @app.post("/api/jobs", response_model=JobRead, status_code=status.HTTP_201_CREATED)
    def create_job(payload: JobCreate, request: Request) -> JobRead:
        return get_repository(request).create(payload)

    @app.get("/api/jobs/{job_id}", response_model=JobRead)
    def get_job(job_id: int, request: Request) -> JobRead:
        job = get_repository(request).get(job_id)
        if job is None:
            raise HTTPException(status_code=404, detail="Job not found")
        return job

    @app.patch("/api/jobs/{job_id}", response_model=JobRead)
    def patch_job(job_id: int, payload: JobUpdate, request: Request) -> JobRead:
        try:
            job = get_repository(request).update(job_id, payload)
        except ValidationError as exc:
            raise HTTPException(status_code=422, detail=jsonable_encoder(exc.errors())) from exc
        if job is None:
            raise HTTPException(status_code=404, detail="Job not found")
        return job

    @app.delete("/api/jobs/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
    def delete_job(job_id: int, request: Request) -> Response:
        deleted = get_repository(request).delete(job_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Job not found")
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    return app


app = create_app()
