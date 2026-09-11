import os
import tempfile
import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.main import app
from src.models import Base, Room, Teacher, Class
from src.api.auth import create_access_token, verify_token

client = TestClient(app)


def test_database_isolation_between_tenants():
    """Valida que registros criados no banco da Instituição Alpha não existem no banco da Instituição Beta."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path_alpha = os.path.join(tmpdir, "alpha.db")
        db_path_beta = os.path.join(tmpdir, "beta.db")

        engine_alpha = create_engine(f"sqlite:///{db_path_alpha}", connect_args={"check_same_thread": False})
        engine_beta = create_engine(f"sqlite:///{db_path_beta}", connect_args={"check_same_thread": False})

        Base.metadata.create_all(bind=engine_alpha)
        Base.metadata.create_all(bind=engine_beta)

        SessionAlpha = sessionmaker(bind=engine_alpha)
        SessionBeta = sessionmaker(bind=engine_beta)

        try:
            # 1. Inserir dados exclusivamente na Instituição Alpha
            with SessionAlpha() as session_a:
                room_alpha = Room(
                    id="room-alpha-101",
                    name="Auditório Alpha Principal",
                    block_id="Bloco A",
                    capacity=150,
                    room_type="auditorio",
                    is_accessible=True,
                    features=[]
                )
                teacher_alpha = Teacher(
                    id="t-alpha-01",
                    name="Prof. Doutor da Alpha",
                    email="doutor@alpha.edu.br"
                )
                class_alpha = Class(
                    id="class-alpha-01",
                    students_count=120,
                    room_type="auditorio",
                    time_slot="M1",
                    coordination_id="coord-alpha-01",
                    urgency=1,
                    require_accessibility=True
                )
                session_a.add_all([room_alpha, teacher_alpha, class_alpha])
                session_a.commit()

            # 2. Consultar o banco da Instituição Beta e assegurar ausência total
            with SessionBeta() as session_b:
                rooms_b = session_b.query(Room).all()
                teachers_b = session_b.query(Teacher).all()
                classes_b = session_b.query(Class).all()

                assert len(rooms_b) == 0, "Banco Beta não deveria conter salas da Alpha"
                assert len(teachers_b) == 0, "Banco Beta não deveria conter docentes da Alpha"
                assert len(classes_b) == 0, "Banco Beta não deveria conter turmas da Alpha"

                # Inserir registro próprio na Beta
                room_beta = Room(
                    id="room-beta-201",
                    name="Laboratório Beta",
                    block_id="Bloco B",
                    capacity=40,
                    room_type="laboratorio",
                    is_accessible=False,
                    features=[]
                )
                session_b.add(room_beta)
                session_b.commit()

            # 3. Confirmar que Alpha não foi contaminada pelos dados da Beta
            with SessionAlpha() as session_a:
                rooms_a = session_a.query(Room).all()
                assert len(rooms_a) == 1
                assert rooms_a[0].id == "room-alpha-101"
                assert session_a.query(Room).filter(Room.id == "room-beta-201").first() is None
        finally:
            engine_alpha.dispose()
            engine_beta.dispose()


def test_jwt_cross_tenant_rejection():
    """Valida que tokens emitidos por um tenant com SECRET_KEY Alpha são rejeitados pelo tenant Beta."""
    secret_alpha = "alpha-secret-key-32-chars-long-12345678"
    secret_beta = "beta-secret-key-32-chars-long-87654321"

    # Emitir token com a chave da Alpha
    os.environ["SECRET_KEY"] = secret_alpha
    token_alpha = create_access_token(data={"sub": "coordenador@alpha.edu.br", "role": "coordenador", "name": "Coord Alpha"})

    # Na Alpha, o token é válido
    data_verified = verify_token(token_alpha)
    assert data_verified.username == "coordenador@alpha.edu.br"
    assert data_verified.role == "coordenador"

    # Mudar o contexto para a Beta (SECRET_KEY da Beta)
    os.environ["SECRET_KEY"] = secret_beta

    # Tentar validar o token da Alpha na Beta deve lançar 401 Unauthorized
    with pytest.raises(HTTPException) as exc_info:
        verify_token(token_alpha)

    assert exc_info.value.status_code == 401
    assert "inválidas" in exc_info.value.detail or "expirado" in exc_info.value.detail

    # Restaurar chave padrão
    os.environ.pop("SECRET_KEY", None)


def test_health_endpoint_metadata():
    """Valida o endpoint de health check e identificação do tenant configurado."""
    os.environ["TENANT_NAME"] = "universidade_piloto"
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["tenant"] == "universidade_piloto"
    assert "timestamp" in data
    assert "version" in data
    os.environ.pop("TENANT_NAME", None)


@pytest.fixture(scope="module", autouse=True)
def ensure_doctor_user():
    from src.database import SessionLocal, engine
    from src.models import User
    from src.api.auth import hash_password
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        doctor = db.query(User).filter(User.email == "doctor@classsync.ai").first()
        if not doctor:
            doctor = User(
                id="u-doctor-iso",
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


def test_cross_tenant_spoofing_header_rejected_403():
    """Valida que uma requisição com token de Tenant A passando X-Tenant-Slug de Tenant B é rejeitada com 403."""
    token_doctor = _get_doctor_token()
    headers_doctor = {"Authorization": f"Bearer {token_doctor}"}

    import uuid
    slug_a = f"iso_a_{uuid.uuid4().hex[:6]}"
    slug_b = f"iso_b_{uuid.uuid4().hex[:6]}"

    # Provisionar Tenant A e Tenant B
    res_a = client.post("/api/v1/platform/tenants", json={
        "name": "Instituição Alfa",
        "slug": slug_a,
        "port": 8171,
        "master_chef_email": f"gestor@{slug_a}.edu.br",
        "master_chef_password": "SenhaSegura@2026"
    }, headers=headers_doctor)
    assert res_a.status_code == 202

    res_b = client.post("/api/v1/platform/tenants", json={
        "name": "Instituição Beta",
        "slug": slug_b,
        "port": 8172,
        "master_chef_email": f"gestor@{slug_b}.edu.br",
        "master_chef_password": "SenhaSegura@2026"
    }, headers=headers_doctor)
    assert res_b.status_code == 202

    try:
        # Login no Tenant A
        login_res = client.post(
            "/api/v1/auth/login",
            json={"email": f"gestor@{slug_a}.edu.br", "password": "SenhaSegura@2026", "tenant_slug": slug_a}
        )
        assert login_res.status_code == 200
        token_a = login_res.json()["access_token"]

        # Tentar acessar Tenant B usando token de Tenant A -> Deve retornar 403 Forbidden
        spoof_res = client.get(
            "/api/v1/rooms",
            headers={"Authorization": f"Bearer {token_a}", "X-Tenant-Slug": slug_b}
        )
        assert spoof_res.status_code == 403
        assert "Acesso negado" in spoof_res.json()["detail"] or "pertence a outra instituição" in spoof_res.json()["detail"]
    finally:
        client.request("DELETE", f"/api/v1/platform/tenants/{slug_a}", json={"confirm_slug": slug_a}, headers=headers_doctor)
        client.request("DELETE", f"/api/v1/platform/tenants/{slug_b}", json={"confirm_slug": slug_b}, headers=headers_doctor)


def test_tenant_claim_fallback_in_jwt_when_header_omitted():
    """Valida que requisição com token de Tenant A sem header X-Tenant-Slug acessa a base do Tenant A."""
    token_doctor = _get_doctor_token()
    headers_doctor = {"Authorization": f"Bearer {token_doctor}"}

    import uuid
    slug_fb = f"iso_fb_{uuid.uuid4().hex[:6]}"

    res = client.post("/api/v1/platform/tenants", json={
        "name": "Instituição Fallback",
        "slug": slug_fb,
        "port": 8173,
        "master_chef_email": f"gestor@{slug_fb}.edu.br",
        "master_chef_password": "SenhaSegura@2026"
    }, headers=headers_doctor)
    assert res.status_code == 202

    try:
        login_res = client.post(
            "/api/v1/auth/login",
            json={"email": f"gestor@{slug_fb}.edu.br", "password": "SenhaSegura@2026", "tenant_slug": slug_fb}
        )
        assert login_res.status_code == 200
        token = login_res.json()["access_token"]

        # Cadastrar uma sala sem enviar X-Tenant-Slug (apenas token)
        create_res = client.post(
            "/api/v1/rooms",
            json={
                "name": "Sala Teste Fallback",
                "block_id": "Bloco FB",
                "capacity": 35,
                "room_type": "common",
                "is_accessible": True,
                "features": []
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        assert create_res.status_code in (200, 201)

        # Listar salas sem enviar X-Tenant-Slug
        list_res = client.get("/api/v1/rooms", headers={"Authorization": f"Bearer {token}"})
        assert list_res.status_code == 200
        rooms = list_res.json()
        assert any(r["name"] == "Sala Teste Fallback" for r in rooms)
    finally:
        client.request("DELETE", f"/api/v1/platform/tenants/{slug_fb}", json={"confirm_slug": slug_fb}, headers=headers_doctor)


def test_doctor_chef_blocked_from_tenant_pedagogical_data_403():
    """Valida que o usuário doctor-chef é estritamente bloqueado (HTTP 403) de consultar dados de salas/docentes."""
    token_doctor = _get_doctor_token()
    headers = {"Authorization": f"Bearer {token_doctor}"}

    res_rooms = client.get("/api/v1/rooms", headers=headers)
    assert res_rooms.status_code == 403
    assert "doctor-chef" in res_rooms.json()["detail"]

    res_teachers = client.get("/api/v1/teachers", headers=headers)
    assert res_teachers.status_code == 403
    assert "doctor-chef" in res_teachers.json()["detail"]


def test_room_isolation_between_two_active_tenants():
    """Valida que a sala cadastrada na Faculdade Alfa NÃO aparece na Faculdade Beta."""
    token_doctor = _get_doctor_token()
    headers_doctor = {"Authorization": f"Bearer {token_doctor}"}

    import uuid
    slug_1 = f"t1_{uuid.uuid4().hex[:6]}"
    slug_2 = f"t2_{uuid.uuid4().hex[:6]}"

    client.post("/api/v1/platform/tenants", json={
        "name": "Faculdade 1",
        "slug": slug_1,
        "port": 8174,
        "master_chef_email": f"gestor@{slug_1}.edu.br",
        "master_chef_password": "SenhaSegura@2026"
    }, headers=headers_doctor)

    client.post("/api/v1/platform/tenants", json={
        "name": "Faculdade 2",
        "slug": slug_2,
        "port": 8175,
        "master_chef_email": f"gestor@{slug_2}.edu.br",
        "master_chef_password": "SenhaSegura@2026"
    }, headers=headers_doctor)

    try:
        # Login 1
        t1_login = client.post("/api/v1/auth/login", json={"email": f"gestor@{slug_1}.edu.br", "password": "SenhaSegura@2026", "tenant_slug": slug_1})
        token_1 = t1_login.json()["access_token"]

        # Login 2
        t2_login = client.post("/api/v1/auth/login", json={"email": f"gestor@{slug_2}.edu.br", "password": "SenhaSegura@2026", "tenant_slug": slug_2})
        token_2 = t2_login.json()["access_token"]

        # 1 cadastra sala
        client.post(
            "/api/v1/rooms",
            json={"name": "Sala Exclusiva Alfa", "block_id": "Bloco 1", "capacity": 50, "room_type": "common", "is_accessible": True, "features": []},
            headers={"Authorization": f"Bearer {token_1}"}
        )

        # 2 lista salas
        res2 = client.get("/api/v1/rooms", headers={"Authorization": f"Bearer {token_2}"})
        assert res2.status_code == 200
        rooms_2 = res2.json()
        assert not any(r["name"] == "Sala Exclusiva Alfa" for r in rooms_2), "A sala da Faculdade 1 não pode aparecer na Faculdade 2!"
    finally:
        client.request("DELETE", f"/api/v1/platform/tenants/{slug_1}", json={"confirm_slug": slug_1}, headers=headers_doctor)
        client.request("DELETE", f"/api/v1/platform/tenants/{slug_2}", json={"confirm_slug": slug_2}, headers=headers_doctor)


def test_reports_isolation_between_tenants():
    """Valida que relatórios executados no contexto de um tenant não exibem dados de outro."""
    token_doctor = _get_doctor_token()
    headers_doctor = {"Authorization": f"Bearer {token_doctor}"}

    import uuid
    slug_r1 = f"r1_{uuid.uuid4().hex[:6]}"
    slug_r2 = f"r2_{uuid.uuid4().hex[:6]}"

    client.post("/api/v1/platform/tenants", json={
        "name": "Relatório Faculdade 1",
        "slug": slug_r1,
        "port": 8176,
        "master_chef_email": f"gestor@{slug_r1}.edu.br",
        "master_chef_password": "SenhaSegura@2026"
    }, headers=headers_doctor)

    client.post("/api/v1/platform/tenants", json={
        "name": "Relatório Faculdade 2",
        "slug": slug_r2,
        "port": 8177,
        "master_chef_email": f"gestor@{slug_r2}.edu.br",
        "master_chef_password": "SenhaSegura@2026"
    }, headers=headers_doctor)

    try:
        t1_login = client.post("/api/v1/auth/login", json={"email": f"gestor@{slug_r1}.edu.br", "password": "SenhaSegura@2026", "tenant_slug": slug_r1})
        token_1 = t1_login.json()["access_token"]

        t2_login = client.post("/api/v1/auth/login", json={"email": f"gestor@{slug_r2}.edu.br", "password": "SenhaSegura@2026", "tenant_slug": slug_r2})
        token_2 = t2_login.json()["access_token"]

        # Cadastrar sala na Faculdade 1
        client.post(
            "/api/v1/rooms",
            json={"name": "Sala Relatório Exclusiva 1", "block_id": "Bloco R1", "capacity": 50, "room_type": "common", "is_accessible": True, "features": []},
            headers={"Authorization": f"Bearer {token_1}"}
        )

        # Relatório de resumo da Faculdade 1 -> deve conter a sala
        rep1 = client.get("/api/v1/reports/summary", headers={"Authorization": f"Bearer {token_1}"})
        assert rep1.status_code == 200
        rooms_rep1 = rep1.json().get("room_occupancy", [])
        assert any(r.get("room_name") == "Sala Relatório Exclusiva 1" for r in rooms_rep1)

        # Relatório de resumo da Faculdade 2 -> NÃO deve conter a sala da Faculdade 1
        rep2 = client.get("/api/v1/reports/summary", headers={"Authorization": f"Bearer {token_2}"})
        assert rep2.status_code == 200
        rooms_rep2 = rep2.json().get("room_occupancy", [])
        assert not any(r.get("room_name") == "Sala Relatório Exclusiva 1" for r in rooms_rep2)

        # Download do PDF e Excel de ocupação na Faculdade 2
        pdf_res = client.get("/api/v1/reports/occupancy/pdf", headers={"Authorization": f"Bearer {token_2}"})
        assert pdf_res.status_code == 200
        assert "application/pdf" in pdf_res.headers.get("content-type", "")

        excel_res = client.get("/api/v1/reports/occupancy/excel", headers={"Authorization": f"Bearer {token_2}"})
        assert excel_res.status_code == 200
    finally:
        client.request("DELETE", f"/api/v1/platform/tenants/{slug_r1}", json={"confirm_slug": slug_r1}, headers=headers_doctor)
        client.request("DELETE", f"/api/v1/platform/tenants/{slug_r2}", json={"confirm_slug": slug_r2}, headers=headers_doctor)


def test_allocation_run_tenant_isolation():
    """Valida que o endpoint /allocation/run despacha tarefa associada ao tenant correto."""
    token_doctor = _get_doctor_token()
    headers_doctor = {"Authorization": f"Bearer {token_doctor}"}

    import uuid
    slug_w = f"w_{uuid.uuid4().hex[:6]}"

    client.post("/api/v1/platform/tenants", json={
        "name": "Faculdade Worker",
        "slug": slug_w,
        "port": 8178,
        "master_chef_email": f"gestor@{slug_w}.edu.br",
        "master_chef_password": "SenhaSegura@2026"
    }, headers=headers_doctor)

    try:
        t_login = client.post("/api/v1/auth/login", json={"email": f"gestor@{slug_w}.edu.br", "password": "SenhaSegura@2026", "tenant_slug": slug_w})
        token = t_login.json()["access_token"]

        run_res = client.post("/api/v1/allocation/run", headers={"Authorization": f"Bearer {token}"})
        assert run_res.status_code == 202
        task_id = run_res.json()["task_id"]

        from src.api.worker import db_tasks
        assert db_tasks[task_id]["tenant_slug"] == slug_w
    finally:
        client.request("DELETE", f"/api/v1/platform/tenants/{slug_w}", json={"confirm_slug": slug_w}, headers=headers_doctor)


