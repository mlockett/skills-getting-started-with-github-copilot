import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_root_redirect():
    response = client.get("/")
    assert response.status_code == 200 or response.status_code == 307
    # Should redirect to /static/index.html or serve HTML

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Tennis Club" in data

def test_signup_for_activity():
    # Use a unique email to avoid duplicate error
    test_email = "pytestuser@mergington.edu"
    activity = "Tennis Club"
    # Always try to unregister first to ensure a clean state
    client.post(f"/activities/{activity}/unregister?email={test_email}")
    response = client.post(f"/activities/{activity}/signup?email={test_email}")
    assert response.status_code == 200
    assert "Signed up" in response.json().get("message", "")

def test_signup_duplicate():
    activity = "Tennis Club"
    email = "pytestuser@mergington.edu"
    # Sign up once
    client.post(f"/activities/{activity}/signup?email={email}")
    # Try duplicate
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    assert "already signed up" in response.json().get("detail", "")