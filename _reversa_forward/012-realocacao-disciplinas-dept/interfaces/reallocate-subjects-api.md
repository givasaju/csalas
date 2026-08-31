# Especificação de Contrato: POST /api/v1/teachers/reallocate-subjects

> Contrato: HTTP REST  
> Feature: `012-realocacao-disciplinas-dept`  
> Data: `2026-08-10`  

---

## 1. Visão Geral do Contrato

Este endpoint realiza a realocação e transferência atômica de disciplinas lecionáveis entre dois docentes pertencentes ao **mesmo departamento acadêmico**.

- **URL:** `/api/v1/teachers/reallocate-subjects`
- **Método:** `POST`
- **Autenticação:** Requerida (`Bearer <token>`)
- **Content-Type:** `application/json`

---

## 2. Request Schema (`ReallocateSubjectsRequest`)

```json
{
  "source_teacher_id": "string (obrigatório)",
  "target_teacher_id": "string (obrigatório)",
  "subjects": ["string"] (obrigatório, lista de 1 a 6 disciplinas a transferir),
  "replacement_subject": "string (opcional, obrigatório caso o doador fique com 0 disciplinas)"
}
```

### Exemplo de Request Body
```json
{
  "source_teacher_id": "prof-veterano-123",
  "target_teacher_id": "prof-novo-456",
  "subjects": ["Cálculo I", "Álgebra Linear"],
  "replacement_subject": "Geometria Analítica"
}
```

---

## 3. Response Schema (`ReallocateSubjectsResponse`)

### Sucesso (200 OK)
```json
{
  "department": "Engenharia",
  "source_teacher": {
    "id": "prof-veterano-123",
    "name": "Prof. Carlos",
    "subjects": ["Geometria Analítica"]
  },
  "target_teacher": {
    "id": "prof-novo-456",
    "name": "Prof. Lucas",
    "subjects": ["Física I", "Cálculo I", "Álgebra Linear"]
  },
  "migrated_allocations_count": 3,
  "pending_arbitration_allocations_count": 0,
  "message": "Disciplinas e alocações realocadas com sucesso dentro do departamento Engenharia."
}
```

---

## 4. Códigos de Resposta de Erro

| HTTP Code | Condição | Body de Erro |
|-----------|----------|--------------|
| `401 Unauthorized` | Token Ausente ou Inválido | `{"detail": "Token de autorização ausente ou mal-formatado."}` |
| `404 Not Found` | Docente de Origem ou Destino não encontrado | `{"detail": "Docente 'prof-xxx' não encontrado."}` |
| `422 Unprocessable Entity` | Docentes de departamentos diferentes | `{"detail": "Realocação permitida apenas entre docentes do mesmo departamento ('Engenharia' vs 'Letras')."}` |
| `422 Unprocessable Entity` | Doador sem disciplinas e sem `replacement_subject` | `{"detail": "A transferência esvazia o rol do docente doador. Informe uma disciplina substituta em 'replacement_subject'."}` |
| `422 Unprocessable Entity` | Receptor excederia o limite máximo de 6 disciplinas | `{"detail": "O docente de destino excederia o limite máximo de 6 disciplinas (ficaria com 7)."}` |
