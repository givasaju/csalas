import pytest
from src.engine.core import CoreAllocationEngine

def test_building_consolidation_saving():
    """
    Testa se turmas em blocos subutilizados (ocupação < 20%) são migradas
    para salas equivalentes em blocos mais povoados, e se o bloco original
    é sinalizado para desativação (economia energética).
    """
    rooms = [
        # Bloco A é o bloco ativo
        {"id": "sala-a1", "name": "Sala A1", "capacity": 50, "room_type": "common", "features": [], "is_accessible": True, "block_id": "Bloco A"},
        {"id": "sala-a2", "name": "Sala A2", "capacity": 50, "room_type": "common", "features": [], "is_accessible": True, "block_id": "Bloco A"},
        # Bloco B tem apenas uma turma (ocupação muito baixa)
        {"id": "sala-b1", "name": "Sala B1", "capacity": 50, "room_type": "common", "features": [], "is_accessible": True, "block_id": "Bloco B"}
    ]
    coordinations = [{"id": "eng", "name": "Engenharia", "credits": 1000}]
    classes = [
        # Duas turmas no Bloco A
        {"id": "turma-a1", "students_count": 30, "room_type": "common", "time_slot": "M1", "coordination_id": "eng", "urgency": 3},
        {"id": "turma-a2", "students_count": 30, "room_type": "common", "time_slot": "M2", "coordination_id": "eng", "urgency": 3},
        # Uma turma inicialmente no Bloco B (slot M3)
        {"id": "turma-b1", "students_count": 30, "room_type": "common", "time_slot": "M3", "coordination_id": "eng", "urgency": 3}
    ]
    
    engine = CoreAllocationEngine(rooms, coordinations, classes)
    
    # Executar a rodada
    allocations, deactivated_blocks, _ = engine.run_allocation()
    
    # A turma-b1 deve ter sido migrada para a sala A1 ou A2 que estavam livres no slot M3
    assert allocations["turma-b1"]["room_id"] in ["sala-a1", "sala-a2"]
    
    # O Bloco B deve ter sido totalmente consolidado e desativado
    assert "Bloco B" in deactivated_blocks
