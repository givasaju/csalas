import pytest
from src.engine.core import CoreAllocationEngine

def test_mandatory_constraints_capacity():
    """
    Testa se o motor impede a alocação de turmas em salas
    com capacidade física menor do que o número de alunos esperado.
    """
    rooms = [
        {"id": "sala-10", "name": "Sala 10", "capacity": 10, "room_type": "common", "features": [], "is_accessible": True, "block_id": "Bloco A"},
        {"id": "sala-50", "name": "Sala 50", "capacity": 50, "room_type": "common", "features": [], "is_accessible": True, "block_id": "Bloco A"}
    ]
    coordinations = [{"id": "eng", "name": "Engenharia", "credits": 1000}]
    classes = [
        {"id": "eng-01", "students_count": 40, "room_type": "common", "time_slot": "M1", "coordination_id": "eng", "urgency": 3, "require_accessibility": False}
    ]
    
    engine = CoreAllocationEngine(rooms, coordinations, classes)
    allocations, _, _ = engine.run_allocation()
    
    assert allocations["eng-01"]["room_id"] == "sala-50"


def test_mandatory_constraints_accessibility():
    """
    Testa se o motor direciona turmas que necessitam de acessibilidade
    obrigatoriamente para salas com flag is_accessible = True.
    """
    rooms = [
        {"id": "sala-comum", "name": "Sala Comum", "capacity": 40, "room_type": "common", "features": [], "is_accessible": False, "block_id": "Bloco B"},
        {"id": "sala-acessivel", "name": "Sala Acessível", "capacity": 40, "room_type": "common", "features": [], "is_accessible": True, "block_id": "Bloco B"}
    ]
    coordinations = [{"id": "eng", "name": "Engenharia", "credits": 1000}]
    classes = [
        {"id": "eng-02", "students_count": 30, "room_type": "common", "time_slot": "M1", "coordination_id": "eng", "urgency": 3, "require_accessibility": True}
    ]
    
    engine = CoreAllocationEngine(rooms, coordinations, classes)
    allocations, _, _ = engine.run_allocation()
    
    assert allocations["eng-02"]["room_id"] == "sala-acessivel"
