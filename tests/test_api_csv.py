import pytest
import uuid
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_import_csv_success():
    """
    Testa a importação correta de salas de aula a partir de CSV válido.
    """
    headers = {"Authorization": "Bearer mock-token"}
    r1 = f"Sala-{str(uuid.uuid4())[:8]}"
    r2 = f"Lab-{str(uuid.uuid4())[:8]}"
    
    csv_data = (
        "bloco,sala,capacidade,tipo,acessivel,recursos\n"
        f"Bloco X,{r1},50,common,True,projector\n"
        f"Bloco Y,{r2},30,lab,False,computers;projector\n"
    )
    
    files = {"file": ("salas.csv", csv_data, "text/csv")}
    
    response = client.post("/api/v1/rooms/import-csv", files=files, headers=headers)
    assert response.status_code == 200
    assert response.json()["imported_count"] == 2


def test_import_csv_all_or_nothing_rollback():
    """
    Testa a política 'Tudo ou Nada': se houver erro em uma linha do CSV,
    toda a carga deve ser rejeitada e o banco deve continuar intacto.
    """
    headers = {"Authorization": "Bearer mock-token"}
    
    # Segunda linha tem capacidade -10 (inválida)
    csv_data = (
        "bloco,sala,capacidade,tipo,acessivel,recursos\n"
        "Bloco X,Sala 301,50,common,True,projector\n"
        "Bloco Y,Lab 302,-10,lab,False,computers;projector\n"
    )
    
    files = {"file": ("salas_error.csv", csv_data, "text/csv")}
    
    response = client.post("/api/v1/rooms/import-csv", files=files, headers=headers)
    assert response.status_code == 422
