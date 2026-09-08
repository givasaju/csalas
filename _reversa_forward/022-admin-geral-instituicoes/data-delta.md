# Data Delta: Interface do Administrador Geral para Gestão e Delegação de Instituições

> Identificador: `022-admin-geral-instituicoes`
> Data: `2026-09-07`

## 1. Visão Geral das Alterações de Dados

A entrega `022-admin-geral-instituicoes` estende o modelo de usuários e introduz a gestão de metadados de tenants em nível de plataforma:
1. Adição da coluna `must_change_password` na tabela `User`.
2. Adição da role global `doctor-chef` na enumeração/validação de perfis em `src/api/auth.py`.
3. Injeção da conta padrão inicial de SuperAdmin `doctor@classsync.ai` no seed de inicialização.

## 2. Tabela `User` (src/models.py)

### 2.1. Novo Campo

| Coluna | Tipo | Nulo? | Padrão | Descrição |
|---|---|---|---|---|
| `must_change_password` | `Boolean` | Não | `False` | Flag booleana que indica se o usuário deve obrigatoriamente redefinir sua senha no próximo login. Criada como `True` para o `master-chef` recém-provisionado. |

### 2.2. Migração Suave no SQLite / PostgreSQL (src/database.py)

Para garantir compatibilidade retroativa com instâncias pré-existentes:
```python
with engine.connect() as conn:
    try:
        conn.execute(text("SELECT must_change_password FROM User LIMIT 1"))
    except Exception:
        conn.execute(text("ALTER TABLE User ADD COLUMN must_change_password BOOLEAN DEFAULT 0"))
        conn.commit()
```

## 3. Seed Inicial de Usuários (src/database.py)

Garante a presença do usuário global 'doctor-chef' no banco da plataforma caso a variável `APP_ROLE=platform` ou `TENANT_NAME=platform` (ou no banco raiz):
- **Email:** `doctor@classsync.ai`
- **Nome:** "Super Administrador Geral"
- **Role:** `doctor-chef`
- **Senha Inicial:** `Doctor@2026`
- **Must Change Password:** `False`
- **Is Active:** `True`

E no provisionamento de cada novo tenant:
- **Email:** `<informado pelo doctor-chef>`
- **Nome:** "Gestor Geral Institucional"
- **Role:** `gestor` (atua como `master-chef` na instância)
- **Senha Provisória:** `<informada pelo doctor-chef>`
- **Must Change Password:** `True`
- **Is Active:** `True`

## 4. Metadados de Tenants (Registro Dinâmico Desacoplado)

Para manter os bancos 100% isolados fisicamente sem criar dependência de um banco central monolítico, a API de plataforma lê os tenants instalados a partir dos arquivos `.env.*` existentes na raiz do projeto e das pastas em `./data/`:
- `tenant_name`: extraído de `.env.<tenant>` ou nome da pasta em `data/`.
- `port`: lido da variável `PORT` em `.env.<tenant>`.
- `status`: checado via healthcheck local em `http://localhost:{port}/api/v1/health`.
- `created_at`: timestamp de criação do diretório no host.

