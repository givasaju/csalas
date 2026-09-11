import uuid
import time
import logging
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Any, List, Optional
from src.engine.core import CoreAllocationEngine
from src import models
from src.database import SessionLocal, get_db, get_tenant_session

logger = logging.getLogger("core-allocation-engine")

# Banco de dados simulado em memória
db_tasks: Dict[str, Dict[str, Any]] = {}
db_teachers: List[Dict[str, Any]] = [
    {"id": "prof-claudio", "name": "Cláudio", "department": "Engenharia", "email": "claudio@school.edu", "subjects": ["Cálculo I", "Álgebra Linear"]},
    {"id": "prof-isabela", "name": "Isabela", "department": "Ciências", "email": "isabela@school.edu", "subjects": ["Física I", "Física II"]}
]
db_restrictions: List[Dict[str, Any]] = []
db_coordinations: List[Dict[str, Any]] = [
    {"id": "eng", "name": "Engenharia", "credits": 1000},
    {"id": "let", "name": "Letras", "credits": 1000},
]

db_rooms: List[Dict[str, Any]] = []
db_emergency_logs: List[Dict[str, Any]] = []
db_emergency_details: List[Dict[str, Any]] = []

# Pool de threads para processamento em background
executor = ThreadPoolExecutor(max_workers=2)

def save_emergency_reallocation_log(absent_teacher_id: str, start_date: str, end_date: str, mode: str, selected_option_index: int, substitutions: list) -> str:
    log_id = str(uuid.uuid4())
    log_entry = {
        "id": log_id,
        "absent_teacher_id": absent_teacher_id,
        "start_date": start_date,
        "end_date": end_date,
        "mode": mode,
        "selected_option_index": selected_option_index,
        "affected_classes_count": len(substitutions),
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "created_by": "coordinative_user"
    }
    db_emergency_logs.append(log_entry)
    
    for sub in substitutions:
        detail_entry = {
            "id": str(uuid.uuid4()),
            "log_id": log_id,
            "class_id": sub.get("class_id") if isinstance(sub, dict) else sub.class_id,
            "substitute_teacher_id": sub.get("substitute_teacher_id") if isinstance(sub, dict) else sub.substitute_teacher_id,
            "time_slot": sub.get("time_slot") if isinstance(sub, dict) else sub.time_slot,
            "room_id": sub.get("room_id") if isinstance(sub, dict) else sub.room_id
        }
        db_emergency_details.append(detail_entry)
        
    logger.info(f"[EMERGENCY_REALLOCATION] Log {log_id} registrado em modo '{mode}' para docente {absent_teacher_id}")
    return log_id


def execute_allocation_task(task_id: str, tenant_slug: Optional[str] = None):
    """
    Worker que roda a alocação de IA em background e atualiza o progresso no banco isolado da instituição.
    """
    try:
        db_tasks[task_id]["status"] = "running"
        db_tasks[task_id]["progress"] = 10
        time.sleep(1) # Simula leitura do banco

        db_tasks[task_id]["progress"] = 30
        
        if tenant_slug:
            db = get_tenant_session(tenant_slug)
            if db is None:
                raise RuntimeError(f"Base de dados da instituição '{tenant_slug}' não encontrada para execução da alocação.")
        else:
            db = SessionLocal()

        try:
            rooms = db.query(models.Room).all()
            coordinations = db.query(models.Coordination).all()
            classes = db.query(models.Class).all()
            restrictions_objs = db.query(models.Restriction).all()
            
            rooms_list = [{"id": r.id, "block_id": r.block_id, "name": r.name, "capacity": r.capacity, "room_type": r.room_type, "is_accessible": r.is_accessible, "features": r.features or []} for r in rooms]
            coordinations_list = [{"id": str(c.id), "name": c.name, "credits": c.credits} for c in coordinations]
            classes_list = [{"id": c.id, "students_count": c.students_count, "room_type": c.room_type, "time_slot": c.time_slot, "coordination_id": str(c.coordination_id), "urgency": c.urgency, "require_accessibility": c.require_accessibility} for c in classes]
            restrictions_list = [{"id": r.id, "teacher_id": r.teacher_id, "day_of_week": int(r.day_of_week), "time_slot_id": r.time_slot_id} for r in restrictions_objs]

            engine = CoreAllocationEngine(rooms_list, coordinations_list, classes_list, restrictions=restrictions_list)
            
            db_tasks[task_id]["progress"] = 60
            allocations, deactivated_blocks, bids = engine.run_allocation()
            db_tasks[task_id]["bids"] = bids
            
            # Atualizar créditos das coordenações no banco de dados
            for c in coordinations:
                c.credits = engine.accs[str(c.id)].credits
            
            # Persistir logs do leilão
            for bid in bids:
                w_id = int(bid["winner_id"]) if str(bid["winner_id"]).isdigit() else None
                l_id = int(bid["loser_id"]) if str(bid["loser_id"]).isdigit() else None
                new_bid = models.AuctionBid(
                    id=str(uuid.uuid4()),
                    task_id=task_id,
                    room_id=bid["room_id"],
                    time_slot=bid["time_slot"],
                    winner_coordination_id=w_id,
                    loser_coordination_id=l_id,
                    credits_spent=bid["credits_spent"]
                )
                db.add(new_bid)
            
            db.commit()
        finally:
            db.close()

        db_tasks[task_id]["progress"] = 100
        
        # Verificar se há pendências de arbitragem manual
        has_pending = any(a.get("status") == "pending_arbitration" for a in allocations.values())
        
        db_tasks[task_id]["status"] = "pending_arbitration" if has_pending else "completed"
        db_tasks[task_id]["result_summary"] = {
            "allocated_classes": len(allocations),
            "conflits_resolved_by_auction": len(bids),
            "pending_arbitration_rooms": sum(1 for a in allocations.values() if a.get("status") == "pending_arbitration"),
            "deactivated_blocks": deactivated_blocks,
            "estimated_energy_saving_percentage": 25.0 if "Bloco C" in deactivated_blocks else 0.0
        }
        logger.info(f"Tarefa {task_id} finalizada com sucesso. Status final: {db_tasks[task_id]['status']}")

    except Exception as e:
        logger.exception(f"Erro ao processar tarefa {task_id}")
        db_tasks[task_id]["status"] = "failed"
        db_tasks[task_id]["error_log"] = str(e)


def enqueue_allocation_run(tenant_slug: Optional[str] = None) -> str:
    """
    Adiciona uma nova rodada de alocação na fila do worker associada ao tenant especificado.
    """
    task_id = str(uuid.uuid4())
    db_tasks[task_id] = {
        "id": task_id,
        "tenant_slug": tenant_slug,
        "status": "queued",
        "progress": 0,
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "error_log": None,
        "result_summary": None
    }
    # Enviar para execução assíncrona com contexto isolado do tenant
    executor.submit(execute_allocation_task, task_id, tenant_slug)
    return task_id
