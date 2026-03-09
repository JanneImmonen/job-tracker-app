from datetime import datetime, timezone
from threading import Lock
from typing import Dict, List

from .schemas import JobCreate, JobRead, JobUpdate


class JobRepository:
    def __init__(self) -> None:
        self._jobs: Dict[int, JobRead] = {}
        self._next_id = 1
        self._lock = Lock()

    def list(self) -> List[JobRead]:
        return sorted(self._jobs.values(), key=lambda j: j.created_at, reverse=True)

    def get(self, job_id: int) -> JobRead | None:
        return self._jobs.get(job_id)

    def create(self, payload: JobCreate) -> JobRead:
        with self._lock:
            job_id = self._next_id
            self._next_id += 1

        now = datetime.now(timezone.utc)
        job = JobRead(id=job_id, created_at=now, updated_at=now, **payload.model_dump())
        self._jobs[job_id] = job
        return job

    def update(self, job_id: int, payload: JobUpdate) -> JobRead | None:
        current = self._jobs.get(job_id)
        if current is None:
            return None

        merged = current.model_copy(
            update={
                **payload.model_dump(exclude_none=True),
                "updated_at": datetime.now(timezone.utc),
            }
        )
        self._jobs[job_id] = merged
        return merged

    def delete(self, job_id: int) -> bool:
        return self._jobs.pop(job_id, None) is not None
