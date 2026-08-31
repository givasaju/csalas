import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.engine.core import CoreAllocationEngine

client = TestClient(app)
AUTH_HEADER = {"Authorization": "Bearer test-token"}

def test_engine_calculate_emergency_reallocation():
    rooms = [{"id": "r1", "block_id": "b1", "name": "Sala 101", "capacity": 40, "room_type": "common", "is_accessible": True, "features": []}]
    coordinations = [{"id": "eng", "name": "Engenharia", "credits": 1000}]
    restrictions = [{"id": "res1", "teacher_id": "t-sub", "day_of_week": 1, "time_slot_id": "M2"}]
    
    engine = CoreAllocationEngine(rooms, coordinations, [], restrictions=restrictions)
    
    teachers = [
        {"id": "t-ausente", "name": "Prof. Ausente", "department": "Engenharia", "subjects": ["Cálculo"]},
        {"id": "t-sub", "name": "Prof. Substituto", "department": "Engenharia", "subjects": ["Cálculo"]},
        {"id": "t-outro", "name": "Prof. Outro", "department": "Letras", "subjects": ["Inglês"]}
    ]
    
    current_allocations = [
        {"id": "c1", "teacher_id": "t-ausente", "day_of_week": 1, "shift": "M", "sub_slot": 1, "room_id": "r1"}
    ]
    
    result = engine.calculate_emergency_reallocation("t-ausente", teachers, current_allocations)
    assert result["absent_teacher_id"] == "t-ausente"
    assert result["total_affected_classes"] == 1
    assert len(result["options"]) >= 1
    assert result["options"][0]["substitutions"][0]["substitute_teacher_id"] == "t-sub"


def test_api_emergency_reallocation_endpoints():
    # 1. Testar sem token JWT (deve retornar 401)
    resp_unauth = client.post("/api/v1/emergency-reallocations/calculate", json={
        "absent_teacher_id": "prof-claudio",
        "start_date": "2026-09-01",
        "end_date": "2026-10-31",
        "mode": "assisted"
    })
    assert resp_unauth.status_code == 401

    # 2. Testar docente inexistente (deve retornar 404)
    resp_not_found = client.post("/api/v1/emergency-reallocations/calculate", json={
        "absent_teacher_id": "docente-inexistente-123",
        "start_date": "2026-09-01",
        "end_date": "2026-10-31",
        "mode": "assisted"
    }, headers=AUTH_HEADER)
    assert resp_not_found.status_code == 404

    # 3. Testar docente existente
    resp_calc = client.post("/api/v1/emergency-reallocations/calculate", json={
        "absent_teacher_id": "prof-claudio",
        "start_date": "2026-09-01",
        "end_date": "2026-10-31",
        "mode": "assisted"
    }, headers=AUTH_HEADER)
    assert resp_calc.status_code == 200
    data = resp_calc.json()
    assert data["absent_teacher_id"] == "prof-claudio"

    # 4. Efetivar realocação no Modo Assistido
    resp_commit_assisted = client.post("/api/v1/emergency-reallocations/commit", json={
        "absent_teacher_id": "prof-claudio",
        "selected_option_index": 1,
        "mode": "assisted",
        "substitutions": [
            {
                "class_id": "class-1",
                "substitute_teacher_id": "prof-isabela",
                "substitute_teacher_name": "Isabela",
                "time_slot": "M1",
                "room_id": "room-1"
            }
        ]
    }, headers=AUTH_HEADER)
    assert resp_commit_assisted.status_code == 200
    commit_data = resp_commit_assisted.json()
    assert commit_data["status"] == "success"
    assert commit_data["mode_used"] == "assisted"

    # 5. Efetivar realocação no Modo Delegado
    resp_commit_delegated = client.post("/api/v1/emergency-reallocations/commit", json={
        "absent_teacher_id": "prof-claudio",
        "selected_option_index": 1,
        "mode": "delegated",
        "substitutions": [
            {
                "class_id": "class-1",
                "substitute_teacher_id": "prof-isabela",
                "substitute_teacher_name": "Isabela",
                "time_slot": "M1",
                "room_id": "room-1"
            }
        ]
    }, headers=AUTH_HEADER)
    assert resp_commit_delegated.status_code == 200
    commit_delegated_data = resp_commit_delegated.json()
    assert commit_delegated_data["status"] == "success"
    assert commit_delegated_data["mode_used"] == "delegated"
