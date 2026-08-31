# Roadmap: Gestão de Relatórios de Ocupação e Carga Docente

> Identificador: `018-gestao-relatorios-ocupacao-docentes`
> Data: `2026-08-14`
> Requirements: `_reversa_forward/018-gestao-relatorios-ocupacao-docentes/requirements.md`
> Confidência: 🟢 CONFIRMADO, 🟡 INFERIDO, 🔴 LACUNA

## 1. Resumo da abordagem

A implementação consiste em adicionar uma nova aba de relatórios analíticos no frontend e estender a API do backend:
1. No arquivo `src/api/static/index.html`, adicionar o botão de navegação `📊 Relatórios` na navbar superior e criar o container `#reports-tab`.
2. Estruturar a aba `#reports-tab` com um cabeçalho moderno e duas sub-seções em cards:
   - **Ocupação Coletiva por Ambiente**: tabela com filtros de Bloco (`#selectReportBlock`) e Turno (`#selectReportShift`).
   - **Carga Horária & Grade Docente**: tabela com seletor de Professor (`#selectReportTeacher`).
3. Adicionar no `src/api/routes.py` o endpoint `GET /api/v1/reports/summary` que calcula as taxas de ocupação por bloco e turno a partir das alocações e salas cadastradas no SQLite.
4. Conectar os botões de exportação em PDF e Excel para acionar as funções existentes `downloadReport('pdf')` e `downloadReport('excel')`.

## 2. Princípios aplicados

| Princípio | Como a feature se relaciona | Status |
|-----------|------------------------------|--------|
| Design Moderno e Consistência Visual | Adota o padrão Glassmorphism, cards escuros `#0f172a` e badges coloridos de status. | respeita |
| Interatividade Nativa sem Dependências | Filtros e renderização de tabelas executados em JavaScript Vanilla puro. | respeita |

## 3. Decisões técnicas

| ID | Decisão | Justificativa | Alternativas descartadas | Confidência |
|----|---------|----------------|--------------------------|-------------|
| D-01 | Adicionar a nova aba `#reports-tab` no topo da barra de navegação | Garante acesso direto e visibilidade em paridade com as demais telas do sistema | Criar sub-abas dentro do Dashboard | 🟢 |
| D-02 | Criar endpoint agregador `GET /api/v1/reports/summary` | Evita múltiplos cálculos repetidos no cliente e padroniza as estatísticas de ocupação | Calcular todas as estatísticas no JS do cliente | 🟢 |
| D-03 | Reutilizar `downloadReport('pdf')` e `downloadReport('excel')` | Aproveita os geradores PDF (ReportLab) e Excel já testados no backend | Criar novos geradores de PDF no client-side | 🟢 |

## 4. Premissas

Nenhuma premissa adotada. O documento de requisitos possui 0 dúvidas.

## 5. Delta arquitetural

| Componente | Arquivo de origem no legado | Tipo de mudança | Resumo |
|------------|------------------------------|-----------------|--------|
| `occupancy-dashboard` | `_reversa_sdd/architecture.md#occupancy-dashboard` | componente-novo | Adição do container `#reports-tab` e funções JS de filtro em `src/api/static/index.html`. |
| `academic-space-manager` | `_reversa_sdd/inventory.md#src/api/routes.py` | regra-nova | Adição do endpoint `GET /api/v1/reports/summary` em `src/api/routes.py`. |

## 6. Delta no modelo de dados

- Resumo das mudanças: Sem alterações no schema das tabelas SQLite.
- Detalhe completo em: `_reversa_forward/018-gestao-relatorios-ocupacao-docentes/data-delta.md`

## 7. Delta de contratos externos

Não se aplica.

## 8. Plano de migração

Não se aplica.

## 9. Riscos e mitigações

| Risco | Impacto | Probabilidade | Mitigação |
|-------|---------|---------------|-----------|
| Divisão por zero no cálculo de taxa de ocupação quando um bloco não tem salas | baixo | baixa | Tratar `if total_rooms == 0: occupancy_rate = 0.0` no backend. |

## 10. Critério de pronto

- [ ] Todas as ações do `actions.md` marcadas `[X]`
- [ ] Suíte de testes `pytest` executada com 100% de aprovação (61/61 testes)
- [ ] Navegação para a aba "📊 Relatórios" funcionando com filtros por Bloco, Turno e Docente

## 11. Histórico de alterações

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-08-14 | Versão inicial gerada por `/reversa-plan` | reversa |
