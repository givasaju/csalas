# Data Delta: Cadastro de Disciplinas Lecionáveis por Docente

> Identificador: `009-disciplinas-docentes`
> Data: `2026-08-09`
> Artefato base: `_reversa_sdd/architecture.md#3-modelo-de-entidade-relacionamento-erd`

---

## 1. Alterações no Modelo de Dados (`src/models.py`)

### Tabela `Teacher`

```diff
 class Teacher(Base):
     __tablename__ = 'Teacher'
     id = Column(String, primary_key=True)
     name = Column(String, nullable=False)
     department = Column(String, default="Geral")
     email = Column(String, nullable=True)
+    subjects = Column(JSON, default=list)
```

- **Novo campo:** `subjects`
- **Tipo:** `JSON` (Armazena array de strings JSON, ex.: `["Cálculo I", "Álgebra Linear"]`)
- **Valor Padrão:** `[]` (Array JSON vazio)
- **Nullability:** Falso / Valor Padrão `list`

---

## 2. Alterações nos Schemas Pydantic (`src/api/schemas.py`)

### Class `TeacherCreate`

```python
class TeacherCreate(BaseModel):
    id: str = Field(..., min_length=1, description="Matrícula / ID do docente é obrigatório.")
    name: str = Field(..., min_length=1, description="Nome completo do docente é obrigatório.")
    department: str = Field(default="Geral", description="Departamento ou área acadêmica do docente.")
    subjects: List[str] = Field(..., min_items=1, description="Lista de disciplinas lecionáveis (pelo menos 1).")
```

### Class `TeacherResponse`

```python
class TeacherResponse(BaseModel):
    id: str
    name: str
    department: str
    email: Optional[str] = None
    subjects: List[str]
```

---

## 3. Armazenamento em Memória (`src/api/worker.py` / `db_teachers`)

A estrutura em memória armazena o dicionário representando o docente:

```json
{
  "id": "DOC-101",
  "name": "Prof. Carlos",
  "department": "Engenharia",
  "email": "carlos@universidade.edu.br",
  "subjects": ["Cálculo I", "Álgebra Linear"]
}
```

---

## 4. Migração e Compatibilidade

Não é necessária migração DDL de banco relacional para o cenário em memória. No caso de inicialização de docentes sem a chave `subjects`, o getter aplicará fallback para `[]`.
