# Delta no Modelo de Dados: Realocação Departamental de Disciplinas

> Feature: `012-realocacao-disciplinas-dept`
> Data: `2026-08-10`

---

## 1. Resumo das Alterações de Dados

Esta feature não altera a estrutura de tabelas relacionais do banco SQLite/PostgreSQL nem exige migrações DDL de colunas (as tabelas `teachers` e `allocations` já suportam `subjects` em JSON e `subject` em VARCHAR a partir dos adendos `009` e `011`).

As alterações são estritamente **operações DML / mutações de estado de dados**:

## 2. Entidades Mapeadas e Mutações

### 2.1 Entidade `Teacher` (`src/models.py`)
- **Campo `subjects` (JSON):**
  - **Doador (`source_teacher`):** Remoção das disciplinas especificadas na requisição. Caso a lista fique vazia, adição da `replacement_subject`.
  - **Receptor (`target_teacher`):** Inclusão das disciplinas transferidas (garantindo união sem duplicatas e limite máximo de 6 disciplinas).

### 2.2 Entidade `Allocation` (`src/models.py`)
- **Campo `teacher_id` (String):**
  - Alocações cuja `subject` corresponda a uma das disciplinas transferidas e cujo `teacher_id` seja o `source_teacher_id` têm seu `teacher_id` atualizado para `target_teacher_id`.
- **Campo `status` (String):**
  - Caso a reatribuição para `target_teacher_id` fira restrição de indisponibilidade ou limite de 4 aulas seguidas no mesmo turno, o `status` é alterado para `"pending_arbitration"`.

## 3. Validações de Consistência e Constraints de Negócio

| Entidade | Regra / Constraint | Comportamento de Erro |
|----------|-------------------|-----------------------|
| `Teacher` | `source.department == target.department` | Retorna HTTP `422 Unprocessable Entity` se divergente |
| `Teacher` | `len(target.subjects) <= 6` | Retorna HTTP `422 Unprocessable Entity` se exceder 6 |
| `Teacher` | `len(source.subjects) >= 1` | Retorna HTTP `422 Unprocessable Entity` se ficar com 0 sem `replacement_subject` |
