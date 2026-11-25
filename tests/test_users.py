import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.database import Base, get_db
from app.main import app

@pytest.fixture()
def client():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSession()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)
    engine.dispose()

def sample_user(email="student@example.com"):
    return {
        "full_name": "Test Student",
        "email": email,
        "password": "StrongPassword123!",
        "phone_number": "+919876543210",
    }

def test_register_and_list_users(client):
    response = client.post("/users/register", json=sample_user())
    assert response.status_code == 201
    assert response.json()["email"] == "student@example.com"
    assert "password_hash" not in response.json()
    assert client.get("/users").status_code == 200
    assert len(client.get("/users").json()) == 1

def test_duplicate_email(client):
    client.post("/users/register", json=sample_user())
    response = client.post("/users/register", json=sample_user())
    assert response.status_code == 409

def test_invalid_email_and_short_password(client):
    payload = sample_user()
    payload["email"] = "not-an-email"
    assert client.post("/users/register", json=payload).status_code == 422
    payload = sample_user("other@example.com")
    payload["password"] = "short"
    assert client.post("/users/register", json=payload).status_code == 422

def test_get_update_delete_user(client):
    created = client.post("/users/register", json=sample_user()).json()
    user_id = created["id"]
    assert client.get(f"/users/{user_id}").status_code == 200
    updated = client.put(f"/users/{user_id}", json={"full_name": "Updated Student"})
    assert updated.status_code == 200
    assert updated.json()["full_name"] == "Updated Student"
    assert client.delete(f"/users/{user_id}").status_code == 204
    assert client.get(f"/users/{user_id}").status_code == 404

def test_missing_user(client):
    assert client.get("/users/9999").status_code == 404
