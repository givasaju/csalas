# Actions: Implementar o gerenciador acadêmico academic-space-manager

> Identificador: `002-implementar-space-manager`  
> Data: `2026-08-07`  
> Roadmap: `_reversa_forward/002-implementar-space-manager/roadmap.md`  

---

## Resumo

| Métrica | Valor |
|---------|-------|
| Total de ações | 13 |
| Paralelizáveis (`[//]`) | 6 |
| Maior cadeia de dependência | 6 |

---

## Fase 1, Preparação

<!-- Setup, scaffolding, migrações iniciais, configuração de infraestrutura local. -->

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T001 | Criar os esquemas Pydantic `RoomCreate` e `RestrictionCreate` para validação de payloads de APIs | - | `[//]` | `src/api/schemas.py` | 🟢 | `[X]` |
| T002 | Criar repositórios de dados simulados em memória `db_teachers` e `db_restrictions` | - | `[//]` | `src/api/worker.py` | 🟢 | `[X]` |
| T003 | Configurar endpoints iniciais vazios na API FastAPI | T001 | - | `src/api/routes.py` | 🟡 | `[X]` |

---

## Fase 2, Testes

<!-- Testes que precisam existir antes ou logo após o núcleo. -->

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T004 | Desenvolver testes unitários para a rota POST `/api/v1/rooms` e suas validações de capacidade | T003 | `[//]` | `tests/test_api_rooms.py` | 🟢 | `[X]` |
| T005 | Desenvolver testes unitários para a importação transacional de salas via arquivo CSV | T003 | `[//]` | `tests/test_api_csv.py` | 🟢 | `[X]` |
| T006 | Desenvolver testes unitários para a rota POST de restrição docente e a lógica de reset semestral | T003 | `[//]` | `tests/test_api_restrictions.py` | 🟢 | `[X]` |

---

## Fase 3, Núcleo

<!-- Lógica central da feature. -->

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T007 | Implementar rota de criação de salas de aula e validações Pydantic correspondentes | T004 | - | `src/api/routes.py` | 🟡 | `[X]` |
| T008 | Implementar a lógica de leitura, validação e carga em lote transacional de arquivos CSV de salas | T005 | - | `src/api/routes.py` | 🟡 | `[X]` |
| T009 | Implementar a rota de cadastro de indisponibilidade docente e a rota de reset horários de semestres passados | T006 | - | `src/api/routes.py` | 🟡 | `[X]` |

---

## Fase 4, Integração

<!-- Cola com outras partes do sistema, contratos externos, ganchos. -->

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T010 | Implementar a rota GET `/api/v1/allocation/input-data` agregando salas, coordenações e turmas ativas | T007, T009 | - | `src/api/routes.py` | 🟢 | `[X]` |
| T011 | Integrar validação de regras de bloqueio HTTP 409 de deleção física de salas ativas ou com IA executando | T010 | - | `src/api/routes.py` | 🟢 | `[X]` |

---

## Fase 5, Polimento

<!-- Logs, telemetria, mensagens de erro, documentação curta. -->

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T012 | Adicionar logs detalhados e depuração das importações de CSV efetuadas e resets horários ativados | T008, T009 | `[//]` | `src/api/routes.py` | 🟢 | `[X]` |
| T013 | Escrever guia explicativo técnico resumido do Space Manager contendo contratos e formatos no README do código | - | `[//]` | `src/README.md` | 🟢 | `[X]` |

---

## Notas de execução

<!--
Reservado para /reversa-coding registrar avisos ou observações que surgiram durante a execução.
Não use isso para corrigir ações, edits manuais ficam fora desse arquivo, vão direto no código.
-->

Todas as rotas e validações do gerenciador acadêmico e predial foram implementadas em conformidade com as especificações. Os testes integrados passam com sucesso.

---

## Histórico de alterações

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-08-07 | Versão inicial gerada por `/reversa-to-do` | reversa |
| 2026-08-07 | Conclusão de todas as tarefas de código | reversa |
