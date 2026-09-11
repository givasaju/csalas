import os
import uuid
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.main import app
from src.models import Base, Room, Teacher, Allocation, User
from src.database import (
    SessionLocal,
    engine,
    backup_and_purge_central_database,
    get_tenant_session
)
from src.api.auth import create_access_token, hash_password

client = TestClient(app)


@pytest.fixture(scope="module", autouse=True)
def ensure_doctor():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        doctor = db.query(User).filter(User.email == "doctor@classsync.ai").first()
        if not doctor:
            doctor = User(
                id="u-doctor-seg",
                name="Super Administrador Geral",
                email="doctor@classsync.ai",
                password_hash=hash_password("Doctor@2026"),
                role="doctor-chef",
                department="Plataforma",
                is_active=True,
                must_change_password=False
            )
            db.add(doctor)
            db.commit()
    finally:
        db.close()


def _get_doctor_token():
    res = client.post("/api/v1/auth/login", json={"email": "doctor@classsync.ai", "password": "Doctor@2026"})
    assert res.status_code == 200
    return res.json()["access_token"]


def test_backup_and_purge_central_database():
    """Valida que o backup preventivo é gerado e que os dados acadêmicos são expurgados da base central."""
    # 1. Semear dados na base central
    with SessionLocal() as db:
        room = Room(id="temp-room-purge", name="Sala Purge", block_id="X", capacity=20, room_type="common")
        teacher = Teacher(id="temp-teach-purge", name="Docente Purge", department="Geral", subjects=["Geral"])
        db.merge(room)
        db.merge(teacher)
        db.commit()

    # 2. Executar rotina de backup e expurgo
    result = backup_and_purge_central_database()
    assert result["status"] == "success"
    assert os.path.exists(result["backup_path"])

    # 3. Conferir que base central está limpa
    with SessionLocal() as db:
        assert db.query(Room).filter(Room.id == "temp-room-purge").first() is None
        assert db.query(Teacher).filter(Teacher.id == "temp-teach-purge").first() is None
        # Conferir que doctor-chef continua intacto
        doctor = db.query(User).filter(User.email == "doctor@classsync.ai").first()
        assert doctor is not None
        assert doctor.role == "doctor-chef"

        # Restaurar professor padrão de teste para não quebrar testes legados de UI
        claudio = db.query(Teacher).filter(Teacher.id == "prof-claudio").first()
        if not claudio:
            db.add(Teacher(id="prof-claudio", name="Cláudio", department="Engenharia", subjects=["Cálculo I"]))
            db.commit()


def test_zero_silent_fallback_anonymous_academic_requests_401():
    """Valida que requisições anônimas em rotas pedagógicas são rejeitadas com HTTP 401."""
    # GET /rooms sem credencial
    res_rooms = client.get("/api/v1/rooms")
    assert res_rooms.status_code == 401

    # POST /rooms sem credencial
    res_post_room = client.post("/api/v1/rooms", json={
        "name": "Sala Fantasma",
        "block_id": "Bloco Zero",
        "capacity": 30,
        "room_type": "common"
    })
    assert res_post_room.status_code == 401

    # GET /teachers sem credencial
    res_teachers = client.get("/api/v1/teachers")
    assert res_teachers.status_code == 401


def test_zero_silent_fallback_token_without_tenant_claim_401():
    """Valida que token JWT real sem a claim 'tenant' não consegue acessar rotas de tenant."""
    token_no_tenant = create_access_token({
        "sub": "usuario_sem_tenant@teste.com",
        "role": "docente",
        "name": "Sem Tenant"
    })
    headers = {"Authorization": f"Bearer {token_no_tenant}"}

    res = client.get("/api/v1/rooms", headers=headers)
    assert res.status_code == 401
    assert "Contexto institucional ausente" in res.json()["detail"]


def test_anti_spoofing_token_versus_header_mismatch_403():
    """Valida que token de Tenant A tentando acessar Tenant B via header é rejeitado com HTTP 403."""
    token_alfa = create_access_token({
        "sub": "gestor@alfa.com",
        "role": "gestor",
        "name": "Gestor Alfa",
        "tenant": "inst_alfa"
    })
    headers = {
        "Authorization": f"Bearer {token_alfa}",
        "X-Tenant-Slug": "inst_beta"
    }

    res = client.get("/api/v1/rooms", headers=headers)
    assert res.status_code == 403
    assert "Acesso negado" in res.json()["detail"]
    assert "inst_alfa" in res.json()["detail"]


def test_doctor_chef_cannot_access_pedagogical_routes_403():
    """Valida que o SuperAdmin Doctor-Chef é proibido de acessar rotas pedagógicas de instituições."""
    token_doctor = _get_doctor_token()
    headers = {"Authorization": f"Bearer {token_doctor}"}

    res_rooms = client.get("/api/v1/rooms", headers=headers)
    assert res_rooms.status_code == 403
    assert "doctor-chef" in res_rooms.json()["detail"]

    res_teachers = client.get("/api/v1/teachers", headers=headers)
    assert res_teachers.status_code == 403
    assert "doctor-chef" in res_teachers.json()["detail"]


def test_strict_segregation_and_zero_central_db_pollution():
    """
    Valida o fluxo completo de isolamento multitenant:
    1. Criação de duas instituições com bases dedicadas.
    2. Cadastro de salas em uma instituição.
    3. Garantia de que a outra instituição tem retorno vazio.
    4. Garantia de que a base central não recebeu nenhuma sala.
    """
    token_doctor = _get_doctor_token()
    headers_doctor = {"Authorization": f"Bearer {token_doctor}"}

    slug_a = f"seg_a_{uuid.uuid4().hex[:6]}"
    slug_b = f"seg_b_{uuid.uuid4().hex[:6]}"

    # 1. Provisionar as duas instituições
    res_a = client.post("/api/v1/platform/tenants", json={
        "name": "Faculdade Alfa Seg",
        "slug": slug_a,
        "port": 8181,
        "master_chef_email": f"gestor@{slug_a}.edu.br",
        "master_chef_password": "SenhaSegura@2026"
    }, headers=headers_doctor)
    assert res_a.status_code == 202

    res_b = client.post("/api/v1/platform/tenants", json={
        "name": "Faculdade Beta Seg",
        "slug": slug_b,
        "port": 8182,
        "master_chef_email": f"gestor@{slug_b}.edu.br",
        "master_chef_password": "SenhaSegura@2026"
    }, headers=headers_doctor)
    assert res_b.status_code == 202

    try:
        # 2. Login em Alfa
        login_a = client.post("/api/v1/auth/login", json={
            "email": f"gestor@{slug_a}.edu.br",
            "password": "SenhaSegura@2026",
            "tenant_slug": slug_a
        })
        assert login_a.status_code == 200
        token_a = login_a.json()["access_token"]

        # 3. Login em Beta
        login_b = client.post("/api/v1/auth/login", json={
            "email": f"gestor@{slug_b}.edu.br",
            "password": "SenhaSegura@2026",
            "tenant_slug": slug_b
        })
        assert login_b.status_code == 200
        token_b = login_b.json()["access_token"]

        # 4. Cadastrar sala em Alfa
        sala_alfa_nome = f"Sala Robótica Alfa {slug_a}"
        create_res = client.post(
            "/api/v1/rooms",
            json={
                "name": sala_alfa_nome,
                "block_id": "Bloco A",
                "capacity": 45,
                "room_type": "lab",
                "is_accessible": True,
                "features": ["robos", "computadores"]
            },
            headers={"Authorization": f"Bearer {token_a}"}
        )
        assert create_res.status_code in (200, 201)

        # 5. Listar salas em Beta -> Deve ser vazia
        list_beta = client.get("/api/v1/rooms", headers={"Authorization": f"Bearer {token_b}"})
        assert list_beta.status_code == 200
        rooms_beta = list_beta.json()
        assert len(rooms_beta) == 0, f"Faculdade Beta não deveria ver a sala de Alfa! Retornou: {rooms_beta}"

        # 6. Listar salas em Alfa -> Deve conter a sala criada
        list_alfa = client.get("/api/v1/rooms", headers={"Authorization": f"Bearer {token_a}"})
        assert list_alfa.status_code == 200
        rooms_alfa = list_alfa.json()
        assert any(r["name"] == sala_alfa_nome for r in rooms_alfa)

        # 7. Inspecionar a base central -> A sala de Alfa NÃO PODE estar na base central!
        with SessionLocal() as db_central:
            sala_na_central = db_central.query(Room).filter(Room.name == sala_alfa_nome).first()
            assert sala_na_central is None, "Violação de sigilo: Sala da Faculdade Alfa foi gravada na base central compartilhada!"

    finally:
        client.request("DELETE", f"/api/v1/platform/tenants/{slug_a}", json={"confirm_slug": slug_a}, headers=headers_doctor)
        client.request("DELETE", f"/api/v1/platform/tenants/{slug_b}", json={"confirm_slug": slug_b}, headers=headers_doctor)
