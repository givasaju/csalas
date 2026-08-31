"""
Validador de alocações de aula e consecutividade de horários docentes.
"""

from typing import List, Dict, Any


def check_consecutive_limit(existing_sub_slots: List[int], new_sub_slot: int) -> bool:
    """
    Verifica se adicionar 'new_sub_slot' resulta em uma sequência de mais de 4 sub-slots consecutivos.
    Retorna True se for válido (<= 4 consecutivos) e False se violar (> 4 consecutivos).
    """
    all_slots = sorted(set(existing_sub_slots + [new_sub_slot]))
    if len(all_slots) <= 4:
        return True

    max_consecutive = 1
    current = 1
    for i in range(1, len(all_slots)):
        if all_slots[i] == all_slots[i - 1] + 1:
            current += 1
            if current > max_consecutive:
                max_consecutive = current
        else:
            current = 1

    return max_consecutive <= 4
