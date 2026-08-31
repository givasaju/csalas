# Actions: Realocação Docente Emergencial

> Identificador: `014-realocacao-docente-emergencial`
> Data: `2026-08-13`
> Roadmap: `_reversa_forward/014-realocacao-docente-emergencial/roadmap.md`

## Resumo

| Métrica | Valor |
|---------|-------|
| Total de ações | 8 |
| Paralelizáveis (`[//]`) | 4 |
| Maior cadeia de dependência | 5 |

---

## Fase 1, Preparação

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T001 | Definir os schemas Pydantic de realocação emergencial (`EmergencyReallocationRequest`, `ProposedSubstitution`, `EmergencyReallocationOption`, `EmergencyReallocationCalculateResponse`, `EmergencyReallocationCommitRequest`, `EmergencyReallocationCommitResponse`) em `src/api/schemas.py` | - | `[//]` | `src/api/schemas.py` | 🟢 | `[x]` |
| T002 | Adicionar o DDL de criação das tabelas `emergency_reallocation_logs` e `emergency_reallocation_details` em `db/migrations.sql` | - | `[//]` | `db/migrations.sql` | 🟢 | `[x]` |

---

## Fase 2, Testes

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T003 | Criar arquivo de testes automatizados `tests/test_emergency_reallocation.py` com cenários de cálculo de alternativas, expansão para coordenações correlatas, efetivação assistida e efetivação delegada | T001, T002 | `[//]` | `tests/test_emergency_reallocation.py` | 🟢 | `[x]` |

---

## Fase 3, Núcleo

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T004 | Implementar a estrutura de persistência e leitura das tabelas de realocação emergencial em `src/api/worker.py` | T001, T002 | - | `src/api/worker.py` | 🟢 | `[x]` |
| T005 | Implementar o método `calculate_emergency_reallocation` no `CoreAllocationEngine` (`src/engine/core.py`) com ranqueamento por menor impacto e suporte a busca expandida em coordenações correlatas | T004 | - | `src/engine/core.py` | 🟢 | `[x]` |
| T006 | Criar os endpoints HTTP REST API `POST /api/v1/emergency-reallocations/calculate` e `POST /api/v1/emergency-reallocations/commit` em `src/api/routes.py` | T005 | - | `src/api/routes.py` | 🟢 | `[x]` |

---

## Fase 4, Integração

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T007 | Implementar a interface visual de realocação emergencial no `occupancy-dashboard` com suporte ao seletor de modo (Assistido vs. Delegado) em `src/api/static/index.html` | T006 | - | `src/api/static/index.html` | 🟢 | `[x]` |

---

## Fase 5, Polimento

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T008 | Adicionar logs de auditoria estruturados `[EMERGENCY_REALLOCATION]` e executar a validação final da suíte de testes com `pytest` | T003, T007 | `[//]` | `tests/test_emergency_reallocation.py` | 🟢 | `[x]` |

---

## Notas de execução

Todas as 8 ações T001 a T008 foram concluídas e validadas com 100% de sucesso na suíte de testes automatizados `pytest` (61 testes passando sem regressões).

---

## Histórico de alterações

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-08-13 | Versão inicial gerada por `/reversa-to-do` | reversa |
| 2026-08-13 | Conclusão de todas as tarefas T001-T008 por `/reversa-coding` | reversa |
