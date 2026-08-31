# Legacy Impact: Nova aba Gestão com IA no Navbar Principal

> Identificador: `016-gestao-com-ia-aba`
> Data: `2026-08-14`

## 1. Arquivos Afetados

| Arquivo afetado | Componente | Tipo | Severidade | Justificativa |
|-----------------|------------|------|------------|---------------|
| `src/api/static/index.html` | `occupancy-dashboard` (`_reversa_sdd/architecture.md#occupancy-dashboard`) | `contrato-alterado` | LOW | Adição do container `#ai-management-tab` e deslocamento das seções de IA para a nova aba. |

## 2. Diff Conceitual por Componente

### `occupancy-dashboard`
- **Navegação principal**: Adicionado botão de aba `🤖 Gestão com IA` disposta após `👨‍🏫 Gestão de Docentes`.
- **Relocação de Seções**:
  - `Disparar Alocação de IA` (`#btnRunAllocation`) movido para o cabeçalho interno da nova aba `#ai-management-tab`.
  - `Auditoria e Extrato` (`.auctions-card`) e `Status da Tarefa de IA` movidos para `#ai-management-tab`.
- **Manutenção de IDs**: Todos os seletores DOM e scripts de escuta de eventos JS foram mantidos sem nenhuma quebra de funcionalidade.

## 3. Regras Preservadas

| Regra | Arquivo no Legado | Status |
|-------|-------------------|--------|
| Exibição dos KPI Cards de Ocupação e Energia no Dashboard | `_reversa_sdd/architecture.md#occupancy-dashboard` | Intacta |
| Lógica e endpoints HTTP de execução do solver de IA | `_reversa_sdd/domain.md#auditoria-leiloes` | Intacta |
| Roteamento dinâmico de abas via `switchTab` | `_reversa_sdd/inventory.md#src/api/static/index.html` | Intacta |

## 4. Regras Modificadas

| Regra Original | Nova Regra | Justificativa |
|----------------|------------|---------------|
| Seções de IA integradas ao `#dashboard-tab` e botão global no header | Seções de IA agrupadas exclusivamente na aba `🤖 Gestão com IA` (`#ai-management-tab`) | Organização e especialização da interface visual conforme pedido do usuário. |
