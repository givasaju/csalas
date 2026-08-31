import logging
from typing import List, Dict, Any

logger = logging.getLogger("core-allocation-engine")

class BuildingOptimizer:
    """
    BuildingOptimizer.
    Otimiza a ocupação física do campus reagrupando turmas em blocos prediais,
    com o objetivo de consolidar o uso e permitir o desligamento ou economia
    de blocos prediais subutilizados (com menos de 20% de ocupação esperada).
    """
    @staticmethod
    def optimize_building_occupancy(
        allocations: Dict[str, Dict[str, Any]],  # class_id -> {room_id, time_slot, ...}
        rooms: List[Dict[str, Any]],              # lista de salas cadastradas
        blocks: List[str]                         # lista de nomes de blocos
    ) -> tuple[Dict[str, Dict[str, Any]], List[str]]:
        """
        Retorna a nova distribuição de alocações otimizada predialmente
        e a lista de blocos prediais desativados (economizados).
        """
        # 1. Calcular a taxa de ocupação por bloco
        block_alloc_counts = {b: 0 for b in blocks}
        block_total_slots = {b: 0 for b in blocks}
        
        # Calcular total de slots por bloco (capacidade física das salas * 6 turnos)
        for room in rooms:
            b = room["block_id"]
            if b in block_total_slots:
                block_total_slots[b] += 6 # Assume 6 slots de tempo padrão por dia
                
        # Contar alocações ativas por bloco
        for alloc in allocations.values():
            r_id = alloc.get("room_id")
            if r_id is None:
                continue
            room = next((r for r in rooms if r["id"] == r_id), None)
            if room:
                b = room["block_id"]
                if b in block_alloc_counts:
                    block_alloc_counts[b] += 1

        # 2. Identificar blocos subutilizados (ocupação < 20%)
        underutilized_blocks = []
        for b in blocks:
            total = block_total_slots.get(b, 0)
            if total > 0:
                occupancy = block_alloc_counts.get(b, 0) / total
                logger.info(f"Bloco {b}: Ocupação de {occupancy*100:.1f}% ({block_alloc_counts[b]}/{total} slots)")
                if occupancy < 0.20 and block_alloc_counts[b] > 0:
                    underutilized_blocks.append(b)

        if not underutilized_blocks:
            logger.info("Nenhum bloco subutilizado identificado para consolidação.")
            # Calcular mesmo assim se algum bloco já começou com zero alocações
            final_block_counts = {b: 0 for b in blocks}
            for alloc in allocations.values():
                r_id = alloc.get("room_id")
                if r_id:
                    room = next((r for r in rooms if r["id"] == r_id), None)
                    if room:
                        final_block_counts[room["block_id"]] += 1
            deactivated_blocks = [b for b, count in final_block_counts.items() if count == 0]
            return allocations, deactivated_blocks

        logger.info(f"Blocos subutilizados identificados para esvaziamento: {underutilized_blocks}")
        
        # 3. Tentar mover as turmas dos blocos subutilizados para blocos com maior ocupação
        new_allocations = dict(allocations)

        for target_block in underutilized_blocks:
            # Selecionar turmas alocadas neste bloco
            classes_to_move = []
            for class_id, alloc in new_allocations.items():
                r_id = alloc.get("room_id")
                if r_id is None:
                    continue
                room = next((r for r in rooms if r["id"] == r_id), None)
                if room and room["block_id"] == target_block:
                    classes_to_move.append((class_id, alloc, room))

            for class_id, alloc, current_room in classes_to_move:
                # Buscar sala substituta em um bloco ativo (não subutilizado)
                alternative_room = None
                for candidate_room in rooms:
                    if candidate_room["block_id"] in underutilized_blocks:
                        continue # Não mover para outro bloco subutilizado
                    
                    # Restrições mandatórias (Hard Constraints)
                    # 1. Capacidade
                    if candidate_room["capacity"] < alloc["students_count"]:
                        continue
                    # 2. Tipo/Acessibilidade
                    if current_room["room_type"] != candidate_room["room_type"]:
                        continue
                    if current_room["is_accessible"] and not candidate_room["is_accessible"]:
                        continue
                    # 3. Equipamentos/features necessários
                    features_match = all(f in candidate_room["features"] for f in current_room["features"])
                    if not features_match:
                        continue
                        
                    # 4. Slot de tempo livre (não ocupado por outra alocação ativa)
                    slot_busy = any(
                        other_alloc.get("room_id") == candidate_room["id"] and other_alloc["time_slot"] == alloc["time_slot"]
                        for other_alloc in new_allocations.values()
                    )
                    if not slot_busy:
                        alternative_room = candidate_room
                        break

                if alternative_room:
                    # Executar migração predial
                    new_allocations[class_id] = {
                        **alloc,
                        "room_id": alternative_room["id"]
                    }
                    logger.info(f"Turma {class_id} migrada com sucesso da sala {current_room['name']} ({current_room['block_id']}) para sala {alternative_room['name']} ({alternative_room['block_id']})")
            
        # 4. Calcular quais blocos terminaram com zero alocações ativas
        final_block_counts = {b: 0 for b in blocks}
        for alloc in new_allocations.values():
            r_id = alloc.get("room_id")
            if r_id:
                room = next((r for r in rooms if r["id"] == r_id), None)
                if room:
                    final_block_counts[room["block_id"]] += 1
                    
        deactivated_blocks = [b for b, count in final_block_counts.items() if count == 0]
        logger.info(f"Blocos prediais finais desativados (zero ocupação): {deactivated_blocks}")

        return new_allocations, deactivated_blocks
