# Regression Watch: Interface do Administrador Geral para Gestão e Delegação de Instituições

> Identificador: `022-admin-geral-instituicoes`
> Data: `2026-09-07`

## 1. Itens de Vigilância de Regressão

| ID | Origem (arquivo, seção) | Regra esperada após mudança | Tipo de verificação | Sinal de violação |
|----|-------------------------|-----------------------------|---------------------|-------------------|
| W001 | `_reversa_sdd/architecture.md#jwt-auth-service` | A role `doctor-chef` deve ter acesso exclusivo a endpoints de governança (`/api/v1/platform/tenants`), rejeitando `gestor`, `coordenador` e `docente` com HTTP 403. | `presença` | Permissão concedida a gestores comuns para provisionar novas instituições ou visualizar tenants de terceiros. |
| W002 | `_reversa_sdd/architecture.md#database` | A coluna booleana `must_change_password` na tabela `User` deve forçar redefinição no 1º acesso e ser sanitizada automaticamente nas migrações SQLite. | `presença` | Falha ao consultar tabela User por ausência de coluna ou usuários com flag True operando sem trocar a senha. |
| W003 | `_reversa_sdd/architecture.md#web-app-api` | Endpoint `POST /api/v1/platform/tenants` deve responder em até 300ms com HTTP 202 Accepted, provisionando instâncias e master-chef via `BackgroundTasks`. | `presença` | Bloqueio síncrono do event loop da FastAPI ou falha na subida das variáveis `.env` e volumes `./data/{tenant}`. |
| W004 | `_reversa_sdd/architecture.md#web-app-api` | Endpoint `POST /api/v1/auth/change-password` deve autenticar a credencial atual, exigir mínimo 8 caracteres e atualizar a flag `must_change_password` para `False`. | `presença` | Aceitação de senhas fracas (<8 chars), erro 500 no hashing PBKDF2 ou persistência indevida da flag de obrigatoriedade. |
| W005 | `tests/test_platform_tenants_api.py` | Suíte de testes automatizados cobrindo controle de acesso RBAC, provisionamento e troca de senha deve manter 100% de aprovação. | `presença` | Regressão nos testes unitários ou falha de isolamento de papéis e portas. |

## 2. Histórico de re-extrações

*(Vazio - será preenchido nas próximas re-extrações `/reversa`)*

## 3. Arquivadas

*(Vazio)*

## 4. Observações

- Suíte de testes automatizados `pytest` executada com 100% de aprovação (76/76 testes passando sem regressões no legado).
