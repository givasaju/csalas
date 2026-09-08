# Interface: Platform Tenants API & Auth Handover

> Identificador: `022-admin-geral-instituicoes`
> Tipo: HTTP REST (JSON)
> Protocolo: HTTP / HTTPS

## 1. Visão Geral

Endpoints da API protegidos por JWT e autorização RBAC para governança da plataforma pelo superadministrador (`doctor-chef`) e redefinição obrigatória de senha pelo gestor geral institucional (`master-chef`).

## 2. Endpoints

### 2.1. Listar Instituições Ativas da Plataforma
- **Método:** `GET`
- **Caminho:** `/api/v1/platform/tenants`
- **Autenticação:** Bearer Token JWT (Role obrigatória: `doctor-chef`)
- **Headers:** `Authorization: Bearer <token>`
- **Resposta Sucesso (200 OK):**
```json
{
  "total": 2,
  "next_available_port": 8003,
  "tenants": [
    {
      "name": "Faculdade Alpha",
      "slug": "faculdade_alpha",
      "port": 8001,
      "status": "online",
      "url": "http://localhost:8001/",
      "created_at": "2026-09-07T12:00:00Z"
    },
    {
      "name": "Faculdade Beta",
      "slug": "faculdade_beta",
      "port": 8002,
      "status": "online",
      "url": "http://localhost:8002/",
      "created_at": "2026-09-07T13:30:00Z"
    }
  ]
}
```
- **Respostas de Erro:**
  - `401 Unauthorized`: Token ausente ou inválido.
  - `403 Forbidden`: Token válido, mas role diferente de `doctor-chef`.

---

### 2.2. Criar e Provisionar Nova Instituição
- **Método:** `POST`
- **Caminho:** `/api/v1/platform/tenants`
- **Autenticação:** Bearer Token JWT (Role obrigatória: `doctor-chef`)
- **Headers:** `Authorization: Bearer <token>`, `Content-Type: application/json`
- **Corpo da Requisição (JSON):**
```json
{
  "name": "Faculdade Gama",
  "slug": "faculdade_gama",
  "port": 8003,
  "master_chef_email": "diretor@gama.edu.br",
  "master_chef_password": "GamaProvisoria@2026"
}
```
- **Validações:**
  - `name`: string não vazia, 3 a 100 caracteres.
  - `slug`: string alfanumérica e underscores em minúsculas (`^[a-z0-9_]{3,40}$`), sem duplicidade.
  - `port`: inteiro entre 1024 e 65535, não ocupada no host.
  - `master_chef_email`: e-mail corporativo válido.
  - `master_chef_password`: mínimo 8 caracteres.
- **Resposta Sucesso (202 Accepted):**
```json
{
  "status": "provisioning",
  "message": "Provisionamento da instituição iniciado em background.",
  "tenant": {
    "name": "Faculdade Gama",
    "slug": "faculdade_gama",
    "port": 8003,
    "url": "http://localhost:8003/",
    "master_chef_email": "diretor@gama.edu.br"
  }
}
```
- **Respostas de Erro:**
  - `400 Bad Request`: Payload malformado ou campos inválidos.
  - `403 Forbidden`: Usuário não é `doctor-chef`.
  - `409 Conflict`: Slug ou porta já cadastrados e em uso.

---

### 2.3. Redefinição Obrigatória de Senha (Handover do Master-Chef)
- **Método:** `POST`
- **Caminho:** `/api/v1/auth/change-password`
- **Autenticação:** Bearer Token JWT
- **Headers:** `Authorization: Bearer <token>`, `Content-Type: application/json`
- **Corpo da Requisição (JSON):**
```json
{
  "current_password": "GamaProvisoria@2026",
  "new_password": "NovaSenhaDefinitiva#2026"
}
```
- **Resposta Sucesso (200 OK):**
```json
{
  "status": "success",
  "message": "Senha atualizada com sucesso. Seu acesso foi liberado.",
  "must_change_password": false
}
```
- **Respostas de Erro:**
  - `400 Bad Request`: Nova senha não atende aos requisitos mínimos ou igual à anterior.
  - `401 Unauthorized`: Senha atual incorreta.

