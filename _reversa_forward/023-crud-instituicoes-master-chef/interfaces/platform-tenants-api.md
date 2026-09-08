# Interface Specification: Platform Tenants CRUD API

> Identificador: `023-crud-instituicoes-master-chef`
> Contrato: `platform-tenants-crud-api`
> Tipo: HTTP (REST / JSON)
> Segurança: Bearer Token JWT obrigatório com claim `role: "doctor-chef"`

---

## 1. Visão Geral

Esta interface expande a API de governança do ClassSync AI com capacidades completas de detalhamento, atualização cadastral, arquivamento/descomissionamento e redefinição de credenciais do gestor institucional ('master-chef') das instâncias multi-tenant isoladas.

---

## 2. Endpoints

### 2.1. Obter Detalhes da Instituição e Master-Chef
- **Método:** `GET`
- **Caminho:** `/api/v1/platform/tenants/{slug}`
- **Descrição:** Retorna os metadados cadastrais, porta TCP, status do container e dados de contato do master-chef da instituição.
- **Cabeçalhos:**
  - `Authorization: Bearer <TOKEN_DOCTOR_CHEF>`
- **Resposta de Sucesso (HTTP 200 OK):**
  ```json
  {
    "name": "Faculdade Inovação",
    "slug": "faculdade_inovacao",
    "port": 8002,
    "url": "http://localhost:8002",
    "status": "online",
    "created_at": "2026-09-07T14:30:00Z",
    "container_name": "classsync_tenant_faculdade_inovacao",
    "master_chef": {
      "id": 1,
      "email": "master@inovacao.edu.br",
      "name": "Diretor Inovação",
      "role": "gestor",
      "must_change_password": false,
      "is_active": true
    }
  }
  ```
- **Respostas de Erro:**
  - `401 Unauthorized`: Token ausente, expirado ou inválido.
  - `403 Forbidden`: Token não pertence à role `doctor-chef`.
  - `404 Not Found`: Instituição com o slug especificado não encontrada.

---

### 2.2. Atualizar Metadados da Instituição
- **Método:** `PUT`
- **Caminho:** `/api/v1/platform/tenants/{slug}`
- **Descrição:** Atualiza o nome de exibição da instituição e, opcionalmente, sincroniza o e-mail cadastral do master-chef. O `slug` e a `port` são imutáveis.
- **Cabeçalhos:**
  - `Authorization: Bearer <TOKEN_DOCTOR_CHEF>`
  - `Content-Type: application/json`
- **Corpo da Requisição (JSON):**
  ```json
  {
    "name": "Centro Universitário Inovação",
    "master_chef_email": "novo.diretor@inovacao.edu.br"
  }
  ```
- **Resposta de Sucesso (HTTP 200 OK):**
  ```json
  {
    "name": "Centro Universitário Inovação",
    "slug": "faculdade_inovacao",
    "port": 8002,
    "url": "http://localhost:8002",
    "status": "online",
    "created_at": "2026-09-07T14:30:00Z",
    "container_name": "classsync_tenant_faculdade_inovacao",
    "master_chef": {
      "id": 1,
      "email": "novo.diretor@inovacao.edu.br",
      "name": "Diretor Inovação",
      "role": "gestor",
      "must_change_password": false,
      "is_active": true
    }
  }
  ```
- **Respostas de Erro:**
  - `400 Bad Request`: Payload inválido ou nome em branco.
  - `401 Unauthorized` / `403 Forbidden`: Falha de autenticação RBAC.
  - `404 Not Found`: Instituição inexistente.

---

### 2.3. Excluir / Arquivar Instituição (Soft Delete)
- **Método:** `DELETE`
- **Caminho:** `/api/v1/platform/tenants/{slug}`
- **Descrição:** Interrompe e remove o container Docker, desocupa a porta TCP e move os arquivos de dados para `./data/.archived/{slug}/`. Exige envio de confirmação com o slug exato.
- **Cabeçalhos:**
  - `Authorization: Bearer <TOKEN_DOCTOR_CHEF>`
- **Corpo da Requisição (Opcional ou via Query):**
  ```json
  {
    "confirm_slug": "faculdade_inovacao"
  }
  ```
- **Resposta de Sucesso (HTTP 200 OK):**
  ```json
  {
    "slug": "faculdade_inovacao",
    "status": "archived",
    "freed_port": 8002,
    "archived_path": "./data/.archived/faculdade_inovacao",
    "message": "Instituição arquivada e desprovisionada com sucesso. A porta 8002 está liberada."
  }
  ```
- **Respostas de Erro:**
  - `400 Bad Request`: Confirmação do slug incorreta ou ausente.
  - `401 Unauthorized` / `403 Forbidden`: Falha de autorização.
  - `404 Not Found`: Instituição inexistente.

---

### 2.4. Redefinir Credencial do Master-Chef
- **Método:** `POST`
- **Caminho:** `/api/v1/platform/tenants/{slug}/master-chef/reset`
- **Descrição:** Atualiza a senha do gestor na base isolada do tenant e força `must_change_password=True`. Gera senha aleatória forte se não fornecida no payload.
- **Cabeçalhos:**
  - `Authorization: Bearer <TOKEN_DOCTOR_CHEF>`
  - `Content-Type: application/json`
- **Corpo da Requisição (JSON - Opcional):**
  ```json
  {
    "new_password": "SenhaOpcionalManual123!",
    "email": "gestor@inovacao.edu.br"
  }
  ```
- **Resposta de Sucesso (HTTP 200 OK):**
  ```json
  {
    "slug": "faculdade_inovacao",
    "email": "gestor@inovacao.edu.br",
    "temporary_password": "SenhaOpcionalManual123!",
    "must_change_password": true,
    "message": "Credencial provisória configurada com sucesso. O usuário deverá alterá-la no primeiro acesso."
  }
  ```
- **Respostas de Erro:**
  - `400 Bad Request`: Senha não atende aos requisitos mínimos de segurança.
  - `401 Unauthorized` / `403 Forbidden`: Acesso não autorizado.
  - `404 Not Found`: Instituição ou usuário master-chef não encontrado na base.

---

## 3. Idempotência e Concorrência

- **Leitura (`GET`):** Estritamente idempotente e sem efeitos colaterais.
- **Atualização (`PUT`):** Idempotente.
- **Exclusão (`DELETE`):** Se executado mais de uma vez para o mesmo slug, a primeira chamada arquiva e retorna `200 OK`, e as subsequentes retornam `404 Not Found`.
- **Reset de Senha (`POST`):** Cada chamada atualiza o hash do usuário e marca `must_change_password = 1`.
