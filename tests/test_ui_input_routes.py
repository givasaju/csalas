import pytest
import uuid
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)
AUTH_HEADERS = {"Authorization": "Bearer test-valid-token"}

def test_ui_endpoints_html_served():
    """Garante que a rota /index.html contém os novos componentes de UI de entrada de dados."""
    res = client.get("/")
    assert res.status_code == 200
    assert "Cadastrar Sala" in res.text
    assert "Importação CSV" in res.text
    assert "Gestão de Docentes" in res.text
    assert "Restrições Docentes" in res.text
    assert "Inventário de Salas" in res.text


def test_ui_input_data_and_rooms_flow():
    """Garante que a UI consegue obter input-data e criar salas via POST /api/v1/rooms."""
    res = client.get("/api/v1/allocation/input-data", headers=AUTH_HEADERS)
    assert res.status_code == 200
    data = res.json()
    assert "rooms" in data
    assert "teachers" in data

    # Testar criação de nova sala
    room_name = f"Sala UI-{str(uuid.uuid4())[:8]}"
    new_room = {
        "block_id": "Bloco UI Teste",
        "name": room_name,
        "capacity": 30,
        "room_type": "lab",
        "is_accessible": True,
        "features": ["projetor", "ar_condicionado"]
    }
    res_post = client.post("/api/v1/rooms", json=new_room, headers=AUTH_HEADERS)
    assert res_post.status_code == 201
    created = res_post.json()
    assert created["name"] == room_name
    assert created["block_id"] == "Bloco UI Teste"

def test_ui_restrictions_and_reset():
    """Testa cadastro e reset de restrições docentes exigido pela UI."""
    req_body = {
        "teacher_id": "prof-claudio",
        "day_of_week": 2,
        "time_slot_id": "T1"
    }
    res_restr = client.post("/api/v1/allocation/restrictions", json=req_body, headers=AUTH_HEADERS)
    assert res_restr.status_code in [201, 409] # 201 se criado, 409 se já existente

    # Reset semestral
    res_reset = client.delete("/api/v1/allocation/restrictions", headers=AUTH_HEADERS)
    assert res_reset.status_code == 200
    assert "cleared_count" in res_reset.json()
