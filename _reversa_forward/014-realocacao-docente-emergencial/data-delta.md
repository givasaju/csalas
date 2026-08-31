# Data Delta: Realocação Docente Emergencial

> Identificador: `014-realocacao-docente-emergencial`
> Data: `2026-08-13`
> Roadmap: `_reversa_forward/014-realocacao-docente-emergencial/roadmap.md`

---

## 1. Visão Geral

Este documento descreve as alterações no esquema de dados e modelos da API para suportar a funcionalidade de realocação emergencial de docentes.

---

## 2. Alterações na Base de Dados (SQL DDL em `db/migrations.sql`)

### 2.1 Tabela `emergency_reallocation_logs` (Nova)

Armazena o registro de auditoria e status de cada realocação emergencial acionada.

```sql
CREATE TABLE IF NOT EXISTS emergency_reallocation_logs (
    id VARCHAR(36) PRIMARY KEY,
    absent_teacher_id VARCHAR(50) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    mode VARCHAR(20) NOT NULL, -- 'assisted' | 'delegated'
    selected_option_index INT,
    affected_classes_count INT NOT NULL,
    expanded_coordinations BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(100) DEFAULT 'coordinative_user',
    FOREIGN KEY (absent_teacher_id) REFERENCES teachers(id)
);
```

### 2.2 Tabela `emergency_reallocation_details` (Nova)

Armazena as atribuições específicas de cada turma afetada na realocação.

```sql
CREATE TABLE IF NOT EXISTS emergency_reallocation_details (
    id VARCHAR(36) PRIMARY KEY,
    log_id VARCHAR(36) NOT NULL,
    class_id VARCHAR(50) NOT NULL,
    substitute_teacher_id VARCHAR(50) NOT NULL,
    time_slot VARCHAR(20) NOT NULL,
    room_id VARCHAR(36),
    FOREIGN KEY (log_id) REFERENCES emergency_reallocation_logs(id),
    FOREIGN KEY (class_id) REFERENCES classes(id),
    FOREIGN KEY (substitute_teacher_id) REFERENCES teachers(id)
);
```

---

## 3. Novos Schemas Pydantic (`src/api/schemas.py`)

```python
class EmergencyReallocationRequest(BaseModel):
    absent_teacher_id: str
    start_date: str
    end_date: str
    mode: str = "assisted" # "assisted" | "delegated"

class ProposedSubstitution(BaseModel):
    class_id: str
    substitute_teacher_id: str
    substitute_teacher_name: str
    time_slot: str
    room_id: Optional[str] = None

class EmergencyReallocationOption(BaseModel):
    option_index: int
    impact_score: float
    description: str
    expanded_coordinations: bool = False
    substitutions: List[ProposedSubstitution]

class EmergencyReallocationCalculateResponse(BaseModel):
    absent_teacher_id: str
    total_affected_classes: int
    options: List[EmergencyReallocationOption]

class EmergencyReallocationCommitRequest(BaseModel):
    absent_teacher_id: str
    selected_option_index: int
    mode: str  # "assisted" | "delegated"
    substitutions: List[ProposedSubstitution]

class EmergencyReallocationCommitResponse(BaseModel):
    log_id: str
    status: str
    mode_used: str
    message: str
```
