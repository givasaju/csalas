"""
Testes de integração para o endpoint POST /api/v1/teachers/reallocate-subjects.
"""

import uuid
import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.database import SessionLocal
from src import models

client = TestClient(app)
AUTH_HEADERS = {"Authorization": "Bearer mock-token"}


def test_reallocate_subjects_success():
    unique_str = str(uuid.uuid4())[:8]
    db = SessionLocal()
    source_id = f"prof-source-{unique_str}"
    target_id = f"prof-target-{unique_str}"

    # Criar docentes do mesmo departamento
    source_teacher = models.Teacher(
        id=source_id,
        name="Prof. Doador",
        department="Engenharia",
        subjects=["Cálculo I", "Vetores"]
    )
    target_teacher = models.Teacher(
        id=target_id,
        name="Prof. Receptor",
        department="Engenharia",
        subjects=["Física I"]
    )
    db.add(source_teacher)
    db.add(target_teacher)
    db.commit()
    db.close()

    payload = {
        "source_teacher_id": source_id,
        "target_teacher_id": target_id,
        "subjects": ["Cálculo I"]
    }

    response = client.post("/api/v1/teachers/reallocate-subjects", json=payload, headers=AUTH_HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["department"] == "Engenharia"
    assert "Cálculo I" in data["target_teacher"]["subjects"]
    assert "Cálculo I" not in data["source_teacher"]["subjects"]
    assert "Vetores" in data["source_teacher"]["subjects"]


def test_reallocate_subjects_different_departments_fails():
    unique_str = str(uuid.uuid4())[:8]
    db = SessionLocal()
    source_id = f"prof-eng-{unique_str}"
    target_id = f"prof-letras-{unique_str}"

    # Criar docentes de departamentos diferentes
    source_teacher = models.Teacher(
        id=source_id,
        name="Prof. Engenheiro",
        department="Engenharia",
        subjects=["Cálculo I"]
    )
    target_teacher = models.Teacher(
        id=target_id,
        name="Prof. Linguista",
        department="Letras",
        subjects=["Gramática"]
    )
    db.add(source_teacher)
    db.add(target_teacher)
    db.commit()
    db.close()

    payload = {
        "source_teacher_id": source_id,
        "target_teacher_id": target_id,
        "subjects": ["Cálculo I"],
        "replacement_subject": "Álgebra Linear"
    }

    response = client.post("/api/v1/teachers/reallocate-subjects", json=payload, headers=AUTH_HEADERS)
    assert response.status_code == 422
    assert "mesmo departamento" in response.json()["detail"].lower()


def test_reallocate_subjects_empty_source_without_replacement_fails():
    unique_str = str(uuid.uuid4())[:8]
    db = SessionLocal()
    source_id = f"prof-single-{unique_str}"
    target_id = f"prof-recv-{unique_str}"

    source_teacher = models.Teacher(
        id=source_id,
        name="Prof. Uma Disciplina",
        department="Computação",
        subjects=["Algoritmos"]
    )
    target_teacher = models.Teacher(
        id=target_id,
        name="Prof. Receptor Comp",
        department="Computação",
        subjects=["Banco de Dados"]
    )
    db.add(source_teacher)
    db.add(target_teacher)
    db.commit()
    db.close()

    payload = {
        "source_teacher_id": source_id,
        "target_teacher_id": target_id,
        "subjects": ["Algoritmos"]
    }

    response = client.post("/api/v1/teachers/reallocate-subjects", json=payload, headers=AUTH_HEADERS)
    assert response.status_code == 422
    assert "substituta" in response.json()["detail"].lower()


def test_reallocate_subjects_with_replacement_success():
    unique_str = str(uuid.uuid4())[:8]
    db = SessionLocal()
    source_id = f"prof-single-ok-{unique_str}"
    target_id = f"prof-recv-ok-{unique_str}"

    source_teacher = models.Teacher(
        id=source_id,
        name="Prof. Doador Total",
        department="Matemática",
        subjects=["Geometria"]
    )
    target_teacher = models.Teacher(
        id=target_id,
        name="Prof. Novo Contratado",
        department="Matemática",
        subjects=["Estatística"]
    )
    db.add(source_teacher)
    db.add(target_teacher)
    db.commit()
    db.close()

    payload = {
        "source_teacher_id": source_id,
        "target_teacher_id": target_id,
        "subjects": ["Geometria"],
        "replacement_subject": "Matemática Discreta"
    }

    response = client.post("/api/v1/teachers/reallocate-subjects", json=payload, headers=AUTH_HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["source_teacher"]["subjects"] == ["Matemática Discreta"]
    assert "Geometria" in data["target_teacher"]["subjects"]
