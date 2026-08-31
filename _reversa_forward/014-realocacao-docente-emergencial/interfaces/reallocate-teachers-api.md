# Interface Contract: Realocação Docente Emergencial API

> Identificador: `014-realocacao-docente-emergencial`
> Data: `2026-08-13`
> Tipo: HTTP REST API

---

## 1. Endpoint: Calcular Opções de Realocação Emergencial

- **URL:** `/api/v1/emergency-reallocations/calculate`
- **Método:** `POST`
- **Headers:** `Content-Type: application/json`

### Request Body
```json
{
  "absent_teacher_id": "T001",
  "start_date": "2026-09-01",
  "end_date": "2026-10-31",
  "mode": "assisted"
}
```

### Response (200 OK)
```json
{
  "absent_teacher_id": "T001",
  "total_affected_classes": 2,
  "options": [
    {
      "option_index": 1,
      "impact_score": 1.0,
      "description": "Substituição completa por docentes da própria coordenação de Computação",
      "expanded_coordinations": false,
      "substitutions": [
        {
          "class_id": "C001",
          "substitute_teacher_id": "T005",
          "substitute_teacher_name": "Prof. Carlos Silva",
          "time_slot": "M1",
          "room_id": "R101"
        }
      ]
    }
  ]
}
```

---

## 2. Endpoint: Efetivar Realocação Emergencial

- **URL:** `/api/v1/emergency-reallocations/commit`
- **Método:** `POST`
- **Headers:** `Content-Type: application/json`

### Request Body
```json
{
  "absent_teacher_id": "T001",
  "selected_option_index": 1,
  "mode": "delegated",
  "substitutions": [
    {
      "class_id": "C001",
      "substitute_teacher_id": "T005",
      "substitute_teacher_name": "Prof. Carlos Silva",
      "time_slot": "M1",
      "room_id": "R101"
    }
  ]
}
```

### Response (200 OK)
```json
{
  "log_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "success",
  "mode_used": "delegated",
  "message": "Realocação emergencial efetivada com sucesso. Notificações enviadas aos professores substitutos."
}
```

### Erros Possíveis
- `400 Bad Request`: Docente não possui turmas alocadas no período.
- `404 Not Found`: Docente ausente ou turma não encontrada.
- `422 Unprocessable Entity`: Formato JSON inválido.
