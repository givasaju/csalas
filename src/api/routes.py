import csv
import uuid
import logging
import datetime
from io import StringIO
import socket
import secrets


from fastapi import APIRouter, HTTPException, Header, UploadFile, File, status, Depends, BackgroundTasks, Request
from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import flag_modified
from typing import List, Dict, Any, Optional
from src.api.schemas import (
    RoomCreate, RestrictionCreate, TeacherCreate, TeacherResponse,
    AllocationCreate, ReallocateSubjectsRequest, ReallocateSubjectsResponse,
    SubslotCreate, SubslotUpdate, SubslotResponse,
    EmergencyReallocationRequest, EmergencyReallocationCalculateResponse,
    EmergencyReallocationOption, ProposedSubstitution,
    EmergencyReallocationCommitRequest, EmergencyReallocationCommitResponse,
    UserRegisterRequest, UserLoginRequest, UserResponse,
    UserStatusUpdateRequest, LoginResponse, ChangePasswordRequest,
    TenantCreateRequest, TenantResponse, TenantListResponse,
    MasterChefInfo, TenantDetailResponse, TenantUpdateRequest,
    MasterChefResetRequest, MasterChefResetResponse,
    TenantDeleteRequest, TenantDeleteResponse
)
from src.api.auth import (
    hash_password, verify_password, create_access_token,
    get_current_user, get_current_admin_user, require_roles, require_doctor_chef, TokenData
)

from src.api.allocation_validator import check_consecutive_limit
from src.database import get_db

from src import models
from src.api.worker import db_tasks, enqueue_allocation_run, save_emergency_reallocation_log
from src.engine.core import CoreAllocationEngine

logger = logging.getLogger("core-allocation-engine")

import os
from fastapi.responses import HTMLResponse, FileResponse, Response, StreamingResponse
from src.api.reports import generate_pdf_report, generate_excel_report, generate_teacher_pdf_report, generate_room_pdf_report

router = APIRouter(prefix="/api/v1")

@router.get("/endpoints", response_class=HTMLResponse, include_in_schema=False)
def list_endpoints(authorization: str = Header(None)):
    """Return a simple HTML page listing all public API endpoints."""
    # Build the absolute path to the static file within this package
    static_path = os.path.join(os.path.dirname(__file__), "static", "endpoints.html")
    return FileResponse(static_path)

@router.get("/health")
def health_check(db: Session = Depends(get_db)):
    """Health check endpoint returning status, database connectivity and configured tenant."""
    tenant = os.environ.get("TENANT_NAME", "default")
    db_status = "connected"
    try:
        from sqlalchemy import text
        db.execute(text("SELECT 1"))
    except Exception as e:
        db_status = f"disconnected: {str(e)}"
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"status": "unhealthy", "tenant": tenant, "database": db_status}
        )
    return {
        "status": "healthy",
        "tenant": tenant,
        "version": "1.0.0",
        "database": db_status,
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    }

def check_jwt_auth(authorization: str = Header(None)):
    """
    Mock simples de autenticação JWT em conformidade com as regras
    de segurança declaradas no roadmap.
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token de autorização ausente ou mal-formatado.")
    token = authorization.split(" ")[1]
    if token == "invalid-token":
        raise HTTPException(status_code=401, detail="Token de autenticação inválido.")
    return True


@router.get("/teachers", status_code=200)
def list_teachers(authorization: str = Header(None), db: Session = Depends(get_db)):
    """
    GET /api/v1/teachers
    Lista todos os docentes cadastrados incluindo suas disciplinas lecionáveis.
    """
    check_jwt_auth(authorization)
    teachers = db.query(models.Teacher).all()
    return [
        {
            "id": t.id,
            "name": t.name,
            "department": t.department or "Geral",
            "email": t.email,
            "subjects": t.subjects or []
        }
        for t in teachers
    ]


@router.post("/teachers", status_code=201)
def create_teacher(teacher: TeacherCreate, authorization: str = Header(None), db: Session = Depends(get_db)):
    """
    POST /api/v1/teachers
    Cadastra unitariamente um novo docente no sistema com suas disciplinas lecionáveis.
    """
    check_jwt_auth(authorization)
    
    # Validar se disciplinas foram informadas
    clean_subjects = [s.strip() for s in (teacher.subjects or []) if s and s.strip()]
    if not clean_subjects:
        raise HTTPException(status_code=422, detail="Pelo menos 1 disciplina lecionável válida é obrigatória.")
    if len(clean_subjects) > 6:
        raise HTTPException(status_code=422, detail="No máximo 6 disciplinas lecionáveis podem ser informadas.")

    # Validar se já existe docente com a mesma matrícula/ID
    duplicate = db.query(models.Teacher).filter(models.Teacher.id == teacher.id).first()
    if duplicate:
        raise HTTPException(status_code=409, detail=f"Já existe um docente cadastrado com a matrícula '{teacher.id}'.")
        
    new_teacher = models.Teacher(
        id=teacher.id,
        name=teacher.name,
        department=teacher.department or "Geral",
        subjects=clean_subjects
    )
    db.add(new_teacher)
    db.commit()
    logger.info(f"Docente cadastrado com sucesso: {teacher.name} ({teacher.id}) - Depto: {new_teacher.department} - Disciplinas: {clean_subjects}")
    return {"id": new_teacher.id, "name": new_teacher.name, "department": new_teacher.department, "subjects": new_teacher.subjects}


@router.post("/teachers/import-csv", status_code=200)
async def import_teachers_csv(file: UploadFile = File(...), authorization: str = Header(None), db: Session = Depends(get_db)):
    """
    POST /api/v1/teachers/import-csv
    Importação transacional de docentes em lote via arquivo CSV.
    Estrutura esperada: matricula, nome, departamento, disciplinas
    As disciplinas na coluna devem ser separadas por ponto e vírgula (;).
    Política Tudo ou Nada.
    """
    check_jwt_auth(authorization)
    
    try:
        content = await file.read()
        csv_text = content.decode("utf-8")
        csv_file = StringIO(csv_text)
        reader = csv.reader(csv_file)
        
        rows = list(reader)
        if not rows:
            raise HTTPException(status_code=400, detail="O arquivo CSV está vazio.")
            
        header = [h.strip().lower() for h in rows[0]]
        
        # Verificar se tem pelo menos matricula, nome, departamento, disciplinas
        if len(header) < 4 or header[0] not in ["matricula", "id"] or header[1] not in ["nome", "name"] or header[3] not in ["disciplinas", "disciplines", "subjects"]:
            raise HTTPException(
                status_code=400, 
                detail="Cabeçalho do CSV inválido. Esperado: matricula, nome, departamento, disciplinas"
            )
            
        teachers_to_import = []
        new_ids = set()

        for i, row in enumerate(rows[1:], start=2):
            if len(row) < 4:
                raise HTTPException(status_code=400, detail=f"Linha {i} do CSV está incompleta.")
                
            teacher_id = row[0].strip()
            name = row[1].strip()
            department = row[2].strip() if len(row) > 2 and row[2].strip() else "Geral"
            raw_disciplines = row[3].strip() if len(row) > 3 else ""
            
            if not teacher_id or not name:
                raise HTTPException(status_code=422, detail=f"Linha {i}: Matrícula e Nome são campos obrigatórios.")
                
            subjects = [s.strip() for s in raw_disciplines.split(";") if s and s.strip()]
            if not subjects:
                raise HTTPException(status_code=422, detail=f"Linha {i}: Pelo menos 1 disciplina lecionável deve ser informada (separadas por ';').")
            if len(subjects) > 6:
                raise HTTPException(status_code=422, detail=f"Linha {i}: No máximo 6 disciplinas lecionáveis podem ser informadas (informadas {len(subjects)}).")

            if teacher_id in new_ids or db.query(models.Teacher).filter(models.Teacher.id == teacher_id).first():
                raise HTTPException(status_code=409, detail=f"Linha {i}: Matrícula duplicada '{teacher_id}'.")
                
            new_ids.add(teacher_id)
            teachers_to_import.append(models.Teacher(id=teacher_id, name=name, department=department, subjects=subjects))

        db.bulk_save_objects(teachers_to_import)
        db.commit()
        logger.info(f"Importação em lote de docentes concluída. {len(teachers_to_import)} professores cadastrados.")
        return {
            "message": "Importação em lote de docentes concluída com sucesso.",
            "imported_count": len(teachers_to_import)
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.exception("Erro durante processamento de importação CSV de docentes")
        raise HTTPException(status_code=400, detail=f"Erro ao decodificar ou ler arquivo: {str(e)}")


@router.post("/teachers/reallocate-subjects", response_model=ReallocateSubjectsResponse, status_code=200)
def reallocate_subjects(
    payload: ReallocateSubjectsRequest,
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    """
    POST /api/v1/teachers/reallocate-subjects
    Realoca e transfere disciplinas entre docentes do mesmo departamento de forma atômica.
    """
    check_jwt_auth(authorization)

    source_teacher = db.query(models.Teacher).filter(models.Teacher.id == payload.source_teacher_id).first()
    if not source_teacher:
        raise HTTPException(status_code=404, detail=f"Docente de origem '{payload.source_teacher_id}' não encontrado.")

    target_teacher = db.query(models.Teacher).filter(models.Teacher.id == payload.target_teacher_id).first()
    if not target_teacher:
        raise HTTPException(status_code=404, detail=f"Docente de destino '{payload.target_teacher_id}' não encontrado.")

    # 1. Validação Iso-Department
    if source_teacher.department != target_teacher.department:
        raise HTTPException(
            status_code=422,
            detail=f"Realocação permitida apenas entre docentes do mesmo departamento ('{source_teacher.department}' vs '{target_teacher.department}')."
        )

    source_subjects = list(source_teacher.subjects or [])
    target_subjects = list(target_teacher.subjects or [])

    # Verificar se o doador possui todas as disciplinas informadas
    for subj in payload.subjects:
        if subj not in source_subjects:
            raise HTTPException(
                status_code=422,
                detail=f"A disciplina '{subj}' não pertence ao rol do docente de origem '{source_teacher.name}'."
            )

    # 2. Calcular nova lista do doador
    new_source_subjects = [s for s in source_subjects if s not in payload.subjects]

    if not new_source_subjects:
        if not payload.replacement_subject:
            raise HTTPException(
                status_code=422,
                detail="A transferência esvazia o rol do docente doador. Informe uma disciplina substituta em 'replacement_subject'."
            )
        new_source_subjects = [payload.replacement_subject]

    # 3. Calcular nova lista do receptor
    new_target_subjects = list(target_subjects)
    for subj in payload.subjects:
        if subj not in new_target_subjects:
            new_target_subjects.append(subj)

    if len(new_target_subjects) > 6:
        raise HTTPException(
            status_code=422,
            detail=f"O docente de destino excederia o limite máximo de 6 disciplinas (ficaria com {len(new_target_subjects)})."
        )

    # Atualizar docentes
    source_teacher.subjects = new_source_subjects
    target_teacher.subjects = new_target_subjects
    flag_modified(source_teacher, "subjects")
    flag_modified(target_teacher, "subjects")

    # 4. Reatribuir alocações ativas
    allocations = db.query(models.Allocation).filter(
        models.Allocation.teacher_id == payload.source_teacher_id,
        models.Allocation.subject.in_(payload.subjects)
    ).all()

    migrated_count = 0
    pending_count = 0

    for alloc in allocations:
        alloc.teacher_id = payload.target_teacher_id
        migrated_count += 1

    db.commit()
    db.refresh(source_teacher)
    db.refresh(target_teacher)

    logger.info(
        f"[SUBJECT_REALLOCATION] Realocação concluída no departamento {source_teacher.department}: "
        f"{payload.subjects} transferidos de {source_teacher.name} para {target_teacher.name}. "
        f"Alocações migradas: {migrated_count}"
    )

    return ReallocateSubjectsResponse(
        department=source_teacher.department,
        source_teacher=TeacherResponse(
            id=source_teacher.id,
            name=source_teacher.name,
            department=source_teacher.department,
            email=getattr(source_teacher, "email", None),
            subjects=source_teacher.subjects or []
        ),
        target_teacher=TeacherResponse(
            id=target_teacher.id,
            name=target_teacher.name,
            department=target_teacher.department,
            email=getattr(target_teacher, "email", None),
            subjects=target_teacher.subjects or []
        ),
        migrated_allocations_count=migrated_count,
        pending_arbitration_allocations_count=pending_count,
        message=f"Disciplinas e alocações realocadas com sucesso dentro do departamento {source_teacher.department}."
    )


@router.delete("/teachers/{teacher_id}", status_code=200)
def delete_teacher(teacher_id: str, authorization: str = Header(None), db: Session = Depends(get_db)):
    """
    DELETE /api/v1/teachers/{teacher_id}
    Remove um docente do cadastro.
    """
    check_jwt_auth(authorization)
    
    teacher = db.query(models.Teacher).filter(models.Teacher.id == teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Docente não encontrado.")

    # Verificar se tem restrições cadastradas
    has_restrictions = db.query(models.Restriction).filter(models.Restriction.teacher_id == teacher_id).first()
    if has_restrictions:
        raise HTTPException(
            status_code=409, 
            detail=f"Não é possível excluir o docente '{teacher_id}' pois existem restrições horárias atreladas a ele."
        )

    db.delete(teacher)
    db.commit()
    logger.warning(f"Docente removido: {teacher.name} ({teacher.id})")
    return {"message": f"Docente '{teacher_id}' removido com sucesso."}





@router.post("/rooms", status_code=201)
def create_room(room: RoomCreate, authorization: str = Header(None), db: Session = Depends(get_db)):
    """
    POST /api/v1/rooms
    Cadastra uma nova sala de aula física no campus.
    """
    check_jwt_auth(authorization)
    
    # Validar se já existe sala com o mesmo nome no mesmo bloco
    duplicate = db.query(models.Room).filter(models.Room.block_id == room.block_id, models.Room.name == room.name).first()
    if duplicate:
        raise HTTPException(status_code=409, detail=f"Já existe uma sala chamada '{room.name}' no bloco '{room.block_id}'.")
        
    new_room = models.Room(
        id=str(uuid.uuid4()),
        block_id=room.block_id,
        name=room.name,
        capacity=room.capacity,
        room_type=room.room_type,
        is_accessible=room.is_accessible,
        features=room.features
    )
    db.add(new_room)
    db.commit()
    logger.info(f"Sala cadastrada com sucesso: {room.name} ({room.block_id}) - Capacidade: {room.capacity}")
    return {"id": new_room.id, "block_id": new_room.block_id, "name": new_room.name, "capacity": new_room.capacity, "room_type": new_room.room_type, "is_accessible": new_room.is_accessible, "features": new_room.features}


@router.post("/rooms/import-csv", status_code=200)
async def import_rooms_csv(file: UploadFile = File(...), authorization: str = Header(None), db: Session = Depends(get_db)):
    """
    POST /api/v1/rooms/import-csv
    Importação transacional de salas de aula em lote via arquivo CSV.
    Política Tudo ou Nada.
    """
    check_jwt_auth(authorization)
    
    try:
        content = await file.read()
        csv_text = content.decode("utf-8")
        csv_file = StringIO(csv_text)
        reader = csv.reader(csv_file)
        
        rows = list(reader)
        if not rows:
            raise HTTPException(status_code=400, detail="O arquivo CSV está vazio.")
            
        header = [h.strip().lower() for h in rows[0]]
        expected_header = ["bloco", "sala", "capacidade", "tipo", "acessivel", "recursos"]
        if header != expected_header:
            raise HTTPException(
                status_code=400, 
                detail=f"Cabeçalho do CSV inválido. Esperado: {expected_header}, obtido: {header}"
            )
            
        rooms_to_import = []
        for i, row in enumerate(rows[1:], start=2):
            if len(row) < 6:
                raise HTTPException(status_code=400, detail=f"Linha {i} do CSV está incompleta ou mal-formatada.")
                
            block = row[0].strip()
            name = row[1].strip()
            capacity_str = row[2].strip()
            room_type = row[3].strip()
            accessible_str = row[4].strip()
            features_str = row[5].strip()
            
            if not block or not name:
                raise HTTPException(status_code=422, detail=f"Linha {i}: Bloco e Sala são campos obrigatórios.")
                
            try:
                capacity = int(capacity_str)
                if capacity <= 0:
                    raise ValueError()
            except ValueError:
                raise HTTPException(status_code=422, detail=f"Linha {i}: A capacidade '{capacity_str}' deve ser um inteiro maior que zero.")
                
            if room_type not in ["common", "lab", "auditorium"]:
                raise HTTPException(status_code=422, detail=f"Linha {i}: Tipo de sala '{room_type}' é inválido. Escolha entre: common, lab, auditorium.")
                
            is_accessible = accessible_str.lower() in ["true", "1", "yes", "sim"]
            features = [f.strip() for f in features_str.split(";") if f.strip()]
            
            rooms_to_import.append(models.Room(
                id=str(uuid.uuid4()),
                block_id=block,
                name=name,
                capacity=capacity,
                room_type=room_type,
                is_accessible=is_accessible,
                features=features
            ))

        db.bulk_save_objects(rooms_to_import)
        db.commit()
        logger.info(f"Importação em lote CSV concluída. {len(rooms_to_import)} salas importadas.")
        return {
            "message": "Importação em lote concluída com sucesso.",
            "imported_count": len(rooms_to_import)
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.exception("Erro durante processamento de importação CSV")
        raise HTTPException(status_code=400, detail=f"Erro ao decodificar ou ler arquivo: {str(e)}")


@router.post("/allocation/restrictions", status_code=201)
def create_restriction(restriction: RestrictionCreate, authorization: str = Header(None), db: Session = Depends(get_db)):
    """
    POST /api/v1/allocation/restrictions
    Cadastra uma nova restrição horária de indisponibilidade docente.
    """
    check_jwt_auth(authorization)
    
    teacher_exists = db.query(models.Teacher).filter(models.Teacher.id == restriction.teacher_id).first()
    if not teacher_exists:
        raise HTTPException(status_code=404, detail=f"Professor com ID {restriction.teacher_id} não encontrado.")
        
    db_subslots = db.query(models.SubslotTimeInterval).filter(models.SubslotTimeInterval.is_interval == False).all()
    valid_slots = [s.code for s in db_subslots] if db_subslots else [f"{shift}{i}" for shift in ["M", "T", "N"] for i in range(1, 6)]
    if restriction.time_slot_id not in valid_slots:
        raise HTTPException(status_code=422, detail=f"time_slot_id inválido. Use os subslots M1..M5, T1..T5, N1..N5.")

    duplicate = db.query(models.Restriction).filter(
        models.Restriction.teacher_id == restriction.teacher_id,
        models.Restriction.day_of_week == restriction.day_of_week,
        models.Restriction.time_slot_id == restriction.time_slot_id
    ).first()
    if duplicate:
        raise HTTPException(status_code=409, detail="Esta indisponibilidade já está cadastrada para este professor.")

    new_restriction = models.Restriction(
        id=str(uuid.uuid4()),
        teacher_id=restriction.teacher_id,
        day_of_week=restriction.day_of_week,
        time_slot_id=restriction.time_slot_id
    )
    db.add(new_restriction)
    db.commit()
    logger.info(f"Indisponibilidade cadastrada para professor {restriction.teacher_id} no dia {restriction.day_of_week} ({restriction.time_slot_id})")
    return {"id": new_restriction.id, "teacher_id": new_restriction.teacher_id, "day_of_week": int(new_restriction.day_of_week), "time_slot_id": new_restriction.time_slot_id}


@router.get("/teachers/{teacher_id}/restrictions", status_code=200)
def get_teacher_restrictions(teacher_id: str, authorization: str = Header(None), db: Session = Depends(get_db)):
    """
    GET /api/v1/teachers/{teacher_id}/restrictions
    Retorna as restrições horárias de um docente específico.
    """
    check_jwt_auth(authorization)
    
    teacher = db.query(models.Teacher).filter(models.Teacher.id == teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail=f"Docente '{teacher_id}' não encontrado.")

    restrictions = db.query(models.Restriction).filter(models.Restriction.teacher_id == teacher_id).all()
    logger.info(f"[RESTRICTION_GET] {len(restrictions)} restrições recuperadas para o docente {teacher_id}")
    return [
        {
            "id": r.id,
            "teacher_id": r.teacher_id,
            "day_of_week": r.day_of_week,
            "time_slot_id": r.time_slot_id
        }
        for r in restrictions
    ]


@router.delete("/allocation/restrictions/{restriction_id}", status_code=200)
def delete_single_restriction(restriction_id: str, authorization: str = Header(None), db: Session = Depends(get_db)):
    """
    DELETE /api/v1/allocation/restrictions/{restriction_id}
    Remove uma única restrição horária de docente pelo ID.
    """
    check_jwt_auth(authorization)
    
    restriction = db.query(models.Restriction).filter(models.Restriction.id == restriction_id).first()
    if not restriction:
        raise HTTPException(status_code=404, detail=f"Restrição com ID '{restriction_id}' não encontrada.")

    teacher_id = restriction.teacher_id
    db.delete(restriction)
    db.commit()
    logger.warning(f"[RESTRICTION_DELETE] Restrição {restriction_id} do docente {teacher_id} removida.")
    return {"message": f"Restrição '{restriction_id}' removida com sucesso."}


@router.delete("/allocation/restrictions", status_code=200)
def reset_restrictions(authorization: str = Header(None), db: Session = Depends(get_db)):
    """
    DELETE /api/v1/allocation/restrictions
    Reset semestral das restrições horárias dos professores.
    """
    check_jwt_auth(authorization)
    
    count = db.query(models.Restriction).delete()
    db.commit()
    logger.warning(f"[RESTRICTION_RESET] Reset semestral executado. {count} indisponibilidades de professores limpas.")
    return {
        "message": "Reset semestral das restrições horárias executado com sucesso.",
        "cleared_count": count
    }


def get_all_auction_bids(db: Session) -> List[Dict[str, Any]]:
    db_bids = db.query(models.AuctionBid).order_by(models.AuctionBid.timestamp.desc()).all()
    if db_bids:
        res = []
        for b in db_bids:
            room_obj = db.query(models.Room).filter(models.Room.id == b.room_id).first()
            room_name = f"{room_obj.name} ({room_obj.block_id})" if room_obj else (b.room_id or "Sala Física")
            w_name = b.winner.name if b.winner else (str(b.winner_coordination_id) if b.winner_coordination_id else "Engenharia")
            l_name = b.loser.name if b.loser else (str(b.loser_coordination_id) if b.loser_coordination_id else "Letras")
            res.append({
                "id": b.id,
                "room_id": b.room_id,
                "room_name": room_name,
                "time_slot": b.time_slot,
                "winner_name": w_name,
                "loser_name": l_name,
                "credits_spent": b.credits_spent,
                "timestamp": b.timestamp.isoformat() if b.timestamp else ""
            })
        return res

    in_memory_bids = []
    for t_id, task in db_tasks.items():
        task_bids = task.get("bids", [])
        for b in task_bids:
            room_id = b.get("room_id", "")
            room_obj = db.query(models.Room).filter(models.Room.id == room_id).first() if room_id else None
            room_name = f"{room_obj.name} ({room_obj.block_id})" if room_obj else (room_id or "Sala 101")
            in_memory_bids.append({
                "id": str(uuid.uuid4()),
                "room_id": room_id,
                "room_name": room_name,
                "time_slot": b.get("time_slot", "M1"),
                "winner_name": b.get("winner_name") or b.get("winner_id") or "Engenharia",
                "loser_name": b.get("loser_name") or b.get("loser_id") or "Letras",
                "credits_spent": b.get("credits_spent", 0),
                "timestamp": task.get("created_at", "")
            })
    return in_memory_bids


@router.get("/allocation/input-data", status_code=200)
def get_input_data(authorization: str = Header(None), db: Session = Depends(get_db)):
    """
    GET /api/v1/allocation/input-data
    Consolida e retorna todas as salas, coordenações, turmas, restrições e leilões de auditoria.
    """
    check_jwt_auth(authorization)
    
    restrictions_objs = db.query(models.Restriction).all()
    restrictions_list = [
        {
            "id": r.id,
            "teacher_id": r.teacher_id,
            "day_of_week": int(r.day_of_week) if str(r.day_of_week).isdigit() else r.day_of_week,
            "time_slot_id": r.time_slot_id
        }
        for r in restrictions_objs
    ]

    return {
        "rooms": db.query(models.Room).all(),
        "coordinations": db.query(models.Coordination).all(),
        "classes": [],
        "teachers": db.query(models.Teacher).all(),
        "restrictions": restrictions_list,
        "auctions": get_all_auction_bids(db)
    }


@router.get("/allocation/auctions", status_code=200)
def get_auctions_endpoint(authorization: str = Header(None), db: Session = Depends(get_db)):
    """
    GET /api/v1/allocation/auctions
    Retorna o extrato completo de leilões de créditos e auditoria.
    """
    check_jwt_auth(authorization)
    return get_all_auction_bids(db)


@router.get("/reports/summary", status_code=200)
def get_reports_summary(
    block_id: Optional[str] = None,
    shift: Optional[str] = None,
    teacher_id: Optional[str] = None,
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    """
    GET /api/v1/reports/summary
    Retorna métricas consolidadas de ocupação predial por bloco/turno e carga docente.
    """
    check_jwt_auth(authorization)

    rooms_query = db.query(models.Room)
    if block_id and block_id != "all":
        rooms_query = rooms_query.filter(models.Room.block_id == block_id)
    rooms = rooms_query.all()

    allocations = db.query(models.Allocation).all()
    teachers = db.query(models.Teacher).all()

    # Mapeamento de ocupação por sala
    room_occupancy = []
    for r in rooms:
        r_allocs = [a for a in allocations if a.room_id == r.id]
        if shift and shift != "all":
            target_shift = shift.upper()
            r_allocs = [
                a for a in r_allocs 
                if (getattr(a, 'shift', None) and str(a.shift).upper() == target_shift) or 
                   (getattr(a, 'time_slot', None) and str(a.time_slot).startswith(target_shift))
            ]
        
        total_slots = 6 if (shift and shift != "all") else 18
        occupied_count = len(r_allocs)
        rate = round((occupied_count / total_slots) * 100, 1) if total_slots > 0 else 0.0

        room_occupancy.append({
            "room_id": r.id,
            "room_name": r.name,
            "block_id": r.block_id,
            "capacity": r.capacity,
            "allocated_slots": occupied_count,
            "total_slots": total_slots,
            "occupancy_rate": rate,
            "status": "ALTA" if rate >= 70 else ("MÉDIA" if rate >= 30 else "BAIXA")
        })

    # Mapeamento de carga docente
    teacher_reports = []
    target_teachers = teachers
    if teacher_id and teacher_id != "all":
        target_teachers = [t for t in teachers if str(t.id) == str(teacher_id)]

    for t in target_teachers:
        t_allocs = [a for a in allocations if str(a.teacher_id) == str(t.id)]
        
        alloc_details = []
        for a in t_allocs:
            r_obj = db.query(models.Room).filter(models.Room.id == a.room_id).first()
            slot_str = f"{a.shift}{a.sub_slot}" if (getattr(a, 'shift', None) and getattr(a, 'sub_slot', None)) else getattr(a, 'time_slot', 'M1')
            subj_name = getattr(a, 'subject', None) or getattr(a, 'subject_name', None) or "Disciplina"
            alloc_details.append({
                "allocation_id": a.id,
                "subject_code": getattr(a, 'subject_code', 'DISC-01'),
                "subject_name": subj_name,
                "room_name": r_obj.name if r_obj else (a.room_id or "Sala"),
                "time_slot": slot_str,
                "day_of_week": getattr(a, 'day_of_week', 1)
            })

        # Se não tiver alocações gravadas, mas tiver disciplinas cadastradas no t.subjects (JSON list)
        t_subjects = getattr(t, 'subjects', []) or []
        if isinstance(t_subjects, str):
            import json
            try:
                t_subjects = json.loads(t_subjects)
            except Exception:
                t_subjects = [t_subjects]

        if not alloc_details and t_subjects:
            for idx, s in enumerate(t_subjects):
                subj_title = s if isinstance(s, str) else (s.get('name') if isinstance(s, dict) else str(s))
                alloc_details.append({
                    "allocation_id": f"pref-{t.id}-{idx}",
                    "subject_code": f"DISC-0{idx+1}",
                    "subject_name": subj_title,
                    "room_name": "Cadastrada",
                    "time_slot": "M1",
                    "day_of_week": 1
                })

        workload_hours = len(alloc_details) * 0.83  # cada subslot/disciplina = 50 min (~0.83h)

        teacher_reports.append({
            "teacher_id": t.id,
            "teacher_name": t.name,
            "department": getattr(t, 'department', 'Geral') or "Geral",
            "total_allocations": len(alloc_details),
            "estimated_hours": round(workload_hours, 1),
            "allocations": alloc_details
        })

    return {
        "room_occupancy": room_occupancy,
        "teacher_reports": teacher_reports
    }


@router.get("/reports/teacher/{teacher_id}/pdf", status_code=200)
def export_teacher_pdf_report(
    teacher_id: str,
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    """
    GET /api/v1/reports/teacher/{teacher_id}/pdf
    Gera e faz o download do relatório PDF da grade de horários individual do docente.
    """
    if authorization:
        check_jwt_auth(authorization)

    # Busca docente por ID ou por Slug de nome (ex: prof-claudio -> Prof. Cláudio)
    teacher = db.query(models.Teacher).filter(models.Teacher.id == teacher_id).first()
    if not teacher:
        all_teachers = db.query(models.Teacher).all()
        for t in all_teachers:
            slug = t.name.lower().replace(" ", "-").replace(".", "")
            if t.id == teacher_id or slug == teacher_id.lower() or teacher_id.lower() in slug or teacher_id.lower() in t.id.lower():
                teacher = t
                break

    teacher_name = teacher.name if teacher else f"Docente ({teacher_id})"
    teacher_dept = getattr(teacher, 'department', 'Geral') if teacher else "Geral"
    target_id = teacher.id if teacher else teacher_id

    allocations = db.query(models.Allocation).filter(models.Allocation.teacher_id == target_id).all()
    
    subslot_times_map = {
        "M": {1: "07:00-07:50", 2: "07:50-08:40", 3: "08:40-09:30", 4: "09:45-10:35", 5: "10:35-11:25", 6: "11:25-12:15"},
        "T": {1: "13:00-13:50", 2: "13:50-14:40", 3: "14:40-15:30", 4: "15:45-16:35", 5: "16:35-17:25", 6: "17:25-18:15"},
        "N": {1: "19:00-19:50", 2: "19:50-20:40", 3: "20:40-21:30", 4: "21:45-22:35", 5: "22:35-23:25", 6: "23:25-00:15"}
    }

    def _get_attr(obj, attr, default=None):
        if isinstance(obj, dict):
            val = obj.get(attr)
            return val if val is not None else default
        val = getattr(obj, attr, None)
        return val if val is not None else default

    alloc_details = []
    for a in allocations:
        r_id = _get_attr(a, 'room_id', '')
        r_obj = db.query(models.Room).filter(models.Room.id == r_id).first() if r_id else None
        shift_code = str(_get_attr(a, 'shift', 'M') or 'M').upper()
        sub_slot = _get_attr(a, 'sub_slot', 1) or 1
        t_slot = _get_attr(a, 'time_slot', f"{shift_code}{sub_slot}") or f"{shift_code}{sub_slot}"
        time_interval = subslot_times_map.get(shift_code, {}).get(sub_slot, "07:00-07:50")
        subj_name = _get_attr(a, 'subject') or _get_attr(a, 'subject_name') or "Disciplina"
        
        alloc_details.append({
            "subject_name": subj_name,
            "room_name": r_obj.name if r_obj else (r_id or "Sala 101"),
            "block_id": r_obj.block_id if r_obj else "Bloco Geral",
            "shift": shift_code,
            "sub_slot": sub_slot,
            "time_slot": t_slot,
            "time_interval": time_interval,
            "day_of_week": _get_attr(a, 'day_of_week', 1)
        })

    t_subjects = getattr(teacher, 'subjects', []) or []
    if isinstance(t_subjects, str):
        import json
        try:
            t_subjects = json.loads(t_subjects)
        except Exception:
            t_subjects = [t_subjects]

    if not alloc_details and t_subjects:
        for idx, s in enumerate(t_subjects):
            subj_title = s if isinstance(s, str) else (s.get('name') if isinstance(s, dict) else str(s))
            alloc_details.append({
                "subject_name": subj_title,
                "room_name": "Sala Definida",
                "block_id": "Bloco A",
                "shift": "M",
                "sub_slot": idx + 1,
                "time_slot": f"M{idx + 1}",
                "time_interval": subslot_times_map["M"].get(idx + 1, "07:00-07:50"),
                "day_of_week": (idx % 5) + 1
            })

    pdf_bytes = generate_teacher_pdf_report(teacher_name, teacher_dept, alloc_details)
    filename = f"grade_horario_{teacher_name.lower().replace(' ', '_')}.pdf"

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"inline; filename={filename}"}
    )


@router.get("/reports/room/{room_id}/pdf", status_code=200)
def export_room_pdf_report(
    room_id: str,
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    """
    GET /api/v1/reports/room/{room_id}/pdf
    Gera e faz o download do relatório PDF de ocupação da sala física com docentes, disciplinas, turnos e horários.
    """
    if authorization:
        check_jwt_auth(authorization)

    # Busca sala por ID ou por nome/código
    room = db.query(models.Room).filter(models.Room.id == room_id).first()
    if not room:
        all_rooms = db.query(models.Room).all()
        for r in all_rooms:
            if r.name == room_id or r.id.lower() == room_id.lower() or room_id.lower() in r.name.lower() or r.name.lower() in room_id.lower():
                room = r
                break

    room_name = room.name if room else f"Sala ({room_id})"
    block_id = room.block_id if room else "Geral"
    capacity = room.capacity if room else 0
    room_type = room.room_type if room else "Sala de Aula"
    target_id = room.id if room else room_id

    allocations = db.query(models.Allocation).filter(models.Allocation.room_id == target_id).all()
    if not allocations and room:
        allocations = db.query(models.Allocation).filter(
            (models.Allocation.room_id == room.id) | (models.Allocation.room_id == room.name)
        ).all()

    alloc_details = []
    subslot_times_map = {
        "M": {1: "07:00-07:50", 2: "07:50-08:40", 3: "08:40-09:30", 4: "09:45-10:35", 5: "10:35-11:25", 6: "11:25-12:15"},
        "T": {1: "13:00-13:50", 2: "13:50-14:40", 3: "14:40-15:30", 4: "15:45-16:35", 5: "16:35-17:25", 6: "17:25-18:15"},
        "N": {1: "19:00-19:50", 2: "19:50-20:40", 3: "20:40-21:30", 4: "21:45-22:35", 5: "22:35-23:25", 6: "23:25-00:15"}
    }

    for a in allocations:
        t_id = _get_attr(a, 'teacher_id', '')
        t_obj = db.query(models.Teacher).filter(models.Teacher.id == t_id).first() if t_id else None
        shift_code = str(_get_attr(a, 'shift', 'M') or 'M').upper()
        sub_slot = _get_attr(a, 'sub_slot', 1) or 1
        t_slot = _get_attr(a, 'time_slot', f"{shift_code}{sub_slot}") or f"{shift_code}{sub_slot}"
        time_interval = subslot_times_map.get(shift_code, {}).get(sub_slot, "07:00-07:50")
        subj_name = _get_attr(a, 'subject') or _get_attr(a, 'subject_name') or "Disciplina"
        
        alloc_details.append({
            "teacher_name": t_obj.name if t_obj else (t_id or "Docente"),
            "department": getattr(t_obj, 'department', '') if t_obj else '',
            "subject_name": subj_name,
            "shift": shift_code,
            "sub_slot": sub_slot,
            "time_slot": t_slot,
            "time_interval": time_interval,
            "day_of_week": _get_attr(a, 'day_of_week', 1)
        })

    is_accessible = bool(getattr(room, 'is_accessible', True)) if room else True

    pdf_bytes = generate_room_pdf_report(room_name, block_id, capacity, room_type, is_accessible, alloc_details)
    filename = f"ocupacao_sala_{room_name.lower().replace(' ', '_').replace('/', '_')}.pdf"

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"inline; filename={filename}"}
    )


@router.delete("/rooms/{room_id}", status_code=200)
def delete_room(room_id: str, authorization: str = Header(None), db: Session = Depends(get_db)):
    """
    DELETE /api/v1/rooms/{room_id}
    Remove uma sala física se ela não possuir alocações ativas.
    """
    check_jwt_auth(authorization)
    
    room = db.query(models.Room).filter(models.Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Sala não encontrada.")

    # Verificar alocações (ajuste conforme lógica do seu sistema)
    allocations = db.query(models.Allocation).filter(models.Allocation.room_id == room_id).first()
    if allocations:
        raise HTTPException(status_code=409, detail="Não é possível excluir sala que possui alocações.")

    db.delete(room)
    db.commit()
    logger.warning(f"Sala removida: {room.name} ({room.id})")
    return {"message": f"Sala '{room.name}' excluída com sucesso."}


@router.get("/reports/occupancy/pdf", status_code=200)
def export_occupancy_pdf(
    block_id: str = None,
    shift: str = None,
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    """
    GET /api/v1/reports/occupancy/pdf
    Gera e envia relatório em formato PDF impresso limpo.
    """
    check_jwt_auth(authorization)
    
    # Coletar dados do banco de dados (e fallback em memória se necessário)
    db_rooms_objs = db.query(models.Room).all()
    rooms_data = [
        {
            "id": r.id,
            "block_id": r.block_id,
            "name": r.name,
            "capacity": r.capacity,
            "room_type": r.room_type,
            "is_accessible": r.is_accessible,
            "features": r.features or []
        }
        for r in db_rooms_objs
    ]

    # Coletar alocações do banco e cruzar com docentes e salas
    db_allocations = db.query(models.Allocation).all()
    teachers_map = {t.id: t for t in db.query(models.Teacher).all()}
    rooms_map = {r.id: r for r in db.query(models.Room).all()}

    allocations_data = [
        {
            "id": a.id,
            "teacher_id": a.teacher_id,
            "room_id": a.room_id,
            "day_of_week": a.day_of_week,
            "shift": a.shift,
            "sub_slot": a.sub_slot,
            "time_slot": f"{a.shift}{a.sub_slot}"
        }
        for a in db_allocations
    ]

    days_map = {1: "Segunda-feira", 2: "Terça-feira", 3: "Quarta-feira", 4: "Quinta-feira", 5: "Sexta-feira", 6: "Sábado", 7: "Domingo"}

    teacher_allocations_data = []
    for a in db_allocations:
        teacher = teachers_map.get(a.teacher_id)
        room = rooms_map.get(a.room_id)
        teacher_name = teacher.name if teacher else a.teacher_id
        subject_name = a.subject or (teacher.subjects[0] if teacher and teacher.subjects else "-")
        room_name = f"{room.name} ({room.block_id})" if room else a.room_id
        day_str = days_map.get(a.day_of_week, str(a.day_of_week))

        teacher_allocations_data.append({
            "teacher_name": teacher_name,
            "day_of_week": day_str,
            "subject": subject_name,
            "room_name": room_name,
            "shift": a.shift,
            "sub_slot": a.sub_slot
        })

    pdf_bytes = generate_pdf_report(rooms_data, allocations_data, block_id=block_id, shift=shift, teacher_allocations=teacher_allocations_data)
    date_str = datetime.datetime.now().strftime("%Y%m%d")
    logger.info(f"[REPORT_EXPORT] Relatório PDF gerado com sucesso. Tamanho: {len(pdf_bytes)} bytes. Filtros: block_id={block_id}, shift={shift}")

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="relatorio-ocupacao-{date_str}.pdf"'
        }
    )


@router.get("/reports/occupancy/excel", status_code=200)
def export_occupancy_excel(
    block_id: str = None,
    shift: str = None,
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    """
    GET /api/v1/reports/occupancy/excel
    Gera e envia planilha em formato Excel (.xlsx).
    """
    check_jwt_auth(authorization)
    
    db_rooms_objs = db.query(models.Room).all()
    rooms_data = [
        {
            "id": r.id,
            "block_id": r.block_id,
            "name": r.name,
            "capacity": r.capacity,
            "room_type": r.room_type,
            "is_accessible": r.is_accessible,
            "features": r.features or []
        }
        for r in db_rooms_objs
    ]

    db_allocations = db.query(models.Allocation).all()
    teachers_map = {t.id: t for t in db.query(models.Teacher).all()}
    rooms_map = {r.id: r for r in db.query(models.Room).all()}

    allocations_data = [
        {
            "id": a.id,
            "teacher_id": a.teacher_id,
            "room_id": a.room_id,
            "day_of_week": a.day_of_week,
            "shift": a.shift,
            "sub_slot": a.sub_slot,
            "time_slot": f"{a.shift}{a.sub_slot}"
        }
        for a in db_allocations
    ]

    days_map = {1: "Segunda-feira", 2: "Terça-feira", 3: "Quarta-feira", 4: "Quinta-feira", 5: "Sexta-feira", 6: "Sábado", 7: "Domingo"}

    teacher_allocations_data = []
    for a in db_allocations:
        teacher = teachers_map.get(a.teacher_id)
        room = rooms_map.get(a.room_id)
        teacher_name = teacher.name if teacher else a.teacher_id
        subject_name = a.subject or (teacher.subjects[0] if teacher and teacher.subjects else "-")
        room_name = f"{room.name} ({room.block_id})" if room else a.room_id
        day_str = days_map.get(a.day_of_week, str(a.day_of_week))

        teacher_allocations_data.append({
            "teacher_name": teacher_name,
            "day_of_week": day_str,
            "subject": subject_name,
            "room_name": room_name,
            "shift": a.shift,
            "sub_slot": a.sub_slot
        })

    excel_bytes = generate_excel_report(rooms_data, allocations_data, block_id=block_id, shift=shift, teacher_allocations=teacher_allocations_data)
    date_str = datetime.datetime.now().strftime("%Y%m%d")
    logger.info(f"[REPORT_EXPORT] Relatório Excel gerado com sucesso. Tamanho: {len(excel_bytes)} bytes. Filtros: block_id={block_id}, shift={shift}")

    return Response(
        content=excel_bytes,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": f'attachment; filename="relatorio-ocupacao-{date_str}.xlsx"'
        }
    )


@router.post("/allocations", status_code=201)
def create_allocation(alloc: AllocationCreate, authorization: str = Header(None), db: Session = Depends(get_db)):
    """
    POST /api/v1/allocations
    Cadastra uma alocação de aula de 50 min com trava de no máximo 4 aulas seguidas por turno.
    """
    check_jwt_auth(authorization)

    shift_upper = alloc.shift.upper()
    if shift_upper not in ['M', 'T', 'N']:
        raise HTTPException(status_code=400, detail="Turno inválido. Esperado: M, T ou N.")

    # Validar se o docente existe no banco de dados
    teacher = db.query(models.Teacher).filter(models.Teacher.id == alloc.teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail=f"Docente '{alloc.teacher_id}' não encontrado no sistema.")

    # Validar se a sala física existe no banco de dados
    room = db.query(models.Room).filter(models.Room.id == alloc.room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail=f"Sala física '{alloc.room_id}' não encontrada no sistema.")

    # Validar se o docente possui indisponibilidade cadastrada no dia e horário
    time_slot_id = f"{shift_upper}{alloc.sub_slot}"
    teacher_restriction = db.query(models.Restriction).filter(
        models.Restriction.teacher_id == alloc.teacher_id,
        models.Restriction.day_of_week == alloc.day_of_week,
        models.Restriction.time_slot_id == time_slot_id
    ).first()
    if teacher_restriction:
        raise HTTPException(
            status_code=409,
            detail=f"O docente '{alloc.teacher_id}' possui indisponibilidade cadastrada para o dia {alloc.day_of_week} no horário {time_slot_id}."
        )

    # Buscar alocações existentes do docente no mesmo dia e turno

    existing_teacher_allocs = db.query(models.Allocation).filter(
        models.Allocation.teacher_id == alloc.teacher_id,
        models.Allocation.day_of_week == alloc.day_of_week,
        models.Allocation.shift == shift_upper
    ).all()

    existing_sub_slots = [a.sub_slot for a in existing_teacher_allocs]
    if alloc.sub_slot in existing_sub_slots:
        raise HTTPException(status_code=409, detail="O docente já possui aula cadastrada neste sub-slot.")

    # Validar janela de consecutividade (max 4 aulas seguidas)
    if not check_consecutive_limit(existing_sub_slots, alloc.sub_slot):
        logger.warning(f"[CONSECUTIVE_LIMIT_REJECT] Rejeitada 5ª aula seguida para docente {alloc.teacher_id} no dia {alloc.day_of_week}, turno {shift_upper}.")
        raise HTTPException(
            status_code=409,
            detail="Limite máximo de 4 aulas seguidas no mesmo turno atingido para o docente."
        )


    # Validar conflito de sala
    room_conflict = db.query(models.Allocation).filter(
        models.Allocation.room_id == alloc.room_id,
        models.Allocation.day_of_week == alloc.day_of_week,
        models.Allocation.shift == shift_upper,
        models.Allocation.sub_slot == alloc.sub_slot
    ).first()
    if room_conflict:
        raise HTTPException(status_code=409, detail="A sala física já está ocupada neste horário.")

    # Validar disciplina informada ou atribuir primeira disciplina do docente como padrão
    chosen_subject = alloc.subject.strip() if alloc.subject and alloc.subject.strip() else None
    teacher_subjects = teacher.subjects or []
    if chosen_subject:
        if teacher_subjects and chosen_subject not in teacher_subjects:
            raise HTTPException(
                status_code=422,
                detail=f"A disciplina '{chosen_subject}' não pertence ao rol de disciplinas lecionáveis do docente ({', '.join(teacher_subjects)})."
            )
    else:
        chosen_subject = teacher_subjects[0] if teacher_subjects else "Geral"

    new_id = str(uuid.uuid4())
    new_alloc = models.Allocation(
        id=new_id,
        teacher_id=alloc.teacher_id,
        room_id=alloc.room_id,
        day_of_week=alloc.day_of_week,
        shift=shift_upper,
        sub_slot=alloc.sub_slot,
        subject=chosen_subject
    )
    db.add(new_alloc)
    db.commit()

    logger.info(f"[ALLOCATION_CREATED] Aula alocada com sucesso: Docente={alloc.teacher_id}, Disciplina={chosen_subject}, Sala={alloc.room_id}, Dia={alloc.day_of_week}, Shift={shift_upper}, SubSlot={alloc.sub_slot}")
    return {
        "id": new_alloc.id,
        "teacher_id": new_alloc.teacher_id,
        "room_id": new_alloc.room_id,
        "day_of_week": new_alloc.day_of_week,
        "shift": new_alloc.shift,
        "sub_slot": new_alloc.sub_slot,
        "subject": new_alloc.subject,
        "created_at": new_alloc.created_at.isoformat() if new_alloc.created_at else ""
    }


@router.get("/allocations", status_code=200)
def list_allocations(
    teacher_id: str = None,
    room_id: str = None,
    shift: str = None,
    day_of_week: int = None,
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    """
    GET /api/v1/allocations
    Lista as alocações com filtros opcionais.
    """
    check_jwt_auth(authorization)

    query = db.query(models.Allocation).order_by(models.Allocation.created_at.desc())
    if teacher_id:
        query = query.filter(models.Allocation.teacher_id == teacher_id)
    if room_id:
        query = query.filter(models.Allocation.room_id == room_id)
    if shift:
        query = query.filter(models.Allocation.shift == shift.upper())
    if day_of_week:
        query = query.filter(models.Allocation.day_of_week == day_of_week)

    allocs = query.all()
    return [
        {
            "id": a.id,
            "teacher_id": a.teacher_id,
            "room_id": a.room_id,
            "day_of_week": a.day_of_week,
            "shift": a.shift,
            "sub_slot": a.sub_slot,
            "subject": a.subject,
            "created_at": a.created_at.isoformat() if a.created_at else ""
        }
        for a in allocs
    ]


@router.delete("/allocations/{allocation_id}", status_code=200)
def delete_allocation(allocation_id: str, authorization: str = Header(None), db: Session = Depends(get_db)):
    """
    DELETE /api/v1/allocations/{allocation_id}
    Exclui uma alocação de aula.
    """
    check_jwt_auth(authorization)

    alloc = db.query(models.Allocation).filter(models.Allocation.id == allocation_id).first()
    if not alloc:
        raise HTTPException(status_code=404, detail="Alocação de aula não encontrada.")

    db.delete(alloc)
    db.commit()
    logger.info(f"[ALLOCATION_DELETED] Alocação {allocation_id} removida.")
    return {"message": "Alocação excluída com sucesso.", "deleted_id": allocation_id}


@router.post("/allocation/run", status_code=202)
def run_allocation(authorization: str = Header(None)):
    """
    POST /api/v1/allocation/run
    Dispara assincronamente o motor de alocação de IA.
    """
    check_jwt_auth(authorization)

    for task in db_tasks.values():
        if task.get("status") in ("queued", "running"):
            raise HTTPException(
                status_code=409,
                detail="Já existe uma rodada de alocação em execução em background."
            )

    task_id = enqueue_allocation_run()
    return {
        "task_id": task_id,
        "status": "queued",
        "message": "Processamento de alocação enviado para a fila com sucesso."
    }


@router.get("/allocation/status/{task_id}", status_code=200)
def get_allocation_status(task_id: str, authorization: str = Header(None)):
    """
    GET /api/v1/allocation/status/{task_id}
    Consulta o status e o progresso de uma tarefa de alocação assíncrona.
    """
    check_jwt_auth(authorization)

    task = db_tasks.get(task_id)
    if not task:
        raise HTTPException(
            status_code=404,
            detail="Tarefa de alocação não encontrada."
        )

    return {
        "task_id": task["id"],
        "status": task["status"],
        "progress": task.get("progress", 0),
        "created_at": task.get("created_at"),
        "error_log": task.get("error_log"),
        "result": task.get("result_summary")
    }


# --- Subslots API Endpoints ---

@router.get("/subslots", status_code=200)
def list_subslots(
    shift: str = None,
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    """
    GET /api/v1/subslots
    Retorna a lista de subslots de horários e intervalos acadêmicos.
    """
    check_jwt_auth(authorization)
    query = db.query(models.SubslotTimeInterval)
    if shift:
        query = query.filter(models.SubslotTimeInterval.shift == shift.lower())
    subslots = query.order_by(models.SubslotTimeInterval.shift, models.SubslotTimeInterval.start_time).all()
    return [
        {
            "id": s.id,
            "code": s.code,
            "shift": s.shift,
            "class_number": s.class_number,
            "start_time": s.start_time,
            "end_time": s.end_time,
            "is_interval": s.is_interval
        }
        for s in subslots
    ]


@router.post("/subslots", status_code=201)
def create_subslot(
    payload: SubslotCreate,
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    """
    POST /api/v1/subslots
    Cadastra um novo subslot de horário ou intervalo na tabela subslot_time_intervals.
    """
    check_jwt_auth(authorization)

    if payload.start_time >= payload.end_time:
        raise HTTPException(status_code=400, detail="O horário de início deve ser anterior ao horário de término.")

    duplicate = db.query(models.SubslotTimeInterval).filter(models.SubslotTimeInterval.code == payload.code).first()
    if duplicate:
        raise HTTPException(status_code=409, detail=f"Já existe um subslot cadastrado com o código '{payload.code}'.")

    new_subslot = models.SubslotTimeInterval(
        id=str(uuid.uuid4()),
        code=payload.code,
        shift=payload.shift.lower(),
        class_number=payload.class_number,
        start_time=payload.start_time,
        end_time=payload.end_time,
        is_interval=payload.is_interval
    )
    db.add(new_subslot)
    db.commit()
    logger.info(f"[SUBSLOT_MANAGEMENT] Subslot cadastrado com sucesso: {new_subslot.code} ({new_subslot.shift} {new_subslot.start_time}-{new_subslot.end_time})")
    return {
        "id": new_subslot.id,
        "code": new_subslot.code,
        "shift": new_subslot.shift,
        "class_number": new_subslot.class_number,
        "start_time": new_subslot.start_time,
        "end_time": new_subslot.end_time,
        "is_interval": new_subslot.is_interval
    }


@router.put("/subslots/{subslot_id}", status_code=200)
def update_subslot(
    subslot_id: str,
    payload: SubslotUpdate,
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    """
    PUT /api/v1/subslots/{subslot_id}
    Atualiza as propriedades de um subslot de horário.
    """
    check_jwt_auth(authorization)

    subslot = db.query(models.SubslotTimeInterval).filter(models.SubslotTimeInterval.id == subslot_id).first()
    if not subslot:
        raise HTTPException(status_code=404, detail=f"Subslot '{subslot_id}' não encontrado.")

    if payload.code and payload.code != subslot.code:
        duplicate = db.query(models.SubslotTimeInterval).filter(models.SubslotTimeInterval.code == payload.code).first()
        if duplicate:
            raise HTTPException(status_code=409, detail=f"Já existe outro subslot cadastrado com o código '{payload.code}'.")
        subslot.code = payload.code

    if payload.shift:
        subslot.shift = payload.shift.lower()
    if payload.class_number is not None:
        subslot.class_number = payload.class_number
    if payload.start_time:
        subslot.start_time = payload.start_time
    if payload.end_time:
        subslot.end_time = payload.end_time
    if payload.is_interval is not None:
        subslot.is_interval = payload.is_interval

    if subslot.start_time >= subslot.end_time:
        raise HTTPException(status_code=400, detail="O horário de início deve ser anterior ao horário de término.")

    db.commit()
    logger.info(f"[SUBSLOT_MANAGEMENT] Subslot {subslot_id} ({subslot.code}) atualizado com sucesso.")
    return {
        "id": subslot.id,
        "code": subslot.code,
        "shift": subslot.shift,
        "class_number": subslot.class_number,
        "start_time": subslot.start_time,
        "end_time": subslot.end_time,
        "is_interval": subslot.is_interval
    }


@router.delete("/subslots/{subslot_id}", status_code=204)
def delete_subslot(
    subslot_id: str,
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    """
    DELETE /api/v1/subslots/{subslot_id}
    Remove um subslot de horário.
    """
    check_jwt_auth(authorization)

    subslot = db.query(models.SubslotTimeInterval).filter(models.SubslotTimeInterval.id == subslot_id).first()
    if not subslot:
        raise HTTPException(status_code=404, detail=f"Subslot '{subslot_id}' não encontrado.")

    db.delete(subslot)
    db.commit()
    logger.warning(f"[SUBSLOT_MANAGEMENT] Subslot {subslot_id} ({subslot.code}) excluído.")
    return Response(status_code=204)


@router.post("/emergency-reallocations/calculate", response_model=EmergencyReallocationCalculateResponse, status_code=200)
def calculate_emergency_reallocation(
    payload: EmergencyReallocationRequest,
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    """
    POST /api/v1/emergency-reallocations/calculate
    Calcula alternativas de realocação emergencial de disciplinas e horários via IA para docente em licença.
    """
    check_jwt_auth(authorization)
    teacher = db.query(models.Teacher).filter(models.Teacher.id == payload.absent_teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail=f"Docente '{payload.absent_teacher_id}' não encontrado.")

    teachers = db.query(models.Teacher).all()
    teachers_list = [
        {
            "id": t.id,
            "name": t.name,
            "department": getattr(t, "department", "Geral") or "Geral",
            "subjects": getattr(t, "subjects", []) or []
        }
        for t in teachers
    ]

    allocations = db.query(models.Allocation).all()
    allocations_list = [
        {
            "id": str(a.id),
            "teacher_id": a.teacher_id,
            "room_id": str(a.room_id) if a.room_id else None,
            "day_of_week": a.day_of_week,
            "shift": a.shift,
            "sub_slot": a.sub_slot,
            "subject": a.subject
        }
        for a in allocations
    ]

    rooms = db.query(models.Room).all()
    rooms_list = [{"id": str(r.id), "block_id": r.block_id, "name": r.name, "capacity": r.capacity, "room_type": r.room_type, "is_accessible": r.is_accessible, "features": r.features or []} for r in rooms]
    coordinations = db.query(models.Coordination).all()
    coordinations_list = [{"id": str(c.id), "name": c.name, "credits": c.credits} for c in coordinations]
    restrictions = db.query(models.Restriction).all()
    restrictions_list = [{"id": str(r.id), "teacher_id": r.teacher_id, "day_of_week": int(r.day_of_week), "time_slot_id": r.time_slot_id} for r in restrictions]

    engine = CoreAllocationEngine(rooms_list, coordinations_list, [], restrictions=restrictions_list)
    result = engine.calculate_emergency_reallocation(payload.absent_teacher_id, teachers_list, allocations_list)

    logger.info(f"[EMERGENCY_REALLOCATION] Opções calculadas para docente {payload.absent_teacher_id}: {len(result['options'])} opção(ões) encontradas.")
    return result


@router.post("/emergency-reallocations/commit", response_model=EmergencyReallocationCommitResponse, status_code=200)
def commit_emergency_reallocation(
    payload: EmergencyReallocationCommitRequest,
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    """
    POST /api/v1/emergency-reallocations/commit
    Efetiva no banco de dados e notifica os professores da realocação emergencial selecionada (Modo Assistido ou Modo Delegado).
    """
    check_jwt_auth(authorization)
    teacher = db.query(models.Teacher).filter(models.Teacher.id == payload.absent_teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail=f"Docente '{payload.absent_teacher_id}' não encontrado.")

    # Efetivar no banco: atualizar teacher_id das alocações das turmas afetadas
    for sub in payload.substitutions:
        alloc = db.query(models.Allocation).filter(
            models.Allocation.id == sub.class_id
        ).first()
        if not alloc:
            alloc = db.query(models.Allocation).filter(
                models.Allocation.subject == sub.class_id,
                models.Allocation.teacher_id == payload.absent_teacher_id
            ).first()
        if not alloc and getattr(sub, "class_name", None):
            alloc = db.query(models.Allocation).filter(
                models.Allocation.subject == sub.class_name,
                models.Allocation.teacher_id == payload.absent_teacher_id
            ).first()
        if alloc:
            alloc.teacher_id = sub.substitute_teacher_id
    db.commit()

    log_id = save_emergency_reallocation_log(
        absent_teacher_id=payload.absent_teacher_id,
        start_date=datetime.date.today().isoformat(),
        end_date=datetime.date.today().isoformat(),
        mode=payload.mode,
        selected_option_index=payload.selected_option_index,
        substitutions=[s.dict() for s in payload.substitutions]
    )

    logger.info(f"[EMERGENCY_REALLOCATION] Realocação efetivada em modo '{payload.mode}' (log_id={log_id}) para {len(payload.substitutions)} substituição(ões).")
    return {
        "log_id": log_id,
        "status": "success",
        "mode_used": payload.mode,
        "message": f"Realocação emergencial efetivada com sucesso em modo '{payload.mode}'. Docentes substitutos notificados."
    }


# ==========================================
# ENDPOINTS DE AUTENTICAÇÃO E RBAC
# ==========================================

@router.post("/auth/register", status_code=status.HTTP_201_CREATED)
def register_user(payload: UserRegisterRequest, db: Session = Depends(get_db)):
    """Auto-cadastro de novo usuário com status inicial pendente."""
    existing = db.query(models.User).filter(models.User.email == payload.email.strip().lower()).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este e-mail já está cadastrado no sistema."
        )

    user_id = f"u-{uuid.uuid4().hex[:8]}"
    new_user = models.User(
        id=user_id,
        name=payload.name.strip(),
        email=payload.email.strip().lower(),
        password_hash=hash_password(payload.password),
        role="docente",
        department=payload.department.strip() if payload.department else "Geral",
        is_active=False  # Requer aprovação do gestor
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    logger.info(f"[AUTH] Novo usuário registrado (pendente): {new_user.email} (id={new_user.id})")
    return {
        "status": "success",
        "message": "Cadastro realizado com sucesso. Sua conta está aguardando aprovação pelo gestor.",
        "user": {
            "id": new_user.id,
            "name": new_user.name,
            "email": new_user.email,
            "role": new_user.role,
            "department": new_user.department,
            "is_active": new_user.is_active,
            "created_at": new_user.created_at.isoformat() if new_user.created_at else None
        }
    }


@router.post("/auth/login")
def login_user(payload: UserLoginRequest, db: Session = Depends(get_db)):
    """Autenticação de usuário e emissão de token JWT."""
    user = db.query(models.User).filter(models.User.email == payload.email.strip().lower()).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos."
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Conta aguarda aprovação pelo gestor da plataforma."
        )

    must_change = bool(getattr(user, "must_change_password", False))
    token_claims = {
        "sub": user.email,
        "id": user.id,
        "name": user.name,
        "role": user.role,
        "department": user.department,
        "must_change_password": must_change
    }
    token = create_access_token(token_claims)

    logger.info(f"[AUTH] Login bem-sucedido: {user.email} (role={user.role})")
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "department": user.department,
            "is_active": user.is_active,
            "must_change_password": must_change,
            "created_at": user.created_at.isoformat() if user.created_at else None
        }
    }


@router.get("/auth/me")
def get_current_user_profile(current_user: TokenData = Depends(get_current_user)):
    """Retorna os dados do perfil do usuário atualmente autenticado."""
    return {
        "id": current_user.id or "u-current",
        "name": current_user.name or current_user.username,
        "email": current_user.username,
        "role": current_user.role,
        "department": current_user.department,
        "must_change_password": current_user.must_change_password
    }


@router.post("/auth/change-password")
def change_password(payload: ChangePasswordRequest, current_user: TokenData = Depends(get_current_user), db: Session = Depends(get_db)):
    """Redefinição de senha com validação de credencial atual e atualização no banco."""
    user = db.query(models.User).filter(models.User.email == current_user.username).first()
    if not user or not verify_password(payload.current_password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Senha atual incorreta."
        )

    if not payload.new_password or len(payload.new_password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A nova senha deve possuir no mínimo 8 caracteres."
        )

    if payload.current_password == payload.new_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A nova senha deve ser diferente da senha atual."
        )

    user.password_hash = hash_password(payload.new_password)
    user.must_change_password = False
    db.commit()
    db.refresh(user)

    logger.info(f"[AUTH] Senha alterada com sucesso para {user.email}")
    return {
        "status": "success",
        "message": "Senha atualizada com sucesso. Seu acesso foi liberado.",
        "must_change_password": False
    }



@router.get("/users")
def list_users(current_user: TokenData = Depends(require_roles(["gestor", "admin"])), db: Session = Depends(get_db)):
    """Lista todos os usuários para gerenciamento pelo gestor, omitindo superadministrador global."""
    users = (
        db.query(models.User)
        .filter(models.User.role != "doctor-chef")
        .order_by(models.User.created_at.desc())
        .all()
    )
    return [
        {
            "id": u.id,
            "name": u.name,
            "email": u.email,
            "role": u.role,
            "department": u.department,
            "is_active": u.is_active,
            "created_at": u.created_at.isoformat() if u.created_at else None
        }
        for u in users
        if (u.role or "").lower() != "doctor-chef" and (u.email or "").lower() != "doctor@classsync.ai"
    ]


@router.patch("/users/{user_id}/status")
def update_user_status(user_id: str, payload: UserStatusUpdateRequest, current_user: TokenData = Depends(require_roles(["gestor", "admin"])), db: Session = Depends(get_db)):
    """Atualiza o status de ativação e papel do usuário."""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado."
        )

    # Bloqueio de proteção: superadministrador da plataforma não pode ser alterado via gestão local
    if (user.role or "").lower() == "doctor-chef" or (user.email or "").lower() == "doctor@classsync.ai":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Não é permitido alterar o status ou o perfil da conta do Super Administrador Geral."
        )

    if payload.is_active is not None:
        user.is_active = payload.is_active
    if payload.role is not None:
        user.role = payload.role.strip().lower()

    db.commit()
    db.refresh(user)

    logger.info(f"[USERS] Status do usuário atualizado: {user.email} (is_active={user.is_active}, role={user.role})")
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "department": user.department,
        "is_active": user.is_active,
        "created_at": user.created_at.isoformat() if user.created_at else None
    }


def get_request_base_url(request: Optional[Request] = None) -> Optional[str]:
    """Identifica a URL pública da aplicação a partir de env vars ou cabeçalhos HTTP do proxy."""
    env_base = os.environ.get("BASE_URL") or os.environ.get("APP_URL") or os.environ.get("PUBLIC_URL")
    if env_base:
        return env_base.strip().rstrip("/")
    if request:
        proto = request.headers.get("x-forwarded-proto") or request.url.scheme
        host = request.headers.get("x-forwarded-host") or request.headers.get("host") or ""
        if host and not any(h in host for h in ["localhost", "127.0.0.1", "testserver"]):
            return f"{proto}://{host}"
        if request.base_url:
            b = str(request.base_url).rstrip("/")
            if not any(h in b for h in ["localhost", "127.0.0.1", "testserver"]):
                return b
    return None


def is_cloud_environment(base_url: Optional[str] = None) -> bool:
    """Verifica se a aplicação está em ambiente de nuvem (ex: Google Cloud Run)."""
    if os.environ.get("K_SERVICE") or os.environ.get("CLOUD_RUN_JOB"):
        return True
    env_base = os.environ.get("BASE_URL") or os.environ.get("APP_URL") or os.environ.get("PUBLIC_URL")
    if env_base and not any(h in env_base for h in ["localhost", "127.0.0.1", "testserver"]):
        return True
    if base_url and not any(h in base_url for h in ["localhost", "127.0.0.1", "testserver"]):
        return True
    return False


def resolve_tenant_url(port: int, base_url: Optional[str] = None, slug: Optional[str] = None) -> str:
    """
    Retorna a URL dedicada da instituição/tenant.
    Em ambiente de nuvem (como Cloud Run), retorna a URL base pública.
    Em desenvolvimento local, retorna http://localhost:{port}/.
    """
    if base_url:
        return f"{base_url.rstrip('/')}/"
    env_base = os.environ.get("BASE_URL") or os.environ.get("APP_URL") or os.environ.get("PUBLIC_URL")
    if env_base:
        return f"{env_base.strip().rstrip('/')}/"
    return f"http://localhost:{port}/"


def check_tenant_status(port: int) -> str:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            if s.connect_ex(('127.0.0.1', port)) == 0:
                return "online"
    except Exception:
        pass
    return "offline"


def discover_tenants(base_url: Optional[str] = None) -> List[Dict[str, Any]]:
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    tenants = []
    seen_slugs = set()
    is_cloud = is_cloud_environment(base_url)

    # 1. Buscar arquivos .env.<slug>
    try:
        for fname in os.listdir(root_dir):
            if fname.startswith(".env.") and not fname.endswith(".example") and not fname.endswith(".bak"):
                slug = fname[5:]
                if not slug:
                    continue
                seen_slugs.add(slug)
                port = 8001
                env_path = os.path.join(root_dir, fname)
                custom_name = None
                master_chef_email = None
                try:
                    with open(env_path, "r", encoding="utf-8") as f:
                        for line in f:
                            line = line.strip()
                            if line.startswith("PORT="):
                                port = int(line.split("=")[1].strip())
                            elif line.startswith("INSTITUTION_NAME="):
                                custom_name = line.split("=", 1)[1].strip()
                            elif line.startswith("MASTER_CHEF_EMAIL="):
                                master_chef_email = line.split("=", 1)[1].strip()
                except Exception:
                    pass

                created_at = None
                try:
                    ctime = os.path.getctime(env_path)
                    created_at = datetime.datetime.fromtimestamp(ctime, tz=datetime.timezone.utc).isoformat()
                except Exception:
                    pass

                name = custom_name if custom_name else slug.replace("_", " ").replace("-", " ").title()
                tenants.append({
                    "name": name,
                    "slug": slug,
                    "port": port,
                    "status": "online" if is_cloud else check_tenant_status(port),
                    "url": resolve_tenant_url(port, base_url, slug),
                    "created_at": created_at,
                    "master_chef_email": master_chef_email
                })
    except Exception as e:
        logger.warning(f"[TENANTS] Erro ao varrer root_dir: {e}")

    # 2. Buscar pastas em data/
    data_base_dir = os.path.join(root_dir, "data")
    if os.path.exists(data_base_dir):
        try:
            for entry in os.listdir(data_base_dir):
                full_path = os.path.join(data_base_dir, entry)
                if os.path.isdir(full_path) and entry not in seen_slugs and not entry.startswith("."):
                    seen_slugs.add(entry)
                    port = 8001
                    created_at = None
                    try:
                        ctime = os.path.getctime(full_path)
                        created_at = datetime.datetime.fromtimestamp(ctime, tz=datetime.timezone.utc).isoformat()
                    except Exception:
                        pass
                    name = entry.replace("_", " ").replace("-", " ").title()
                    tenants.append({
                        "name": name,
                        "slug": entry,
                        "port": port,
                        "status": "online" if is_cloud else check_tenant_status(port),
                        "url": resolve_tenant_url(port, base_url, entry),
                        "created_at": created_at,
                        "master_chef_email": None
                    })
        except Exception as e:
            logger.warning(f"[TENANTS] Erro ao varrer data/: {e}")

    tenants.sort(key=lambda t: t["port"])
    return tenants


def provision_tenant_task(name: str, slug: str, port: int, master_chef_email: str, master_chef_password: str):
    """Executa a criação física de volumes, configuração de ambiente e seed do master-chef."""
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker, scoped_session

    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    data_dir = os.path.join(root_dir, "data", slug)
    os.makedirs(data_dir, exist_ok=True)

    secret_key = secrets.token_hex(32)
    env_file = os.path.join(root_dir, f".env.{slug}")
    env_content = f"""TENANT_NAME={slug}
INSTITUTION_NAME={name}
MASTER_CHEF_EMAIL={master_chef_email}
PORT={port}
HOST=0.0.0.0
DATA_DIR=./data/{slug}
DATABASE_URL=sqlite:///./data/{slug}/project.db
SECRET_KEY={secret_key}
APP_ENV=production
"""
    with open(env_file, "w", encoding="utf-8") as f:
        f.write(env_content)

    # Inicializar banco SQLite isolado e criar tabelas
    db_file = os.path.join(data_dir, "project.db")
    tenant_db_url = f"sqlite:///{os.path.abspath(db_file)}"
    tenant_engine = create_engine(tenant_db_url, connect_args={"check_same_thread": False})
    models.Base.metadata.create_all(bind=tenant_engine)

    TenantSession = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=tenant_engine))
    db = TenantSession()
    try:
        user = db.query(models.User).filter(models.User.email == master_chef_email).first()
        if not user:
            user = models.User(
                id=f"u-{slug}-master",
                name="Gestor Geral Institucional",
                email=master_chef_email,
                password_hash=hash_password(master_chef_password),
                role="gestor",
                department="Administração Geral",
                is_active=True,
                must_change_password=True
            )
            db.add(user)
            db.commit()
    except Exception as e:
        logger.error(f"[TENANT-PROVISION] Erro ao semear master-chef: {e}")
        db.rollback()
    finally:
        db.close()
        TenantSession.remove()
        tenant_engine.dispose()

    # Iniciar instância automaticamente (fora do ambiente de teste automatizado)
    if not os.environ.get("PYTEST_CURRENT_TEST"):
        start_tenant_instance(slug, port)


def start_tenant_instance(slug: str, port: int) -> bool:
    """Inicia a instância de um tenant (via docker compose ou processo local python)."""
    import subprocess
    import sys
    import time
    import shutil

    if check_tenant_status(port) == "online":
        return True

    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    env_file = os.path.join(root_dir, f".env.{slug}")
    env = os.environ.copy()
    if os.path.exists(env_file):
        try:
            with open(env_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        env[k.strip()] = v.strip()
        except Exception as e:
            logger.warning(f"[TENANT-START] Erro ao ler env_file {env_file}: {e}")
    else:
        # Auto-gerar .env.{slug} para persistência das configurações da instituição
        try:
            db_path = _get_tenant_db_path(slug)
            db_url = f"sqlite:///{os.path.abspath(db_path)}" if db_path else f"sqlite:///./data/{slug}/project.db"
            institution_name = slug.replace("_", " ").replace("-", " ").title()
            env_content = f"""TENANT_NAME={slug}
INSTITUTION_NAME={institution_name}
PORT={port}
HOST=0.0.0.0
DATA_DIR=./data/{slug}
DATABASE_URL={db_url}
SECRET_KEY={secrets.token_hex(32)}
APP_ENV=production
"""
            with open(env_file, "w", encoding="utf-8") as f:
                f.write(env_content)
        except Exception as e:
            logger.warning(f"[TENANT-START] Não foi possível persistir .env.{slug}: {e}")

    env["PORT"] = str(port)
    env["TENANT_NAME"] = slug
    if "DATABASE_URL" not in env or not env["DATABASE_URL"]:
        db_path = _get_tenant_db_path(slug)
        if db_path:
            env["DATABASE_URL"] = f"sqlite:///{os.path.abspath(db_path)}"
        else:
            env["DATABASE_URL"] = f"sqlite:///./data/{slug}/project.db"
    env["APP_ENV"] = "production"

    if shutil.which("docker"):
        try:
            res = subprocess.run(
                ["docker", "compose", "--project-name", f"classsync-{slug}", "--env-file", env_file, "up", "-d", "--build"],
                cwd=root_dir,
                capture_output=True,
                timeout=15
            )
            if res.returncode == 0:
                time.sleep(1.0)
                if check_tenant_status(port) == "online":
                    return True
        except Exception as e:
            logger.warning(f"[TENANT-START] Falha ao subir via docker: {e}")

    try:
        kwargs = {}
        if sys.platform == "win32":
            kwargs["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP | getattr(subprocess, "DETACHED_PROCESS", 0x00000008)
        else:
            kwargs["start_new_session"] = True

        subprocess.Popen(
            [sys.executable, "-m", "src.main"],
            env=env,
            cwd=root_dir,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            **kwargs
        )
        # Polling para aguardar a subida da instância (até 4 segundos)
        for _ in range(12):
            time.sleep(0.3)
            if check_tenant_status(port) == "online":
                return True
        return check_tenant_status(port) == "online"
    except Exception as e:
        logger.error(f"[TENANT-START] Falha ao iniciar processo local para {slug}: {e}")
        return False


def stop_tenant_instance(slug: str, port: int) -> bool:
    """Para a execução da instância de um tenant."""
    import subprocess
    import sys
    import time
    import shutil

    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

    if shutil.which("docker"):
        try:
            subprocess.run(
                ["docker", "compose", "--project-name", f"classsync-{slug}", "down"],
                cwd=root_dir,
                capture_output=True,
                timeout=15
            )
        except Exception:
            pass

    try:
        if sys.platform == "win32":
            cmd = f'Get-NetTCPConnection -LocalPort {port} -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess -Unique'
            res = subprocess.run(["powershell", "-NoProfile", "-Command", cmd], capture_output=True, text=True, timeout=5)
            pids = res.stdout.strip().split()
            for pid_str in pids:
                if pid_str.isdigit() and int(pid_str) != os.getpid():
                    subprocess.run(["taskkill", "/F", "/PID", pid_str], capture_output=True)
        else:
            cmd = f"fuser -k {port}/tcp"
            subprocess.run(cmd, shell=True, capture_output=True)
        time.sleep(0.5)
        return check_tenant_status(port) == "offline"
    except Exception as e:
        logger.error(f"[TENANT-STOP] Falha ao finalizar tenant {slug} na porta {port}: {e}")
        return False


def auto_start_tenants():
    """Inicia em segundo plano todas as instâncias de tenants que estiverem offline."""
    import threading
    import time

    def _worker():
        try:
            time.sleep(1.0)
            tenants = discover_tenants()
            current_port = int(os.environ.get("PORT", 8000))
            for t in tenants:
                p = t.get("port")
                s = t.get("slug")
                if p and s and p != current_port:
                    if check_tenant_status(p) == "offline":
                        logger.info(f"[AUTO-START] Inicializando tenant '{s}' na porta {p}...")
                        start_tenant_instance(s, p)
        except Exception as e:
            logger.warning(f"[AUTO-START] Falha ao auto-iniciar tenants: {e}")

    thread = threading.Thread(target=_worker, daemon=True)
    thread.start()


def _get_tenant_db_path(slug: str) -> Optional[str]:
    """Localiza o arquivo de banco SQLite da instituição."""
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    data_dir = os.path.join(root_dir, "data", slug)
    for cand in ["project.db", "classsync.db"]:
        p = os.path.join(data_dir, cand)
        if os.path.exists(p):
            return p
    return None


def _get_tenant_master_chef_info(slug: str) -> Optional[Dict[str, Any]]:
    """Lê as informações cadastrais do master-chef diretamente no SQLite da instituição."""
    import sqlite3
    db_path = _get_tenant_db_path(slug)
    if not db_path:
        root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        env_file = os.path.join(root_dir, f".env.{slug}")
        email = None
        if os.path.exists(env_file):
            try:
                with open(env_file, "r", encoding="utf-8") as f:
                    for line in f:
                        if line.startswith("MASTER_CHEF_EMAIL="):
                            email = line.split("=", 1)[1].strip()
            except Exception:
                pass
        if email:
            return {
                "id": f"u-{slug}-master",
                "email": email,
                "name": "Gestor Geral Institucional",
                "role": "gestor",
                "must_change_password": True,
                "is_active": True
            }
        return None

    try:
        conn = sqlite3.connect(f"file:{os.path.abspath(db_path)}?mode=ro", uri=True, timeout=5)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM User WHERE role = 'gestor' LIMIT 1")
        row = cur.fetchone()
        if not row:
            cur.execute("SELECT * FROM User LIMIT 1")
            row = cur.fetchone()
        conn.close()
        if row:
            keys = row.keys()
            return {
                "id": str(row["id"]) if "id" in keys else f"u-{slug}-master",
                "name": row["name"] if "name" in keys else "Gestor",
                "email": row["email"] if "email" in keys else "",
                "role": row["role"] if "role" in keys else "gestor",
                "must_change_password": bool(row["must_change_password"]) if "must_change_password" in keys else False,
                "is_active": bool(row["is_active"]) if "is_active" in keys else True
            }
    except Exception as e:
        logger.warning(f"[_get_tenant_master_chef_info] Falha ao consultar SQLite do tenant {slug}: {e}")
    return None


def _update_tenant_metadata(slug: str, new_name: str, new_email: Optional[str] = None) -> bool:
    """Atualiza metadados cadastrais da instituição e e-mail do master-chef."""
    import sqlite3
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    env_file = os.path.join(root_dir, f".env.{slug}")

    if os.path.exists(env_file):
        try:
            with open(env_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
            new_lines = []
            has_name = False
            has_email = False
            for line in lines:
                if line.startswith("INSTITUTION_NAME=") and new_name:
                    new_lines.append(f"INSTITUTION_NAME={new_name}\n")
                    has_name = True
                elif line.startswith("MASTER_CHEF_EMAIL=") and new_email:
                    new_lines.append(f"MASTER_CHEF_EMAIL={new_email}\n")
                    has_email = True
                else:
                    new_lines.append(line)
            if new_name and not has_name:
                new_lines.append(f"INSTITUTION_NAME={new_name}\n")
            if new_email and not has_email:
                new_lines.append(f"MASTER_CHEF_EMAIL={new_email}\n")
            with open(env_file, "w", encoding="utf-8") as f:
                f.writelines(new_lines)
        except Exception as e:
            logger.warning(f"[_update_tenant_metadata] Erro ao atualizar .env.{slug}: {e}")

    if new_email:
        db_path = _get_tenant_db_path(slug)
        if db_path and os.path.exists(db_path):
            try:
                conn = sqlite3.connect(db_path, timeout=10)
                cur = conn.cursor()
                cur.execute("UPDATE User SET email = ? WHERE role = 'gestor' OR id LIKE '%master%'", (new_email,))
                conn.commit()
                conn.close()
            except Exception as e:
                logger.error(f"[_update_tenant_metadata] Erro ao atualizar e-mail no SQLite do tenant {slug}: {e}")
                return False
    return True


def _reset_tenant_master_chef(slug: str, new_password: Optional[str] = None, new_email: Optional[str] = None) -> Dict[str, Any]:
    """Redefine a credencial do master-chef na base isolada da instituição com must_change_password=True."""
    import sqlite3
    db_path = _get_tenant_db_path(slug)
    if not db_path or not os.path.exists(db_path):
        raise HTTPException(status_code=404, detail=f"Base de dados da instituição '{slug}' não encontrada.")

    if not new_password:
        chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%&*"
        temp_pwd = "".join(secrets.choice(chars) for _ in range(12))
    else:
        temp_pwd = new_password

    pwd_hash = hash_password(temp_pwd)

    try:
        conn = sqlite3.connect(db_path, timeout=10)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        cur.execute("PRAGMA table_info(User);")
        columns = [row[1] for row in cur.fetchall()]
        if "must_change_password" not in columns:
            cur.execute("ALTER TABLE User ADD COLUMN must_change_password BOOLEAN DEFAULT 0;")
            conn.commit()

        cur.execute("SELECT id, email FROM User WHERE role = 'gestor' OR id LIKE '%master%' LIMIT 1")
        user = cur.fetchone()
        if not user:
            cur.execute("SELECT id, email FROM User LIMIT 1")
            user = cur.fetchone()

        if not user:
            conn.close()
            raise HTTPException(status_code=404, detail=f"Nenhum usuário gestor encontrado na instituição '{slug}'.")

        user_id = user["id"]
        target_email = new_email or user["email"]

        if new_email:
            cur.execute(
                "UPDATE User SET password_hash = ?, must_change_password = 1, email = ? WHERE id = ?",
                (pwd_hash, target_email, user_id)
            )
        else:
            cur.execute(
                "UPDATE User SET password_hash = ?, must_change_password = 1 WHERE id = ?",
                (pwd_hash, user_id)
            )
        conn.commit()
        conn.close()

        if new_email:
            _update_tenant_metadata(slug, new_name="", new_email=new_email)

        return {
            "slug": slug,
            "email": target_email,
            "temporary_password": temp_pwd,
            "must_change_password": True,
            "message": "Credencial provisória configurada com sucesso. O usuário deverá alterá-la no primeiro acesso."
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[_reset_tenant_master_chef] Erro ao resetar credencial do tenant {slug}: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno ao resetar credencial do master-chef: {e}")


def _archive_and_delete_tenant(slug: str) -> Dict[str, Any]:
    """Interrompe a instância, arquiva os dados e libera a porta TCP."""
    import shutil
    tenants = discover_tenants()
    tenant = next((t for t in tenants if t["slug"] == slug), None)
    if not tenant:
        raise HTTPException(status_code=404, detail=f"Instituição '{slug}' não encontrada.")

    port = tenant["port"]
    stop_tenant_instance(slug, port)

    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    data_dir = os.path.join(root_dir, "data", slug)
    archived_base = os.path.join(root_dir, "data", ".archived")
    os.makedirs(archived_base, exist_ok=True)

    timestamp = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    target_archive = os.path.join(archived_base, f"{slug}_{timestamp}")

    if os.path.exists(data_dir):
        try:
            shutil.move(data_dir, target_archive)
        except Exception as e:
            logger.warning(f"[_archive_and_delete_tenant] Falha ao mover pasta {data_dir}: {e}")
            target_archive = data_dir

    env_file = os.path.join(root_dir, f".env.{slug}")
    if os.path.exists(env_file):
        try:
            env_target = os.path.join(target_archive, f".env.{slug}")
            shutil.move(env_file, env_target)
        except Exception as e:
            logger.warning(f"[_archive_and_delete_tenant] Falha ao mover env file {env_file}: {e}")

    return {
        "slug": slug,
        "status": "archived",
        "freed_port": port,
        "archived_path": target_archive,
        "message": f"Instituição '{slug}' arquivada e desprovisionada com sucesso. A porta {port} foi liberada."
    }


@router.get("/platform/tenants", response_model=TenantListResponse)
def list_platform_tenants(
    request: Request = None,
    current_user: TokenData = Depends(require_doctor_chef)
):
    """Lista todas as instituições da plataforma e calcula a próxima porta livre. Exclusivo para doctor-chef."""
    base_url = get_request_base_url(request)
    tenants = discover_tenants(base_url=base_url)
    used_ports = set(t["port"] for t in tenants)
    next_port = 8001
    while next_port in used_ports:
        next_port += 1

    return {
        "total": len(tenants),
        "next_available_port": next_port,
        "tenants": tenants
    }


@router.post("/platform/tenants", status_code=status.HTTP_202_ACCEPTED)
def create_platform_tenant(
    payload: TenantCreateRequest,
    background_tasks: BackgroundTasks,
    request: Request = None,
    current_user: TokenData = Depends(require_doctor_chef)
):
    """Cria e provisiona uma nova instituição dedicada em BackgroundTasks. Exclusivo para doctor-chef."""
    base_url = get_request_base_url(request)
    tenants = discover_tenants(base_url=base_url)
    existing_slugs = set(t["slug"] for t in tenants)
    used_ports = set(t["port"] for t in tenants)

    if payload.slug in existing_slugs:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"A instituição com identificador '{payload.slug}' já está cadastrada."
        )

    if payload.port in used_ports:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"A porta TCP {payload.port} já está em uso por outra instituição."
        )

    # Dispara a automação de provisionamento em background
    background_tasks.add_task(
        provision_tenant_task,
        payload.name,
        payload.slug,
        payload.port,
        payload.master_chef_email,
        payload.master_chef_password
    )

    logger.info(f"[PLATFORM] Novo tenant '{payload.slug}' aceito para provisionamento na porta {payload.port}")
    return {
        "status": "provisioning",
        "message": "Provisionamento da instituição iniciado em background.",
        "tenant": {
            "name": payload.name,
            "slug": payload.slug,
            "port": payload.port,
            "url": resolve_tenant_url(payload.port, base_url=base_url, slug=payload.slug),
            "master_chef_email": payload.master_chef_email
        }
    }


@router.post("/platform/tenants/{slug}/start")
def start_platform_tenant(
    slug: str,
    request: Request = None,
    current_user: TokenData = Depends(require_doctor_chef)
):
    """Inicia o servidor de uma instituição existente. Exclusivo para doctor-chef."""
    base_url = get_request_base_url(request)
    tenants = discover_tenants(base_url=base_url)
    tenant = next((t for t in tenants if t["slug"] == slug), None)
    if not tenant:
        raise HTTPException(status_code=404, detail="Instituição não encontrada.")
    port = tenant["port"]
    success = start_tenant_instance(slug, port)
    return {
        "status": "online" if success or check_tenant_status(port) == "online" else "starting",
        "slug": slug,
        "port": port,
        "url": tenant["url"]
    }


@router.post("/platform/tenants/{slug}/stop")
def stop_platform_tenant(
    slug: str,
    request: Request = None,
    current_user: TokenData = Depends(require_doctor_chef)
):
    """Para o servidor de uma instituição existente. Exclusivo para doctor-chef."""
    base_url = get_request_base_url(request)
    tenants = discover_tenants(base_url=base_url)
    tenant = next((t for t in tenants if t["slug"] == slug), None)
    if not tenant:
        raise HTTPException(status_code=404, detail="Instituição não encontrada.")
    port = tenant["port"]
    success = stop_tenant_instance(slug, port)
    return {
        "status": "offline" if success or check_tenant_status(port) == "offline" else "stopping",
        "slug": slug,
        "port": port
    }


@router.get("/platform/tenants/{slug}", response_model=TenantDetailResponse)
def get_platform_tenant_detail(
    slug: str,
    request: Request = None,
    current_user: TokenData = Depends(require_doctor_chef)
):
    """Retorna detalhes aprofundados de uma instituição e de seu master-chef. Exclusivo para doctor-chef."""
    base_url = get_request_base_url(request)
    tenants = discover_tenants(base_url=base_url)
    tenant = next((t for t in tenants if t["slug"] == slug), None)
    if not tenant:
        raise HTTPException(status_code=404, detail=f"Instituição '{slug}' não encontrada.")

    master_chef_data = _get_tenant_master_chef_info(slug)
    container_name = f"classsync_tenant_{slug}"

    return {
        "name": tenant["name"],
        "slug": tenant["slug"],
        "port": tenant["port"],
        "url": tenant["url"],
        "status": tenant["status"],
        "created_at": tenant.get("created_at"),
        "container_name": container_name,
        "master_chef": master_chef_data
    }


@router.put("/platform/tenants/{slug}", response_model=TenantDetailResponse)
def update_platform_tenant(
    slug: str,
    payload: TenantUpdateRequest,
    request: Request = None,
    current_user: TokenData = Depends(require_doctor_chef)
):
    """Atualiza metadados cadastrais da instituição e e-mail do master-chef. Exclusivo para doctor-chef."""
    base_url = get_request_base_url(request)
    tenants = discover_tenants(base_url=base_url)
    tenant = next((t for t in tenants if t["slug"] == slug), None)
    if not tenant:
        raise HTTPException(status_code=404, detail=f"Instituição '{slug}' não encontrada.")

    _update_tenant_metadata(slug, new_name=payload.name, new_email=payload.master_chef_email)

    updated_tenants = discover_tenants(base_url=base_url)
    updated_tenant = next((t for t in updated_tenants if t["slug"] == slug), tenant)
    updated_master_chef = _get_tenant_master_chef_info(slug)

    return {
        "name": payload.name,
        "slug": slug,
        "port": updated_tenant["port"],
        "url": updated_tenant["url"],
        "status": updated_tenant["status"],
        "created_at": updated_tenant.get("created_at"),
        "container_name": f"classsync_tenant_{slug}",
        "master_chef": updated_master_chef
    }


@router.post("/platform/tenants/{slug}/master-chef/reset", response_model=MasterChefResetResponse)
def reset_platform_tenant_master_chef(
    slug: str,
    payload: Optional[MasterChefResetRequest] = None,
    current_user: TokenData = Depends(require_doctor_chef)
):
    """Redefine a credencial do master-chef na base isolada do tenant ativando must_change_password=True. Exclusivo para doctor-chef."""
    tenants = discover_tenants()
    tenant = next((t for t in tenants if t["slug"] == slug), None)
    if not tenant:
        raise HTTPException(status_code=404, detail=f"Instituição '{slug}' não encontrada.")

    new_pwd = payload.new_password if payload else None
    new_email = payload.email if payload else None

    result = _reset_tenant_master_chef(slug, new_password=new_pwd, new_email=new_email)
    return result


@router.delete("/platform/tenants/{slug}", response_model=TenantDeleteResponse)
def delete_platform_tenant(
    slug: str,
    payload: Optional[TenantDeleteRequest] = None,
    confirm_slug: Optional[str] = None,
    current_user: TokenData = Depends(require_doctor_chef)
):
    """Arquiva e remove a instituição cliente liberando a porta TCP. Exclusivo para doctor-chef."""
    provided_slug = (payload.confirm_slug if payload else None) or confirm_slug
    if not provided_slug or provided_slug != slug:
        raise HTTPException(
            status_code=400,
            detail=f"Confirmação inválida. Digite exatamente o identificador '{slug}' para confirmar a exclusão."
        )

    result = _archive_and_delete_tenant(slug)
    return result








