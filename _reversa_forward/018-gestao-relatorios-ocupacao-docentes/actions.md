# Actions: Gestão de Relatórios de Ocupação e Carga Docente

> Identificador: `018-gestao-relatorios-ocupacao-docentes`
> Data: `2026-08-14`
> Roadmap: `_reversa_forward/018-gestao-relatorios-ocupacao-docentes/roadmap.md`

## Resumo

| Métrica | Valor |
|---------|-------|
| Total de ações | 4 |
| Paralelizáveis (`[//]`) | 2 |
| Maior cadeia de dependência | 4 |

## Fase 1, Preparação

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T001 | Criar a função auxiliar e o endpoint `GET /api/v1/reports/summary` em `src/api/routes.py` para agregar ocupação por bloco e turno a partir do SQLite | - | `[//]` | `src/api/routes.py` | 🟢 | `[x]` |

## Fase 3, Núcleo

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T002 | Adicionar o botão da aba `📊 Relatórios` e o container HTML `#reports-tab` com filtros e tabelas de Ocupação e Carga Docente em `src/api/static/index.html` | T001 | - | `src/api/static/index.html` | 🟢 | `[x]` |
| T003 | Implementar a lógica JavaScript de busca de dados, filtros dinâmicos e exportação de relatórios em `src/api/static/index.html` | T002 | - | `src/api/static/index.html` | 🟢 | `[x]` |

## Fase 5, Polimento

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T004 | Validar a suíte de testes `pytest` e testar a geração/download dos relatórios na interface | T003 | `[//]` | `tests/test_reports_api.py` | 🟢 | `[x]` |

## Notas de execução

Todas as 4 ações T001 a T004 foram executadas com sucesso e validadas pela suíte de testes (61/61 passed).

## Histórico de alterações

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-08-14 | Versão inicial gerada por `/reversa-to-do` | reversa |
| 2026-08-14 | Conclusão de todas as tarefas T001-T004 por `/reversa-coding` | reversa |
