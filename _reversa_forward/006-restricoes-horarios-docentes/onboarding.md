# Onboarding Executável: Gestão de Restrições Horárias Docentes

> Identificador: `006-restricoes-horarios-docentes`  
> Data: `2026-08-08`  

---

## 1. Objetivo

Este guia orienta o teste de ponta a ponta da gestão de indisponibilidades docentes e do respeito às restrições pelo motor de alocação de IA.

---

## 2. Pré-requisitos

1. Servidor executando em `http://localhost:8000`.
2. Token JWT válido (ex.: `Authorization: Bearer valid-token`).
3. Um docente cadastrado (ex.: ID `prof-claudio`).

---

## 3. Passo a Passo de Teste

### Passo 1: Cadastrar Restrição para Docente

Execute a chamada HTTP POST para registrar a indisponibilidade:

```bash
curl -X POST "http://localhost:8000/api/v1/allocation/restrictions" \
  -H "Authorization: Bearer valid-token" \
  -H "Content-Type: application/json" \
  -d '{
    "teacher_id": "prof-claudio",
    "day_of_week": 1,
    "time_slot_id": "M1"
  }'
```

**Resultado esperado:** Status `201 Created` retornando os dados da restrição cadastrada.

---

### Passo 2: Listar Restrições do Docente

```bash
curl -X GET "http://localhost:8000/api/v1/teachers/prof-claudio/restrictions" \
  -H "Authorization: Bearer valid-token"
```

**Resultado esperado:** Status `200 OK` listando a restrição recém-criada (Dia 1, Slot M1).

---

### Passo 3: Testar Bloqueio no Motor de IA

Tente simular uma alocação de turma atrelada ao `prof-claudio` no slot `M1`, dia 1:
- O motor deve recusar a alocação no slot `M1` para a turma do `prof-claudio` e buscar um slot/sala alternativa livre.

---

### Passo 4: Remover a Restrição Específica

```bash
curl -X DELETE "http://localhost:8000/api/v1/allocation/restrictions/<RESTRICTION_ID>" \
  -H "Authorization: Bearer valid-token"
```

**Resultado esperado:** Status `200 OK` confirmando a remoção da restrição.
