import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.database import SessionLocal
from src import models

client = TestClient(app)
AUTH_HEADERS = {"Authorization": "Bearer valid-token"}

def setup_module(module):
    """Setup docente de teste no banco."""
    db = SessionLocal()
    teacher = db.query(models.Teacher).filter(models.Teacher.id == "prof-claudio").first()
    if not teacher:
        db.add(models.Teacher(id="prof-claudio", name="Cláudio", department="Engenharia"))
        db.commit()
    db.close()

def test_get_teacher_restrictions_empty():
    """Testa busca de restrições para professor sem indisponibilidade cadastrada."""
    response = client.get("/api/v1/teachers/prof-claudio/restrictions", headers=AUTH_HEADERS)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_teacher_restrictions_not_found():
    """Testa busca de restrições para docente inexistente."""
    response = client.get("/api/v1/teachers/prof-inexistente/restrictions", headers=AUTH_HEADERS)
    assert response.status_code == 404

def test_create_and_delete_single_restriction():
    """Testa criação e exclusão pontual por ID de restrição docente (T002, T003)."""
    import uuid
    db = SessionLocal()
    teacher_id = f"prof-restr-{str(uuid.uuid4())[:8]}"
    db.add(models.Teacher(id=teacher_id, name="Prof. Restrição Única", department="Engenharia"))
    db.commit()
    db.close()

    # 1. Cadastrar
    payload = {
        "teacher_id": teacher_id,
        "day_of_week": 1,
        "time_slot_id": "M1"
    }
    create_res = client.post("/api/v1/allocation/restrictions", json=payload, headers=AUTH_HEADERS)
    assert create_res.status_code == 201
    restriction_id = create_res.json()["id"]

    # 2. Listar
    list_res = client.get(f"/api/v1/teachers/{teacher_id}/restrictions", headers=AUTH_HEADERS)
    assert list_res.status_code == 200
    restrictions = list_res.json()
    assert len(restrictions) == 1

    # 3. Deletar por ID
    del_res = client.delete(f"/api/v1/allocation/restrictions/{restriction_id}", headers=AUTH_HEADERS)
    assert del_res.status_code == 200

    # 4. Deletar novamente (deve dar 404)
    del_res_404 = client.delete(f"/api/v1/allocation/restrictions/{restriction_id}", headers=AUTH_HEADERS)
    assert del_res_404.status_code == 404
