import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_for_activity_success():
    response = client.post("/activities/Chess Club/signup?email=testuser@mergington.edu")
    assert response.status_code == 200
    assert "Signed up testuser@mergington.edu for Chess Club" in response.json().get("message", "")

    # Clean up: remove test user
    client.delete("/activities/Chess Club/unregister?email=testuser@mergington.edu")

def test_signup_for_activity_duplicate():
    # First signup
    client.post("/activities/Programming Class/signup?email=dupe@mergington.edu")
    # Duplicate signup
    response = client.post("/activities/Programming Class/signup?email=dupe@mergington.edu")
    assert response.status_code == 400
    assert "already signed up" in response.json().get("detail", "")
    # Clean up
    client.delete("/activities/Programming Class/unregister?email=dupe@mergington.edu")

def test_unregister_participant():
    # Add then remove
    client.post("/activities/Gym Class/signup?email=remove@mergington.edu")
    response = client.delete("/activities/Gym Class/unregister?email=remove@mergington.edu")
    assert response.status_code == 200
    assert "Removed remove@mergington.edu from Gym Class" in response.json().get("message", "")

def test_unregister_nonexistent_participant():
    response = client.delete("/activities/Art Club/unregister?email=notfound@mergington.edu")
    assert response.status_code == 404
    assert "Participant not found" in response.json().get("detail", "")
