"""
Testes de integração para as rotas REST da tabela de subslots de horários e intervalos (subslot_time_intervals).
"""

import pytest
import uuid
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)
AUTH_HEADERS = {"Authorization": "Bearer mock-token"}


def test_list_subslots_default_seed():
    """Testa a listagem inicial dos subslots padrão gerados no seed."""
    res = client.get("/api/v1/subslots", headers=AUTH_HEADERS)
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert len(data) >= 18

    # Verificar subslots do turno matutino
    matutino_slots = [s for s in data if s["shift"] == "matutino"]
    assert len(matutino_slots) == 7
    
    # Validar aula M1 (07:00 - 07:50)
    m1 = next((s for s in matutino_slots if s["code"] == "M1"), None)
    assert m1 is not None
    assert m1["start_time"] == "07:00"
    assert m1["end_time"] == "07:50"
    assert m1["is_interval"] is False
    assert m1["class_number"] == 1

    # Validar intervalo M_INT (09:30 - 09:45)
    m_int = next((s for s in matutino_slots if s["code"] == "M_INT"), None)
    assert m_int is not None
    assert m_int["start_time"] == "09:30"
    assert m_int["end_time"] == "09:45"
    assert m_int["is_interval"] is True
    assert m_int["class_number"] is None


def test_list_subslots_filter_by_shift():
    """Testa a filtragem de subslots por turno (matutino, vespertino, noturno)."""
    res_vesp = client.get("/api/v1/subslots?shift=vespertino", headers=AUTH_HEADERS)
    assert res_vesp.status_code == 200
    vesp_slots = res_vesp.json()
    assert len(vesp_slots) == 7
    assert all(s["shift"] == "vespertino" for s in vesp_slots)

    # Validar aula T4 (15:45 - 16:35)
    t4 = next((s for s in vesp_slots if s["code"] == "T4"), None)
    assert t4 is not None
    assert t4["start_time"] == "15:45"
    assert t4["end_time"] == "16:35"


def test_create_and_delete_custom_subslot():
    """Testa a criação, atualização e exclusão de um subslot customizado via API REST."""
    unique_code = f"M{str(uuid.uuid4())[:4].upper()}"
    payload = {
        "code": unique_code,
        "shift": "matutino",
        "class_number": 6,
        "start_time": "11:25",
        "end_time": "12:15",
        "is_interval": False
    }

    # 1. Criar subslot
    res_create = client.post("/api/v1/subslots", json=payload, headers=AUTH_HEADERS)
    assert res_create.status_code == 201
    created_data = res_create.json()
    assert created_data["code"] == unique_code
    subslot_id = created_data["id"]

    # 2. Conflito por código duplicado -> 409 Conflict
    res_dup = client.post("/api/v1/subslots", json=payload, headers=AUTH_HEADERS)
    assert res_dup.status_code == 409

    # 3. Atualizar subslot
    update_payload = {"end_time": "12:20"}
    res_update = client.put(f"/api/v1/subslots/{subslot_id}", json=update_payload, headers=AUTH_HEADERS)
    assert res_update.status_code == 200
    assert res_update.json()["end_time"] == "12:20"

    # 4. Excluir subslot
    res_delete = client.delete(f"/api/v1/subslots/{subslot_id}", headers=AUTH_HEADERS)
    assert res_delete.status_code == 204

    # 5. Confirmar exclusão -> GET por ID ou verificação
    res_check = client.get("/api/v1/subslots", headers=AUTH_HEADERS)
    assert not any(s["id"] == subslot_id for s in res_check.json())


def test_subslot_unauthorized():
    """Testa tentativa de chamada sem autenticação."""
    res = client.get("/api/v1/subslots")
    assert res.status_code == 401
