import pytest
from src.engine.core import CoreAllocationEngine

def test_engine_hard_constraint_teacher_restriction():
    """
    Testa que o motor recusa alocação de turma em slot indisponível do professor (Hard Constraint).
    """
    rooms = [
        {"id": "r101", "block_id": "A", "name": "Sala 101", "capacity": 50, "room_type": "common", "is_accessible": True, "features": []}
    ]
    coordinations = [
        {"id": "eng", "name": "Engenharia", "credits": 1000}
    ]
    classes = [
        {
            "id": "turma-1",
            "students_count": 30,
            "room_type": "common",
            "time_slot": "M1",
            "day_of_week": 1,
            "coordination_id": "eng",
            "teacher_id": "prof-claudio"
        }
    ]
    restrictions = [
        {"teacher_id": "prof-claudio", "day_of_week": 1, "time_slot_id": "M1"}
    ]

    engine = CoreAllocationEngine(rooms, coordinations, classes, restrictions)
    allocations, deactivated, bids = engine.run_allocation()

    assert "turma-1" in allocations
    # Turma não deve ter sido alocada na sala r101 devido à restrição do professor
    assert allocations["turma-1"]["room_id"] is None
    assert allocations["turma-1"]["status"] == "pending_arbitration"


def test_engine_teacher_allocations_map_consecutive_limit():
    """
    Testa que o mapa auxiliar teacher_allocations_map é atualizado e limita aulas consecutivas a no máximo 4.
    """
    rooms = [
        {"id": f"r10{i}", "block_id": "A", "name": f"Sala 10{i}", "capacity": 50, "room_type": "common", "is_accessible": True, "features": []}
        for i in range(1, 6)
    ]
    coordinations = [{"id": "eng", "name": "Engenharia", "credits": 1000}]
    
    classes = [
        {
            "id": f"turma-{i}",
            "students_count": 30,
            "room_type": "common",
            "time_slot": f"M{i}",
            "day_of_week": 1,
            "coordination_id": "eng",
            "teacher_id": "prof-speed"
        }
        for i in range(1, 6)
    ]

    engine = CoreAllocationEngine(rooms, coordinations, classes)
    allocations, deactivated, bids = engine.run_allocation()

    # As primeiras 4 turmas devem ser alocadas com sucesso
    for i in range(1, 5):
        assert allocations[f"turma-{i}"]["room_id"] is not None

    # A 5ª turma (M5) deve ser recusada por atingir o limite de 4 aulas seguidas no mesmo turno
    assert allocations["turma-5"]["room_id"] is None
    assert allocations["turma-5"]["status"] == "pending_arbitration"
    assert "4 aulas seguidas" in allocations["turma-5"]["conflict_reason"]
    # Verificar indexação do mapa auxiliar O(1)
    assert engine.teacher_allocations_map[("prof-speed", "1")] == ["M1", "M2", "M3", "M4"]
