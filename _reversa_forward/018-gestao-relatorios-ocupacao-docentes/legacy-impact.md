# Legacy Impact: Gestão de Relatórios de Ocupação e Carga Docente

> Identificador: `018-gestao-relatorios-ocupacao-docentes`
> Data: `2026-08-14`

## 1. Arquivos Afetados

| Arquivo afetado | Componente | Tipo | Severidade | Justificativa |
|-----------------|------------|------|------------|---------------|
| `src/api/routes.py` | `academic-space-manager` (`_reversa_sdd/architecture.md#academic-space-manager`) | `contrato-novo` | LOW | Adição do endpoint `GET /api/v1/reports/summary`. |
| `src/api/static/index.html` | `occupancy-dashboard` (`_reversa_sdd/architecture.md#occupancy-dashboard`) | `componente-novo` | LOW | Adição da aba `#reports-tab` no navbar e funções JS de filtro e renderização. |

## 2. Diff Conceitual por Componente

### `academic-space-manager`
- **Novo Endpoint REST**: `GET /api/v1/reports/summary` agrega dinamicamente a taxa de ocupação por bloco/turno e a grade de horas por docente a partir das tabelas `Room`, `Allocation` e `Teacher`.

### `occupancy-dashboard`
- **Nova Aba Principal**: Botão `📊 Relatórios` no navbar principal e container `#reports-tab`.
- **Filtros Interativos**: Seletores dinâmicos de Bloco, Turno e Docente para re-renderização em tempo real.

## 3. Regras Preservadas

| Regra | Arquivo no Legado | Status |
|-------|-------------------|--------|
| Geradores de relatório PDF (ReportLab) e Excel (openpyxl) | `_reversa_sdd/inventory.md#src/api/routes.py` | Intactos |
| Estrutura de rotas e autenticação JWT mock | `_reversa_sdd/architecture.md#c4-context` | Intacta |

## 4. Regras Modificadas

| Regra Original | Nova Regra | Justificativa |
|----------------|------------|---------------|
| Relatórios eram acessados exclusivamente por downloads diretos no topo | Ocupação por bloco/turno e carga docente podem ser filtradas e visualizadas interativamente na tela antes de exportar | Suporte a decisões gerenciais e auditoria direta na UI. |
