# Data Delta: Landing Page Institucional, Auto-Cadastro e Login com RBAC

> Identificador: `020-landing-page-login-rbac`
> Data: `2026-08-26`

## 1. Resumo do Delta

Inclusão da tabela `User` (`users`) no banco de dados SQLite para suportar autenticação local segura, papéis de permissão (RBAC) e o ciclo de aprovação de novos cadastros pelo gestor.

## 2. Nova Entidade: `User` (`src/models.py`)

```python
class User(Base):
    __tablename__ = 'User'
    
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="docente", nullable=False)  # "gestor", "coordenador", "docente"
    department = Column(String, default="Geral", nullable=False)
    is_active = Column(Boolean, default=False, nullable=False)  # Pendente de aprovação por padrão
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
```

## 3. Dicionário de Dados

| Campo | Tipo | Nulo? | Padrão | Descrição |
|-------|------|-------|--------|-----------|
| `id` | String (UUID) | Não | UUID4 | Identificador único do usuário |
| `name` | String | Não | - | Nome completo do usuário |
| `email` | String | Não | - | E-mail institucional (único no sistema) |
| `password_hash` | String | Não | - | Hash criptográfico da senha (bcrypt) |
| `role` | String | Não | `"docente"` | Papel de acesso: `gestor`, `coordenador` ou `docente` |
| `department` | String | Não | `"Geral"` | Departamento acadêmico ou curso |
| `is_active` | Boolean | Não | `False` | `True` = conta aprovada; `False` = aguardando aprovação |
| `created_at` | DateTime | Não | `utcnow()` | Data e hora de criação da conta |

## 4. Estratégia de Inicialização / Seed

Na inicialização da aplicação (`src/database.py` / `src/main.py`), a tabela é criada automaticamente se não existir. Se a tabela estiver vazia, um usuário administrador padrão é provisionado:
- **E-mail:** `admin@classsync.ai`
- **Senha padrão:** `admin123` (criptografada com bcrypt)
- **Role:** `gestor`
- **Status:** `is_active: True`
