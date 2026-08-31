import pytest
import uuid
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_create_room_success():
    """
    Testa cadastro bem-sucedido de salas com payload correto.
    """
    headers = {"Authorization": "Bearer mock-token"}
    room_name = f"Sala-{str(uuid.uuid4())[:8]}"
    payload = {
        "block_id": "Bloco D",
        "name": room_name,
        "capacity": 35,
        "room_type": "common",
        "is_accessible": True,
        "features": ["projector"]
    }
    
    response = client.post("/api/v1/rooms", json=payload, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == room_name
    assert data["capacity"] == 35


def test_create_room_invalid_capacity():
    """
    Testa rejeição automática se a capacidade for <= 0.
    """
    headers = {"Authorization": "Bearer mock-token"}
    payload = {
        "block_id": "Bloco D",
        "name": "Sala Inválida",
        "capacity": 0,
        "room_type": "common",
        "is_accessible": True,
        "features": []
    }
    
    response = client.post("/api/v1/rooms", json=payload, headers=headers)
    assert response.status_code == 422
    assert "capacity" in response.text


def test_delete_room_success():
    """
    Testa exclusão bem-sucedida de salas física.
    """
    headers = {"Authorization": "Bearer mock-token"}
    room_name = f"Sala-Del-{str(uuid.uuid4())[:8]}"
    create_res = client.post("/api/v1/rooms", json={
        "block_id": "Bloco D",
        "name": room_name,
        "capacity": 30,
        "room_type": "common",
        "is_accessible": True,
        "features": []
    }, headers=headers)
    assert create_res.status_code == 201
    room_id = create_res.json()["id"]
    
    response = client.delete(f"/api/v1/rooms/{room_id}", headers=headers)
    assert response.status_code == 200
