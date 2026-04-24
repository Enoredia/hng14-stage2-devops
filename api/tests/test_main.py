import sys
from pathlib import Path
from fastapi.testclient import TestClient

import main


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


client = TestClient(main.app)

class MockRedis:
    def __init__(self):
        self.hashes = {}
        self.queues = []

    def ping(self):
        return True

    def hset(self, name, key=None, value=None, mapping=None):
        if name not in self.hashes:
            self.hashes[name] = {}

        if mapping:
            self.hashes[name].update(mapping)
        else:
            self.hashes[name][key] = value

        return 1

    def hget(self, name, key):
        return self.hashes.get(name, {}).get(key)

    def lpush(self, queue_name, value):
        self.queues.append((queue_name, value))
        return len(self.queues)


def setup_function():
    main.r = MockRedis()


def test_health_returns_healthy():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_create_job_returns_job_id_and_queued_status():
    response = client.post("/jobs")
    data = response.json()

    assert response.status_code == 200
    assert "job_id" in data
    assert data["status"] == "queued"


def test_get_existing_job_returns_status():
    create_response = client.post("/jobs")
    job_id = create_response.json()["job_id"]

    response = client.get(f"/jobs/{job_id}")

    assert response.status_code == 200
    assert response.json() == {
        "job_id": job_id,
        "status": "queued"
    }


def test_get_missing_job_returns_404():
    response = client.get("/jobs/not-real")

    assert response.status_code == 404
