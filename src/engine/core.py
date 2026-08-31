import logging
from collections import defaultdict
from typing import List, Dict, Any, Tuple
from src.engine.agents import ACC, AMR
from src.engine.optimization import BuildingOptimizer

from src.api.allocation_validator import check_consecutive_limit

# Configuração de logger conforme RNF-03 de Observabilidade
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("core-allocation-engine")

class CoreAllocationEngine:
    """
    CoreAllocationEngine.
    Orquestrador principal do ClassSync AI. Junta as etapas de alocação inicial,
    leilões multiagentes de mediação de concorrência e otimização energética predial.
    """
    def __init__(self, rooms: List[Dict[str, Any]], coordinations: List[Dict[str, Any]], classes: List[Dict[str, Any]], restrictions: List[Dict[str, Any]] = None):
        self.rooms = rooms
        # Instanciar agentes ACC das coordenações
        self.accs = {str(c["id"]): ACC(str(c["id"]), c["name"], c.get("credits", 1000)) for c in coordinations}
        self.classes = classes
        self.restrictions = restrictions or []
        # Indexar restrições para busca em O(1): (teacher_id, str(day_of_week), time_slot_id)
        self.restrictions_set = {
            (r["teacher_id"], str(r["day_of_week"]), r["time_slot_id"])
            for r in self.restrictions
        }
        # Mapa auxiliar de alocações ativas por docente para verificação em O(1): (teacher_id, str(day_of_week)) -> List[time_slot]
        self.teacher_allocations_map: Dict[Tuple[str, str], List[str]] = defaultdict(list)
        self.amr = AMR()

    def _register_teacher_allocation(self, teacher_id: str, day_of_week: Any, time_slot: str) -> None:
        """Registra uma alocação no mapa auxiliar indexado do docente."""
        if teacher_id:
            key = (teacher_id, str(day_of_week))
            self.teacher_allocations_map[key].append(time_slot)

    def is_teacher_restricted(self, teacher_id: str, day_of_week: Any, time_slot: str) -> bool:
        """Verifica se o docente possui restrição horária cadastrada para o dia e slot."""
        if not teacher_id:
            return False
        return (teacher_id, str(day_of_week), time_slot) in self.restrictions_set

    def check_teacher_consecutive_limit(self, allocations: Dict[str, Dict[str, Any]], teacher_id: str, day_of_week: Any, time_slot: str) -> bool:
        """
        Verifica se a alocação resultaria em mais de 4 aulas seguidas no mesmo turno para o docente.
        Utiliza a indexação O(1) via mapa auxiliar teacher_allocations_map.
        """
        if not teacher_id:
            return True
        shift = time_slot[0] if time_slot else 'M'
        sub_slot_val = int(time_slot[1]) if len(time_slot) > 1 and time_slot[1].isdigit() else 1

        key = (teacher_id, str(day_of_week))
        teacher_slots = self.teacher_allocations_map.get(key, [])
        existing_sub_slots = []
        for alloc_slot in teacher_slots:
            if alloc_slot.startswith(shift):
                val = int(alloc_slot[1]) if len(alloc_slot) > 1 and alloc_slot[1].isdigit() else 1
                existing_sub_slots.append(val)

        return check_consecutive_limit(existing_sub_slots, sub_slot_val)

    def run_allocation(self) -> Tuple[Dict[str, Dict[str, Any]], List[str], List[Dict[str, Any]]]:
        """
        Executa a rodada de alocação de ponta a ponta.
        Retorna:
          1. Dicionário de alocações (class_id -> {room_id, time_slot, students_count})
          2. Lista de blocos prediais desativados (para economia de energia)
          3. Histórico de lances (bids) de auditoria
        """
        logger.info("=== Iniciando processamento de alocação pelo ClassSync AI ===")
        allocations: Dict[str, Dict[str, Any]] = {}
        
        # 1. Alocação Inicial (AAC)
        logger.info("Fase 1: Executando alocação inicial baseada em restrições mandatórias...")
        for cls in self.classes:
            class_id = cls["id"]
            students_count = cls["students_count"]
            required_features = cls.get("required_features", [])
            room_type = cls.get("room_type", "common")
            time_slot = cls["time_slot"]
            coord_id = cls["coordination_id"]
            teacher_id = cls.get("teacher_id")
            day_of_week = cls.get("day_of_week", 1)

            # Verificar Hard Constraint de indisponibilidade docente
            if self.is_teacher_restricted(teacher_id, day_of_week, time_slot):
                logger.warning(f"[HARD_CONSTRAINT_REJECT] Turma {class_id} do docente {teacher_id} recusada no slot {time_slot} (Dia {day_of_week}) por indisponibilidade cadastrada.")
                allocations[class_id] = {
                    "room_id": None,
                    "time_slot": time_slot,
                    "students_count": students_count,
                    "coordination_id": coord_id,
                    "urgency": cls.get("urgency", 3),
                    "status": "pending_arbitration",
                    "conflict_reason": f"Docente {teacher_id} indisponível no slot {time_slot}"
                }
                continue

            # Verificar Hard Constraint de máx 4 aulas seguidas por turno
            if not self.check_teacher_consecutive_limit(allocations, teacher_id, day_of_week, time_slot):
                logger.warning(f"[HARD_CONSTRAINT_REJECT] Turma {class_id} do docente {teacher_id} recusada no slot {time_slot}: Limite máximo de 4 aulas seguidas no turno atingido.")
                allocations[class_id] = {
                    "room_id": None,
                    "time_slot": time_slot,
                    "students_count": students_count,
                    "coordination_id": coord_id,
                    "urgency": cls.get("urgency", 3),
                    "status": "pending_arbitration",
                    "conflict_reason": f"Docente {teacher_id} atingiu limite de 4 aulas seguidas no turno"
                }
                continue

                
            # Filtrar salas candidatas
            candidate_rooms = []
            for room in self.rooms:
                # 1. Capacidade
                if room["capacity"] < students_count:
                    continue
                # 2. Tipo de sala
                if room["room_type"] != room_type:
                    continue
                # 3. Features requeridas (ex. laboratório de química, projetor)
                if not all(feat in room["features"] for feat in required_features):
                    continue
                # 4. Acessibilidade se aplicável
                if cls.get("require_accessibility", False) and not room["is_accessible"]:
                    continue
                
                candidate_rooms.append(room)

            if not candidate_rooms:
                logger.error(f"Erro: Nenhuma sala física atende às restrições da turma {class_id}.")
                continue
                
            # Selecionar a primeira sala disponível (ou a com capacidade mais justa para evitar desperdício)
            candidate_rooms.sort(key=lambda r: r["capacity"])
            selected_room = candidate_rooms[0]
            
            allocations[class_id] = {
                "room_id": selected_room["id"],
                "time_slot": time_slot,
                "students_count": students_count,
                "coordination_id": coord_id,
                "urgency": cls.get("urgency", 3),
                "teacher_id": teacher_id,
                "day_of_week": day_of_week
            }
            self._register_teacher_allocation(teacher_id, day_of_week, time_slot)
            logger.info(f"Turma {class_id} alocada temporariamente na sala {selected_room['name']} ({selected_room['block_id']}) no slot {time_slot}.")

        # 2. Resolução de Conflitos por Leilão Multiagente (ACC + AMR)
        logger.info("Fase 2: Identificando e arbitrando conflitos de concorrência...")
        has_conflit = True
        iterations = 0
        max_iterations = 5 # Risco de loop mitigado a no máximo 5 iterações

        while has_conflit and iterations < max_iterations:
            has_conflit = False
            iterations += 1
            logger.info(f"Rodada de mediação {iterations}...")

            # Agrupar alocações por sala e slot de tempo para achar colisões
            room_slot_usage: Dict[Tuple[str, str], List[str]] = {}
            for class_id, alloc in list(allocations.items()):
                key = (alloc["room_id"], alloc["time_slot"])
                if key not in room_slot_usage:
                    room_slot_usage[key] = []
                room_slot_usage[key].append(class_id)

            # Resolver colisões encontradas
            for (room_id, time_slot), class_ids in room_slot_usage.items():
                if len(class_ids) > 1:
                    has_conflit = True
                    logger.warning(f"Conflito na sala {room_id} no slot {time_slot} entre as turmas: {class_ids}")

                    # Obter lances dos agentes ACC das coordenações afetadas
                    competitor_bids = {}
                    for c_id in class_ids:
                        alloc = allocations[c_id]
                        acc = self.accs[str(alloc["coordination_id"])]
                        bid = acc.make_bid(c_id, room_id, alloc["urgency"])
                        competitor_bids[acc] = bid
                        logger.info(f"Agente ACC {acc.name} deu lance de {bid} créditos para a turma {c_id}.")

                    # Arbitrar pelo AMR
                    winner_acc = self.amr.resolve_dispute(room_id, time_slot, competitor_bids)
                    
                    # O vencedor mantém a sala, os perdedores são desalocados e voltam para a fila de alocação inicial
                    for c_id in class_ids:
                        alloc = allocations[c_id]
                        acc = self.accs[alloc["coordination_id"]]
                        if acc != winner_acc:
                            logger.info(f"Turma {c_id} desalocada devido a derrota no leilão.")
                            # Tenta mover para uma sala alternativa livre imediatamente
                            moved = False
                            for alt_room in self.rooms:
                                if alt_room["id"] == room_id:
                                    continue
                                if alt_room["capacity"] < alloc["students_count"]:
                                    continue
                                # Verificar se está livre nesse horário
                                slot_busy = any(
                                    other_alloc["room_id"] == alt_room["id"] and other_alloc["time_slot"] == time_slot
                                    for other_alloc in allocations.values()
                                )
                                if not slot_busy:
                                    allocations[c_id]["room_id"] = alt_room["id"]
                                    moved = True
                                    logger.info(f"Turma {c_id} reallocada alternativamente para a sala {alt_room['name']} ({alt_room['block_id']}).")
                                    break
                            
                            if not moved:
                                logger.error(f"Erro Crítico: Não há sala alternativa para realocar turma {c_id} no slot {time_slot}. Fica pendente de arbitragem física.")
                                # Marca como pendente de arbitragem manual
                                allocations[c_id]["status"] = "pending_arbitration"
                                allocations[c_id]["room_id"] = None

        # 3. Otimização de Ocupação Predial (BuildingOptimizer)
        logger.info("Fase 3: Executando otimização de consolidação predial...")
        unique_blocks = list(set(r["block_id"] for r in self.rooms))
        optimized_allocations, deactivated_blocks = BuildingOptimizer.optimize_building_occupancy(
            allocations, self.rooms, unique_blocks
        )

        logger.info("=== Processamento de alocação concluído com sucesso! ===")
        # Retornar o saldo final de créditos das coordenações atualizado nos ACCs
        for c_id, acc in self.accs.items():
            logger.info(f"ACC {acc.name} - Saldo final de créditos: {acc.credits}")

        return optimized_allocations, deactivated_blocks, self.amr.bids_history

    def calculate_emergency_reallocation(self, absent_teacher_id: str, teachers: List[Dict[str, Any]], current_allocations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calcula opções emergenciais de substituição para um docente ausente.
        1. Identifica turmas lecionadas pelo docente ausente em current_allocations.
        2. Procura professores substitutos da mesma coordenação/departamento sem restrição no slot.
        3. Se necessário, expande a busca para docentes de outras coordenações.
        4. Retorna até 3 opções de substituição ordenadas por impact_score.
        """
        affected_allocations = [a for a in current_allocations if a.get("teacher_id") == absent_teacher_id]
        if not affected_allocations:
            return {
                "absent_teacher_id": absent_teacher_id,
                "total_affected_classes": 0,
                "options": []
            }
        
        # Encontrar departamento/coordenação do docente ausente
        absent_teacher = next((t for t in teachers if t.get("id") == absent_teacher_id), None)
        absent_dept = absent_teacher.get("department", "Geral") if absent_teacher else "Geral"
        
        same_dept_teachers = [t for t in teachers if t.get("id") != absent_teacher_id and t.get("department") == absent_dept]
        other_dept_teachers = [t for t in teachers if t.get("id") != absent_teacher_id and t.get("department") != absent_dept]
        
        options = []
        
        # Opção 1: Mesma coordenação (Prioritária)
        substitutions_opt1 = []
        expanded_opt1 = False
        
        for idx, alloc in enumerate(affected_allocations):
            day = alloc.get("day_of_week", 1)
            shift = alloc.get("shift", "M")
            sub_slot = alloc.get("sub_slot", 1)
            time_slot = f"{shift}{sub_slot}"
            class_id = alloc.get("id", f"class-{idx}")
            room_id = alloc.get("room_id")
            
            # Procurar substituto no mesmo departamento sem restrição
            candidate = None
            for t in same_dept_teachers:
                if not self.is_teacher_restricted(t["id"], day, time_slot):
                    candidate = t
                    break
            
            if not candidate:
                # Expansão para outras coordenações se não achou no mesmo dept
                for t in other_dept_teachers:
                    if not self.is_teacher_restricted(t["id"], day, time_slot):
                        candidate = t
                        expanded_opt1 = True
                        break
            
            if candidate:
                substitutions_opt1.append({
                    "class_id": class_id,
                    "class_name": alloc.get("subject") or class_id,
                    "day_of_week": day,
                    "shift": shift,
                    "sub_slot": sub_slot,
                    "substitute_teacher_id": candidate["id"],
                    "substitute_teacher_name": candidate["name"],
                    "time_slot": time_slot,
                    "room_id": room_id
                })
        
        if substitutions_opt1:
            options.append({
                "option_index": 1,
                "impact_score": 1.0 if not expanded_opt1 else 2.5,
                "description": f"Substituição emergencial prioritária ({'Mesma Coordenação' if not expanded_opt1 else 'Busca Expandida'})",
                "expanded_coordinations": expanded_opt1,
                "substitutions": substitutions_opt1
            })
            
        # Opção 2: Rotação alternada de docentes (se houver candidatos adicionais)
        if len(same_dept_teachers) > 1:
            substitutions_opt2 = []
            expanded_opt2 = False
            for idx, alloc in enumerate(affected_allocations):
                day = alloc.get("day_of_week", 1)
                shift = alloc.get("shift", "M")
                sub_slot = alloc.get("sub_slot", 1)
                time_slot = f"{shift}{sub_slot}"
                class_id = alloc.get("id", f"class-{idx}")
                room_id = alloc.get("room_id")
                
                # Pegar o candidato rotacionado
                candidates = [t for t in same_dept_teachers if not self.is_teacher_restricted(t["id"], day, time_slot)]
                candidate = candidates[1] if len(candidates) > 1 else (candidates[0] if candidates else None)
                
                if not candidate and other_dept_teachers:
                    candidate = other_dept_teachers[0]
                    expanded_opt2 = True
                
                if candidate:
                    substitutions_opt2.append({
                        "class_id": class_id,
                        "class_name": alloc.get("subject") or class_id,
                        "day_of_week": day,
                        "shift": shift,
                        "sub_slot": sub_slot,
                        "substitute_teacher_id": candidate["id"],
                        "substitute_teacher_name": candidate["name"],
                        "time_slot": time_slot,
                        "room_id": room_id
                    })
            
            if substitutions_opt2 and substitutions_opt2 != substitutions_opt1:
                options.append({
                    "option_index": 2,
                    "impact_score": 2.0,
                    "description": "Substituição com distribuição equilibrada entre docentes",
                    "expanded_coordinations": expanded_opt2,
                    "substitutions": substitutions_opt2
                })
                
        return {
            "absent_teacher_id": absent_teacher_id,
            "total_affected_classes": len(affected_allocations),
            "options": options
        }

