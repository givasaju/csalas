# Unit: painel-ocupacao, Design Técnico

> Especificação de design técnico detalhando componentes visuais, interações DOM, classes de estilização e lógicas Javascript do painel do dashboard.

## Interface

Esta unit é implementada como uma página HTML5 estática contendo CSS e Javascript puros embutidos (SPA), servida no endpoint `/` da API. Ela consome assincronamente os endpoints REST sob o prefixo `/api/v1`.

### Elementos do DOM e Símbolos Javascript Principais

| Símbolo | Tipo / Elemento | Ação / Escopo | Observação |
|---------|-----------------|---------------|------------|
| `document.DOMContentLoaded` | Evento | Inicializa o painel executando `loadInputData()`. | Disparado pelo carregamento do navegador. |
| `loadInputData()` | Função JS | Consome `GET /api/v1/allocation/input-data`. | Atualiza KPIs de tela e renderiza tabela de lances. |
| `triggerAllocation()` | Função JS | Consome `POST /api/v1/allocation/run`. | Dispara a alocação de IA, desabilita botões e inicia o polling. |
| `pollTaskStatus(taskId)`| Função JS | Consome `GET /api/v1/allocation/status/{taskId}`. | Loop de requisições recursivas a cada 1000ms. |
| `kpiOccupancy` | ID HTML | Exibe percentual médio de preenchimento de salas. | Card de KPI. |
| `kpiEnergy` | ID HTML | Exibe estimativa de redução de custos energéticos. | Card de KPI. |
| `kpiBlocks` | ID HTML | Exibe blocos prediais desativados. | Card de KPI. |
| `kpiConflicts` | ID HTML | Exibe contagem de conflitos resolvidos. | Card de KPI. |
| `auctionsTableBody` | ID HTML | Corpo de tabela de extrato do leilão cooperativo. | Renderiza as linhas de transações do leilão. |
| `btnRunIA` | ID HTML | Botão "Disparar Alocação de IA". | Dispara o fluxo assíncrono. |

---

## Fluxo Principal (UI / Interativo)

1.  **Carregamento e Renderização Inicial**:
    *   O evento `DOMContentLoaded` inicia o script e executa `loadInputData()` (`src/api/static/index.html`).
    *   Faz requisição assíncrona para obter o inventário agregador (`src/api/static/index.html`).
    *   Oculta as animações de shimmer loading nos cartões de KPI e insere as métricas gerais (`src/api/static/index.html`).
    *   Preenche a tabela de transações do leilão com o histórico retornado pelo AMR (`src/api/static/index.html`).
2.  **Disparo e Acompanhamento de Tarefa**:
    *   O usuário clica no botão `btnRunIA` que dispara `triggerAllocation()` (`src/api/static/index.html`).
    *   A função desabilita o botão, limpa a barra de progresso visual para 0% e altera o badge para o status `queued` (`src/api/static/index.html`).
    *   Envia requisição POST e recebe o `task_id` da tarefa em fila no worker.
    *   Inicializa `setInterval` recursivo de `pollTaskStatus(taskId)` com intervalo estrito de 1000ms (`src/api/static/index.html`).
3.  **Acompanhamento da Fila e Transição de Badges**:
    *   A cada 1000ms o status da tarefa é consultado.
    *   Se status for `running`: a largura da barra de carregamento é atualizada com o progresso numérico e o badge visual altera para `running` (`src/api/static/index.html`).
    *   Se status for `completed` ou `pending_arbitration`: o timer de polling é destruído com `clearInterval`, a barra é fixada em 100%, o badge muda para o estado correspondente e os KPIs são recarregados executando `loadInputData()` (`src/api/static/index.html`).

---

## Fluxos Alternativos

*   **Falha ou Erro no Polling (status `failed`)**: O timer de polling é interrompido, a barra de progresso visual altera para cor vermelha de alerta, o badge passa a ser `failed` e a mensagem de erro retornada no log de erros da tarefa é renderizada na caixa de status da UI (`src/api/static/index.html`).
*   **Concorrência de Disparos de IA**: Se a chamada POST retornar `409 Conflict` (IA ativa rodando no backend), a interface emite um alerta Javascript informando ao usuário e bloqueando novas tentativas (`src/api/static/index.html`).

---

## Dependências

*   **Google Fonts (Inter)**: Importado externamente via CDN para padronização tipográfica premium (`src/api/static/index.html`).
*   **Vanilla CSS3 / Vanilla Javascript**: A SPA não consome bibliotecas ou frameworks pesados como React ou jQuery, rodando inteiramente de forma nativa e rápida no navegador (`src/api/static/index.html` e `src/api/static/index.css`).

---

## Decisões de Design Identificadas

| Decisão | Evidência no código | Confiança |
|---------|---------------------|-----------|
| **Estilo Dark Mode Nativo**: Uso de variáveis CSS no escopo `:root` permitindo alteração fluida de paleta de cores. | `src/api/static/index.css:12-25` | 🟢 |
| **Glassmorphism**: Aplicação de filtros de blur translúcidos para criar profundidade e estética premium nos painéis de cards. | `src/api/static/index.css:40-42` | 🟢 |
| **Animação Shimmer de Carregamento**: Gradiente linear animado simulando esqueleto de loading fluido durante o fetch de dados. | `src/api/static/index.css:98` | 🟢 |
| **Fila Polling a cada 1000ms**: Acompanhamento dinâmico do estado do worker em background via Javascript nativo. | `src/api/static/index.html` | 🟢 |

---

## Estado Interno

*   **Identificador de Tarefa (`taskId`)**: String. Mantém em memória do cliente a referência do UUID da tarefa de alocação ativa.
*   **Timer de Polling (`pollInterval`)**: Objeto timer JS. Referência do `setInterval` ativo que executa a checagem no backend.

---

## Observabilidade

*   **Auditoria de Console**: Logs gerados por `console.log` e `console.error` no navegador rastreando as chamadas assíncronas feitas às APIs.

---

## Riscos e Lacunas

*   🔴 **DESACOPLAMENTO E MOCK DE RESULTADOS (CRÍTICO)**: Como a API do backend não expõe endpoints dinâmicos para execução e status, o script do frontend está configurado com dados mockados estáticos. O polling é disparado mas os resultados preenchidos nos cards de KPI (ocupação de `"78.5%"`, economia energética de `"25.0%"`, bloco de origem `"Bloco C"` e 3 conflitos resolvidos) são strings fixas injetadas diretamente via código no script do `index.html`. A interface gráfica não renderiza os resultados dinâmicos gerados de fato pela alocação da IA do backend.
