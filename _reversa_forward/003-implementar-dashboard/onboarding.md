# Onboarding: occupancy-dashboard

Este guia descreve os passos práticos para implantar, visualizar e validar a interface visual do ClassSync AI.

---

## 1. Instalação e Execução Local

1.  Acesse o diretório do frontend ou crie os arquivos de teste:
    ```bash
    npm install
    ```
2.  Inicie a aplicação React/Next.js local em modo de desenvolvimento:
    ```bash
    npm run dev
    ```
3.  Acesse o endereço no seu navegador:
    ```
    http://localhost:3000
    ```

---

## 2. Validação dos Cenários Visuais

### Cenário A: Visualizar Estado Carregando (Skeleton Screen)
1.  Para testar a tela de carregamento, force um atraso artificial de 3 segundos na chamada de API `/api/v1/allocation/input-data`.
2.  Confirme que os cards de KPI exibem o efeito cinza animado (Shimmer animation) e a tabela está vazia com linhas de mock temporárias.

### Cenário B: Disparar Rodada de Alocação de IA
1.  No painel superior direito, clique no botão "Disparar Alocação de IA".
2.  Verifique se o painel de status transita imediatamente para "Enfileirado" (`queued`) e depois para "Executando" com barra de progresso crescente em tempo real.
3.  Quando o processamento concluir, confirme se as métricas nos 4 cards de KPI são atualizadas na tela e a tabela de auditoria de leilões é populada com as transações de créditos.
