# Actions: UI Moderna de Entrada de Dados do ClassSync AI

> Identificador: `004-ui-entrada-dados`  
> Data: `2026-08-07`  
> Roadmap: `_reversa_forward/004-ui-entrada-dados/roadmap.md`  

---

## Resumo

| Métrica | Valor |
|---------|-------|
| Total de ações | 10 |
| Paralelizáveis (`[//]`) | 4 |
| Maior cadeia de dependência | 4 |

---

## Fase 1, Preparação

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T001 | Atualizar a folha de estilos CSS global com tokens visuais, suporte a temas e estilos para componentes de entrada de dados | - | `[//]` | `src/api/static/index.css` | 🟢 | `[X]` |
| T002 | Montar a estrutura HTML dos painéis de formulário (Cadastro de Sala, Importação CSV, Restrições e Tabela de Inventário) | - | `[//]` | `src/api/static/index.html` | 🟢 | `[X]` |

---

## Fase 2, Testes

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T003 | Desenvolver suíte de testes de integração pytest para validação de endpoints REST da entrada de dados | - | `[//]` | `tests/test_ui_input_routes.py` | 🟢 | `[X]` |

---

## Fase 3, Núcleo

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T004 | Implementar script JS do formulário de cadastro unitário de salas com validação client-side e POST /api/v1/rooms | T002 | - | `src/api/static/index.html` | 🟢 | `[X]` |
| T005 | Implementar script JS para área de Drag & Drop de arquivos CSV com preview e POST /api/v1/rooms/import-csv | T002 | - | `src/api/static/index.html` | 🟢 | `[X]` |
| T006 | Implementar script JS para Matriz Interativa de Indisponibilidade Docente e POST /api/v1/allocation/restrictions | T002 | - | `src/api/static/index.html` | 🟢 | `[X]` |
| T007 | Implementar renderização dinâmica do inventário de salas com filtro, exclusão DELETE /api/v1/rooms/{id} e tratamento do erro 409 | T002 | - | `src/api/static/index.html` | 🟢 | `[X]` |

---

## Fase 4, Integração

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T008 | Implementar botão e modal de reset semestral acionando DELETE /api/v1/allocation/restrictions | T006 | - | `src/api/static/index.html` | 🟢 | `[X]` |
| T009 | Garantir persistência do cabeçalho JWT Bearer em todas as chamadas fetch da UI | T004, T005, T006, T007 | - | `src/api/static/index.html` | 🟢 | `[X]` |

---

## Fase 5, Polimento

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T010 | Integrar feedback visual com Toasts animados para status 200/201, 400, 409 e 422 | T001 | `[//]` | `src/api/static/index.css` | 🟢 | `[X]` |

---

## Notas de execução

Todas as 10 tarefas executadas e validadas com suíte de testes unitários e de integração (17 testes passando).

---

## Histórico de alterações

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-08-07 | Versão inicial gerada por `/reversa-to-do` | reversa |
| 2026-08-07 | Execução de todas as ações concluída por `/reversa-coding` | reversa-coding |
