# Requirements: Painel Explicativo Interativo e Flutuante na Gestão com IA

> Identificador: `017-painel-explicativo-interativo-ia`
> Data: `2026-08-14`
> Pasta da extração reversa: `_reversa_sdd/`
> Confidência: 🟢 CONFIRMADO, 🟡 INFERIDO, 🔴 LACUNA / DÚVIDA

## 1. Resumo executivo

Implementar um painel explicativo interativo com estética moderna, elegante e flutuante na aba **Gestão com IA** (`#ai-management-tab`). O painel orientará o coordenador sobre quando utilizar ou não a inteligência artificial para otimização de salas, além de explicar as opções da tela. O usuário terá controle total para arrastar (drag & drop), reposicionar, ajustar o tamanho da fonte (`A-`/`A+`) e fechar/reabrir o painel a qualquer momento.

## 2. Contexto a partir do legado

| Fonte | Trecho relevante | Confidência |
|-------|------------------|-------------|
| `_reversa_sdd/architecture.md#occupancy-dashboard` | Estrutura da aba Gestão com IA (`#ai-management-tab`) e roteamento de interface. | 🟢 |
| `_reversa_sdd/domain.md#auditoria-leiloes` | Regras do solver de IA de otimização predial e leilão de créditos. | 🟢 |
| `_reversa_sdd/inventory.md#src/api/static/index.html` | Interface HTML estática e script JS do frontend. | 🟢 |
| `_reversa_sdd/addenda/016-gestao-com-ia-aba.md` | Estrutura recente da aba `#ai-management-tab`. | 🟢 |

## 3. Personas e cenários de uso

| Persona | Objetivo | Cenário-chave |
|---------|----------|---------------|
| Coordenador de Infraestrutura / Acadêmico | Compreender o momento ideal de acionar o solver de IA | Ao acessar "Gestão com IA", lê a orientação interativa, ajusta o tamanho do texto conforme preferência de leitura, move a caixa se necessário e fecha quando quiser. |

## 4. Regras de negócio novas ou alteradas

1. **RN-01:** Apresentação de um widget flutuante moderno de guia interativo (`#aiGuideWidget`) automaticamente ao acessar a aba `Gestão com IA`. 🟢
   - Origem no legado: `_reversa_sdd/addenda/016-gestao-com-ia-aba.md`
   - Tipo: nova
2. **RN-02:** Exibição de conteúdo explicativo claro em seções destacadas: 🟢
   - **Quando usar a IA**: Matrizes complexas de turmas/salas, otimização de custos de energia com esvaziamento de blocos e resolução automatizada de conflitos.
   - **Quando não usar a IA**: Alocações pontuais unitárias de pouca complexidade ou ajustes diretos manuais.
   - **Guia das Opções**: Explicações curtas do botão Disparar Alocação, Status da Tarefa e Extrato de Leilões.
3. **RN-03:** Suporte a movimentação por clique e arraste (Draggable header) permitindo deslocar o widget livremente pela tela. 🟢
   - Origem no legado: `_reversa_sdd/inventory.md#src/api/static/index.html`
   - Tipo: nova
4. **RN-04:** Controle dinâmico de tamanho de fonte (`A-` para diminuir, `A+` para aumentar) com limite proporcional. 🟢
   - Origem no legado: `_reversa_sdd/inventory.md#src/api/static/index.html`
   - Tipo: nova
5. **RN-05:** Botão de fechar (✖) que oculta o painel com transição suave, disponibilizando um botão discreto de gatilho "💡 Guia Interativo" para reabri-lo quando desejado. 🟢
   - Origem no legado: `_reversa_sdd/inventory.md#src/api/static/index.html`
   - Tipo: nova

## 5. Requisitos Funcionais

| ID | Requisito | Prioridade | Critério de aceite | Confidência |
|----|-----------|------------|--------------------|-------------|
| RF-01 | Criar o componente visual flutuante `#aiGuideWidget` com glassmorphism e bordas suaves na aba Gestão com IA. | Must | O widget é renderizado com design moderno no topo da aba. | 🟢 |
| RF-02 | Incluir o texto explicativo sobre casos recomendados, casos não recomendados e opções da tela. | Must | O conteúdo é formatado em tópicos claros e legíveis. | 🟢 |
| RF-03 | Implementar funcionalidade de arraste (drag & drop) ao clicar e mover a barra superior do widget. | Must | O usuário pode arrastar o widget para qualquer posição da tela. | 🟢 |
| RF-04 | Implementar botões de controle de tamanho de fonte (`A-` / `A+`). | Must | Clicar em `A+` aumenta a fonte do texto e em `A-` diminui proporcionalmente. | 🟢 |
| RF-05 | Permitir fechar o widget (botão ✖) e reabri-lo via botão auxiliar "💡 Guia de IA". | Must | Clicar em ✖ oculta a caixa e exibir o botão de abertura traz a caixa de volta. | 🟢 |

## 6. Requisitos Não Funcionais

| Tipo | Requisito | Evidência ou justificativa | Confidência |
|------|-----------|----------------------------|-------------|
| Usabilidade | Garantir movimentação suave (smooth dragging) sem trepidação em monitores com diferentes resoluções. | Rationale de experiência do usuário | 🟢 |
| Desempenho | O controle de tamanho de fonte e arraste deve ser processado em JavaScript Vanilla leve sem bibliotecas pesadas de terceiros. | Rationale de performance e dependências | 🟢 |

## 7. Critérios de Aceitação

```gherkin
Cenário: Interação com o painel guia na Gestão com IA
  Dado que o usuário navega para a aba "Gestão com IA"
  Quando o painel guia flutuante é apresentado
  Então ele pode ler os conselhos de quando utilizar o motor de IA
  E ao arrastar a barra do painel, a caixa se move livremente na tela
  E ao clicar nos botões A- / A+, o tamanho da fonte do texto se ajusta em tempo real

Cenário: Fechamento e reabertura do painel
  Dado que o painel guia está visível
  Quando o usuário clica no botão "✖ Fechar"
  Então o painel se oculta suavemente
  E ao clicar no botão "💡 Guia Interativo", o painel reaparece no mesmo local
```

## 8. Prioridade MoSCoW

| Item | MoSCoW | Justificativa |
|------|--------|---------------|
| RF-01 | Must | Componente visual principal da caixa explicativa. |
| RF-02 | Must | Conteúdo informativo valioso para tomada de decisão do usuário. |
| RF-03 | Must | Requisito explícito de arraste e soltura (drag and drop). |
| RF-04 | Must | Requisito explícito de redimensionamento dinâmico de fonte. |
| RF-05 | Must | Requisito de fechamento e controle pelo usuário. |

## 9. Esclarecimentos

> Nenhuma sessão de dúvidas registrada ainda. Rode `/reversa-clarify` quando houver `[DÚVIDA]` pendente.

## 10. Lacunas

Nenhuma lacuna ou `[DÚVIDA]` pendente.

## 11. Histórico de alterações

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-08-14 | Versão inicial gerada por `/reversa-requirements` | reversa |
