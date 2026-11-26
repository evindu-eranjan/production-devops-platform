
import os

# Test environment database settings
os.environ["DB_HOST"] = "localhost"
os.environ["DB_PORT"] = "5432"
os.environ["DB_NAME"] = "testdb"
os.environ["DB_USER"] = "testuser"
os.environ["DB_PASSWORD"] = "testpassword"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db
from app.models import TaskDB


# SQLite test database
TEST_DATABASE_URL = "sqlite://"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine
)


# Override PostgreSQL dependency with SQLite
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


# Prepare a fresh database before each test
@pytest.fixture(autouse=True)
def prepare_test_database():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    db = TestingSessionLocal()

    db.add(TaskDB(
        id=1,
        title="Master Pytest",
        description="Learn automated testing",
        completed=False
    ))

    db.commit()
    db.close()

    yield

    Base.metadata.drop_all(bind=test_engine)


def test_home_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Task Management API is running!",
        "status": "success"
    }


def test_get_all_tasks():
    response = client.get("/tasks")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_task_by_id():
    response = client.get("/tasks/1")
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Master Pytest"


def test_create_task():
    task_data = {
        "title": "Learn Pytest",
        "description": "Practice automated API testing",
        "completed": False
    }

    response = client.post("/tasks", json=task_data)

    assert response.status_code == 201

    data = response.json()
    assert data["title"] == "Learn Pytest"
    assert data["description"] == "Practice automated API testing"
    assert data["completed"] is False
    assert "id" in data


def test_update_task():
    task_data = {
        "title": "Master Pytest",
        "description": "Learn production-level automated testing",
        "completed": True
    }

    response = client.put("/tasks/1", json=task_data)

    assert response.status_code == 200

    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Master Pytest"
    assert data["description"] == "Learn production-level automated testing"
    assert data["completed"] is True


def test_partial_update_task():
    update_data = {"completed": False}

    response = client.patch("/tasks/1", json=update_data)

    assert response.status_code == 200

    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Master Pytest"
    assert data["completed"] is False


def test_delete_task():
    response = client.delete("/tasks/1")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Task deleted successfully",
        "task_id": 1
    }
