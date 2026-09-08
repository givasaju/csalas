# Legacy Impact: Interface do Administrador Geral para Gestão e Delegação de Instituições

> Identificador: `022-admin-geral-instituicoes`
> Data: `2026-09-07`
> Política de Edição do Legado: `allowLegacyEdits: true` com caminhos autorizados em `allowedPaths` (`src/**`, `data/**`, `tests/**`, `scripts/**`, `nginx/**`, `Dockerfile`, `docker-compose.yml`, `docker-compose-proxy.yml`, `.env.example`)

## 1. Arquivos Afetados

| Arquivo afetado | Componente | Tipo | Severidade | Justificativa |
|-----------------|------------|------|------------|---------------|
| `src/models.py` | `database-schema` (`_reversa_sdd/architecture.md#database`) | `regra-alterada` | LOW | Adição da coluna booleana `must_change_password` (default=False) e documentação da role `doctor-chef`. |
| `src/database.py` | `database-schema` (`_reversa_sdd/architecture.md#database`) | `regra-alterada` | LOW | Migração automática da coluna `must_change_password` no SQLite e seed do usuário global padrão `doctor@classsync.ai` (role `doctor-chef`). |
| `src/api/auth.py` | `jwt-auth-service` (`_reversa_sdd/c4-context.md#personas`) | `regra-alterada` | MEDIUM | Suporte à claim `must_change_password` no token JWT, validação estrita da role `doctor-chef` e dependency `require_doctor_chef`. |
| `src/api/schemas.py` | `web-app-api` (`_reversa_sdd/architecture.md#web-app-api`) | `contrato-novo` | LOW | Esquemas Pydantic `TenantCreateRequest`, `TenantResponse`, `TenantListResponse` e `ChangePasswordRequest`. |
| `src/api/routes.py` | `web-app-api` (`_reversa_sdd/architecture.md#web-app-api`) | `contrato-novo` | MEDIUM | Implementação de `GET /api/v1/platform/tenants`, `POST /api/v1/platform/tenants`, `POST /api/v1/auth/change-password`, descoberta de tenants e background task de provisionamento. |
| `scripts/deploy-institution.ps1` / `.sh` | `infra-automation` | `regra-alterada` | LOW | Parâmetros opcionais `-MasterChefEmail` e `-MasterChefPassword` com seed automático do master-chef na nova base de dados. |
| `src/api/static/index.html` | `frontend-spa` | `componente-novo` | LOW | Aba 'Administração Geral', KPIs de instâncias, formulário com sugestão de portas, listagem de tenants e modal de troca obrigatória de senha. |
| `src/api/static/index.css` | `frontend-spa` | `regra-alterada` | LOW | Classes CSS para badge de role `doctor-chef` e status de tenants (`online`, `offline`, `provisioning`). |
| `tests/test_platform_tenants_api.py` | `test-suite` | `componente-novo` | LOW | Suíte de testes automatizados com 100% de aprovação cobrindo controle RBAC, criação de instâncias e fluxo de troca de senha. |

## 2. Diff Conceitual por Componente

### `jwt-auth-service` & `database-schema`
- **Role Global Hierárquica (`doctor-chef`):** Segregação estrita entre administração da infraestrutura SaaS e administração pedagógica interna dos clientes. Usuários com papéis acadêmicos locais (`gestor`, `coordenador`, `docente`) recebem HTTP 403 Forbidden ao tentar invocar a gestão de instâncias.
- **Handover Seguro e Conformidade LGPD (`must_change_password`):** O 'master-chef' é semeado com a flag `must_change_password=True`. No primeiro login, a aplicação obriga a substituição da senha provisória cadastrada pelo operador SaaS por uma nova credencial privativa via `POST /api/v1/auth/change-password`.

### `web-app-api` & `infra-automation`
- **Provisionamento Assíncrono Desacoplado:** `POST /api/v1/platform/tenants` retorna HTTP 202 Accepted imediatamente e orquestra a criação de volumes em `./data/{slug}/`, arquivos `.env.{slug}` e o seed do master-chef através de `BackgroundTasks` da FastAPI, sem bloquear o event loop e sem expor diretamente o socket Docker.
- **Descoberta Dinâmica e Alocação Incremental de Portas:** O backend inspeciona instâncias ativas e sugere a próxima porta TCP livre a partir de 8001, mantendo flexibilidade para override manual.

### `frontend-spa`
- **Experiência Unificada na SPA:** Adicionada a aba 'Administração Geral' visível exclusivamente para usuários autenticados como `doctor-chef`, mantendo o bundle em Vanilla JavaScript e CSS sem adicionar dependências externas pesadas.

## 3. Regras Preservadas

| Regra | Arquivo no Legado | Status |
|-------|-------------------|--------|
| Motor multiagente de alocação de salas (ACC / AMR / BuildingOptimizer) | `_reversa_sdd/architecture.md#core-allocation-engine` | 100% Intacto |
| Módulo de Gestão de Docentes, Ambientes e Restrições | `_reversa_sdd/architecture.md#academic-space-manager` | 100% Intacto |
| Isolamento Físico Multi-Tenant por container e volume desacoplado | `_reversa_forward/021-gestao-privativa-instituicoes/` | 100% Intacto |
| Todas as suítes de testes anteriores (70/70 testes legados preservados) | `tests/` | 100% Aprovados (76/76 total) |

## 4. Regras Modificadas

| Regra Original | Nova Regra | Justificativa |
|----------------|------------|---------------|
| Autenticação permitia apenas papéis locais (`gestor`, `coordenador`, `docente`) | Introduzida a role global `doctor-chef` exclusiva para governança de plataforma | Viabilizar operação SaaS sem misturar escopos locais de campus. |
| Usuários criados operavam indefinidamente com a credencial inicial | Usuários com `must_change_password=True` devem obrigatoriamente redefinir a senha | Cumprimento rigoroso da LGPD e garantia de privacidade dos dados institucionais. |
