# Investigation: occupancy-dashboard

## 1. Pesquisa de fundo

A otimização de interfaces SPA de visualização de dados exige alta eficiência de re-renderização de componentes de gráficos. Investigamos padrões de carregamento e plotagem responsiva:

*   **Responsive SVG Containers:** Gráficos baseados em SVG (como os do Recharts) exigem cálculos de aspect ratio corretos para não estourar a grade fluida em telas de smartphones.
*   **Skeleton Loading Pattern:** O uso de telas de esqueleto melhora a percepção de tempo de resposta da aplicação pelo usuário comparado a spinners tradicionais de carregamento.

---

## 2. Alternativas avaliadas

### Alternativa A: Plotagem imperativa usando Chart.js (Canvas 2D)
*   *Descrição:* Renderizar gráficos diretamente em uma tag `<canvas>` HTML5.
*   *Prós:* Alta performance para milhares de pontos de dados de séries temporais.
*   *Contras:* A customização visual exige chamadas de API imperativas complexas e não se integra nativamente ao ciclo de vida e declaração de componentes do React, dificultando a implementação de designs responsivos avançados e temas.

### Alternativa B: Recharts SVG Declarativo (Adotada)
*   *Descrição:* Gráficos renderizados como componentes JSX React nativos sob SVG.
*   *Prós:* Altamente declarativo, controle completo de estilos CSS para hover effects, animações e redimensionamento automático.
*   *Contras:* Performance decai em plotagens contendo dezenas de milhares de elementos simultâneos (cenário não aplicável a dados resumidos de ocupação de salas de aula do ClassSync AI).

---

## 3. Padrões aplicáveis

*   **Debounced Polling Hook:** Padrão React para consulta periódica de status da API assíncrona com cancelamento seguro de timers ao desmontar o componente.
*   **Skeleton Loader Component:** Componente reutilizável para simular a geometria da tela real durante a busca assíncrona inicial de dados.
