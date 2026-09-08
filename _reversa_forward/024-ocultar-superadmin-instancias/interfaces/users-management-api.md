# Interface: API de Gestão de Usuários Institucionais

> Identificador: `024-ocultar-superadmin-instancias`
> Protocolo: `HTTP/REST`
> Rota base: `/api/v1/users`

## 1. Endpoint: Listar Usuários da Instituição

Retorna a lista de usuários acadêmicos cadastrados para gestão pelo gestor institucional, com omissão de contas globais de plataforma (`doctor-chef`).

- **Método:** `GET`
- **Caminho:** `/api/v1/users`
- **Autenticação:** Obrigatória (`Bearer <JWT>`, roles permitidas: `gestor`, `admin`).
- **Idempotência:** Sim (operação de leitura).

### Resposta de Sucesso (HTTP 200 OK)

```json
[
  {
    "id": "u-001",
    "name": "Gestor Principal",
    "email": "admin@classsync.ai",
    "role": "gestor",
    "department": "Administração Geral",
    "is_active": true,
    "created_at": "2026-09-08T12:00:00"
  },
  {
    "id": "u-docente-01",
    "name": "Prof. Carlos Silva",
    "email": "carlos@universidade.edu.br",
    "role": "docente",
    "department": "Engenharia de Software",
    "is_active": true,
    "created_at": "2026-09-08T12:05:00"
  }
]
```

### Respostas de Erro

- **401 Unauthorized:** Token JWT ausente, expirado ou inválido.
- **403 Forbidden:** Usuário autenticado não possui papel com privilégio administrativo local (`gestor` ou `admin`).

---

## 2. Endpoint: Atualizar Status e Papel de Usuário

Atualiza o status de ativação (`is_active`) e/ou o papel (`role`) de um usuário cadastrado na base institucional.

- **Método:** `PATCH`
- **Caminho:** `/api/v1/users/{user_id}/status`
- **Autenticação:** Obrigatória (`Bearer <JWT>`, roles permitidas: `gestor`, `admin`).
- **Idempotência:** Não estrita (modificação de estado).

### Corpo da Requisição (`application/json`)

```json
{
  "is_active": true,
  "role": "coordenador"
}
```

### Resposta de Sucesso (HTTP 200 OK)

```json
{
  "id": "u-docente-01",
  "name": "Prof. Carlos Silva",
  "email": "carlos@universidade.edu.br",
  "role": "coordenador",
  "department": "Engenharia de Software",
  "is_active": true,
  "created_at": "2026-09-08T12:05:00"
}
```

### Respostas de Erro

- **401 Unauthorized:** Token JWT ausente, expirado ou inválido.
- **403 Forbidden (Tentativa de alteração de superadministrador):**
  ```json
  {
    "detail": "Não é permitido alterar o status ou o papel de contas de administração global (doctor-chef)."
  }
  ```
- **404 Not Found:** Usuário não encontrado no banco de dados da instituição.
