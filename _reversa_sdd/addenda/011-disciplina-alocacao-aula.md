# Addendum 011: Seleção de Disciplina na Alocação de Aulas por Subslot

> Data de sincronização: `2026-08-09`  
> Origem: `_reversa_forward/011-disciplina-alocacao-aula/`  

---

## 1. Contexto da Evolução

Implementada a seleção e exibição da disciplina lecionada no formulário e na tabela de alocações de aulas por subslot (50 min), vinculada estritamente ao rol de disciplinas lecionáveis cadastradas para o docente.

---

## 2. Resumo da Entrega

- **`src/models.py` & `src/database.py`**:
  - Adicionado o campo `subject = Column(String, nullable=True)` à entidade `Allocation`.
  - Adicionada migração inline `ALTER TABLE Allocation ADD COLUMN subject VARCHAR` para compatibilidade com o SQLite.
- **`src/api/schemas.py`**:
  - Atualizados os Pydantic schemas `AllocationCreate` e `AllocationResponse` com o atributo opcional `subject`.
- **`src/api/routes.py`**:
  - Em `POST /api/v1/allocations`, implementada a validação do campo `subject`. Caso fornecida, a API garante que pertença ao rol do professor (`teacher.subjects`), retornando HTTP `422 Unprocessable Entity` se for inválida. Se omitida, assume a 1ª disciplina do docente.
  - Em `GET /api/v1/allocations`, incluída a propriedade `subject` no JSON de resposta.
- **`src/api/static/index.html`**:
  - Incluído o campo `<select id="allocSubject">` no formulário de alocação de aulas.
  - Implementada a função JS `updateAllocSubjectOptions()` que atualiza dinamicamente as disciplinas disponíveis sempre que um professor é selecionado.
  - Adicionada a coluna **"Disciplina"** com badge em destaque na tabela de alocações ativas no campus.
- **`tests/test_allocations_api.py`**:
  - Adicionados testes automatizados `test_create_allocation_with_subject_flow` validando alocações com disciplinas válidas e rejeição com erro 422 para disciplinas fora do rol, executados com 100% de aprovação (6/6 testes).
