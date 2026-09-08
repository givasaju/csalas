# Data Delta: Ocultação do Super Administrador Geral

> Identificador: `024-ocultar-superadmin-instancias`
> Data: `2026-09-08`

## 1. Resumo do Modelo de Dados

Não há criação, alteração ou exclusão de tabelas, colunas, chaves estrangeiras ou índices no banco de dados SQLite.

## 2. Entidades Avaliadas

### Entidade `User` (`src/models.py`)
- **Status:** 100% Inalterada.
- **Campos existentes:** `id`, `name`, `email`, `password_hash`, `role`, `department`, `is_active`, `must_change_password`, `created_at`, `updated_at`.
- **Comportamento da Mudança:** Apenas a consulta ORM de leitura (`db.query(models.User)`) no endpoint de listagem passa a incluir cláusula de exclusão:
  ```python
  query = db.query(models.User).filter(models.User.role != "doctor-chef")
  ```

## 3. Script de Migração

Nenhuma migração física de esquema (DDL) ou script SQL é necessária.
