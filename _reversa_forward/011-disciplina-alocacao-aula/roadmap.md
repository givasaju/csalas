# Roadmap: Seleção de Disciplina na Alocação de Aulas por Subslot

> Identificador: `011-disciplina-alocacao-aula`  
> Data: `2026-08-09`  
> Requirements: `_reversa_forward/011-disciplina-alocacao-aula/requirements.md`  

---

## 1. Arquitetura da solução

Expandir a entidade `Allocation` e o ecossistema de rotas e interface SPA do ClassSync AI para suportar a escolha e exibição da disciplina lecionada no subslot.

---

## 2. Componentes afetados

1. `src/models.py` & `src/database.py`:
   - Adicionar o atributo `subject = Column(String, nullable=True)` à classe `Allocation`.
   - Adicionar migração inline no SQLite para garantir a presença da coluna `subject`.
2. `src/api/schemas.py`:
   - Adicionar `subject: Optional[str] = None` aos schemas `AllocationCreate` e `AllocationResponse`.
3. `src/api/routes.py`:
   - Em `create_allocation`, validar se a disciplina selecionada pertence ao docente e salvá-la.
   - Em `list_allocations`, incluir `subject` no dicionário de resposta.
4. `src/api/static/index.html`:
   - Incluir campo de seleção `<select id="allocSubject">` no formulário de alocação de aula.
   - Adicionar ouvinte de evento no select de professores para popular dinamicamente as disciplinas lecionáveis daquele professor.
   - Adicionar a coluna **"Disciplina"** na tabela de alocações.
5. `tests/test_allocations_api.py`:
   - Atualizar e adicionar testes validando alocações com disciplinas.
