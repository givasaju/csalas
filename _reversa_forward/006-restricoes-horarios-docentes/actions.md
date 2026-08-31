# Actions: Gestão de Restrições de Horários por Professor e Alertas de Conflitos

> Identificador: `006-restricoes-horarios-docentes`  
> Data: `2026-08-08`  
> Roadmap: `_reversa_forward/006-restricoes-horarios-docentes/roadmap.md`  

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
| T001 | Criar fixtures e helpers de teste para restrições horárias docentes | - | `[//]` | `tests/conftest.py` | 🟢 | `[X]` |

---

## Fase 2, Testes

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T002 | Criar testes automatizados para a rota `GET /api/v1/teachers/{teacher_id}/restrictions` | T001 | `[//]` | `tests/test_restrictions.py` | 🟢 | `[X]` |
| T003 | Criar testes automatizados para a rota `DELETE /api/v1/allocation/restrictions/{restriction_id}` | T002 | - | `tests/test_restrictions.py` | 🟢 | `[X]` |
| T004 | Criar teste de integração para o motor de IA validando Hard Constraint de indisponibilidade docente | T001 | `[//]` | `tests/test_engine_restrictions.py` | 🟢 | `[X]` |

---

## Fase 3, Núcleo

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T005 | Implementar o endpoint `GET /api/v1/teachers/{teacher_id}/restrictions` no backend FastAPI | T001 | - | `src/api/routes.py` | 🟢 | `[X]` |
| T006 | Implementar o endpoint `DELETE /api/v1/allocation/restrictions/{restriction_id}` no backend | T005 | - | `src/api/routes.py` | 🟢 | `[X]` |
| T007 | Incorporar o filtro de restrição docente como Hard Constraint no loop de alocação do motor de IA | T001 | - | `src/engine/core.py` | 🟢 | `[X]` |

---

## Fase 4, Integração

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T008 | Integrar matriz gráfica interativa de indisponibilidade docente (Seg-Dom × M1-N2) na SPA web | T005, T006 | - | `src/api/static/index.html` | 🟡 | `[X]` |

---

## Fase 5, Polimento

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T009 | Adicionar rotinas de log estruturado para exclusões de restrições e rejeições pelo motor de IA | T006, T007 | `[//]` | `src/api/routes.py` | 🟢 | `[X]` |

---

## Notas de execução

Nenhuma observação no momento.

---

## Histórico de alterações

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-08-08 | Versão inicial gerada por `/reversa-to-do` | reversa |
