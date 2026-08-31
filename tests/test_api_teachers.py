import pytest
import uuid
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)
AUTH_HEADERS = {"Authorization": "Bearer test-valid-token"}

def test_create_teacher_success():
    """Testa cadastro unitário de professor."""
    t_id = f"prof-test-{str(uuid.uuid4())[:8]}"
    payload = {
        "id": t_id,
        "name": "Prof. Alan Turing",
        "department": "Computação",
        "subjects": ["Algoritmos"]
    }
    res = client.post("/api/v1/teachers", json=payload, headers=AUTH_HEADERS)
    assert res.status_code == 201
    data = res.json()
    assert data["id"] == t_id
    assert data["name"] == "Prof. Alan Turing"

def test_create_teacher_duplicate_conflict():
    """Garante que matrícula duplicada retorna 409 Conflict."""
    t_id = f"prof-dup-{str(uuid.uuid4())[:8]}"
    payload = {
        "id": t_id,
        "name": "Prof. Ada Lovelace",
        "department": "Matemática",
        "subjects": ["Matemática I"]
    }
    res1 = client.post("/api/v1/teachers", json=payload, headers=AUTH_HEADERS)
    assert res1.status_code == 201
    
    res2 = client.post("/api/v1/teachers", json=payload, headers=AUTH_HEADERS)
    assert res2.status_code == 409

def test_import_teachers_csv_success():
    """Testa importação em lote via CSV de docentes com sucesso."""
    id1 = f"prof-csv-{str(uuid.uuid4())[:8]}"
    id2 = f"prof-csv-{str(uuid.uuid4())[:8]}"
    csv_data = f"matricula,nome,departamento,disciplinas\n{id1},Prof. Grace Hopper,Computação,Compiladores\n{id2},Prof. Claude Shannon,Engenharia,Teoria da Informação"
    files = {"file": ("teachers.csv", csv_data, "text/csv")}
    res = client.post("/api/v1/teachers/import-csv", files=files, headers=AUTH_HEADERS)
    assert res.status_code == 200
    assert res.json()["imported_count"] == 2

def test_import_teachers_csv_validation_failure():
    """Garante rejeição tudo-ou-nada em caso de dados inválidos no CSV."""
    csv_data = "matricula,nome,departamento,disciplinas\nprof-valid-99,Prof. Válido,Física,Física I\n,Prof. Sem Matrícula,Química,Química General"
    files = {"file": ("invalid_teachers.csv", csv_data, "text/csv")}
    res = client.post("/api/v1/teachers/import-csv", files=files, headers=AUTH_HEADERS)
    assert res.status_code == 422
