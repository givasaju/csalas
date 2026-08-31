# Requirements: Nova aba Gestão com IA no Navbar Principal

> Identificador: `016-gestao-com-ia-aba`
> Data: `2026-08-14`
> Pasta da extração reversa: `_reversa_sdd/`
> Confidência: 🟢 CONFIRMADO, 🟡 INFERIDO, 🔴 LACUNA / DÚVIDA

## 1. Resumo executivo

Adicionar uma nova aba de navegação principal intitulada **🤖 Gestão com IA** disposta após a opção **Gestão de Docentes** no cabeçalho do sistema. Relocar para esta nova interface as seções de **Auditoria e Extrato de Leilões de Créditos**, **Status da Tarefa de IA** e o botão de ação **Disparar Alocação de IA** (anteriormente localizado no topo do header).

## 2. Contexto a partir do legado

| Fonte | Trecho relevante | Confidência |
|-------|------------------|-------------|
| `_reversa_sdd/architecture.md#occupancy-dashboard` | Estrutura de abas do Dashboard de Ocupação e layout de navegação principal. | 🟢 |
| `_reversa_sdd/domain.md#auditoria-leiloes` | Regras de monitoramento de leilões e status da tarefa assíncrona de IA. | 🟢 |
| `_reversa_sdd/inventory.md#src/api/static/index.html` | Interface estática contendo o navbar principal (`.tab-navigation`), `dashboard-tab`, `rooms-tab` e `teachers-tab`. | 🟢 |
| `_reversa_sdd/addenda/015-reduzir-fonte-auditoria-extrato.md` | Estilos de tipografia compacta (`0.44rem`) vigentes para a seção de auditoria e extrato. | 🟢 |

## 3. Personas e cenários de uso

| Persona | Objetivo | Cenário-chave |
|---------|----------|---------------|
| Coordenador / Administrador de IA | Centralizar o controle das otimizações inteligentes | Acessar a aba "Gestão com IA" para disparar novos cálculos do solver de IA, acompanhar o status em tempo real e auditar o extrato de lances de leilões. |

## 4. Regras de negócio novas ou alteradas

1. **RN-01:** Adição de novo item de menu principal `🤖 Gestão com IA` no navbar (`.tab-navigation`), posicionado após a aba `👨‍🏫 Gestão de Docentes`. 🟢
   - Origem no legado: `_reversa_sdd/inventory.md#src/api/static/index.html`
   - Tipo: nova
2. **RN-02:** Criação do container `#ai-management-tab` e deslocamento das seções "Auditoria e Extrato de Leilões" e "Status da Tarefa de IA" da aba `#dashboard-tab` para a nova aba `#ai-management-tab`. 🟢
   - Origem no legado: `_reversa_sdd/architecture.md#occupancy-dashboard`
   - Tipo: alterada
3. **RN-03:** Deslocamento do botão `Disparar Alocação de IA` (`#btnRunAllocation`) do cabeçalho global (`<header>`) para o painel da nova aba `🤖 Gestão com IA`. 🟢
   - Origem no legado: `_reversa_sdd/inventory.md#src/api/static/index.html`
   - Tipo: alterada
4. **RN-04:** Manutenção dos KPIs (Ocupação Geral, Economia de Energia, Blocos Desativados, Conflitos Resolvidos) no `#dashboard-tab`. 🟢
   - Origem no legado: `_reversa_sdd/architecture.md#occupancy-dashboard`
   - Tipo: mantida

## 5. Requisitos Funcionais

| ID | Requisito | Prioridade | Critério de aceite | Confidência |
|----|-----------|------------|--------------------|-------------|
| RF-01 | Criar a aba `🤖 Gestão com IA` no navbar principal logo após `👨‍🏫 Gestão de Docentes`. | Must | A aba aparece no navbar e alterna para o container `#ai-management-tab` ao ser clicada. | 🟢 |
| RF-02 | Mover o card `Auditoria e Extrato de Leilões de Créditos` (`.auctions-card`) para `#ai-management-tab`. | Must | O extrato de leilões passa a ser renderizado na nova aba. | 🟢 |
| RF-03 | Mover o card `Status da Tarefa de IA` (`#taskStatusBadge`, `#progressBar`, `#taskProgressMessage`) para `#ai-management-tab`. | Must | O progresso e status da IA passam a ser visíveis na nova aba. | 🟢 |
| RF-04 | Mover o botão `Disparar Alocação de IA` (`#btnRunAllocation`) para dentro do painel em `#ai-management-tab`. | Must | O acionamento manual do cálculo de IA passa a ser feito a partir da aba de Gestão com IA. | 🟢 |

## 6. Requisitos Não Funcionais

| Tipo | Requisito | Evidência ou justificativa | Confidência |
|------|-----------|----------------------------|-------------|
| Usabilidade | Garantir transição fluida sem recarregar a página ao alternar para a aba "Gestão com IA" utilizando a função `switchTab`. | Rationale de experiência do usuário | 🟢 |
| Manutenibilidade | Preservar todos os seletores de ID HTML existentes (`#btnRunAllocation`, `#auctionsTableBody`, `#taskStatusBadge`) para não quebrar os eventos e requisições no script JavaScript. | Rationale de integração de scripts | 🟢 |

## 7. Critérios de Aceitação

```gherkin
Cenário: Navegação para a nova aba Gestão com IA
  Dado que o usuário está na página inicial da aplicação
  Quando ele observa a barra de navegação superior
  Então a opção "🤖 Gestão com IA" é exibida após "👨‍🏫 Gestão de Docentes"
  E ao clicar no botão, a interface exibe o conteúdo da aba Gestão com IA

Cenário: Execução de ações de IA na nova aba
  Dado que o usuário está na aba "🤖 Gestão com IA"
  Quando ele verifica o conteúdo da tela
  Então as seções "Disparar Alocação de IA", "Status da Tarefa de IA" e "Auditoria e Extrato" são apresentadas
  E a ação de disparar alocação executa normalmente atualizando o status e a tabela de auditoria
```

## 8. Prioridade MoSCoW

| Item | MoSCoW | Justificativa |
|------|--------|---------------|
| RF-01 | Must | Reorganização essencial da barra de navegação solicitada pelo usuário. |
| RF-02 | Must | Reagrupamento da seção de auditoria no módulo de IA. |
| RF-03 | Must | Reagrupamento do status de execução assíncrona no módulo de IA. |
| RF-04 | Must | Reagrupamento do botão de ação principal do solver de IA. |

## 9. Esclarecimentos

> Nenhuma sessão de dúvidas registrada ainda. Rode `/reversa-clarify` quando houver `[DÚVIDA]` pendente.

## 10. Lacunas

Nenhuma lacuna ou `[DÚVIDA]` pendente.

## 11. Histórico de alterações

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-08-14 | Versão inicial gerada por `/reversa-requirements` | reversa |
