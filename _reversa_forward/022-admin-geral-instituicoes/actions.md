# Actions: Interface do Administrador Geral para Gestão e Delegação de Instituições

> Identificador: `022-admin-geral-instituicoes`
> Data: `2026-09-07`
> Roadmap: `_reversa_forward/022-admin-geral-instituicoes/roadmap.md`

## Resumo

| Métrica | Valor |
|---------|-------|
| Total de ações | 10 |
| Paralelizáveis (`[//]`) | 4 |
| Maior cadeia de dependência | 5 |

## Fase 1, Preparação

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T001 | Atualizar o modelo `User` em `src/models.py` adicionando o atributo booleano `must_change_password` (default=False) | - | - | `src/models.py` | 🟢 | `[X]` |
| T002 | Atualizar `src/database.py` para aplicar migração automática da coluna `must_change_password` no SQLite e semear o usuário global padrão `doctor@classsync.ai` (role `doctor-chef`) | T001 | - | `src/database.py` | 🟢 | `[X]` |
| T003 | Atualizar `src/api/auth.py` para reconhecer a role `doctor-chef`, incluir claim `must_change_password` no token JWT e implementar endpoint `POST /api/v1/auth/change-password` | T001, T002 | - | `src/api/auth.py` | 🟢 | `[X]` |

## Fase 2, Testes

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T004 | Criar a suíte de testes automatizados `tests/test_platform_tenants_api.py` cobrindo controle de acesso por role, cálculo de portas TCP, validação de payload e fluxo de troca de senha | T003 | `[//]` | `tests/test_platform_tenants_api.py` | 🟢 | `[X]` |

## Fase 3, Núcleo

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T005 | Criar esquemas Pydantic em `src/api/schemas.py` para validação de entrada e saída da plataforma (`TenantCreateRequest`, `TenantResponse`, `TenantListResponse`, `ChangePasswordRequest`) | T003 | `[//]` | `src/api/schemas.py` | 🟢 | `[X]` |
| T006 | Implementar lógica utilitária de descoberta de instâncias, cálculo incremental de portas TCP livres e orquestração assíncrona em `BackgroundTasks` | T005 | - | `src/api/routes.py` | 🟢 | `[X]` |
| T007 | Implementar os endpoints REST `GET /api/v1/platform/tenants` e `POST /api/v1/platform/tenants` protegidos com verificação de role `doctor-chef` | T006 | - | `src/api/routes.py` | 🟢 | `[X]` |

## Fase 4, Integração

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T008 | Atualizar os scripts de provisionamento `scripts/deploy-institution.ps1` e `scripts/deploy-institution.sh` para receber parâmetros opcionais do master-chef (`-MasterChefEmail`, `-MasterChefPassword`) e semeá-lo no novo banco com `must_change_password=True` | - | `[//]` | `scripts/deploy-institution.ps1` | 🟢 | `[X]` |
| T009 | Desenvolver a interface visual na SPA em `src/api/static/index.html` e `index.css` com a aba 'Administração Geral', tabela de tenants ativos, formulário de provisionamento e modal de redefinição obrigatória de senha | T007 | - | `src/api/static/index.html` | 🟢 | `[X]` |

## Fase 5, Polimento

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T010 | Executar a suíte completa de testes com `pytest` (incluindo testes de isolamento multi-tenant e regressão geral) para validar 100% de integridade | T004, T007, T008, T009 | `[//]` | `tests/` | 🟢 | `[X]` |


## Notas de execução

Nenhuma observação no momento da criação do plano.

## Histórico de alterações

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-09-07 | Versão inicial gerada por `/reversa-to-do` a partir do roadmap 022 | reversa |

