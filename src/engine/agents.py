import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger("core-allocation-engine")

class ACC:
    """
    Agente Coordenador de Curso (ACC).
    Representa os interesses de uma coordenação de curso, defendendo a alocação
    de suas disciplinas e gerenciando seus créditos acadêmicos.
    """
    def __init__(self, id_coord: str, name: str, credits: int = 1000):
        self.id_coord = id_coord
        self.name = name
        self.credits = credits

    def make_bid(self, class_id: str, room_id: str, urgency: int) -> int:
        """
        Calcula o lance (bid) para disputar uma sala baseado na urgência acadêmica
        e no saldo de créditos atual do agente.
        """
        # Regra de lance: consome no máximo 20% do saldo atual proporcional à urgência (1 a 5)
        if self.credits <= 0:
            return 0
        max_allocable = int(self.credits * 0.20)
        bid = int(max_allocable * (urgency / 5.0))
        return max(1, bid)

    def deduct_credits(self, amount: int):
        self.credits = max(0, self.credits - amount)

    def receive_credits(self, amount: int):
        self.credits += amount


class AMR:
    """
    Agente Mediador e Reputação (AMR).
    Arbitra disputas de alocação de salas entre diferentes ACCs usando leilões de créditos.
    """
    def __init__(self):
        self.bids_history: List[Dict[str, Any]] = []

    def resolve_dispute(self, room_id: str, time_slot: str, competitor_bids: Dict[ACC, int]) -> ACC:
        """
        Arbitra a disputa entre coordenações concorrentes.
        Retorna o ACC vencedor.
        O vencedor paga o lance ao perdedor como compensação (leilão cooperativo).
        """
        if not competitor_bids:
            raise ValueError("Não há competidores para resolver a disputa.")

        # Ordenar competidores pelo valor do lance de forma decrescente
        sorted_competitors = sorted(competitor_bids.items(), key=lambda item: item[1], reverse=True)
        winner_acc, winning_bid = sorted_competitors[0]

        # Se houver empate no maior lance
        if len(sorted_competitors) > 1 and sorted_competitors[0][1] == sorted_competitors[1][1]:
            # Em caso de empate, o vencedor é quem tem mais créditos totais no momento
            if sorted_competitors[0][0].credits >= sorted_competitors[1][0].credits:
                winner_acc, winning_bid = sorted_competitors[0]
            else:
                winner_acc, winning_bid = sorted_competitors[1]

        # Processar compensações de créditos
        for competitor, bid in competitor_bids.items():
            if competitor == winner_acc:
                competitor.deduct_credits(winning_bid)
                logger.info(f"ACC {competitor.name} venceu o leilão e pagou {winning_bid} créditos.")
            else:
                competitor.receive_credits(winning_bid)
                logger.info(f"ACC {competitor.name} perdeu o leilão e recebeu {winning_bid} créditos de compensação.")
                
                # Registrar transação na auditoria
                self.bids_history.append({
                    "room_id": room_id,
                    "time_slot": time_slot,
                    "winner_id": winner_acc.id_coord,
                    "winner_name": winner_acc.name,
                    "loser_id": competitor.id_coord,
                    "loser_name": competitor.name,
                    "credits_spent": winning_bid
                })

        return winner_acc
