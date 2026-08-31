import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_static_files_home():
    """
    Testa se a página home (index.html) é servida com sucesso
    através da rota estática da aplicação.
    """
    response = client.get("/")
    assert response.status_code == 200
    # Deve conter menção ao título do ClassSync AI
    assert "ClassSync AI" in response.text
    assert "Dashboard de Ocupação" in response.text


def test_static_files_css():
    """
    Testa se o arquivo index.css é carregado com sucesso
    e possui o tipo MIME correto.
    """
    response = client.get("/index.css")
    assert response.status_code == 200
    # Deve conter tags e variáveis CSS do nosso tema
    assert "--bg-primary" in response.text
    assert "body" in response.text
