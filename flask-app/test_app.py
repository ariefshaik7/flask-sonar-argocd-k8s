import pytest
from app import app

@pytest.fixture
def client():
    app.testing = True
    return app.test_client()

def test_get_empty_tasks(client):
    response = client.get('/tasks')
    assert response.status_code == 200
    assert response.json == []

def test_add_task(client):
    response = client.post('/tasks', json={"task": "Buy milk"})
    assert response.status_code == 201
    assert response.json["message"] == "Task added"

def test_get_tasks_after_adding(client):
    client.post('/tasks', json={"task": "Buy eggs"})
    response = client.get('/tasks')
    assert response.status_code == 200
    assert "Buy eggs" in response.json

def test_delete_task(client):
    client.post('/tasks', json={"task": "Test delete"})
    response = client.delete('/tasks/0')
    assert response.status_code == 200
    assert response.json["message"] == "Task deleted"

def test_delete_invalid_task(client):
    response = client.delete('/tasks/999')
    assert response.status_code == 404
    assert response.json["error"] == "Invalid task ID"
