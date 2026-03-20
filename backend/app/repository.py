import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock
from typing import Optional, Tuple, Union

from .schemas import JobCreate, JobRead, JobUpdate


class JobRepository:
    def __init__(self, db_path: Union[str, Path]) -> None:
        self._db_path = Path(db_path)
        self._lock = Lock()
        self._db_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize_database()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self._db_path)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize_database(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS jobs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    company TEXT NOT NULL,
                    role TEXT NOT NULL,
                    location TEXT,
                    salary_min INTEGER,
                    salary_max INTEGER,
                    status TEXT NOT NULL,
                    source_url TEXT,
                    notes TEXT,
                    applied_on TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
                """
            )
            connection.commit()

    def _row_to_job(self, row: sqlite3.Row) -> JobRead:
        return JobRead.model_validate(dict(row))

    def _job_values(self, job: JobRead) -> Tuple[object, ...]:
        return (
            job.company,
            job.role,
            job.location,
            job.salary_min,
            job.salary_max,
            job.status.value,
            str(job.source_url) if job.source_url is not None else None,
            job.notes,
            job.applied_on.isoformat() if job.applied_on is not None else None,
            job.created_at.isoformat(),
            job.updated_at.isoformat(),
        )

    def list(self) -> list[JobRead]:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT id, company, role, location, salary_min, salary_max, status,
                       source_url, notes, applied_on, created_at, updated_at
                FROM jobs
                ORDER BY created_at DESC, id DESC
                """
            ).fetchall()
        return [self._row_to_job(row) for row in rows]

    def get(self, job_id: int) -> Optional[JobRead]:
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT id, company, role, location, salary_min, salary_max, status,
                       source_url, notes, applied_on, created_at, updated_at
                FROM jobs
                WHERE id = ?
                """,
                (job_id,),
            ).fetchone()
        return self._row_to_job(row) if row is not None else None

    def create(self, payload: JobCreate) -> JobRead:
        now = datetime.now(timezone.utc)
        job = JobRead.model_validate(
            {
                **payload.model_dump(mode="python"),
                "id": 0,
                "created_at": now,
                "updated_at": now,
            }
        )

        with self._lock, self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO jobs (
                    company, role, location, salary_min, salary_max, status,
                    source_url, notes, applied_on, created_at, updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                self._job_values(job),
            )
            job_id = int(cursor.lastrowid)
            row = connection.execute(
                """
                SELECT id, company, role, location, salary_min, salary_max, status,
                       source_url, notes, applied_on, created_at, updated_at
                FROM jobs
                WHERE id = ?
                """,
                (job_id,),
            ).fetchone()
            connection.commit()

        if row is None:
            raise RuntimeError("Created job could not be reloaded from the database")
        return self._row_to_job(row)

    def update(self, job_id: int, payload: JobUpdate) -> Optional[JobRead]:
        current = self.get(job_id)
        if current is None:
            return None

        merged = JobRead.model_validate(
            {
                **current.model_dump(mode="python"),
                **payload.model_dump(mode="python", exclude_unset=True),
                "updated_at": datetime.now(timezone.utc),
            }
        )

        with self._lock, self._connect() as connection:
            connection.execute(
                """
                UPDATE jobs
                SET company = ?, role = ?, location = ?, salary_min = ?, salary_max = ?,
                    status = ?, source_url = ?, notes = ?, applied_on = ?,
                    created_at = ?, updated_at = ?
                WHERE id = ?
                """,
                (*self._job_values(merged), job_id),
            )
            row = connection.execute(
                """
                SELECT id, company, role, location, salary_min, salary_max, status,
                       source_url, notes, applied_on, created_at, updated_at
                FROM jobs
                WHERE id = ?
                """,
                (job_id,),
            ).fetchone()
            connection.commit()

        return self._row_to_job(row) if row is not None else None

    def delete(self, job_id: int) -> bool:
        with self._lock, self._connect() as connection:
            cursor = connection.execute("DELETE FROM jobs WHERE id = ?", (job_id,))
            connection.commit()
        return cursor.rowcount > 0
