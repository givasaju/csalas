# Actions: Reduzir 50% do tamanho das fontes que apresentam os dados da seção Auditoria e Extrato

> Identificador: `015-reduzir-fonte-auditoria-extrato`
> Data: `2026-08-14`
> Roadmap: `_reversa_forward/015-reduzir-fonte-auditoria-extrato/roadmap.md`

## Resumo

| Métrica | Valor |
|---------|-------|
| Total de ações | 3 |
| Paralelizáveis (`[//]`) | 2 |
| Maior cadeia de dependência | 3 |

## Fase 1, Preparação

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T001 | Inspecionar e validar as regras da classe `.auctions-table tbody td` em `src/api/static/index.css` | - | `[//]` | `src/api/static/index.css` | 🟢 | `[x]` |

## Fase 3, Núcleo

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T002 | Aplicar a redução de 50% na fonte (`font-size: 0.44rem`) e no padding (`padding: 0.25rem 0.4rem`) com `font-size: inherit` nas sub-tags (`strong`, `span`) da classe `.auctions-table tbody td` em `src/api/static/index.css` | T001 | - | `src/api/static/index.css` | 🟢 | `[x]` |

## Fase 5, Polimento

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T003 | Executar a validação de testes automatizados com `pytest` e verificar ausência de regressões | T002 | `[//]` | `tests/test_ui_input_routes.py` | 🟢 | `[x]` |

## Notas de execução

Todas as 3 ações T001 a T003 foram concluídas com sucesso e validadas na suíte de testes `pytest` (61 passed em 2.87s).

## Histórico de alterações

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-08-14 | Versão inicial gerada por `/reversa-to-do` | reversa |
| 2026-08-14 | Conclusão de todas as tarefas T001-T003 por `/reversa-coding` | reversa |
