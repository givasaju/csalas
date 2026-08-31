import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.api.worker import db_restrictions, db_teachers

client = TestClient(app)

from src.database import SessionLocal
from src import models

def test_create_restriction_success():
    """
    Testa cadastro bem-sucedido de indisponibilidade docente.
    """
    db = SessionLocal()
    # Garantir que professor exista
    teacher = db.query(models.Teacher).filter(models.Teacher.id == "prof-claudio").first()
    if not teacher:
        teacher = models.Teacher(id="prof-claudio", name="Cláudio", department="Engenharia", subjects=["Cálculo I"])
        db.add(teacher)
        db.commit()
    
    # Limpar restrição prévia de teste se existir
    prev = db.query(models.Restriction).filter(models.Restriction.teacher_id == "prof-claudio", models.Restriction.day_of_week == 1, models.Restriction.time_slot_id == "M1").first()
    if prev:
        db.delete(prev)
        db.commit()
    db.close()

    headers = {"Authorization": "Bearer mock-token"}
    payload = {
        "teacher_id": "prof-claudio",
        "day_of_week": 1,
        "time_slot_id": "M1"
    }
    
    response = client.post("/api/v1/allocation/restrictions", json=payload, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data["teacher_id"] == "prof-claudio"
    assert data["day_of_week"] == 1
    assert data["time_slot_id"] == "M1"


def test_reset_restrictions_success():
    """
    Testa reset semestral de todas as restrições cadastradas.
    """
    headers = {"Authorization": "Bearer mock-token"}
    response = client.delete("/api/v1/allocation/restrictions", headers=headers)
    assert response.status_code == 200
    assert "cleared_count" in response.json()
