import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.database import SessionLocal
from src.models import User
from src.api.auth import hash_password

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_auth_db():
    db = SessionLocal()
    try:
        # Limpar usuários de teste anteriores
        db.query(User).filter(User.email.like("%teste%")).delete()
        db.commit()

        # Garantir que o gestor inicial exista
        admin = db.query(User).filter(User.email == "admin@classsync.ai").first()
        if not admin:
            admin = User(
                id="u-admin-test",
                name="Gestor Principal",
                email="admin@classsync.ai",
                password_hash=hash_password("admin123"),
                role="gestor",
                department="Administração",
                is_active=True
            )
            db.add(admin)
            db.commit()
    finally:
        db.close()

    yield

    db = SessionLocal()
    try:
        db.query(User).filter(User.email.like("%teste%")).delete()
        db.commit()
    finally:
        db.close()


def test_register_and_pending_status():
    # Cadastro de novo usuário
    payload = {
        "name": "Professora Maria",
        "email": "maria.teste@universidade.edu.br",
        "password": "senhaForte123",
        "department": "Ciência da Computação"
    }
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "success"
    assert data["user"]["email"] == "maria.teste@universidade.edu.br"
    assert data["user"]["is_active"] is False


def test_login_pending_user_fails():
    # 1. Registrar usuário
    client.post("/api/v1/auth/register", json={
        "name": "Professor Pendente",
        "email": "pendente.teste@universidade.edu.br",
        "password": "senhaForte123",
        "department": "Engenharia"
    })

    # 2. Tentar login com usuário pendente
    login_payload = {
        "email": "pendente.teste@universidade.edu.br",
        "password": "senhaForte123"
    }
    response = client.post("/api/v1/auth/login", json=login_payload)
    assert response.status_code == 403
    assert "aguarda aprovação" in response.json()["detail"].lower()


def test_login_wrong_password():
    login_payload = {
        "email": "admin@classsync.ai",
        "password": "senhaIncorreta"
    }
    response = client.post("/api/v1/auth/login", json=login_payload)
    assert response.status_code == 401


def test_admin_login_and_user_approval_flow():
    # 1. Registrar usuário
    client.post("/api/v1/auth/register", json={
        "name": "Professora Maria",
        "email": "maria.teste@universidade.edu.br",
        "password": "senhaForte123",
        "department": "Ciência da Computação"
    })

    # 2. Login como gestor
    admin_login = client.post("/api/v1/auth/login", json={
        "email": "admin@classsync.ai",
        "password": "admin123"
    })
    assert admin_login.status_code == 200
    admin_token = admin_login.json()["access_token"]
    auth_headers = {"Authorization": f"Bearer {admin_token}"}

    # 3. Listar usuários
    users_res = client.get("/api/v1/users", headers=auth_headers)
    assert users_res.status_code == 200
    users = users_res.json()
    assert len(users) >= 1

    # 4. Encontrar usuário pendente e aprovar
    pending_user = next((u for u in users if u["email"] == "maria.teste@universidade.edu.br"), None)
    assert pending_user is not None
    assert pending_user["is_active"] is False

    approve_res = client.patch(
        f"/api/v1/users/{pending_user['id']}/status",
        json={"is_active": True, "role": "docente"},
        headers=auth_headers
    )
    assert approve_res.status_code == 200
    assert approve_res.json()["is_active"] is True

    # 5. Login com usuário agora aprovado
    user_login = client.post("/api/v1/auth/login", json={
        "email": "maria.teste@universidade.edu.br",
        "password": "senhaForte123"
    })
    assert user_login.status_code == 200
    user_token = user_login.json()["access_token"]

    # 6. Consultar /auth/me
    me_res = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {user_token}"})
    assert me_res.status_code == 200
    assert me_res.json()["email"] == "maria.teste@universidade.edu.br"

    # 7. Docente não pode listar usuários (403)
    forbidden_res = client.get("/api/v1/users", headers={"Authorization": f"Bearer {user_token}"})
    assert forbidden_res.status_code == 403
