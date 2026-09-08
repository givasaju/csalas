# Data Delta: CRUD de Gestão de Instituições e Master-Chef

> Identificador: `023-crud-instituicoes-master-chef`
> Data: `2026-09-07`

## 1. Resumo Executivo do Delta

A feature não altera as tabelas existentes do banco relacional principal. A evolução de dados ocorre em duas frentes:
1. **Esquemas Pydantic (`src/api/schemas.py`):** Criação de esquemas de requisição e resposta para consulta detalhada, atualização cadastral, exclusão assistida e redefinição de credenciais do gestor institucional.
2. **Ciclo de Vida no Sistema de Arquivos:** Introdução da estrutura de arquivamento `./data/.archived/` e manipulação pontual de credenciais no banco SQLite de cada tenant isolado (`./data/{slug}/classsync.db`).

## 2. Novos Esquemas Pydantic (`src/api/schemas.py`)

### 2.1. `TenantDetailResponse`
Esquema para retorno de detalhes aprofundados da instituição e do seu master-chef:

```python
class MasterChefInfo(BaseModel):
    id: Optional[int] = None
    email: str
    name: Optional[str] = None
    role: str = "gestor"
    must_change_password: bool = True
    is_active: bool = True

class TenantDetailResponse(BaseModel):
    name: str
    slug: str
    port: int
    url: str
    status: str  # "online", "offline", "provisioning", "error"
    created_at: Optional[str] = None
    container_name: Optional[str] = None
    master_chef: Optional[MasterChefInfo] = None
```

### 2.2. `TenantUpdateRequest`
Esquema para atualização de metadados cadastrais permitidos:

```python
class TenantUpdateRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=120, description="Nome de exibição da instituição")
    master_chef_email: Optional[EmailStr] = Field(None, description="Novo e-mail de contato do master-chef")
```

### 2.3. `MasterChefResetRequest` e `MasterChefResetResponse`
Esquemas para solicitação e confirmação de redefinição de credenciais:

```python
class MasterChefResetRequest(BaseModel):
    new_password: Optional[str] = Field(
        None, 
        min_length=6, 
        description="Nova senha provisória manual. Se nulo, o sistema gera aleatoriamente."
    )
    email: Optional[EmailStr] = Field(
        None, 
        description="Atualização opcional do e-mail do master-chef na mesma operação."
    )

class MasterChefResetResponse(BaseModel):
    slug: str
    email: str
    temporary_password: str
    must_change_password: bool = True
    message: str = "Credencial provisória gerada com sucesso. O usuário deve alterá-la no próximo login."
```

### 2.4. `TenantDeleteRequest`
Esquema de salvaguarda para exclusão/arquivamento assistido:

```python
class TenantDeleteRequest(BaseModel):
    confirm_slug: str = Field(..., description="Deve coincidir exatamente com o slug da instituição")
```

## 3. Modelo de Armazenamento e Arquivamento Físico

### 3.1. Diretório de Arquivamento (`./data/.archived/`)
- Ao deletar uma instituição com slug `faculdade_alfa`, o processo:
  1. Cria o diretório `./data/.archived/` se não existir.
  2. Move `./data/faculdade_alfa/` para `./data/.archived/faculdade_alfa_{TIMESTAMP}/` (ou `./data/.archived/faculdade_alfa/`).
  3. Renomeia `.env.faculdade_alfa` para `./data/.archived/faculdade_alfa_{TIMESTAMP}/.env`.
  4. Garante que os dados acadêmicos e auditorias não sejam destruídos.

### 3.2. Manipulação de Hash no Banco SQLite do Tenant
- Ao resetar o master-chef, o sistema abre conexão pontual com `./data/{slug}/classsync.db`:
  - Executa: `SELECT id, email, role FROM users WHERE role = 'gestor' OR email = ? LIMIT 1;`
  - Gera salt seguro e hash PBKDF2: `get_password_hash(senha_provisoria)`
  - Atualiza:
    ```sql
    UPDATE users 
    SET hashed_password = ?, must_change_password = 1, updated_at = CURRENT_TIMESTAMP
    WHERE id = ?;
    ```
  - Comita a transação e fecha imediatamente a conexão para evitar locks de arquivo.

## 4. Matriz de Compatibilidade

- **Bancos Existentes de Tenants:** Compatíveis sem necessidade de intervenção prévia.
- **Isolamento de Tenants:** O SuperAdmin não executa queries em dados pedagógicos (salas, turmas, alocações), operando unicamente na tabela `users` do tenant.
