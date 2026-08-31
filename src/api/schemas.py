from pydantic import BaseModel, Field
from typing import List, Optional

class RoomCreate(BaseModel):
    block_id: str = Field(..., min_length=1, description="O ID/Nome do bloco predial é obrigatório.")
    name: str = Field(..., min_length=1, description="O nome da sala de aula é obrigatório.")
    capacity: int = Field(..., gt=0, description="A capacidade física de alunos deve ser maior do que zero.")
    room_type: str = Field(..., description="Tipo de sala (common, lab, auditorium).")
    is_accessible: bool = Field(default=True, description="Flag indicando acessibilidade física.")
    features: List[str] = Field(default=[], description="Lista de recursos extras disponíveis.")


class RestrictionCreate(BaseModel):
    teacher_id: str = Field(..., min_length=1, description="O ID do professor é obrigatório.")
    day_of_week: int = Field(..., ge=1, le=7, description="O dia da semana deve ser de 1 (Segunda) a 7 (Domingo).")
    time_slot_id: str = Field(..., description="ID da faixa de horário (M1..M6, T1..T6, N1..N6).")


class TeacherCreate(BaseModel):
    id: str = Field(..., min_length=1, description="Matrícula / ID do docente é obrigatório.")
    name: str = Field(..., min_length=1, description="Nome completo do docente é obrigatório.")
    department: str = Field(default="Geral", description="Departamento ou área acadêmica do docente.")
    subjects: List[str] = Field(..., min_length=1, max_length=6, description="Lista de disciplinas lecionáveis (de 1 a 6 disciplinas).")


class TeacherResponse(BaseModel):
    id: str
    name: str
    department: str
    email: Optional[str] = None
    subjects: List[str] = []



from typing import List, Optional

class AllocationCreate(BaseModel):
    teacher_id: str = Field(..., min_length=1, description="ID do docente é obrigatório.")
    room_id: str = Field(..., min_length=1, description="ID da sala física é obrigatório.")
    day_of_week: int = Field(..., ge=1, le=7, description="Dia da semana (1 - Segunda a 7 - Domingo).")
    shift: str = Field(..., description="Turno de alocação (M, T, N).")
    sub_slot: int = Field(..., ge=1, le=6, description="Número da aula de 50 min no turno (1 a 6).")
    subject: Optional[str] = Field(None, description="Disciplina que será lecionada no subslot.")


class AllocationResponse(BaseModel):
    id: str
    teacher_id: str
    room_id: str
    day_of_week: int
    shift: str
    sub_slot: int
    subject: Optional[str] = None
    created_at: str


class ReallocateSubjectsRequest(BaseModel):
    source_teacher_id: str = Field(..., min_length=1, description="ID do docente doador de origem é obrigatório.")
    target_teacher_id: str = Field(..., min_length=1, description="ID do docente receptor de destino é obrigatório.")
    subjects: List[str] = Field(..., min_length=1, description="Lista de disciplinas a transferir.")
    replacement_subject: Optional[str] = Field(None, description="Disciplina substituta caso o doador fique com 0 matérias.")


class ReallocateSubjectsResponse(BaseModel):
    department: str
    source_teacher: TeacherResponse
    target_teacher: TeacherResponse
    migrated_allocations_count: int = 0
    pending_arbitration_allocations_count: int = 0
    message: str


class SubslotCreate(BaseModel):
    code: str = Field(..., min_length=1, max_length=10, description="Código de referência única (ex: M1, M_INT, T1).")
    shift: str = Field(..., description="Turno acadêmico (matutino, vespertino, noturno).")
    class_number: Optional[int] = Field(None, ge=1, le=10, description="Número da aula de 1 a 10 (nulo se for intervalo).")
    start_time: str = Field(..., description="Horário de início HH:MM.")
    end_time: str = Field(..., description="Horário de término HH:MM.")
    is_interval: bool = Field(default=False, description="Flag indicando se o subslot é um intervalo de descanso.")


class SubslotUpdate(BaseModel):
    code: Optional[str] = Field(None, min_length=1, max_length=10)
    shift: Optional[str] = None
    class_number: Optional[int] = Field(None, ge=1, le=10)
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    is_interval: Optional[bool] = None


class SubslotResponse(BaseModel):
    id: str
    code: str
    shift: str
    class_number: Optional[int] = None
    start_time: str
    end_time: str
    is_interval: bool


class EmergencyReallocationRequest(BaseModel):
    absent_teacher_id: str = Field(..., min_length=1, description="ID do docente ausente.")
    start_date: str = Field(..., description="Data inicial do afastamento (YYYY-MM-DD).")
    end_date: str = Field(..., description="Data final do afastamento (YYYY-MM-DD).")
    mode: str = Field(default="assisted", description="Modo de operação ('assisted' ou 'delegated').")


class ProposedSubstitution(BaseModel):
    class_id: str = Field(..., description="ID da turma/disciplina afetada.")
    class_name: Optional[str] = Field(None, description="Nome legível da disciplina.")
    day_of_week: Optional[int] = Field(None, description="Dia da semana (1-7).")
    shift: Optional[str] = Field(None, description="Turno ('M', 'T', 'N').")
    sub_slot: Optional[int] = Field(None, description="Sub-slot de horário (1-5).")
    substitute_teacher_id: str = Field(..., description="ID do docente substituto.")
    substitute_teacher_name: str = Field(..., description="Nome do docente substituto.")
    time_slot: str = Field(..., description="Slot de horário de aula.")
    room_id: Optional[str] = Field(None, description="ID da sala alocada.")


class EmergencyReallocationOption(BaseModel):
    option_index: int = Field(..., description="Índice da alternativa (1, 2, 3).")
    impact_score: float = Field(..., description="Pontuação de menor impacto (quanto menor, mais isolado).")
    description: str = Field(..., description="Descrição resumida do plano de substituição.")
    expanded_coordinations: bool = Field(default=False, description="Flag indicando se envolveu professores de outras coordenações.")
    substitutions: List[ProposedSubstitution] = Field(default=[], description="Lista de substituições propostas.")


class EmergencyReallocationCalculateResponse(BaseModel):
    absent_teacher_id: str
    total_affected_classes: int
    options: List[EmergencyReallocationOption]


class EmergencyReallocationCommitRequest(BaseModel):
    absent_teacher_id: str = Field(..., min_length=1, description="ID do docente ausente.")
    selected_option_index: int = Field(..., description="Índice da alternativa selecionada.")
    mode: str = Field(default="assisted", description="Modo de homologação ('assisted' ou 'delegated').")
    substitutions: List[ProposedSubstitution] = Field(..., description="Lista de substituições a efetivar.")


class EmergencyReallocationCommitResponse(BaseModel):
    log_id: str
    status: str
    mode_used: str
    message: str


class UserRegisterRequest(BaseModel):
    name: str = Field(..., min_length=2, description="Nome completo do usuário.")
    email: str = Field(..., min_length=5, description="E-mail institucional do usuário.")
    password: str = Field(..., min_length=4, description="Senha de acesso.")
    department: Optional[str] = Field(default="Geral", description="Departamento acadêmico do usuário.")


class UserLoginRequest(BaseModel):
    email: str = Field(..., min_length=3, description="E-mail do usuário.")
    password: str = Field(..., min_length=1, description="Senha do usuário.")


class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    role: str
    department: str
    is_active: bool
    created_at: Optional[str] = None


class UserStatusUpdateRequest(BaseModel):
    is_active: Optional[bool] = None
    role: Optional[str] = None


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse





