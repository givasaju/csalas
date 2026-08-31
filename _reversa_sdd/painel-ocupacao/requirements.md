# Unit: painel-ocupacao (Painel de Monitoramento de Ocupação)

> Especificação de requisitos para a unidade de interface web estática (Dashboard) de monitoramento e auditoria predial.

## Visão Geral
Este componente fornece a interface gráfica de página única (SPA) para os diretores de infraestrutura (Isabela) e coordenadores de curso. Ele possibilita acompanhar os indicadores prediais do campus, disparar rodadas de otimização de IA, visualizar o progresso em tempo real e auditar lances de leilões concorrenciais efetuados pelo motor.

## Responsabilidades
- Apresentar cartões informativos de KPIs do campus: Taxa de Ocupação Geral, Economia de Energia predial, Blocos Desativados e Conflitos Resolvidos por leilão.
- Disponibilizar tabela de auditoria e extrato histórico de transações de lances do leilão cooperativo.
- Permitir disparar assincronamente a otimização de IA de distribuição de salas.
- Executar polling recursivo de status para acompanhar o progresso de tarefas ativas, atualizando dinamicamente barras de carregamento e badges de status.
- Implementar uma interface Dark Mode moderna e fluida usando CSS3 puro, aplicando efeitos glassmorphism e animações de esqueleto de carregamento (shimmer).

## Regras de Negócio

*   **RN-01: Autenticação de Requisições de UI**: Toda chamada AJAX efetuada pelos scripts do dashboard para endpoints do backend deve injetar o cabeçalho `Authorization: Bearer mock-token` para validação na API REST. 🟢 (Evidência: `src/api/static/index.html` via Ajax Headers)
*   **RN-02: Bloqueio de Disparo por Concorrência**: O botão de "Disparar Alocação de IA" deve ser desabilitado se houver outra tarefa rodando ou se a API responder com status `409 Conflict`, evitando múltiplos processamentos concorrentes. 🟢 (Evidência: `src/api/static/index.html` em `triggerAllocation()`)
*   **RN-03: Frequência e Loop de Polling**: Após o disparo da tarefa, a interface deve iniciar um loop de consulta assíncrona (polling) a cada 1000ms no endpoint `/api/v1/allocation/status/{taskId}` para atualizar o painel até que a tarefa retorne status de parada (`completed`, `pending_arbitration` ou `failed`). 🟢 (Evidência: `src/api/static/index.html` em `pollTaskStatus()`)
*   **RN-04: Atualização Dinâmica da Barra de Progresso**: O componente visual de barra de progresso deve sincronizar sua largura de 0% a 100% de forma proporcional ao valor numérico contido na propriedade `progress` retornada no polling. 🟢 (Evidência: `src/api/static/index.html` em `pollTaskStatus()`)
*   **RN-05: Cores de Badges por Status de Tarefa**: O badge de status visual no cabeçalho deve alterar sua cor de acordo com o estado da tarefa de alocação de IA ativa:
    *   `queued`: Badge Azul/Ardósia. 🟡
    *   `running`: Badge Roxo/Indigo com efeito piscante. 🟡
    *   `completed`: Badge Verde Esmeralda. 🟡
    *   `pending_arbitration`: Badge Laranja. 🟡
    *   `failed`: Badge Vermelho. 🟡
*   **RN-06: Estética Visual Premium**: O painel deve empregar paleta Dark Mode usando a fonte Google Font `Inter`, com painéis semitransparentes em glassmorphism (`backdrop-filter: blur(12px)`) e efeitos shimmer (gradientes lineares animados de 1.5s) para representar estados de loading. 🟢 (Evidência: `src/api/static/index.css`)

---

## Requisitos Funcionais

| ID | Requisito | Prioridade | Critério de Aceite |
|----|-----------|-----------|-------------------|
| RF-01 | Renderização de KPIs do campus. | Must | Validar que o painel apresenta Ocupação, Economia Energética, Blocos Desativados e Contagem de Conflitos após ler dados da API. |
| RF-02 | Tabela de Auditoria de Leilões. | Must | Validar que cada lance do leilão cooperativo (sala, slot, vencedor, perdedor e créditos pagos) é listado com clareza. |
| RF-03 | Disparo assíncrono de alocação de IA. | Must | Validar que o clique no botão envia o POST de execução, recebe o task_id e inicia a barra em 0%. |
| RF-04 | Acompanhamento visual da tarefa via polling. | Must | Validar que a barra cresce de acordo com o progresso do worker e o badge reflete queued/running/completed no polling. |

---

## Requisitos Não Funcionais

| Tipo | Requisito inferido | Evidência no código | Confiança |
|------|--------------------|---------------------|-----------|
| Usabilidade | Feedback responsivo instantâneo via animações shimmer e bloqueio de botões para evitar ações redundantes de usuários. | `src/api/static/index.css:98` | 🟢 |
| Design / Acessibilidade | Tema escuro de alto contraste utilizando fontes modernas escaláveis para leitura confortável. | `src/api/static/index.css:12-25` | 🟢 |

---

## Critérios de Aceitação

```gherkin
Dado que o usuário acessa o endereço do dashboard do ClassSync AI
Quando a página finaliza o carregamento inicial no navegador
Então o sistema deve realizar uma chamada GET /api/v1/allocation/input-data, preencher os KPIs de monitoramento e a tabela de extrato de leilões, removendo os placeholders de shimmer loading.

Dado que o usuário clica no botão "Disparar Alocação de IA"
Quando a chamada POST /api/v1/allocation/run retorna sucesso com o ID de tarefa
Então o botão de disparo deve ficar desabilitado, o badge de status deve transicionar para "queued" e o polling recursivo de 1000ms deve ser ativado.

Dado que o polling de status detecta que a propriedade "status" passou a ser "completed"
Quando a última iteração do polling finaliza
Então o timer de polling deve ser cancelado, a barra de progresso deve ser fixada em 100%, o badge deve mudar para "completed" e uma chamada de recarga de KPIs de dados de entrada deve ser executada.
```

---

## Prioridade (MoSCoW)

| Requisito | MoSCoW | Justificativa |
|-----------|--------|---------------|
| Renderização de KPIs e Dados | Must | Necessário para a Diretora Isabela visualizar o estado atual do campus letivo. |
| Disparo e Polling de IA | Must | Fluxo principal de operação para interagir com o motor assíncrono em background. |
| Estética Dark Mode / Shimmer | Should | Agrega valor à percepção estética premium do sistema, mas não impede a funcionalidade lógica direta. |
| Tabela de Auditoria de Leilões | Must | Garante transparência nos débitos e créditos acadêmicos disputados pelas coordenações. |

---

## Rastreabilidade de Código

| Arquivo | Função / Classe | Cobertura |
|---------|-----------------|-----------|
| [`src/api/static/index.html`](file:///c:/csalas/src/api/static/index.html) | `loadInputData`, `triggerAllocation`, `pollTaskStatus`, `document.DOMContentLoaded` | 🟢 |
| [`src/api/static/index.css`](file:///c:/csalas/src/api/static/index.css) | Estilos globais `:root`, cartões de status, badges, animação shimmer e responsividade mobile | 🟢 |
