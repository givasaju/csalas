# Legacy Impact: Landing Page de Apresentação Institucional, Auto-Cadastro e Login com RBAC

> Identificador: `020-landing-page-login-rbac`
> Data: `2026-08-26`

## 1. Arquivos Afetados

| Arquivo afetado | Componente | Tipo | Severidade | Justificativa |
|-----------------|------------|------|------------|---------------|
| `src/models.py` | `database-schema` (`_reversa_sdd/architecture.md#database`) | `delta-de-dados` | LOW | Adição da entidade `User` com atributos de conta, hash de senha e papel RBAC. |
| `src/database.py` | `database-schema` (`_reversa_sdd/architecture.md#database`) | `regra-nova` | LOW | Adição da rotina `seed_users()` para provisionar o administrador padrão inicial. |
| `src/api/auth.py` | `jwt-auth-service` (`_reversa_sdd/c4-context.md#personas`) | `componente-alterado` | MEDIUM | Hashing criptográfico de senhas (PBKDF2-SHA256/bcrypt), claims no JWT e middleware `require_roles`. |
| `src/api/schemas.py` | `web-app-api` (`_reversa_sdd/architecture.md#web-app-api`) | `contrato-novo` | LOW | Inclusão de schemas Pydantic de cadastro, login e atualização de usuários. |
| `src/api/routes.py` | `web-app-api` (`_reversa_sdd/architecture.md#web-app-api`) | `contrato-novo` | MEDIUM | Endpoints `/api/v1/auth/register`, `/api/v1/auth/login`, `/api/v1/auth/me`, `/api/v1/users`, `/api/v1/users/{id}/status`. |
| `src/api/static/index.html` | `frontend-spa` (`_reversa_sdd/inventory.md#src/api/static/index.html`) | `componente-alterado` | MEDIUM | Landing Page institucional pública, modais de auth e gestão de contas no SPA. |
| `src/api/static/index.html` | `frontend-spa` (`_reversa_sdd/inventory.md#src/api/static/index.html`) | `regra-alterada` | LOW | Emenda E001: Exibição imediata da grade de horários completa e restrição de abas para o perfil docente. |
| `src/api/static/index.css` | `frontend-spa` (`_reversa_sdd/inventory.md#src/api/static/index.css`) | `componente-novo` | LOW | Estilos da Landing Page, Hero Section, Cards de recursos e modais de autenticação. |

## 2. Diff Conceitual por Componente

### `jwt-auth-service` & `web-app-api`
- **Autenticação Local com Tokens JWT:** Emissão de tokens assinados contendo identificador, nome, departamento e papel de acesso (`gestor`, `coordenador`, `docente`).
- **Segurança de Endpoints:** Middleware declarativo `require_roles` para validação de privilégios em rotas protegidas da API FastAPI.

### `frontend-spa`
- **Fachada Pública Institucional:** Rota inicial `/` exibe a Landing Page de alta fidelidade para visitantes não autenticados, com Hero Section e apresentação dos diferenciais da IA de Alocação de Salas.
- **Auto-Cadastro com Governança:** Novos usuários entram com status pendente e aguardam aprovação pelo Gestor na seção de "Gestão de Usuários".
- **Visão Adaptativa por Papel:** Interface adapta botões e abas operacionais conforme o perfil autenticado.

## 3. Regras Preservadas

| Regra | Arquivo no Legado | Status |
|-------|-------------------|--------|
| Motor multiagente de alocação de salas (ACC / AMR / BuildingOptimizer) | `_reversa_sdd/architecture.md#core-allocation-engine` | 100% Intacto |
| Módulo de Gestão de Docentes, Ambientes e Relatórios Analíticos | `_reversa_sdd/architecture.md#academic-space-manager` | 100% Intacto |
| Compatibilidade de testes com token estático `test-valid-token` | `src/api/auth.py` | Preservada |

## 4. Regras Modificadas

| Regra Original | Nova Regra | Justificativa |
|----------------|------------|---------------|
| Plataforma abria diretamente no painel operacional sem barreira de login | Acesso inicial apresenta Landing Page institucional elegante; operações requerem autenticação por perfil | Presença pública, auto-atendimento e governança de acessos no campus. |
