# Actions: Entrada de Alocação de Aulas Docentes (50 min) e Limite de 4 Aulas Consecutivas

> Identificador: `008-alocacao-docente-max-4-aulas`  
> Data: `2026-08-08`  
> Roadmap: `_reversa_forward/008-alocacao-docente-max-4-aulas/roadmap.md`  

---

## Resumo

| Métrica | Valor |
|---------|-------|
| Total de ações | 9 |
| Paralelizáveis (`[//]`) | 4 |
| Maior cadeia de dependência | 5 |

---

## Fase 1, Preparação

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T001 | Adicionar tabela `Allocation` em `src/models.py` e schemas Pydantic `AllocationCreate` e `Response` em `src/api/schemas.py` | - | `[//]` | `src/models.py` | 🟢 | `[X]` |
| T002 | Criar fixtures de docentes, salas e sub-slots de aula em `tests/conftest.py` | - | `[//]` | `tests/conftest.py` | 🟢 | `[X]` |

---

## Fase 2, Testes

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T003 | Criar testes automatizados para `POST`, `GET` e `DELETE /api/v1/allocations` e rejeição de >4 aulas seguidas no mesmo turno | T001, T002 | `[//]` | `tests/test_allocations_api.py` | 🟢 | `[X]` |

---

## Fase 3, Núcleo

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T004 | Implementar algoritmo de janela deslizante `check_consecutive_limit` em `src/api/allocation_validator.py` | T001 | - | `src/api/allocation_validator.py` | 🟢 | `[X]` |
| T005 | Implementar os endpoints REST `POST`, `GET` e `DELETE /api/v1/allocations` em `src/api/routes.py` | T004 | - | `src/api/routes.py` | 🟢 | `[X]` |
| T006 | Incorporar a verificação de no máximo 4 aulas seguidas por turno como Hard Constraint no loop do motor de IA | T004 | - | `src/engine/core.py` | 🟢 | `[X]` |

---

## Fase 4, Integração

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T007 | Integrar aba "Alocação de Aulas" e formulário interativo de sub-slots (1..5) de 50 min na SPA web | T005 | - | `src/api/static/index.html` | 🟢 | `[X]` |
| T008 | Adicionar estilos visuais e avisos de limite de aulas consecutivas em `src/api/static/index.css` | T007 | - | `src/api/static/index.css` | 🟢 | `[X]` |

---

## Fase 5, Polimento

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T009 | Adicionar logs estruturados para auditoria de alocações e rejeições de 5ª aula seguida | T005 | `[//]` | `src/api/routes.py` | 🟢 | `[X]` |

---

## Notas de execução

Nenhuma observação no momento.

---

## Histórico de alterações

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-08-08 | Versão inicial gerada por `/reversa-to-do` | reversa |
