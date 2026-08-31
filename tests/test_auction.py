import pytest
from src.engine.core import CoreAllocationEngine

def test_auction_cooperative_compensation():
    """
    Testa se o leilão cooperativo deduz créditos do vencedor do leilão
    e compensa o perdedor da disputa de sala.
    """
    rooms = [
        {"id": "sala-unica", "name": "Sala Única", "capacity": 50, "room_type": "common", "features": [], "is_accessible": True, "block_id": "Bloco A"}
    ]
    # Engenharia tem mais créditos históricos (2000) e maior urgência (5) do que Direito (1000 e 3)
    coordinations = [
        {"id": "eng", "name": "Engenharia", "credits": 2000},
        {"id": "dir", "name": "Direito", "credits": 1000}
    ]
    classes = [
        {"id": "eng-01", "students_count": 30, "room_type": "common", "time_slot": "M1", "coordination_id": "eng", "urgency": 5},
        {"id": "dir-01", "students_count": 30, "room_type": "common", "time_slot": "M1", "coordination_id": "dir", "urgency": 3}
    ]
    
    engine = CoreAllocationEngine(rooms, coordinations, classes)
    
    # Executar a rodada
    allocations, _, bids = engine.run_allocation()
    
    # 1. Validar vencedor e perdedor
    assert allocations["eng-01"]["room_id"] == "sala-unica"
    # A turma de Direito deve ser marcada para arbitragem ou ficar sem sala se não houver alternativa livre
    assert allocations["dir-01"]["status"] == "pending_arbitration"
    
    # 2. Validar transferência de créditos
    # Lance esperado do ACC Engenharia: 2000 * 20% * (5/5) = 400 créditos
    # Saldo final Engenharia: 2000 - 400 = 1600
    # Saldo final Direito: 1000 + 400 = 1400 (compensação recebida)
    assert engine.accs["eng"].credits == 1600
    assert engine.accs["dir"].credits == 1400
    
    # 3. Validar se a transação do leilão foi devidamente auditada
    assert len(bids) == 1
    assert bids[0]["winner_id"] == "eng"
    assert bids[0]["loser_id"] == "dir"
    assert bids[0]["credits_spent"] == 400
