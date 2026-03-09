from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_healthcheck() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_list_update_and_delete_job() -> None:
    payload = {
        "company": "OpenAI",
        "role": "Software Engineer",
        "location": "Remote",
        "status": "saved",
    }

    create_response = client.post("/api/jobs", json=payload)
    assert create_response.status_code == 201
    created = create_response.json()
    assert created["id"] > 0
    assert created["company"] == "OpenAI"

    list_response = client.get("/api/jobs")
    assert list_response.status_code == 200
    assert any(job["id"] == created["id"] for job in list_response.json())

    patch_response = client.patch(
        f"/api/jobs/{created['id']}",
        json={"status": "interview", "notes": "Recruiter call scheduled"},
    )
    assert patch_response.status_code == 200
    assert patch_response.json()["status"] == "interview"

    delete_response = client.delete(f"/api/jobs/{created['id']}")
    assert delete_response.status_code == 204

    missing_response = client.get(f"/api/jobs/{created['id']}")
    assert missing_response.status_code == 404
