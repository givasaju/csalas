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
