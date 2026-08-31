# Delta no Modelo de Dados: Alocações e Limite de Aulas Consecutivas

> Identificador da feature: `008-alocacao-docente-max-4-aulas`  
> Data: `2026-08-08`  

---

## 1. Nova Tabela: `Allocation`

Criação da tabela física/relacional `Allocation` em `src/models.py` para armazenar as alocações pontuais de aulas de 50 minutos.

```python
class Allocation(Base):
    __tablename__ = 'Allocation'
    id = Column(String, primary_key=True)  # UUID
    teacher_id = Column(String, ForeignKey('Teacher.id'), nullable=False)
    room_id = Column(String, ForeignKey('Room.id'), nullable=False)
    day_of_week = Column(Integer, nullable=False)  # 1 (Segunda) a 7 (Domingo)
    shift = Column(String, nullable=False)  # 'M', 'T', 'N'
    sub_slot = Column(Integer, nullable=False)  # 1, 2, 3, 4, 5 (períodos de 50 min)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
```

---

## 2. DTOs e Schemas Pydantic (`src/api/schemas.py`)

### AllocationCreate
- `teacher_id` (str, obrigatório): ID do docente.
- `room_id` (str, obrigatório): ID da sala física.
- `day_of_week` (int, obrigatório): Dia da semana (1 a 7).
- `shift` (str, obrigatório): Turno (`M`, `T`, `N`).
- `sub_slot` (int, obrigatório): Número da aula de 50 min no turno (1 a 5).

### AllocationResponse
- `id` (str): UUID da alocação.
- `teacher_id` (str): ID do docente.
- `room_id` (str): ID da sala física.
- `day_of_week` (int): Dia da semana.
- `shift` (str): Turno.
- `sub_slot` (int): Número da aula.
- `created_at` (str): Data/hora de criação em ISO 8601.

---

## 3. Regras de Integridade e Índices

- Índice composto de unicidade parcial: `(room_id, day_of_week, shift, sub_slot)` para impedir que a mesma sala seja ocupada por duas turmas/professores no mesmo sub-slot de 50 minutos.
