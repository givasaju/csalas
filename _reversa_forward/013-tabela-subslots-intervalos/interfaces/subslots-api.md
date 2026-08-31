# Contrato de Interface HTTP: Subslots API

> Identificador: `013-tabela-subslots-intervalos`
> Contrato: `Subslots API`
> Protocolo: HTTP REST / JSON

## 1. Endpoints

### 1.1 Listar Subslots (`GET /api/v1/subslots`)

Retorna a lista de subslots de horários cadastrados no sistema, podendo filtrar por turno.

#### Parâmetros de Query

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| `shift` | string | Não | Filtra por turno (`matutino`, `vespertino`, `noturno`) |

#### Exemplo de Resposta (200 OK)

```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440001",
    "code": "M1",
    "shift": "matutino",
    "class_number": 1,
    "start_time": "07:00",
    "end_time": "07:50",
    "is_interval": false
  },
  {
    "id": "550e8400-e29b-41d4-a716-446655440004",
    "code": "M_INT",
    "shift": "matutino",
    "class_number": null,
    "start_time": "09:30",
    "end_time": "09:45",
    "is_interval": true
  }
]
```

---

### 1.2 Criar Subslot (`POST /api/v1/subslots`)

Cadastra um novo subslot no banco de dados.

#### Exemplo de Payload Request (POST)

```json
{
  "code": "M6",
  "shift": "matutino",
  "class_number": 6,
  "start_time": "11:25",
  "end_time": "12:15",
  "is_interval": false
}
```

#### Exemplo de Resposta (201 Created)

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440019",
  "code": "M6",
  "shift": "matutino",
  "class_number": 6,
  "start_time": "11:25",
  "end_time": "12:15",
  "is_interval": false
}
```

#### Códigos de Erro

- `400 Bad Request`: Horário de término anterior ao início ou formato inválido.
- `409 Conflict`: O código informado em `code` já está cadastrado.
- `401 Unauthorized`: Token de autorização ausente ou inválido.

---

### 1.3 Atualizar Subslot (`PUT /api/v1/subslots/{subslot_id}`)

Atualiza as informações de um subslot existente.

---

### 1.4 Excluir Subslot (`DELETE /api/v1/subslots/{subslot_id}`)

Remove um subslot do sistema.

#### Resposta Esperada (204 No Content)
