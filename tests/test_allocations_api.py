"""
Testes de integração para as rotas REST de alocações e validação de consecutividade docente (max 4 aulas seguidas).
"""

import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.api.allocation_validator import check_consecutive_limit

client = TestClient(app)
AUTH_HEADERS = {"Authorization": "Bearer mock-token"}


def test_check_consecutive_limit_unit():
    # 4 seguidas -> Válido
    assert check_consecutive_limit([1, 2, 3], 4) is True
    # 5 seguidas -> Inválido
    assert check_consecutive_limit([1, 2, 3, 4], 5) is False
    # Não-consecutivo (ex: 1, 2, 3, 5) -> Válido (máx 3 seguidas)
    assert check_consecutive_limit([1, 2, 3], 5) is True


def test_create_allocation_unauthorized():
    res = client.post("/api/v1/allocations", json={
        "teacher_id": "prof-01",
        "room_id": "r-101",
        "day_of_week": 1,
        "shift": "M",
        "sub_slot": 1
    })
    assert res.status_code == 401


import uuid

def test_consecutive_allocations_flow():
    unique_str = str(uuid.uuid4())[:8]
    teacher_id = f"prof-test-{unique_str}"
    room_id = f"room-test-{unique_str}"
    from src.database import SessionLocal
    from src import models

    db = SessionLocal()
    teacher = models.Teacher(id=teacher_id, name="Prof. Teste Consecutive", department="Engenharia", subjects=["Algoritmos"])
    room = models.Room(id=room_id, block_id="BLOCO_TEST", name="Sala Teste", capacity=40, room_type="common", is_accessible=True, features=[])
    db.add(teacher)
    db.add(room)
    db.commit()
    db.close()

    for slot in range(1, 5):
        payload = {
            "teacher_id": teacher_id,
            "room_id": room_id,
            "day_of_week": 1,
            "shift": "M",
            "sub_slot": slot
        }
        res = client.post("/api/v1/allocations", json=payload, headers=AUTH_HEADERS)
        assert res.status_code == 201

    # Tentativa da 5ª aula no mesmo turno -> Deve falhar com 409 Conflict
    payload_5th = {
        "teacher_id": teacher_id,
        "room_id": room_id,
        "day_of_week": 1,
        "shift": "M",
        "sub_slot": 5
    }
    res_5th = client.post("/api/v1/allocations", json=payload_5th, headers=AUTH_HEADERS)
    assert res_5th.status_code == 409
    assert "4 aulas seguidas" in res_5th.json()["detail"]


def test_get_allocations():
    res = client.get("/api/v1/allocations", headers=AUTH_HEADERS)
    assert res.status_code == 200
    assert isinstance(res.json(), list)


def test_allocation_rejected_due_to_teacher_restriction():
    from src.database import SessionLocal
    from src import models

    db = SessionLocal()
    teacher_id = "prof-restr-test"
    room_id = "room-restr-test"

    # Preparar docente, sala e restrição no dia 2 slot T1
    if not db.query(models.Teacher).filter(models.Teacher.id == teacher_id).first():
        db.add(models.Teacher(id=teacher_id, name="Prof. Restrito", department="Física", subjects=["Física I"]))
    if not db.query(models.Room).filter(models.Room.id == room_id).first():
        db.add(models.Room(id=room_id, block_id="BLOCO_TEST", name="Sala 201", capacity=30, room_type="common", is_accessible=True, features=[]))
    
    # Criar restrição no dia 2, slot T1
    prev_restr = db.query(models.Restriction).filter(models.Restriction.teacher_id == teacher_id, models.Restriction.day_of_week == 2, models.Restriction.time_slot_id == "T1").first()
    if not prev_restr:
        db.add(models.Restriction(id=str(uuid.uuid4()), teacher_id=teacher_id, day_of_week=2, time_slot_id="T1"))
    db.commit()
    db.close()

    # Tentativa de alocar aula no slot indisponível -> Deve retornar 409 Conflict
    payload = {
        "teacher_id": teacher_id,
        "room_id": room_id,
        "day_of_week": 2,
        "shift": "T",
        "sub_slot": 1
    }
    res = client.post("/api/v1/allocations", json=payload, headers=AUTH_HEADERS)
    assert res.status_code == 409
    assert "indisponibilidade" in res.json()["detail"].lower()


def test_create_allocation_with_subject_flow():
    from src.database import SessionLocal
    from src import models

    unique_str = str(uuid.uuid4())[:8]
    db = SessionLocal()
    teacher_id = f"prof-subj-{unique_str}"
    room_id = f"room-subj-{unique_str}"

    # Preparar docente com 2 disciplinas e sala
    if not db.query(models.Teacher).filter(models.Teacher.id == teacher_id).first():
        db.add(models.Teacher(id=teacher_id, name="Prof. Disciplinas", department="Computação", subjects=["Banco de Dados", "Estrutura de Dados"]))
    if not db.query(models.Room).filter(models.Room.id == room_id).first():
        db.add(models.Room(id=room_id, block_id="BLOCO_TEST", name="Lab 101", capacity=30, room_type="lab", is_accessible=True, features=[]))
    db.commit()
    db.close()

    # 1. Alocar com disciplina válida do rol
    payload_valid = {
        "teacher_id": teacher_id,
        "room_id": room_id,
        "day_of_week": 3,
        "shift": "N",
        "sub_slot": 1,
        "subject": "Banco de Dados"
    }
    res_valid = client.post("/api/v1/allocations", json=payload_valid, headers=AUTH_HEADERS)
    assert res_valid.status_code == 201
    assert res_valid.json()["subject"] == "Banco de Dados"

    # 2. Alocar com disciplina fora do rol do docente -> Deve retornar 422
    payload_invalid = {
        "teacher_id": teacher_id,
        "room_id": room_id,
        "day_of_week": 3,
        "shift": "N",
        "sub_slot": 2,
        "subject": "Medicina Veterinária"
    }
    res_invalid = client.post("/api/v1/allocations", json=payload_invalid, headers=AUTH_HEADERS)
    assert res_invalid.status_code == 422
    assert "não pertence ao rol" in res_invalid.json()["detail"].lower()


def test_run_allocation_flow():
    # Clear active tasks to ensure clean run
    from src.api.worker import db_tasks
    db_tasks.clear()

    # 1. Disparar alocação
    res = client.post("/api/v1/allocation/run", headers=AUTH_HEADERS)
    assert res.status_code == 202
    data = res.json()
    assert "task_id" in data
    assert data["status"] == "queued"
    task_id = data["task_id"]

    # 2. Tentativa de disparar concorrentemente -> 409 Conflict
    res_conflict = client.post("/api/v1/allocation/run", headers=AUTH_HEADERS)
    assert res_conflict.status_code == 409

    # 3. Consultar status da tarefa
    res_status = client.get(f"/api/v1/allocation/status/{task_id}", headers=AUTH_HEADERS)
    assert res_status.status_code == 200
    status_data = res_status.json()
    assert status_data["task_id"] == task_id
    assert status_data["status"] in ("queued", "running", "completed", "pending_arbitration")


def test_allocation_status_not_found():
    res = client.get("/api/v1/allocation/status/invalid-task-id-12345", headers=AUTH_HEADERS)
    assert res.status_code == 404


def test_get_auctions_endpoint():
    res = client.get("/api/v1/allocation/auctions", headers=AUTH_HEADERS)
    assert res.status_code == 200
    assert isinstance(res.json(), list)

    res_input = client.get("/api/v1/allocation/input-data", headers=AUTH_HEADERS)
    assert res_input.status_code == 200
    assert "auctions" in res_input.json()


