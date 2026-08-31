# Roadmap: Nova aba Gestão com IA no Navbar Principal

> Identificador: `016-gestao-com-ia-aba`
> Data: `2026-08-14`
> Requirements: `_reversa_forward/016-gestao-com-ia-aba/requirements.md`
> Confidência: 🟢 CONFIRMADO, 🟡 INFERIDO, 🔴 LACUNA

## 1. Resumo da abordagem

A abordagem técnica consiste em reorganizar a estrutura DOM em `src/api/static/index.html`:
1. Adicionar o quarto botão de navegação principal `<button class="tab-btn" onclick="switchTab('ai-management-tab')">🤖 Gestão com IA</button>` na barra de navegação superior (`.tab-navigation`).
2. Criar o container `<div id="ai-management-tab" class="tab-content">`.
3. Relocar o botão de ação manual `#btnRunAllocation` do cabeçalho global (`<header>`) para o painel superior da aba `#ai-management-tab`.
4. Relocar as seções de Auditoria e Extrato (`.auctions-card`) e Status da Tarefa de IA do `#dashboard-tab` para o novo container `#ai-management-tab`.
5. Preservar intactas as funções de roteamento JS (`switchTab`), mantendo a compatibilidade de todos os IDs de elementos DOM (`#auctionsTableBody`, `#taskStatusBadge`, `#btnRunAllocation`, `#progressBar`).

## 2. Princípios aplicados

| Princípio | Como a feature se relaciona | Status |
|-----------|------------------------------|--------|
| Manutenção de IDs e Contratos DOM | Preserva rigorosamente os IDs de elementos consumidos pelos scripts JS em `index.html`. | respeita |
| Modularidade de Navegação por Abas | Extende o padrão de navegação SPA sem recarregamento de página utilizado na aplicação. | respeita |

## 3. Decisões técnicas

| ID | Decisão | Justificativa | Alternativas descartadas | Confidência |
|----|---------|----------------|--------------------------|-------------|
| D-01 | Criar a aba `🤖 Gestão com IA` (`ai-management-tab`) | Atende à solicitação direta do usuário para isolamento de funcionalidades de IA | Manter IA misturada no Dashboard | 🟢 |
| D-02 | Mover `#btnRunAllocation` para dentro da aba `ai-management-tab` | Agrupa todas as ações relativas à IA na mesma interface dedicada | Manter o botão duplicado no cabeçalho global | 🟢 |
| D-03 | Reutilizar a função nativa `switchTab` | Mantém o roteamento JS leve sem necessidade de novos seletores complexos | Criar função dedicada `switchAITab` | 🟢 |

## 4. Premissas

Nenhuma premissa adotada. O documento de requisitos possui 0 dúvidas.

## 5. Delta arquitetural

| Componente | Arquivo de origem no legado | Tipo de mudança | Resumo |
|------------|------------------------------|-----------------|--------|
| `occupancy-dashboard` | `_reversa_sdd/architecture.md#occupancy-dashboard` | contrato-alterado | Estrutura de abas estendida em `src/api/static/index.html` com a adição do container `#ai-management-tab`. |

## 6. Delta no modelo de dados

- Resumo das mudanças: Sem alterações em tabelas, schemas Pydantic ou banco SQLite.
- Detalhe completo em: `_reversa_forward/016-gestao-com-ia-aba/data-delta.md`

## 7. Delta de contratos externos

Não se aplica. Alteração restrita à camada de apresentação frontend HTML/CSS/JS.

## 8. Plano de migração

Não se aplica.

## 9. Riscos e mitigações

| Risco | Impacto | Probabilidade | Mitigação |
|-------|---------|---------------|-----------|
| Quebra nos seletores de eventos no JavaScript | alto | baixa | Manter os IDs originais (`#btnRunAllocation`, `#auctionsTableBody`, `#taskStatusBadge`, etc.) intactos no movimento HTML. |
| Problema no layout responsivo da nova aba | médio | baixa | Utilizar as classes utilitárias CSS pré-existentes (`.main-sections`, `.card`) no novo container. |

## 10. Critério de pronto

- [ ] Todas as ações do `actions.md` marcadas `[X]`
- [ ] Suíte de testes `pytest` executada sem regressões (61/61 testes)
- [ ] Renderização e acionamento corretos da aba "Gestão com IA" no navegador

## 11. Histórico de alterações

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-08-14 | Versão inicial gerada por `/reversa-plan` | reversa |
