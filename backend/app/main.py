from fastapi import FastAPI, HTTPException, Response, status

from .repository import JobRepository
from .schemas import JobCreate, JobRead, JobUpdate

app = FastAPI(title="Job Tracker API", version="0.1.0")
repo = JobRepository()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/jobs", response_model=list[JobRead])
def list_jobs() -> list[JobRead]:
    return repo.list()


@app.post("/api/jobs", response_model=JobRead, status_code=status.HTTP_201_CREATED)
def create_job(payload: JobCreate) -> JobRead:
    return repo.create(payload)


@app.get("/api/jobs/{job_id}", response_model=JobRead)
def get_job(job_id: int) -> JobRead:
    job = repo.get(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@app.patch("/api/jobs/{job_id}", response_model=JobRead)
def patch_job(job_id: int, payload: JobUpdate) -> JobRead:
    job = repo.update(job_id, payload)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@app.delete("/api/jobs/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job(job_id: int) -> Response:
    deleted = repo.delete(job_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Job not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
