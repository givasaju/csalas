# Contrato de Interface: API de Autenticação e Gestão de Usuários (RBAC)

> Identificador: `020-landing-page-login-rbac`
> Protocolo: HTTP / REST (FastAPI)
> Formato: JSON

---

## 1. Endpoints de Autenticação

### 1.1 `POST /api/v1/auth/register`
Realiza o auto-cadastro de um novo usuário na plataforma com status inicial `is_active: false` (pendente).

- **Request Body (`application/json`):**
```json
{
  "name": "Prof. Carlos Santos",
  "email": "carlos.santos@universidade.edu.br",
  "password": "senhaSegura123",
  "department": "Engenharia"
}
```

- **Response `201 Created`:**
```json
{
  "status": "success",
  "message": "Cadastro realizado com sucesso. Sua conta está aguardando aprovação pelo gestor.",
  "user": {
    "id": "u-123456",
    "name": "Prof. Carlos Santos",
    "email": "carlos.santos@universidade.edu.br",
    "role": "docente",
    "department": "Engenharia",
    "is_active": false
  }
}
```

- **Erros:**
  - `400 Bad Request`: E-mail já cadastrado ou dados inválidos.

---

### 1.2 `POST /api/v1/auth/login`
Autentica o usuário e emite o token de acesso JWT.

- **Request Body (`application/json`):**
```json
{
  "email": "carlos.santos@universidade.edu.br",
  "password": "senhaSegura123"
}
```

- **Response `200 OK` (Conta Aprovada):**
```json
{
  "access_token": "eyJhbGciOi...",
  "token_type": "bearer",
  "user": {
    "id": "u-123456",
    "name": "Prof. Carlos Santos",
    "email": "carlos.santos@universidade.edu.br",
    "role": "docente",
    "department": "Engenharia"
  }
}
```

- **Response `403 Forbidden` (Conta Pendente):**
```json
{
  "detail": "Conta aguarda aprovação pelo gestor da plataforma."
}
```

- **Erros:**
  - `401 Unauthorized`: Credenciais incorretas (e-mail ou senha inválidos).

---

### 1.3 `GET /api/v1/auth/me`
Retorna as informações do usuário logado baseado no Bearer Token.

- **Headers:** `Authorization: Bearer <token>`
- **Response `200 OK`:**
```json
{
  "id": "u-123456",
  "name": "Prof. Carlos Santos",
  "email": "carlos.santos@universidade.edu.br",
  "role": "docente",
  "department": "Engenharia"
}
```

---

## 2. Endpoints de Gestão de Usuários (Acesso Restrito: Gestor / Admin)

### 2.1 `GET /api/v1/users`
Lista todos os usuários cadastrados e seus status de aprovação.

- **Headers:** `Authorization: Bearer <token-gestor>`
- **Response `200 OK`:**
```json
[
  {
    "id": "u-123456",
    "name": "Prof. Carlos Santos",
    "email": "carlos.santos@universidade.edu.br",
    "role": "docente",
    "department": "Engenharia",
    "is_active": false,
    "created_at": "2026-08-26T18:00:00Z"
  }
]
```

---

### 2.2 `PATCH /api/v1/users/{user_id}/status`
Atualiza o status de ativação e o papel de um usuário.

- **Headers:** `Authorization: Bearer <token-gestor>`
- **Request Body (`application/json`):**
```json
{
  "is_active": true,
  "role": "coordenador"
}
```

- **Response `200 OK`:**
```json
{
  "id": "u-123456",
  "name": "Prof. Carlos Santos",
  "email": "carlos.santos@universidade.edu.br",
  "role": "coordenador",
  "department": "Engenharia",
  "is_active": true
}
```
