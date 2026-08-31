# Legacy Impact: Painel Explicativo Interativo e Flutuante na Gestão com IA

> Identificador: `017-painel-explicativo-interativo-ia`
> Data: `2026-08-14`

## 1. Arquivos Afetados

| Arquivo afetado | Componente | Tipo | Severidade | Justificativa |
|-----------------|------------|------|------------|---------------|
| `src/api/static/index.css` | `occupancy-dashboard` (`_reversa_sdd/architecture.md#occupancy-dashboard`) | `componente-novo` | LOW | Estilos CSS para o widget `#aiGuideWidget` e botões de controle `.btn-font-scale`. |
| `src/api/static/index.html` | `occupancy-dashboard` (`_reversa_sdd/architecture.md#occupancy-dashboard`) | `componente-novo` | LOW | Componente HTML `#aiGuideWidget` e handlers JS para Drag & Drop e redimensionamento de fonte. |

## 2. Diff Conceitual por Componente

### `occupancy-dashboard`
- **Novo Widget Flutuante**: `#aiGuideWidget` exibido na aba `#ai-management-tab` com cartões explicativos ("Quando usar IA", "Quando não usar IA" e "Opções da tela").
- **Drag & Drop Nativo**: Event listeners `mousedown`, `mousemove`, `mouseup` no cabeçalho `.ai-guide-header`.
- **Controle de Acessibilidade**: Botões `A-` e `A+` para escala de fonte em tempo real.
- **Controle de Visibilidade**: Botão de fechar `✖` e botão de restauração `💡 Guia Interativo`.

## 3. Regras Preservadas

| Regra | Arquivo no Legado | Status |
|-------|-------------------|--------|
| Execução de alocações e atualização de status assíncrono da IA | `_reversa_sdd/domain.md#auditoria-leiloes` | Intacta |
| Estrutura de abas principais e sub-abas de navegação | `_reversa_sdd/architecture.md#occupancy-dashboard` | Intacta |

## 4. Regras Modificadas

| Regra Original | Nova Regra | Justificativa |
|----------------|------------|---------------|
| Aba Gestão com IA exibia apenas cards estáticos | Aba Gestão com IA exibe o widget interativo `#aiGuideWidget` com orientação de decisão e controles manipuláveis pelo usuário | Requisito de apoio ao coordenador na escolha de uso da IA. |
