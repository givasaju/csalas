# Actions: Nova aba Gestão com IA no Navbar Principal

> Identificador: `016-gestao-com-ia-aba`
> Data: `2026-08-14`
> Roadmap: `_reversa_forward/016-gestao-com-ia-aba/roadmap.md`

## Resumo

| Métrica | Valor |
|---------|-------|
| Total de ações | 4 |
| Paralelizáveis (`[//]`) | 2 |
| Maior cadeia de dependência | 4 |

## Fase 1, Preparação

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T001 | Inspecionar a estrutura do navbar (`.tab-navigation`), `#dashboard-tab` e `<header>` em `src/api/static/index.html` | - | `[//]` | `src/api/static/index.html` | 🟢 | `[x]` |

## Fase 3, Núcleo

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T002 | Adicionar a opção de aba `<button class="tab-btn" onclick="switchTab('ai-management-tab')">🤖 Gestão com IA</button>` no navbar principal após `Gestão de Docentes` | T001 | - | `src/api/static/index.html` | 🟢 | `[x]` |
| T003 | Criar o container `<div id="ai-management-tab" class="tab-content" style="display: none;">` e deslocar o botão `#btnRunAllocation`, o card `Status da Tarefa de IA` e o card `Auditoria e Extrato` para a nova interface | T002 | - | `src/api/static/index.html` | 🟢 | `[x]` |

## Fase 5, Polimento

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T004 | Executar a validação dos testes automatizados com `pytest` e verificar a alternância das abas e execução da IA no navegador | T003 | `[//]` | `tests/test_ui_input_routes.py` | 🟢 | `[x]` |

## Notas de execução

Todas as 4 ações T001 a T004 foram concluídas com sucesso e validadas com 100% de aprovação no pytest (61 passed em 3.63s).

## Histórico de alterações

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-08-14 | Versão inicial gerada por `/reversa-to-do` | reversa |
| 2026-08-14 | Conclusão de todas as tarefas T001-T004 por `/reversa-coding` | reversa |
