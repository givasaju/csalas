# Guia de Onboarding e Teste Manual: Realocação Departamental de Disciplinas

> Feature: `012-realocacao-disciplinas-dept`
> Data: `2026-08-10`

---

## Passo a Passo para Teste Funcional da Feature

Este guia orienta o testador a validar a realocação departamental de disciplinas entre docentes do mesmo departamento.

### Pré-requisitos
1. Servidor ClassSync AI em execução (`python -m uvicorn src.main:app --reload` ou `pytest`).
2. Dois docentes cadastrados no mesmo departamento (ex: `Engenharia`).

---

### Passo 1: Cadastro de Docentes e Disciplinas
1. Cadastrar o docente doador:
   - **ID:** `prof-veterano`
   - **Nome:** Prof. Carlos
   - **Departamento:** `Engenharia`
   - **Disciplinas:** `["Cálculo I", "Vetores"]`
2. Cadastrar o novo docente recém-contratado:
   - **ID:** `prof-novo`
   - **Nome:** Prof. Lucas
   - **Departamento:** `Engenharia`
   - **Disciplinas:** `["Física I"]`

### Passo 2: Executar Realocação via API REST
Enviar requisição HTTP POST para `/api/v1/teachers/reallocate-subjects`:

```json
POST /api/v1/teachers/reallocate-subjects
Authorization: Bearer mock-token
Content-Type: application/json

{
  "source_teacher_id": "prof-veterano",
  "target_teacher_id": "prof-novo",
  "subjects": ["Cálculo I"]
}
```

**Resultado Esperado:**
- Status `200 OK`.
- `prof-novo` passa a ter disciplinas `["Física I", "Cálculo I"]`.
- `prof-veterano` passa a ter disciplinas `["Vetores"]`.
- Quaisquer alocações ativas da disciplina `Cálculo I` são reatribuídas para `prof-novo`.

---

### Passo 3: Teste de Validação de Departamento Distinto (Caso Negativo)
1. Tentar transferir uma disciplina de `prof-veterano` (`Engenharia`) para `prof-outra-area` (`Letras`).
2. **Resultado Esperado:** HTTP `422 Unprocessable Entity` com a mensagem `"Realocação permitida apenas entre docentes do mesmo departamento"`.

---

### Passo 4: Teste de Exigência de Disciplina Substituta (Caso de Esvaziamento)
1. Tentar transferir a única disciplina remanescente `"Vetores"` de `prof-veterano` sem informar `replacement_subject`.
2. **Resultado Esperado:** HTTP `422 Unprocessable Entity` com aviso exigindo a indicação de uma disciplina substituta.
3. Repetir a requisição incluindo `"replacement_subject": "Geometria Analítica"`.
4. **Resultado Esperado:** Status `200 OK` e `prof-veterano` assume `"Geometria Analítica"`.
