# Especificação de Interface: Restrictions API

> Identificador: `006-restricoes-horarios-docentes`  
> Contrato: REST / HTTP  
> Data: `2026-08-08`  

---

## 1. Endpoints

### 1.1 POST /api/v1/allocation/restrictions

Cadastra uma indisponibilidade docente.

- **Autenticação:** `Bearer <token>`
- **Request Body:**
```json
{
  "teacher_id": "prof-claudio",
  "day_of_week": 1,
  "time_slot_id": "M1"
}
```
- **Respostas:**
  - `201 Created`: Restrição cadastrada com sucesso.
  - `404 Not Found`: Professor não encontrado.
  - `409 Conflict`: Indisponibilidade duplicada.
  - `422 Unprocessable Entity`: Slot ou dia da semana inválido.

---

### 1.2 GET /api/v1/teachers/{teacher_id}/restrictions

Consulta todas as restrições cadastradas para o docente especificado.

- **Autenticação:** `Bearer <token>`
- **Respostas:**
  - `200 OK`: Array de objetos de restrição.
  - `404 Not Found`: Docente não encontrado.

---

### 1.3 DELETE /api/v1/allocation/restrictions/{restriction_id}

Remove uma restrição específica por ID.

- **Autenticação:** `Bearer <token>`
- **Respostas:**
  - `200 OK`: Restrição removida com sucesso.
  - `404 Not Found`: Restrição não encontrada.

---

### 1.4 DELETE /api/v1/allocation/restrictions

Executa a limpeza semestral de todas as restrições.

- **Autenticação:** `Bearer <token>`
- **Respostas:**
  - `200 OK`: Quantidade de restrições removidas.
