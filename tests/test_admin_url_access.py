import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.database import SessionLocal
from src.models import User
from src.api.auth import hash_password

client = TestClient(app)


def setup_module(module):
    """Garante existência dos usuários padrão no banco de teste."""
    db = SessionLocal()
    try:
        doc = db.query(User).filter(User.email == "doctor@classsync.ai").first()
        if not doc:
            doc = User(
                id="u-doctor-test",
                name="Super Administrador Geral",
                email="doctor@classsync.ai",
                password_hash=hash_password("Doctor@2026"),
                role="doctor-chef",
                department="Plataforma Global",
                is_active=True,
                must_change_password=False
            )
            db.add(doc)
            db.commit()
    finally:
        db.close()


def test_admin_direct_routes():
    """Valida que todas as rotas web de administrador geral respondem com 200 e entregam o frontend SPA."""
    admin_routes = [
        "/admin",
        "/admin/",
        "/platform",
        "/platform/",
        "/superadmin",
        "/superadmin/",
        "/administrador",
        "/administrador/",
        "/admin-geral",
        "/admin-geral/",
        "/"
    ]
    for route in admin_routes:
        res = client.get(route)
        assert res.status_code == 200, f"Rota {route} falhou com status {res.status_code}"
        assert "text/html" in res.headers.get("content-type", "")
        assert "tabLoginAdmin" in res.text
        assert "openAdminLoginModal" in res.text
        assert "doctor@classsync.ai" in res.text


def test_login_as_doctor_chef():
    """Valida que o login do doctor-chef funciona diretamente e retorna token válido."""
    res = client.post("/api/v1/auth/login", json={
        "email": "doctor@classsync.ai",
        "password": "Doctor@2026"
    })
    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data
    assert data["user"]["role"] == "doctor-chef"
    assert data["user"]["name"] == "Super Administrador Geral"

    # Valida que o token dá acesso à rota de governança de tenants
    token = data["access_token"]
    tenants_res = client.get("/api/v1/platform/tenants", headers={"Authorization": f"Bearer {token}"})
    assert tenants_res.status_code == 200
    tenants_data = tenants_res.json()
    assert "tenants" in tenants_data
    assert "next_available_port" in tenants_data


def test_cors_headers_configured():
    """Valida que o CORS middleware está configurado para acesso multi-origem."""
    res = client.options("/", headers={
        "Origin": "https://meu-dominio-customizado.com.br",
        "Access-Control-Request-Method": "GET"
    })
    assert res.status_code == 200
    assert res.headers.get("access-control-allow-origin") in ("*", "https://meu-dominio-customizado.com.br")
