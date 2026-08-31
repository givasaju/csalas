# Actions: Painel Explicativo Interativo e Flutuante na Gestão com IA

> Identificador: `017-painel-explicativo-interativo-ia`
> Data: `2026-08-14`
> Roadmap: `_reversa_forward/017-painel-explicativo-interativo-ia/roadmap.md`

## Resumo

| Métrica | Valor |
|---------|-------|
| Total de ações | 4 |
| Paralelizáveis (`[//]`) | 2 |
| Maior cadeia de dependência | 4 |

## Fase 1, Preparação

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T001 | Definir os estilos CSS do widget flutuante (`.ai-guide-widget`, `.ai-guide-header`, `.ai-guide-body`, `.btn-font-scale`, `#btnToggleAiGuide`) em `src/api/static/index.css` | - | `[//]` | `src/api/static/index.css` | 🟢 | `[x]` |

## Fase 3, Núcleo

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T002 | Inserir a estrutura HTML do widget flutuante `#aiGuideWidget` com seções "Quando Usar", "Quando Não Usar" e "Opções" na aba `#ai-management-tab` | T001 | - | `src/api/static/index.html` | 🟢 | `[x]` |
| T003 | Implementar as funções JavaScript de Drag and Drop, escala de fonte (`A-`/`A+`) e fechar/restaurar no `src/api/static/index.html` | T002 | - | `src/api/static/index.html` | 🟢 | `[x]` |

## Fase 5, Polimento

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T004 | Executar a validação dos testes automatizados com `pytest` e testar a interatividade do widget no navegador | T003 | `[//]` | `tests/test_ui_input_routes.py` | 🟢 | `[x]` |

## Notas de execução

Todas as 4 ações T001 a T004 foram concluídas com sucesso e validadas com 100% de aprovação no pytest (61 passed em 2.97s).

## Histórico de alterações

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-08-14 | Versão inicial gerada por `/reversa-to-do` | reversa |
| 2026-08-14 | Conclusão de todas as tarefas T001-T004 por `/reversa-coding` | reversa |
