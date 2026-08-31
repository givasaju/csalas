# Interface HTTP: Allocations API

> Identificador da feature: `008-alocacao-docente-max-4-aulas`  
> Data: `2026-08-08`  

---

## 1. Endpoints

### 1.1 POST /api/v1/allocations

Cadastra uma aula de 50 minutos para um professor em uma sala.

- **Método**: `POST`
- **Headers**:
  - `Authorization: Bearer <token>` (Obrigatório)
  - `Content-Type: application/json`
- **Payload de Requisição**:
  ```json
  {
    "teacher_id": "prof-001",
    "room_id": "sala-a101",
    "day_of_week": 1,
    "shift": "M",
    "sub_slot": 1
  }
  ```
- **Respostas**:
  - `201 Created`:
    ```json
    {
      "id": "alloc-uuid-1234",
      "teacher_id": "prof-001",
      "room_id": "sala-a101",
      "day_of_week": 1,
      "shift": "M",
      "sub_slot": 1,
      "created_at": "2026-08-08T11:45:00Z"
    }
    ```
  - `409 Conflict`: 5ª aula seguida no mesmo turno ou sala ocupada.
  - `404 Not Found`: Professor ou sala não cadastrados.
  - `401 Unauthorized`: Token ausente ou inválido.

---

### 1.2 GET /api/v1/allocations

Lista as alocações cadastradas com suporte a filtros.

- **Método**: `GET`
- **Headers**: `Authorization: Bearer <token>`
- **Query Params**: `teacher_id`, `room_id`, `shift`, `day_of_week`
- **Resposta**: `200 OK` (Array de alocações).

---

### 1.3 DELETE /api/v1/allocations/{id}

Remove uma alocação cadastrada.

- **Método**: `DELETE`
- **Headers**: `Authorization: Bearer <token>`
- **Resposta**: `200 OK`.
