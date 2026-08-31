# Actions: Seleção de Disciplina na Alocação de Aulas por Subslot

> Identificador: `011-disciplina-alocacao-aula`  
> Data: `2026-08-09`  
> Roadmap: `_reversa_forward/011-disciplina-alocacao-aula/roadmap.md`  

---

## Resumo

| Métrica | Valor |
|---------|-------|
| Total de ações | 5 |
| Paralelizáveis (`[//]`) | 2 |
| Maior cadeia de dependência | 4 |

---

## Fase 1, Preparação

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T001 | Atualizar o modelo `Allocation` em `src/models.py` e adicionar migração de coluna em `src/database.py` | - | - | `src/models.py`, `src/database.py` | 🟢 | `[x]` |
| T002 | Atualizar os schemas `AllocationCreate` e `AllocationResponse` em `src/api/schemas.py` | T001 | `[//]` | `src/api/schemas.py` | 🟢 | `[x]` |

---

## Fase 2, Núcleo

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T003 | Atualizar rotas `POST /api/v1/allocations` e `GET /api/v1/allocations` em `src/api/routes.py` para validar e persistir `subject` | T002 | - | `src/api/routes.py` | 🟢 | `[x]` |
| T004 | Atualizar interface SPA `src/api/static/index.html` com select de disciplina dinâmico por professor e coluna de disciplina na tabela | T003 | `[//]` | `src/api/static/index.html` | 🟢 | `[x]` |

---

## Fase 3, Polimento

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T005 | Atualizar e executar suíte de testes automatizados com `pytest` em `tests/test_allocations_api.py` | T004 | - | `tests/test_allocations_api.py` | 🟢 | `[x]` |

---

## Histórico de alterações

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-08-09 | Versão inicial gerada por `/reversa-to-do` | reversa |
| 2026-08-09 | Conclusão de todas as ações T001 a T005 | reversa |
