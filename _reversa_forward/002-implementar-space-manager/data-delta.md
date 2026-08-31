# Data Delta: academic-space-manager

Este documento detalha o mapeamento conceitual das estruturas de dados adicionadas ou alteradas para suportar a funcionalidade de gerenciamento acadêmico e predial.

---

## 1. Estruturas Pydantic (Validação de Input)

### Model `RoomCreate` (Salas)
```python
class RoomCreate(BaseModel):
    block_id: str
    name: str
    capacity: int = Field(gt=0, description="A capacidade de alunos deve ser maior do que zero.")
    room_type: str  # common, lab, auditorium
    is_accessible: bool
    features: List[str] = []
```

### Model `RestrictionCreate` (Indisponibilidade)
```python
class RestrictionCreate(BaseModel):
    teacher_id: str
    day_of_week: int = Field(ge=1, le=7, description="O dia da semana deve ser de 1 (Segunda) a 7 (Domingo).")
    time_slot_id: str  # M1, M2, T1, T2, N1, N2
```

---

## 2. Tabelas em Memória (Estrutura de Persistência no backend)

As coleções em memória gerenciadas pelo repositório em `worker.py` serão estruturadas em dicionários globais:

```python
db_rooms: List[Dict[str, Any]] = [
    # { "id": "uuid", "block_id": "Bloco A", "name": "Sala A1", "capacity": 50, ... }
]

db_teachers: List[Dict[str, Any]] = [
    # { "id": "uuid", "name": "Claudio", "email": "claudio@school.edu" }
]

db_restrictions: List[Dict[str, Any]] = [
    # { "id": "uuid", "teacher_id": "uuid", "day_of_week": 1, "time_slot_id": "M1" }
]
```

---

## 3. Comportamento das Restrições na Remoção de Dados

*   **Integridade Referencial:** Tentativas de deletar salas ou professores que possuam referências ativas em tarefas de alocação finalizadas ou em execução retornarão erros de conflito (HTTP 409).
*   **Limpeza Automática:** Uma API de controle predial permitirá disparar a limpeza de restrições de indisponibilidades horárias ao final de cada período letivo, efetuando o reset do array `db_restrictions = []`.
