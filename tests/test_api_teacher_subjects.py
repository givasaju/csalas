import pytest
from io import BytesIO
from fastapi.testclient import TestClient
from src.main import app
from src.database import SessionLocal
from src import models

client = TestClient(app)
headers = {"Authorization": "Bearer mock-token"}

def test_create_teacher_with_subjects_success():
    """
    Testa cadastro unitário de docente informando lista de disciplinas lecionáveis.
    """
    db = SessionLocal()
    # Limpar docente prévio se existir
    existing = db.query(models.Teacher).filter(models.Teacher.id == "DOC-TEST-001").first()
    if existing:
        db.delete(existing)
        db.commit()
    db.close()

    payload = {
        "id": "DOC-TEST-001",
        "name": "Prof. Carlos Teste",
        "department": "Engenharia",
        "subjects": ["Cálculo I", "Álgebra Linear"]
    }

    response = client.post("/api/v1/teachers", json=payload, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == "DOC-TEST-001"
    assert data["subjects"] == ["Cálculo I", "Álgebra Linear"]


def test_create_teacher_without_subjects_failure():
    """
    Testa rejeição de cadastro unitário de docente sem disciplinas lecionáveis (lista vazia).
    """
    payload = {
        "id": "DOC-TEST-002",
        "name": "Prof. Sem Matéria",
        "department": "Ciências",
        "subjects": []
    }

    response = client.post("/api/v1/teachers", json=payload, headers=headers)
    assert response.status_code == 422


def test_create_teacher_more_than_6_subjects_failure():
    """
    Testa rejeição de cadastro unitário de docente com mais de 6 disciplinas lecionáveis.
    """
    payload = {
        "id": "DOC-TEST-003",
        "name": "Prof. Muitas Matérias",
        "department": "Ciências",
        "subjects": ["Mat1", "Mat2", "Mat3", "Mat4", "Mat5", "Mat6", "Mat7"]
    }

    response = client.post("/api/v1/teachers", json=payload, headers=headers)
    assert response.status_code == 422


def test_import_teachers_csv_with_subjects_success():
    """
    Testa importação em lote CSV de docentes com coluna de disciplinas separadas por ';'.
    """
    db = SessionLocal()
    for tid in ["DOC-CSV-101", "DOC-CSV-102"]:
        t = db.query(models.Teacher).filter(models.Teacher.id == tid).first()
        if t:
            db.delete(t)
    db.commit()
    db.close()

    csv_content = (
        "matricula,nome,departamento,disciplinas\n"
        "DOC-CSV-101,Profa. Ana,Ciências,Física I;Física II\n"
        "DOC-CSV-102,Prof. Bruno,Humanas,Filosofia;Sociologia\n"
    )
    files = {"file": ("docentes.csv", BytesIO(csv_content.encode("utf-8")), "text/csv")}

    response = client.post("/api/v1/teachers/import-csv", files=files, headers=headers)
    assert response.status_code == 200
    assert response.json()["imported_count"] == 2

    # Verificar no GET /teachers
    get_res = client.get("/api/v1/teachers", headers=headers)
    assert get_res.status_code == 200
    teachers_list = get_res.json()
    ana = next((t for t in teachers_list if t["id"] == "DOC-CSV-101"), None)
    assert ana is not None
    assert ana["subjects"] == ["Física I", "Física II"]


def test_import_teachers_csv_without_subjects_failure():
    """
    Testa falha atômica na importação CSV quando algum docente não possui disciplinas lecionáveis.
    """
    csv_content = (
        "matricula,nome,departamento,disciplinas\n"
        "DOC-FAIL-1,Prof. Invalido,Ciências,\n"
    )
    files = {"file": ("invalido.csv", BytesIO(csv_content.encode("utf-8")), "text/csv")}

    response = client.post("/api/v1/teachers/import-csv", files=files, headers=headers)
    assert response.status_code == 422
