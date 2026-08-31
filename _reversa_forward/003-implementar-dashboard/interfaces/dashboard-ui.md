# Interface: dashboard-ui-integration

Este documento descreve os contratos de integração consumidos pelo painel visual do ClassSync AI.

---

## 1. Requisição das Métricas Prediais e Acadêmicas

*   **Método:** `GET`
*   **Path:** `/api/v1/allocation/input-data`
*   **Objetivo:** Alimentar a visualização dos dados cadastrados e inicializar o estado de tabelas do painel.
*   **Formato de resposta esperado:** JSON estruturado contendo a lista completa de salas, disciplinas, turmas e professores.

---

## 2. Disparar Execução em Lote da IA

*   **Método:** `POST`
*   **Path:** `/api/v1/allocation/run`
*   **Objetivo:** Disparar o cálculo inteligente e leilão de créditos em background.
*   **Formato de resposta esperado:**
    ```json
    {
      "task_id": "8f219b22-8356-4c40-9a2c-15a9b75249f0",
      "status": "queued",
      "message": "Processamento de alocação enviado para a fila com sucesso."
    }
    ```

---

## 3. Polling de Progresso da Alocação de Salas

*   **Método:** `GET`
*   **Path:** `/api/v1/allocation/status/{task_id}`
*   **Objetivo:** Consultar a porcentagem de conclusão e os resultados resumidos (blocos fechados, leilões resolvidos).
*   **Formato de resposta esperado:**
    ```json
    {
      "task_id": "8f219b22-8356-4c40-9a2c-15a9b75249f0",
      "status": "completed",
      "progress": 100,
      "result": {
        "allocated_classes": 145,
        "conflits_resolved_by_auction": 12,
        "pending_arbitration_rooms": 0,
        "deactivated_blocks": ["Bloco C"],
        "estimated_energy_saving_percentage": 25.4
      }
    }
    ```
