from pathlib import Path
from tempfile import TemporaryDirectory

from app.main import create_app
from app.repository import JobRepository
from fastapi.testclient import TestClient


def create_client(db_path: Path) -> TestClient:
    return TestClient(create_app(repository=JobRepository(db_path)))


def test_healthcheck() -> None:
    with TemporaryDirectory() as tmp_dir:
        with create_client(Path(tmp_dir) / "jobs.db") as client:
            response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_list_update_and_delete_job() -> None:
    with TemporaryDirectory() as tmp_dir:
        with create_client(Path(tmp_dir) / "jobs.db") as client:
            create_response = client.post(
                "/api/jobs",
                json={
                    "company": "OpenAI",
                    "role": "Software Engineer",
                    "location": "Remote",
                    "status": "saved",
                    "source_url": "https://openai.com/careers",
                },
            )
            assert create_response.status_code == 201
            created = create_response.json()
            assert created["id"] > 0
            assert created["company"] == "OpenAI"

            list_response = client.get("/api/jobs")
            assert list_response.status_code == 200
            assert any(job["id"] == created["id"] for job in list_response.json())

            patch_response = client.patch(
                f"/api/jobs/{created['id']}",
                json={
                    "status": "interview",
                    "applied_on": "2026-03-20",
                    "notes": "Recruiter call scheduled",
                },
            )
            assert patch_response.status_code == 200
            assert patch_response.json()["status"] == "interview"

            clear_notes_response = client.patch(
                f"/api/jobs/{created['id']}",
                json={"notes": None},
            )
            assert clear_notes_response.status_code == 200
            assert clear_notes_response.json()["notes"] is None

            delete_response = client.delete(f"/api/jobs/{created['id']}")
            assert delete_response.status_code == 204

            missing_response = client.get(f"/api/jobs/{created['id']}")
            assert missing_response.status_code == 404


def test_jobs_persist_across_app_instances() -> None:
    with TemporaryDirectory() as tmp_dir:
        database_path = Path(tmp_dir) / "jobs.db"

        with create_client(database_path) as first_client:
            create_response = first_client.post(
                "/api/jobs",
                json={
                    "company": "Anthropic",
                    "role": "Backend Engineer",
                    "status": "applied",
                    "applied_on": "2026-03-18",
                },
            )

        assert create_response.status_code == 201
        created_id = create_response.json()["id"]

        with create_client(database_path) as second_client:
            list_response = second_client.get("/api/jobs")

    assert list_response.status_code == 200
    assert [job["id"] for job in list_response.json()] == [created_id]


def test_list_jobs_supports_filtering_search_and_sorting() -> None:
    with TemporaryDirectory() as tmp_dir:
        with create_client(Path(tmp_dir) / "jobs.db") as client:
            seed_jobs = [
                {
                    "company": "OpenAI",
                    "role": "Platform Engineer",
                    "location": "Remote",
                    "status": "saved",
                    "notes": "Interesting infrastructure role",
                },
                {
                    "company": "Anthropic",
                    "role": "Research Engineer",
                    "location": "London",
                    "status": "applied",
                    "applied_on": "2026-03-10",
                    "notes": "Strong fit for reasoning systems",
                },
                {
                    "company": "GitHub",
                    "role": "Developer Advocate",
                    "location": "Remote",
                    "status": "interview",
                    "applied_on": "2026-03-05",
                    "notes": "Developer tooling and community work",
                },
            ]

            for job in seed_jobs:
                create_response = client.post("/api/jobs", json=job)
                assert create_response.status_code == 201

            applied_response = client.get("/api/jobs", params={"status": "applied"})
            assert applied_response.status_code == 200
            assert [job["company"] for job in applied_response.json()] == ["Anthropic"]

            company_response = client.get("/api/jobs", params={"company": "hub"})
            assert company_response.status_code == 200
            assert [job["company"] for job in company_response.json()] == ["GitHub"]

            search_response = client.get("/api/jobs", params={"q": "engineer"})
            assert search_response.status_code == 200
            assert [job["company"] for job in search_response.json()] == ["Anthropic", "OpenAI"]

            sort_response = client.get(
                "/api/jobs",
                params={"sort_by": "company", "order": "asc"},
            )
            assert sort_response.status_code == 200
            assert [job["company"] for job in sort_response.json()] == [
                "Anthropic",
                "GitHub",
                "OpenAI",
            ]


def test_create_job_rejects_invalid_business_rules() -> None:
    with TemporaryDirectory() as tmp_dir:
        with create_client(Path(tmp_dir) / "jobs.db") as client:
            missing_applied_on_response = client.post(
                "/api/jobs",
                json={
                    "company": "OpenAI",
                    "role": "Engineer",
                    "status": "applied",
                },
            )
            invalid_salary_response = client.post(
                "/api/jobs",
                json={
                    "company": "OpenAI",
                    "role": "Engineer",
                    "salary_min": 6000,
                    "salary_max": 5000,
                },
            )

    assert missing_applied_on_response.status_code == 422
    assert invalid_salary_response.status_code == 422


def test_patch_job_rejects_invalid_merged_state() -> None:
    with TemporaryDirectory() as tmp_dir:
        with create_client(Path(tmp_dir) / "jobs.db") as client:
            create_response = client.post(
                "/api/jobs",
                json={
                    "company": "OpenAI",
                    "role": "Engineer",
                    "status": "saved",
                },
            )
            assert create_response.status_code == 201

            job_id = create_response.json()["id"]
            patch_response = client.patch(
                f"/api/jobs/{job_id}",
                json={"status": "offer"},
            )

    assert patch_response.status_code == 422
