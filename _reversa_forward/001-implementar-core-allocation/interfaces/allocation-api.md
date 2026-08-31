# Interface: allocation-api

Este documento descreve os contratos de integração HTTP expostos pelo motor de IA do ClassSync AI para controle e consulta de execuções de alocação de salas.

---

## 1. Disparar Execução de Alocação

*   **Método:** `POST`
*   **Path:** `/api/v1/allocation/run`
*   **Autenticação:** JWT (Role `Infrastructure` obrigatória)
*   **Request Headers:**
    *   `Content-Type: application/json`
    *   `Authorization: Bearer <token>`
*   **Request Body:** (Vazio)

### Respostas

#### `202 Accepted`
Indica que a alocação foi enviada com sucesso para a fila de processamento assíncrona.
*   **Response Body:**
    ```json
    {
      "task_id": "8f219b22-8356-4c40-9a2c-15a9b75249f0",
      "status": "queued",
      "message": "Processamento de alocação enviado para a fila com sucesso."
    }
    ```

#### `401 Unauthorized`
Token de autenticação ausente ou inválido.

#### `403 Forbidden`
Usuário não possui privilégios de administrador de infraestrutura.

#### `409 Conflict`
Já existe uma rodada de alocação em andamento ativa.

---

## 2. Consultar Status da Alocação

*   **Método:** `GET`
*   **Path:** `/api/v1/allocation/status/{task_id}`
*   **Autenticação:** JWT (Roles `Coordination` ou `Infrastructure`)
*   **Request Headers:**
    *   `Authorization: Bearer <token>`

### Respostas

#### `200 OK`
Status da tarefa consultado com sucesso.
*   **Response Body:**
    ```json
    {
      "task_id": "8f219b22-8356-4c40-9a2c-15a9b75249f0",
      "status": "completed",
      "progress": 100,
      "started_at": "2026-08-07T14:10:00Z",
      "completed_at": "2026-08-07T14:10:45Z",
      "result": {
        "allocated_classes": 145,
        "conflits_resolved_by_auction": 12,
        "pending_arbitration_rooms": 0,
        "deactivated_blocks": ["Bloco C"],
        "estimated_energy_saving_percentage": 25.4
      }
    }
    ```

#### `200 OK` (Em Execução)
*   **Response Body:**
    ```json
    {
      "task_id": "8f219b22-8356-4c40-9a2c-15a9b75249f0",
      "status": "running",
      "progress": 65,
      "started_at": "2026-08-07T14:10:00Z",
      "completed_at": null,
      "result": null
    }
    ```

#### `200 OK` (Pendente de Arbitragem)
*   **Response Body:**
    ```json
    {
      "task_id": "8f219b22-8356-4c40-9a2c-15a9b75249f0",
      "status": "pending_arbitration",
      "progress": 95,
      "started_at": "2026-08-07T14:10:00Z",
      "completed_at": null,
      "result": {
        "allocated_classes": 143,
        "conflits_resolved_by_auction": 10,
        "pending_arbitration_rooms": 2,
        "unresolved_conflict_details": [
          {
            "room_id": "99ee7012-70b1-41ee-b91c-b26a575b6d19",
            "time_slot": "M1",
            "reason": "Empate persistente sem créditos entre Letras e Engenharia."
          }
        ]
      }
    }
    ```

#### `404 Not Found`
ID da tarefa (`task_id`) não encontrado no banco de dados.
