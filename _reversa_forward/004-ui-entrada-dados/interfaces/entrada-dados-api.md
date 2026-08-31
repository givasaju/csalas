# Interface: Entrada de Dados API Contract

## Visão Geral dos Endpoints Consumidos

### 1. `POST /api/v1/rooms`
- **Cabeçalho:** `Authorization: Bearer <token>`
- **Request Body:**
  ```json
  {
    "block_id": "Bloco A",
    "name": "Sala A-101",
    "capacity": 50,
    "room_type": "common",
    "is_accessible": true,
    "features": ["ar_condicionado", "projetor"]
  }
  ```
- **Responses:**
  - `201 Created`: Retorna o objeto da sala criada.
  - `409 Conflict`: Sala com mesmo nome já existe no bloco.
  - `422 Unprocessable Entity`: Validação de esquema falhou.

### 2. `POST /api/v1/rooms/import-csv`
- **Cabeçalho:** `Authorization: Bearer <token>`
- **Request Body:** Multipart `file`
- **Responses:**
  - `200 OK`: `{"message": "Importação em lote concluída com sucesso.", "imported_count": N}`
  - `400 Bad Request`: Formato ou cabeçalho do CSV inválido.
  - `422 Unprocessable Entity`: Linha com dados inválidos (Tudo ou Nada).

### 3. `POST /api/v1/allocation/restrictions`
- **Cabeçalho:** `Authorization: Bearer <token>`
- **Request Body:**
  ```json
  {
    "teacher_id": "prof-001",
    "day_of_week": 1,
    "time_slot_id": "M1"
  }
  ```
- **Responses:**
  - `201 Created`: Retorna o registro da restrição.
  - `404 Not Found`: Professor não encontrado.
  - `409 Conflict`: Indisponibilidade já cadastrada.

### 4. `DELETE /api/v1/allocation/restrictions`
- **Cabeçalho:** `Authorization: Bearer <token>`
- **Responses:**
  - `200 OK`: `{"message": "Reset semestral das restrições horárias executado com sucesso.", "cleared_count": N}`

### 5. `GET /api/v1/allocation/input-data`
- **Cabeçalho:** `Authorization: Bearer <token>`
- **Responses:**
  - `200 OK`: Retorna objeto com `{ rooms, coordinations, classes, teachers, restrictions }`

### 6. `DELETE /api/v1/rooms/{room_id}`
- **Cabeçalho:** `Authorization: Bearer <token>`
- **Responses:**
  - `200 OK`: `{"message": "Sala 'Sala A-101' excluída com sucesso do bloco 'Bloco A'."}`
  - `409 Conflict`: Não é possível excluir salas enquanto rodadas de alocação de IA estiverem executando.
