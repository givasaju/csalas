# Data Delta: occupancy-dashboard

Este documento descreve as estruturas de dados e variáveis de estado necessárias na interface visual React para gerenciar e apresentar os dados prediais e de leilões.

---

## 1. Mapeamento de Estado do Dashboard (React Component State)

```typescript
interface DashboardState {
  kpis: {
    overallOccupancyPercentage: number;   // Taxa de ocupação geral (ex: 78.5)
    estimatedEnergySaving: number;        // Economia de energia em percentage (ex: 25.0)
    deactivatedBlocks: string[];          // Lista de blocos prediais desativados
    totalResolvedConflicts: number;       // Quantidade de leilões efetuados
  };
  auctionsList: AuctionBidItem[];         // Extrato de auditoria de lances
  activeTask: {
    taskId: string | null;
    status: 'idle' | 'queued' | 'running' | 'completed' | 'failed' | 'pending_arbitration';
    progress: number;
    errorLog: string | null;
  };
  isLoading: boolean;                     // Flag para controle do Skeleton screen
  isError: boolean;                       // Controle da tela de erro
}

interface AuctionBidItem {
  id: string;
  roomName: string;
  timeSlot: string;
  winnerCoordName: string;
  loserCoordName: string;
  creditsSpent: number;
  timestamp: string;
}
```

---

## 2. Configurações Visuais de Cores e Alertas (CSS Custom Properties)

```css
:root {
  --color-success: #10b981;          /* Verde para blocos economizados e rodadas OK */
  --color-warning: #f59e0b;          /* Amarelo para tarefas rodando e leilões ativos */
  --color-danger: #ef4444;           /* Vermelho para pendências de arbitragem e erros */
  --color-info: #3b82f6;             /* Azul para capacidade padrão e links */
  
  --animation-shimmer: shimmer 1.5s infinite linear; /* Efeito shimmer de carregamento */
}
```
