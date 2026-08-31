# Unit: painel-ocupacao, Tarefas de Implementação

> Roteiro de tarefas sequenciais para a reconstrução/implementação da unidade de interface visual administrativa.

## Pré-requisitos
- Interface web estática servida em servidor HTTP REST.
- Acesso à API FastAPI nos endpoints `/api/v1/allocation/...` e `/api/v1/rooms`.
- Biblioteca de fontes Google Font Inter integrada.

## Tarefas

- [ ] **T-01: Estruturação do Markup HTML5 da SPA**
  - **Origem no legado**: [`src/api/static/index.html:1-124`](file:///c:/csalas/src/api/static/index.html#L1-L124)
  - **Critério de pronto**: Criar a marcação HTML de cartões KPI (Ocupação, Economia, Blocos, Conflitos), os painéis de carregamento de progresso da IA, tabela de auditoria de leilões e controles de formulário.
  - **Confiança**: 🟢
- [ ] **T-02: Implementação dos Estilos CSS e Animações**
  - **Origem no legado**: [`src/api/static/index.css:1-158`](file:///c:/csalas/src/api/static/index.css#L1-L158)
  - **Critério de pronto**: Definir variáveis CSS de tema escuro, layouts responsivos, painéis com efeito glassmorphism (desfoque backdrop) e a animação do esqueleto shimmer de carregamento assíncrono.
  - **Confiança**: 🟢
- [ ] **T-03: Lógica JS de Integração e Polling Assíncrono**
  - **Origem no legado**: [`src/api/static/index.html:125-253`](file:///c:/csalas/src/api/static/index.html#L125-L253)
  - **Critério de pronto**: Programar o fetch assíncrono de dados de entrada na inicialização, o disparo de alocação de IA (com desativação do botão) e a recursividade de polling de status a cada 1000ms com transições de badges.
  - **Confiança**: 🟢

---

## Tarefas de Teste

- [ ] **TT-01: Teste visual de estados e Shimmer placeholders**
  - **Origem no legado**: [`tests/test_ui_states.py`](file:///c:/csalas/tests/test_ui_states.py)
  - **Critério de pronto**: Verificar que, durante requisições de rede pendentes, a interface exibe corretamente placeholders de esqueleto shimmer e oculta dados antigos.
- [ ] **TT-02: Teste de simulação de transição de polling assíncrono**
  - **Origem no legado**: [`tests/test_ui_states.py`](file:///c:/csalas/tests/test_ui_states.py)
  - **Critério de pronto**: Mockar o endpoint de status e verificar se a barra de progresso avança e os badges refletem queued/running/completed/failed em conformidade com o backend.

---

## Ordem Sugerida
1. **T-01** (Estrutura HTML) e **T-02** (Estilização CSS).
2. **T-03** (Controlador JS e chamadas HTTP).
3. Testes dinâmicos de interface (**TT-01**, **TT-02**).

---

## Lacunas Pendentes (🔴)
- **Renderização Dinâmica Pós-Execução**: Modificar a lógica JS do `index.html` para que, ao finalizar o polling da tarefa, a tabela e KPIs leiam e preencham as informações diretamente a partir do objeto `result_summary` real de resposta do backend, abandonando os dados estáticos mockados no código do cliente.
