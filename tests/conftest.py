import sys
import os
import pytest
from fastapi.testclient import TestClient

# Add project root to sys.path so that imports like `from src.main import app` work in tests.
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.main import app
from src.database import get_db, SessionLocal
from src import models

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def sample_report_data():
    rooms = [
        {"id": "r1", "block_id": "BLOCO_A", "name": "Sala A101", "capacity": 40, "room_type": "common", "is_accessible": True, "features": ["projetor"]},
        {"id": "r2", "block_id": "BLOCO_A", "name": "Lab A102", "capacity": 25, "room_type": "lab", "is_accessible": False, "features": ["pcs"]},
        {"id": "r3", "block_id": "BLOCO_B", "name": "AuditB1", "capacity": 100, "room_type": "auditorium", "is_accessible": True, "features": ["som"]}
    ]
    allocations = [
        {"room_id": "r1", "time_slot": "M1", "class_id": "c101", "coordination_id": "coord_cs"},
        {"room_id": "r2", "time_slot": "T1", "class_id": "c102", "coordination_id": "coord_eng"}
    ]
    return rooms, allocations
@pytest.fixture
def sample_allocation_fixtures():
    teacher_payload = {
        "id": "prof-test-consecutive",
        "name": "Prof. Ada Lovelace",
        "department": "Computação",
        "subjects": ["Computação"]
    }
    room_payload = {
        "id": "room-test-consecutive",
        "block_id": "BLOCO_TEST",
        "name": "Sala 101 Test",
        "capacity": 40,
        "room_type": "common",
        "is_accessible": True,
        "features": []
    }
    return teacher_payload, room_payload
