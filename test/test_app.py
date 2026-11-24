
import pytest

import database
from app import app


@pytest.fixture
def client(tmp_path, monkeypatch):
    # Use a separate temporary database for each test.
    test_db = tmp_path / "test_sessions.db"

    monkeypatch.setattr(
        database,
        "DATABASE_PATH",
        str(test_db)
    )

    database.init_db()

    app.config["TESTING"] = True

    with app.test_client() as test_client:
        yield test_client


def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json["status"] == "success"


def test_get_sessions_empty(client):
    response = client.get("/sessions")

    assert response.status_code == 200
    assert response.json["count"] == 0
    assert response.json["sessions"] == []


def test_create_session(client):
    session = {
        "title": "Morning Meditation",
        "description": "A guided meditation",
        "category": "Meditation",
        "duration": 30
    }

    response = client.post("/sessions", json=session)

    assert response.status_code == 201
    assert response.json["session"]["title"] == session["title"]

    get_response = client.get("/sessions")

    assert get_response.status_code == 200
    assert get_response.json["count"] == 1
    assert get_response.json["sessions"][0]["duration"] == 30


def test_missing_title(client):
    session = {
        "description": "A guided meditation",
        "category": "Meditation",
        "duration": 30
    }

    response = client.post("/sessions", json=session)

    assert response.status_code == 400
    assert "title" in response.json["error"]


def test_negative_duration(client):
    session = {
        "title": "Morning Meditation",
        "description": "A guided meditation",
        "category": "Meditation",
        "duration": -30
    }

    response = client.post("/sessions", json=session)

    assert response.status_code == 400
    assert "duration" in response.json["error"]


def test_empty_title(client):
    session = {
        "title": "   ",
        "description": "A guided meditation",
        "category": "Meditation",
        "duration": 30
    }

    response = client.post("/sessions", json=session)

    assert response.status_code == 400


def test_boolean_duration(client):
    session = {
        "title": "Morning Meditation",
        "description": "A guided meditation",
        "category": "Meditation",
        "duration": True
    }

    response = client.post("/sessions", json=session)

    assert response.status_code == 400
