# Legacy Impact: CRUD de Gestão de Instituições e Master-Chef

> Identificador: `023-crud-instituicoes-master-chef`
> Data: `2026-09-07`
> Política de Edição do Legado: `allowLegacyEdits: true` com caminhos autorizados em `allowedPaths` (`src/**`, `data/**`, `tests/**`, `scripts/**`, `nginx/**`, `Dockerfile`, `docker-compose.yml`, `docker-compose-proxy.yml`, `.env.example`)

## 1. Arquivos Afetados

| Arquivo afetado | Componente | Tipo | Severidade | Justificativa |
|-----------------|------------|------|------------|---------------|
| `src/api/schemas.py` | `web-app-api` (`_reversa_sdd/architecture.md#web-app-api`) | `contrato-novo` | LOW | Adição dos esquemas Pydantic `MasterChefInfo`, `TenantDetailResponse`, `TenantUpdateRequest`, `MasterChefResetRequest`, `MasterChefResetResponse`, `TenantDeleteRequest` e `TenantDeleteResponse`. |
| `src/api/routes.py` | `web-app-api` (`_reversa_sdd/architecture.md#web-app-api`) | `contrato-novo` | MEDIUM | Endpoints `GET /platform/tenants/{slug}`, `PUT /platform/tenants/{slug}`, `DELETE /platform/tenants/{slug}`, `POST /platform/tenants/{slug}/master-chef/reset` e helpers de arquivamento e manipulação de SQLite isolado. |
| `src/api/static/index.html` | `frontend-spa` (`_reversa_sdd/architecture.md#web-app-api`) | `componente-novo` | LOW | Modais de Edição Cadastral, Redefinição de Master-Chef e Exclusão Assistida com confirmação de slug, botões de ação na tabela e handlers JS reativos. |
| `tests/test_platform_tenants_api.py` | `test-suite` | `componente-novo` | LOW | Cobertura de testes automatizados para os fluxos de consulta, edição, reset de credencial, arquivamento assistido e bloqueio RBAC para papéis comuns. |

## 2. Diff Conceitual por Componente

### `web-app-api`
- **Ciclo de Vida Completo de Tenants (CRUD):** Implementação de endpoints REST dedicados para inspeção detalhada de tenant e master-chef (`GET`), atualização controlada de metadados cadastrais (`PUT`) e arquivamento assistido com liberação de portas (`DELETE`).
- **Gestão Segura de Master-Chefs (`POST .../master-chef/reset`):** Rotação de senhas com geração automática aleatória de alta entropia ou especificação manual, persistência com hash seguro PBKDF2/SHA256 diretamente no SQLite do tenant e enforcement obrigatório de `must_change_password=True`.
- **Soft Delete e Preservação de Histórico:** Descomissionamento de instâncias movendo diretórios de dados para `./data/.archived/{slug}_{timestamp}/`, desocupando a porta TCP sem destruir dados acadêmicos históricos.

### `frontend-spa`
- **Ações Contextuais por Linha:** Botões de ação rápida integrados à tabela de instituições ('Acessar', 'Editar', 'Master-Chef', 'Excluir').
- **Salvaguarda contra Ações Destrutivas:** Modal de exclusão com trava de digitação obrigatória do identificador (`slug`) exato para habilitar o botão de exclusão.
- **Transparência e Cópia de Credenciais:** Modal com gerador randômico de senhas e botão de cópia direta para a área de transferência.

## 3. Regras Preservadas

| Regra | Arquivo no Legado | Status |
|-------|-------------------|--------|
| Motor multiagente de alocação de salas (ACC / AMR / BuildingOptimizer) | `_reversa_sdd/architecture.md#core-allocation-engine` | 100% Intacto |
| Módulo de Gestão de Docentes, Ambientes e Restrições | `_reversa_sdd/architecture.md#academic-space-manager` | 100% Intacto |
| Segregação Física Multi-Tenant por container e volume desacoplado | `_reversa_sdd/addenda/021-gestao-privativa-instituicoes.md` | 100% Intacto |
| Controle de Acesso Baseado em Perfis (RBAC) e role `doctor-chef` | `_reversa_sdd/addenda/022-admin-geral-instituicoes.md` | 100% Intacto |
| Todas as suítes de testes do repositório (81/81 testes aprovados) | `tests/` | 100% Aprovados |

## 4. Regras Modificadas

| Regra Original | Nova Regra | Justificativa |
|----------------|------------|---------------|
| Instituições criadas só podiam ser consultadas em listagem genérica sem edição ou exclusão via UI | Instituições podem ser detalhadas, atualizadas e arquivadas via interface visual pelo SuperAdmin | Viabilizar manutenção contínua e ciclo de vida completo de clientes no SaaS. |
| Credenciais do master-chef só eram definidas no momento inicial de provisionamento da instância | Credenciais do master-chef podem ser redefinidas a qualquer momento pelo SuperAdmin mantendo `must_change_password=True` | Permitir suporte ágil a clientes em caso de perda de acesso ou transição de diretoria sem quebra de compliance LGPD. |
| Exclusão exigia intervenção direta via terminal no servidor | Exclusão é orquestrada pela API com soft delete em `./data/.archived/` e trava de segurança por digitação de slug | Eliminar necessidade de comandos manuais no terminal garantindo retenção de auditoria. |
