# Regression Watch: Landing Page de Apresentação Institucional, Auto-Cadastro e Login com RBAC

> Identificador: `020-landing-page-login-rbac`
> Data: `2026-08-26`

## 1. Itens de Vigilância de Regressão

| ID | Origem (arquivo, seção) | Regra esperada após mudança | Tipo de verificação | Sinal de violação |
|----|-------------------------|-----------------------------|---------------------|-------------------|
| W001 | `_reversa_sdd/architecture.md#web-app-api` | Rota raiz `/` deve servir a Landing Page com Hero, Recursos de IA e botões de Login e Cadastro. | `presença` | Falha ao carregar a Landing Page ou retorno de tela em branco. |
| W002 | `_reversa_sdd/inventory.md#src/api/routes.py` | Endpoints `/api/v1/auth/register`, `/api/v1/auth/login` e `/api/v1/auth/me` devem responder com status codes e contratos padronizados. | `presença` | Falha nos endpoints de autenticação ou quebra nos testes `test_auth_rbac.py`. |
| W003 | `_reversa_sdd/architecture.md#database` | Tabela `User` deve ser mantida com campos `email`, `password_hash`, `role` e `is_active`. | `presença` | Erro ao consultar ou persistir usuários no SQLite. |
| W004 | `_reversa_sdd/c4-context.md#personas` | Endpoints de gestão (`/api/v1/users`) devem rejeitar requisições de perfis não autorizados com HTTP 403 Forbidden. | `presença` | Usuário docente conseguir listar ou alterar outros usuários. |

## 2. Histórico de re-extrações

*(Vazio - será preenchido nas próximas re-extrações `/reversa`)*

## 3. Arquivadas

*(Vazio)*

## 4. Observações

- Suíte de testes automatizados `pytest` executada e 100% aprovada (67/67 testes passando).
