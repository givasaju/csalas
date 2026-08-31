# Legacy Impact: Reduzir 50% do tamanho das fontes na seção Auditoria e Extrato

> Identificador: `015-reduzir-fonte-auditoria-extrato`
> Data: `2026-08-14`

## 1. Arquivos Afetados

| Arquivo afetado | Componente | Tipo | Severidade | Justificativa |
|-----------------|------------|------|------------|---------------|
| `src/api/static/index.css` | `occupancy-dashboard` (`_reversa_sdd/architecture.md#occupancy-dashboard`) | `regra-alterada` | LOW | Alteração de tipografia escopada em 50% para `.auctions-table tbody td`. |

## 2. Diff Conceitual por Componente

### `occupancy-dashboard`
- **Alteração**: Redução do tamanho da fonte da classe `.auctions-table tbody td` de `0.875rem` / `1rem` para `0.44rem` (~50% do valor base).
- **Propriedades internas**: `font-size: inherit` adicionado para `strong` e `span` dentro das células de auditoria.
- **Espaçamento**: Padding reduzido para `0.25rem 0.4rem` e `line-height` ajustado para `1.2`.

## 3. Regras Preservadas

| Regra | Arquivo no Legado | Status |
|-------|-------------------|--------|
| Cores de destaque (Vencedor `#10b981`, Perdedor `#ef4444`, Lances `#6366f1`, Slot Badge `#818cf8`) | `_reversa_sdd/domain.md#auditoria-leiloes` | Intacta |
| Cabeçalho da tabela (`th`) e título do card (`section-title`) | `_reversa_sdd/architecture.md#occupancy-dashboard` | Intacta |
| Demais tabelas e estilos das abas Ambientes e Docentes | `_reversa_sdd/inventory.md#src/api/static/index.css` | Intacta |

## 4. Regras Modificadas

| Regra Original | Nova Regra | Justificativa |
|----------------|------------|---------------|
| Fonte de dados em tamanho padrão (`0.875rem` / `1rem`) | Fonte de dados compacta reduzida em 50% (`0.44rem`) | Solicitação explícita do usuário para otimização de espaço visual na auditoria. |
