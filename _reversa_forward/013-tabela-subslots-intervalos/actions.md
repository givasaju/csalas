# Actions: Tabela de Subslots com Intervalos de Aula

> Identificador: `013-tabela-subslots-intervalos`
> Data: `2026-08-11`
> Roadmap: `_reversa_forward/013-tabela-subslots-intervalos/roadmap.md`

---

## Resumo

| Métrica | Valor |
|---------|-------|
| Total de ações | 7 |
| Paralelizáveis (`[//]`) | 4 |
| Maior cadeia de dependência | 5 |

---

## Fase 1, Preparação

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T001 | Definir os schemas Pydantic `SubslotCreate`, `SubslotUpdate` e `SubslotResponse` em `src/api/schemas.py` | - | `[//]` | `src/api/schemas.py` | 🟢 | `[x]` |
| T002 | Adicionar DDL de criação da tabela `subslot_time_intervals` e a carga inicial (seed SQL) dos 18 subslots em `db/migrations.sql` | - | `[//]` | `db/migrations.sql` | 🟢 | `[x]` |

---

## Fase 2, Testes

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T003 | Criar arquivo de testes automatizados `tests/test_subslot_time_intervals.py` com cenários de listagem `GET`, filtro por turno, criação `POST` e validação de sobreposição | T001 | `[//]` | `tests/test_subslot_time_intervals.py` | 🟢 | `[x]` |

---

## Fase 3, Núcleo

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T004 | Implementar repositório e estrutura de dados de persistência da tabela `subslot_time_intervals` com semente padrão em `src/api/worker.py` | T001, T002 | - | `src/api/worker.py` | 🟢 | `[x]` |
| T005 | Implementar os endpoints REST API (`GET`, `POST`, `PUT`, `DELETE /api/v1/subslots`) em `src/api/routes.py` | T004 | - | `src/api/routes.py` | 🟢 | `[x]` |

---

## Fase 4, Integração

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T006 | Mapear códigos de subslots (`M1`..`M5`, `T1`..`T5`, `N1`..`N5`) para interoperabilidade com validação de restrições docentes em `src/api/routes.py` | T005 | - | `src/api/routes.py` | 🟢 | `[x]` |

---

## Fase 5, Polimento

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T007 | Adicionar logs de auditoria estruturados `[SUBSLOT_MANAGEMENT]` e executar validação final da suíte com `pytest` | T003, T006 | `[//]` | `tests/test_subslot_time_intervals.py` | 🟢 | `[x]` |

---

## Notas de execução

Todas as 7 ações T001 a T007 concluídas e validadas com 100% de aprovação na suíte automatizada pytest (59 testes passando).

---

## Histórico de alterações

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-08-11 | Versão inicial gerada por `/reversa-to-do` | reversa |
| 2026-08-11 | Conclusão e validação de todas as ações T001-T007 | reversa |
