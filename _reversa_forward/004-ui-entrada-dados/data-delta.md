# Data Delta: Modelo de Dados da Entrada de Dados

## Mudanças Conceituais

Nenhum campo novo ou remoção de tabelas no backend Python. A UI consome diretamente a estrutura de dados existente exposta por `GET /api/v1/allocation/input-data`.

## Estrutura das Entidades Consumidas pela UI

### 1. Sala Física (`Room`)
```json
{
  "id": "uuid-string",
  "block_id": "string (ex: Bloco A)",
  "name": "string (ex: Sala 101)",
  "capacity": 45,
  "room_type": "common | lab | auditorium",
  "is_accessible": true,
  "features": ["ar_condicionado", "projetor"]
}
```

### 2. Indisponibilidade Docente (`Restriction`)
```json
{
  "id": "uuid-string",
  "teacher_id": "string",
  "day_of_week": 1,
  "time_slot_id": "M1 | M2 | T1 | T2 | N1 | N2"
}
```
