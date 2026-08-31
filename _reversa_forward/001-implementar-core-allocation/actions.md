# Actions: Implementar o motor de alocação core-allocation-engine

> Identificador: `001-implementar-core-allocation`  
> Data: `2026-08-07`  
> Roadmap: `_reversa_forward/001-implementar-core-allocation/roadmap.md`  

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
| T001 | Criar `requirements.txt` com as dependências do Python (como FastAPI, Pydantic) | - | `[//]` | `requirements.txt` | 🟢 | `[X]` |
| T002 | Implementar script SQL de criação das tabelas `AllocationTask`, `AuctionBid` e coluna de créditos na tabela `Coordination` | - | `[//]` | `db/migrations.sql` | 🟢 | `[X]` |
| T003 | Criar estrutura básica de classes e módulos do motor de IA de alocação | T001 | - | `src/engine/agents.py` | 🟡 | `[X]` |

---

## Fase 2, Testes

<!-- Testes que precisam existir antes ou logo após o núcleo. -->

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T004 | Desenvolver testes unitários para validação de restrições mandatórias (acessibilidade, capacidade mínima) | T003 | `[//]` | `tests/test_constraints.py` | 🟢 | `[X]` |
| T005 | Desenvolver testes unitários para a dinâmica de leilão cooperativo (compra, débito e compensação de créditos) | T003 | `[//]` | `tests/test_auction.py` | 🟢 | `[X]` |
| T006 | Desenvolver testes unitários para a otimização predial (fitness e fechamento predial) | T003 | `[//]` | `tests/test_building_optimization.py` | 🟢 | `[X]` |

---

## Fase 3, Núcleo

<!-- Lógica central da feature. -->

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T007 | Implementar classes dos agentes ACC, AAC e AMR no motor de negociação cooperativo | T004, T005 | - | `src/engine/agents.py` | 🟡 | `[X]` |
| T008 | Implementar heurística de otimização predial de agrupamento físico de turmas em blocos | T006 | - | `src/engine/optimization.py` | 🟡 | `[X]` |
| T009 | Implementar a classe orquestradora principal `CoreAllocationEngine` integrando alocação, leilões e otimizações | T007, T008 | - | `src/engine/core.py` | 🟡 | `[X]` |

---

## Fase 4, Integração

<!-- Cola com outras partes do sistema, contratos externos, ganchos. -->

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T010 | Implementar endpoints HTTP POST `/api/v1/allocation/run` e GET `/api/v1/allocation/status/{task_id}` na API do backend | T002, T009 | - | `src/api/routes.py` | 🟢 | `[X]` |
| T011 | Implementar fila de processamento assíncrono em background (ThreadPoolExecutor) para gerenciar o motor sem bloquear conexões | T010 | - | `src/api/worker.py` | 🟢 | `[X]` |

---

## Fase 5, Polimento

<!-- Logs, telemetria, mensagens de erro, documentação curta. -->

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T012 | Adicionar logs detalhados e verbosos para auditoria detalhada de rodadas de ofertas e transações de créditos | T009 | `[//]` | `src/engine/core.py` | 🟢 | `[X]` |
| T013 | Escrever guia explicativo técnico resumido do motor de IA multiagente e leilão no README do código | - | `[//]` | `src/README.md` | 🟢 | `[X]` |

---

## Notas de execução

<!--
Reservado para /reversa-coding registrar avisos ou observações que surgiram durante a execução.
Não use isso para corrigir ações, edits manuais ficam fora desse arquivo, vão direto no código.
-->

As tarefas foram totalmente implementadas e os testes unitários integrados passam com 100% de sucesso.

---

## Histórico de alterações

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-08-07 | Versão inicial gerada por `/reversa-to-do` | reversa |
| 2026-08-07 | Conclusão de todas as tarefas de código | reversa |
