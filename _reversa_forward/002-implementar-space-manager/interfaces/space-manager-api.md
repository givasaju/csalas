# Interface: space-manager-api

Este documento descreve os contratos de integração HTTP expostos pelo gerenciador acadêmico do ClassSync AI.

---

## 1. Cadastro de Sala de Aula

*   **Método:** `POST`
*   **Path:** `/api/v1/rooms`
*   **Autenticação:** JWT (Role `Infrastructure` obrigatória)
*   **Request Body:**
    ```json
    {
      "block_id": "Bloco A",
      "name": "Sala 101",
      "capacity": 45,
      "room_type": "common",
      "is_accessible": true,
      "features": ["projector"]
    }
    ```

### Respostas

#### `201 Created`
*   **Response Body:**
    ```json
    {
      "id": "7f219b22-8356-4c40-9a2c-15a9b75249f0",
      "block_id": "Bloco A",
      "name": "Sala 101",
      "capacity": 45,
      "room_type": "common",
      "is_accessible": true,
      "features": ["projector"]
    }
    ```

#### `422 Unprocessable Entity`
Erro de validação (ex: capacidade <= 0).

---

## 2. Importação de Salas via CSV

*   **Método:** `POST`
*   **Path:** `/api/v1/rooms/import-csv`
*   **Autenticação:** JWT (Role `Infrastructure` obrigatória)
*   **Request Body:** Multipart Form contendo o parâmetro `file` (arquivo CSV)

### Respostas

#### `200 OK`
*   **Response Body:**
    ```json
    {
      "message": "Importação em lote concluída com sucesso.",
      "imported_count": 25
    }
    ```

#### `400 Bad Request`
Arquivo corrompido ou colunas do cabeçalho em formato incorreto.

---

## 3. Cadastro de Indisponibilidade de Professor

*   **Método:** `POST`
*   **Path:** `/api/v1/allocation/restrictions`
*   **Autenticação:** JWT (Role `Coordination` obrigatória)
*   **Request Body:**
    ```json
    {
      "teacher_id": "8f219b22-8356-4c40-9a2c-15a9b75249f0",
      "day_of_week": 1,
      "time_slot_id": "M1"
    }
    ```

### Respostas

#### `201 Created`
*   **Response Body:**
    ```json
    {
      "id": "9f219b22-8356-4c40-9a2c-15a9b75249f0",
      "teacher_id": "8f219b22-8356-4c40-9a2c-15a9b75249f0",
      "day_of_week": 1,
      "time_slot_id": "M1"
    }
    ```

---

## 4. Obter Payload Consolidado de Dados de Insumo

*   **Método:** `GET`
*   **Path:** `/api/v1/allocation/input-data`
*   **Autenticação:** JWT

### Respostas

#### `200 OK`
*   **Response Body:**
    ```json
    {
      "rooms": [
        {
          "id": "7f219b22-8356-4c40-9a2c-15a9b75249f0",
          "block_id": "Bloco A",
          "name": "Sala 101",
          "capacity": 45,
          "room_type": "common",
          "is_accessible": true,
          "features": ["projector"]
        }
      ],
      "coordinations": [
        {
          "id": "eng",
          "name": "Engenharia",
          "credits": 1000
        }
      ],
      "classes": [
        {
          "id": "eng-101",
          "students_count": 40,
          "room_type": "common",
          "time_slot": "M1",
          "coordination_id": "eng",
          "urgency": 3,
          "require_accessibility": false
        }
      ]
    }
    ```
