import os
import shutil
import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.database import SessionLocal, engine
from src.models import Base, User
from src.api.auth import hash_password, create_access_token

client = TestClient(app)

TEST_TENANT_SLUG = "faculdade_teste_auto_022"
TEST_TENANT_PORT = 8099
TEST_ENV_FILE = f".env.{TEST_TENANT_SLUG}"
TEST_DATA_DIR = os.path.join("data", TEST_TENANT_SLUG)


@pytest.fixture(scope="module", autouse=True)
def setup_platform_users():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Garantir doctor-chef
        doctor = db.query(User).filter(User.email == "doctor@classsync.ai").first()
        if not doctor:
            doctor = User(
                id="u-doctor-test",
                name="Super Administrador Geral",
                email="doctor@classsync.ai",
                password_hash=hash_password("Doctor@2026"),
                role="doctor-chef",
                department="Plataforma",
                is_active=True,
                must_change_password=False
            )
            db.add(doctor)

        # Garantir gestor normal
        gestor = db.query(User).filter(User.email == "admin@classsync.ai").first()
        if not gestor:
            gestor = User(
                id="u-admin-test",
                name="Gestor Principal",
                email="admin@classsync.ai",
                password_hash=hash_password("admin123"),
                role="gestor",
                department="Administração",
                is_active=True,
                must_change_password=False
            )
            db.add(gestor)

        # Usuário docente para teste de permissão
        docente = db.query(User).filter(User.email == "docente.teste@classsync.ai").first()
        if not docente:
            docente = User(
                id="u-docente-test",
                name="Professor Teste",
                email="docente.teste@classsync.ai",
                password_hash=hash_password("Senha1234"),
                role="docente",
                department="Computação",
                is_active=True,
                must_change_password=False
            )
            db.add(docente)

        db.commit()
    finally:
        db.close()

    yield

    # Limpeza pós-testes
    if os.path.exists(TEST_ENV_FILE):
        try:
            os.remove(TEST_ENV_FILE)
        except Exception:
            pass
    if os.path.exists(TEST_DATA_DIR):
        try:
            shutil.rmtree(TEST_DATA_DIR, ignore_errors=True)
        except Exception:
            pass


def get_token_for(email: str, password: str) -> str:
    res = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    assert res.status_code == 200
    return res.json()["access_token"]


def test_doctor_chef_list_tenants_success():
    token = get_token_for("doctor@classsync.ai", "Doctor@2026")
    headers = {"Authorization": f"Bearer {token}"}

    res = client.get("/api/v1/platform/tenants", headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert "total" in data
    assert "next_available_port" in data
    assert isinstance(data["tenants"], list)
    assert data["next_available_port"] >= 8001


def test_roles_forbidden_for_platform_endpoints():
    # Gestor local tentando acessar
    gestor_token = get_token_for("admin@classsync.ai", "admin123")
    headers_gestor = {"Authorization": f"Bearer {gestor_token}"}

    res_get = client.get("/api/v1/platform/tenants", headers=headers_gestor)
    assert res_get.status_code == 403

    res_post = client.post("/api/v1/platform/tenants", json={
        "name": "Tentativa Invalida",
        "slug": "tentativa_invalid",
        "port": 8090,
        "master_chef_email": "invasor@teste.com",
        "master_chef_password": "SenhaSegura123"
    }, headers=headers_gestor)
    assert res_post.status_code == 403

    # Docente tentando acessar
    docente_token = get_token_for("docente.teste@classsync.ai", "Senha1234")
    headers_docente = {"Authorization": f"Bearer {docente_token}"}
    res_docente = client.get("/api/v1/platform/tenants", headers=headers_docente)
    assert res_docente.status_code == 403


def test_unauthenticated_rejected():
    res = client.get("/api/v1/platform/tenants")
    assert res.status_code == 401


def test_create_tenant_provisioning_flow():
    token = get_token_for("doctor@classsync.ai", "Doctor@2026")
    headers = {"Authorization": f"Bearer {token}"}

    payload = {
        "name": "Faculdade Teste Automatizado",
        "slug": TEST_TENANT_SLUG,
        "port": TEST_TENANT_PORT,
        "master_chef_email": "diretor@teste022.edu.br",
        "master_chef_password": "Provisoria@2026"
    }

    res = client.post("/api/v1/platform/tenants", json=payload, headers=headers)
    assert res.status_code == 202
    body = res.json()
    assert body["status"] == "provisioning"
    assert body["tenant"]["slug"] == TEST_TENANT_SLUG
    assert body["tenant"]["port"] == TEST_TENANT_PORT
    assert body["tenant"]["url"] == f"http://localhost:{TEST_TENANT_PORT}/"

    # Background task cria o arquivo .env e o diretório de dados
    assert os.path.exists(TEST_ENV_FILE)
    assert os.path.exists(TEST_DATA_DIR)

    # Validar banco SQLite criado e master-chef semeado com must_change_password=True
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    tenant_db = os.path.join(TEST_DATA_DIR, "project.db")
    assert os.path.exists(tenant_db)

    t_engine = create_engine(f"sqlite:///{os.path.abspath(tenant_db)}")
    TSession = sessionmaker(bind=t_engine)
    session = TSession()
    try:
        user = session.query(User).filter(User.email == "diretor@teste022.edu.br").first()
        assert user is not None
        assert user.role == "gestor"
        assert user.is_active is True
        assert user.must_change_password is True
    finally:
        session.close()
        t_engine.dispose()


def test_create_tenant_conflict():
    token = get_token_for("doctor@classsync.ai", "Doctor@2026")
    headers = {"Authorization": f"Bearer {token}"}

    payload = {
        "name": "Faculdade Duplicada",
        "slug": TEST_TENANT_SLUG,
        "port": TEST_TENANT_PORT,
        "master_chef_email": "outro@teste022.edu.br",
        "master_chef_password": "Provisoria@2026"
    }

    res = client.post("/api/v1/platform/tenants", json=payload, headers=headers)
    assert res.status_code == 409


def test_change_password_flow():
    # Cria usuário com must_change_password=True no banco principal para testar o endpoint /auth/change-password
    db = SessionLocal()
    try:
        test_user = db.query(User).filter(User.email == "troca.senha@teste.com").first()
        if not test_user:
            test_user = User(
                id="u-pwd-test",
                name="Usuário Troca Senha",
                email="troca.senha@teste.com",
                password_hash=hash_password("Provisoria123"),
                role="gestor",
                department="Geral",
                is_active=True,
                must_change_password=True
            )
            db.add(test_user)
            db.commit()
        else:
            test_user.password_hash = hash_password("Provisoria123")
            test_user.must_change_password = True
            db.commit()
    finally:
        db.close()

    # 1. Login com senha provisória
    login_res = client.post("/api/v1/auth/login", json={"email": "troca.senha@teste.com", "password": "Provisoria123"})
    assert login_res.status_code == 200
    token = login_res.json()["access_token"]
    assert login_res.json()["user"]["must_change_password"] is True
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Tentativa com senha atual errada
    err_res = client.post("/api/v1/auth/change-password", json={
        "current_password": "SenhaErrada",
        "new_password": "NovaSenhaForte@2026"
    }, headers=headers)
    assert err_res.status_code == 401

    # 3. Tentativa com nova senha muito curta (<8 chars)
    short_res = client.post("/api/v1/auth/change-password", json={
        "current_password": "Provisoria123",
        "new_password": "curta"
    }, headers=headers)
    assert short_res.status_code == 400

    # 4. Tentativa com nova senha igual à atual
    same_res = client.post("/api/v1/auth/change-password", json={
        "current_password": "Provisoria123",
        "new_password": "Provisoria123"
    }, headers=headers)
    assert same_res.status_code == 400

    # 5. Troca com sucesso
    success_res = client.post("/api/v1/auth/change-password", json={
        "current_password": "Provisoria123",
        "new_password": "NovaSenhaForte@2026"
    }, headers=headers)
    assert success_res.status_code == 200
    assert success_res.json()["status"] == "success"
    assert success_res.json()["must_change_password"] is False

    # 6. Novo login com a senha antiga deve falhar
    old_login = client.post("/api/v1/auth/login", json={"email": "troca.senha@teste.com", "password": "Provisoria123"})
    assert old_login.status_code == 401

    # 7. Novo login com a nova senha deve funcionar com must_change_password=False
    new_login = client.post("/api/v1/auth/login", json={"email": "troca.senha@teste.com", "password": "NovaSenhaForte@2026"})
    assert new_login.status_code == 200
    assert new_login.json()["user"]["must_change_password"] is False


def test_get_tenant_detail_success():
    token = get_token_for("doctor@classsync.ai", "Doctor@2026")
    headers = {"Authorization": f"Bearer {token}"}

    res = client.get(f"/api/v1/platform/tenants/{TEST_TENANT_SLUG}", headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert data["slug"] == TEST_TENANT_SLUG
    assert data["port"] == TEST_TENANT_PORT
    assert "status" in data
    assert data["master_chef"] is not None
    assert data["master_chef"]["email"] == "diretor@teste022.edu.br"
    assert data["master_chef"]["role"] == "gestor"


def test_get_tenant_detail_not_found():
    token = get_token_for("doctor@classsync.ai", "Doctor@2026")
    headers = {"Authorization": f"Bearer {token}"}

    res = client.get("/api/v1/platform/tenants/slug_inexistente_999", headers=headers)
    assert res.status_code == 404


def test_update_tenant_metadata_success():
    token = get_token_for("doctor@classsync.ai", "Doctor@2026")
    headers = {"Authorization": f"Bearer {token}"}

    update_payload = {
        "name": "Centro Universitário Inovação Teste",
        "master_chef_email": "novo_diretor@teste022.edu.br"
    }
    res = client.put(f"/api/v1/platform/tenants/{TEST_TENANT_SLUG}", json=update_payload, headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert data["name"] == "Centro Universitário Inovação Teste"
    assert data["slug"] == TEST_TENANT_SLUG
    assert data["port"] == TEST_TENANT_PORT
    assert data["master_chef"]["email"] == "novo_diretor@teste022.edu.br"

    # Validar que o endpoint de listagem também reflete o novo nome
    list_res = client.get("/api/v1/platform/tenants", headers=headers)
    tenant_item = next((t for t in list_res.json()["tenants"] if t["slug"] == TEST_TENANT_SLUG), None)
    assert tenant_item is not None
    assert tenant_item["name"] == "Centro Universitário Inovação Teste"


def test_reset_master_chef_password():
    token = get_token_for("doctor@classsync.ai", "Doctor@2026")
    headers = {"Authorization": f"Bearer {token}"}

    # 1. Reset automático (sem senha manual informada)
    res_auto = client.post(f"/api/v1/platform/tenants/{TEST_TENANT_SLUG}/master-chef/reset", json={}, headers=headers)
    assert res_auto.status_code == 200
    body_auto = res_auto.json()
    assert body_auto["slug"] == TEST_TENANT_SLUG
    assert len(body_auto["temporary_password"]) >= 10
    assert body_auto["must_change_password"] is True

    # 2. Reset com senha manual especificada
    manual_pwd = "SenhaManualForte@2026"
    res_man = client.post(f"/api/v1/platform/tenants/{TEST_TENANT_SLUG}/master-chef/reset", json={
        "new_password": manual_pwd
    }, headers=headers)
    assert res_man.status_code == 200
    body_man = res_man.json()
    assert body_man["temporary_password"] == manual_pwd
    assert body_man["must_change_password"] is True

    # 3. Conferir na base SQLite do tenant
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from src.api.auth import verify_password
    tenant_db = os.path.join(TEST_DATA_DIR, "project.db")
    t_engine = create_engine(f"sqlite:///{os.path.abspath(tenant_db)}")
    TSession = sessionmaker(bind=t_engine)
    session = TSession()
    try:
        user = session.query(User).filter(User.role == "gestor").first()
        assert user is not None
        assert user.must_change_password is True
        assert verify_password(manual_pwd, user.password_hash) is True
    finally:
        session.close()
        t_engine.dispose()


def test_crud_endpoints_rbac_protection():
    gestor_token = get_token_for("admin@classsync.ai", "admin123")
    headers_gestor = {"Authorization": f"Bearer {gestor_token}"}

    # GET detail bloqueado
    assert client.get(f"/api/v1/platform/tenants/{TEST_TENANT_SLUG}", headers=headers_gestor).status_code == 403
    # PUT update bloqueado
    assert client.put(f"/api/v1/platform/tenants/{TEST_TENANT_SLUG}", json={"name": "Hacker"}, headers=headers_gestor).status_code == 403
    # POST reset bloqueado
    assert client.post(f"/api/v1/platform/tenants/{TEST_TENANT_SLUG}/master-chef/reset", json={}, headers=headers_gestor).status_code == 403
    # DELETE bloqueado
    assert client.request("DELETE", f"/api/v1/platform/tenants/{TEST_TENANT_SLUG}", json={"confirm_slug": TEST_TENANT_SLUG}, headers=headers_gestor).status_code == 403


def test_delete_tenant_soft_delete_and_freed_port():
    token = get_token_for("doctor@classsync.ai", "Doctor@2026")
    headers = {"Authorization": f"Bearer {token}"}

    # 1. Tentativa de deleção com slug divergente deve falhar
    err_res = client.request("DELETE", f"/api/v1/platform/tenants/{TEST_TENANT_SLUG}", json={"confirm_slug": "slug_divergente"}, headers=headers)
    assert err_res.status_code == 400

    # 2. Deleção correta com confirmação de slug
    del_res = client.request("DELETE", f"/api/v1/platform/tenants/{TEST_TENANT_SLUG}", json={"confirm_slug": TEST_TENANT_SLUG}, headers=headers)
    assert del_res.status_code == 200
    del_body = del_res.json()
    assert del_body["status"] == "archived"
    assert del_body["freed_port"] == TEST_TENANT_PORT
    assert "archived_path" in del_body

    # 3. Validar que o diretório foi arquivado em data/.archived
    archived_base = os.path.join("data", ".archived")
    assert os.path.exists(archived_base)
    archived_dirs = [d for d in os.listdir(archived_base) if d.startswith(TEST_TENANT_SLUG)]
    assert len(archived_dirs) > 0

    # 4. Validar que o tenant não aparece mais como ativo
    get_after = client.get(f"/api/v1/platform/tenants/{TEST_TENANT_SLUG}", headers=headers)
    assert get_after.status_code == 404


def test_tenant_start_stop_endpoints_and_status(monkeypatch):
    import src.api.routes as routes_mod
    monkeypatch.setattr(routes_mod, "start_tenant_instance", lambda slug, port: True)
    monkeypatch.setattr(routes_mod, "stop_tenant_instance", lambda slug, port: True)
    monkeypatch.setattr(routes_mod, "check_tenant_status", lambda port: "online")

    token = get_token_for("doctor@classsync.ai", "Doctor@2026")
    headers = {"Authorization": f"Bearer {token}"}

    res_list = client.get("/api/v1/platform/tenants", headers=headers)
    assert res_list.status_code == 200
    tenants = res_list.json()["tenants"]
    if tenants:
        sample_slug = tenants[0]["slug"]
        start_res = client.post(f"/api/v1/platform/tenants/{sample_slug}/start", headers=headers)
        assert start_res.status_code == 200
        assert start_res.json()["slug"] == sample_slug
        assert start_res.json()["status"] == "online"

        monkeypatch.setattr(routes_mod, "check_tenant_status", lambda port: "offline")
        stop_res = client.post(f"/api/v1/platform/tenants/{sample_slug}/stop", headers=headers)
        assert stop_res.status_code == 200
        assert stop_res.json()["slug"] == sample_slug
        assert stop_res.json()["status"] == "offline"


