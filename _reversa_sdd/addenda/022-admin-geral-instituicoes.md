# Addendum: Interface do Administrador Geral para Gestão e Delegação de Instituições

> Identificador: `022-admin-geral-instituicoes`
> Data: `2026-09-07`
> Cenário: Legado (`_reversa_sdd/architecture.md` e `domain.md`)

## Vigência

Vigente desde 2026-09-07.

## Resumo da entrega

Implementação da camada administrativa de alto nível para o SuperAdmin da plataforma (`doctor-chef`), viabilizando a criação e provisionamento autônomo e visual de novas instituições de ensino isoladas (Single-Tenant multi-container) e delegação direta das credenciais do gestor geral institucional (`master-chef`) com obrigatoriedade de redefinição de senha no primeiro login para cumprimento integral da LGPD. A entrega contemplou a extensão do modelo `User` com `must_change_password` e role `doctor-chef` em `src/models.py`, migração automática de coluna SQLite e seed do superadministrador em `src/database.py`, regras estritas de RBAC e endpoint `POST /api/v1/auth/change-password` em `src/api/auth.py` e `routes.py`, descoberta de tenants instalados com alocação automática de portas TCP livres a partir de 8001, endpoints REST `GET` e `POST /api/v1/platform/tenants` operando assincronamente via `BackgroundTasks` (HTTP 202 Accepted), suporte a parâmetros do master-chef nos scripts de provisionamento PowerShell e Bash (`scripts/deploy-institution.*`), visão visual dedicada 'Administração Geral' e modal de redefinição de credencial na SPA em `src/api/static/`, além da suíte de testes automatizados `tests/test_platform_tenants_api.py` com 100% de aprovação (76/76 testes passando no repositório com zero regressões no sistema legado).
Total de ações executadas: 10 de 10 (100% concluído).

## Impacto por artefato da extração

| Artefato | Seção | Tipo de impacto | Delta |
|----------|-------|-----------------|-------|
| `_reversa_sdd/architecture.md` | `#jwt-auth-service` | `regra-alterada` | Introdução da role global `doctor-chef` com acesso exclusivo a endpoints de governança SaaS e claim `must_change_password` no token JWT. |
| `_reversa_sdd/architecture.md` | `#database` | `regra-alterada` | Coluna booleana `must_change_password` (default=False) na tabela `User`, migração automática no SQLite e seed do usuário `doctor@classsync.ai`. |
| `_reversa_sdd/architecture.md` | `#web-app-api` | `contrato-novo` | Endpoints `GET` e `POST /api/v1/platform/tenants` protegidos por `doctor-chef` e rota `POST /api/v1/auth/change-password` para rotação de credenciais. |
| `_reversa_sdd/architecture.md` | `#infra-automation` | `regra-alterada` | Scripts `deploy-institution.ps1` e `.sh` atualizados para receber e semear credenciais do master-chef diretamente no banco SQLite da nova instituição. |
| `_reversa_sdd/architecture.md` | `#frontend-spa` | `componente-novo` | Aba 'Administração Geral' na SPA exibindo KPIs, cálculo automático de portas TCP, formulário de provisionamento e modal forçado de troca de senha. |
| `_reversa_sdd/domain.md` | `#governanca-e-privacidade` | `regra-nova` | Exigência mandatória de redefinição de senha no primeiro login do master-chef institucional para conformidade estrita com a LGPD. |

## Regras sob vigilância

- `W001`: Acesso exclusivo da role `doctor-chef` a endpoints de governança em `_reversa_forward/022-admin-geral-instituicoes/regression-watch.md`
- `W002`: Coluna `must_change_password` na tabela `User` com migração automática SQLite em `_reversa_forward/022-admin-geral-instituicoes/regression-watch.md`
- `W003`: Endpoint `POST /api/v1/platform/tenants` respondendo 202 Accepted assincronamente via `BackgroundTasks` em `_reversa_forward/022-admin-geral-instituicoes/regression-watch.md`
- `W004`: Endpoint `POST /api/v1/auth/change-password` validando requisitos de senha e liberando acesso em `_reversa_forward/022-admin-geral-instituicoes/regression-watch.md`
- `W005`: Suíte de testes `test_platform_tenants_api.py` mantendo 100% de aprovação em `_reversa_forward/022-admin-geral-instituicoes/regression-watch.md`

## Fontes

- `_reversa_forward/022-admin-geral-instituicoes/requirements.md`
- `_reversa_forward/022-admin-geral-instituicoes/roadmap.md`
- `_reversa_forward/022-admin-geral-instituicoes/actions.md`
- `_reversa_forward/022-admin-geral-instituicoes/legacy-impact.md`
- `_reversa_forward/022-admin-geral-instituicoes/regression-watch.md`
