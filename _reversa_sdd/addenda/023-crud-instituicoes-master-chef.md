# Addendum: CRUD de Gestão de Instituições e Master-Chef

> Identificador: `023-crud-instituicoes-master-chef`
> Data: `2026-09-07`
> Cenário: Legado (`_reversa_sdd/architecture.md` e `domain.md`)

## Vigência

Vigente desde 2026-09-07.

## Resumo da entrega

Implementação das capacidades completas de ciclo de vida (CRUD) e governança operacional para a gestão de instituições clientes e seus respectivos gestores gerais ('master-chef') na camada administrativa do SuperAdmin (`doctor-chef`). A entrega contemplou a criação de esquemas Pydantic dedicados em `src/api/schemas.py`; desenvolvimento dos endpoints REST `GET`, `PUT`, `DELETE` em `/api/v1/platform/tenants/{slug}` e `POST /api/v1/platform/tenants/{slug}/master-chef/reset` em `src/api/routes.py`, integrados a rotinas utilitárias para conexão e rotação de credenciais no SQLite isolado do tenant (`./data/{slug}/project.db`) com marcação mandatória de `must_change_password=True` e salvaguarda de soft delete / arquivamento em `./data/.archived/{slug}_{timestamp}/` com liberação imediata da porta TCP; integração visual na SPA (`src/api/static/index.html`) com botões contextuais na tabela e modais de Edição, Reset de Master-Chef e Exclusão com confirmação obrigatória de slug; além da expansão da suíte automatizada `tests/test_platform_tenants_api.py` com 100% de aprovação (81/81 testes passando no repositório com zero regressões no sistema legado).
Total de ações executadas: 10 de 10 (100% concluído).

## Impacto por artefato da extração

| Artefato | Seção | Tipo de impacto | Delta |
|----------|-------|-----------------|-------|
| `_reversa_sdd/architecture.md` | `#web-app-api` | `contrato-novo` | Endpoints REST para detalhamento (`GET`), atualização (`PUT`), exclusão assistida (`DELETE`) e redefinição de master-chef (`POST .../master-chef/reset`). |
| `_reversa_sdd/architecture.md` | `#web-app-api` | `regra-alterada` | Rotinas utilitárias de arquivamento físico de volumes de dados em `./data/.archived/`, liberação de portas e acesso pontual seguro ao banco SQLite de cada tenant. |
| `_reversa_sdd/architecture.md` | `#jwt-auth-service` | `regra-alterada` | Enforcement da role `doctor-chef` como barreira estrita de RBAC em todas as rotas do CRUD de ciclo de vida de tenants. |
| `_reversa_sdd/architecture.md` | `#frontend-spa` | `componente-novo` | Modais de Edição de Instituição, Redefinição de Master-Chef e Exclusão Assistida com confirmação de slug integrados à tabela de Administração Geral. |
| `_reversa_sdd/domain.md` | `#governanca-e-privacidade` | `regra-alterada` | Capacidade de rotação contínua de credenciais provisórias do gestor institucional (`must_change_password=True`) e desativação lógica de tenants para retenção de histórico LGPD. |

## Regras sob vigilância

- `W001`: Endpoint `GET /api/v1/platform/tenants/{slug}` retornando dados e master-chef exclusivamente para `doctor-chef` em `_reversa_forward/023-crud-instituicoes-master-chef/regression-watch.md`
- `W002`: Endpoint `PUT /api/v1/platform/tenants/{slug}` atualizando metadados com imutabilidade de porta e slug em `_reversa_forward/023-crud-instituicoes-master-chef/regression-watch.md`
- `W003`: Endpoint `POST /api/v1/platform/tenants/{slug}/master-chef/reset` ativando `must_change_password=True` em `_reversa_forward/023-crud-instituicoes-master-chef/regression-watch.md`
- `W004`: Endpoint `DELETE /api/v1/platform/tenants/{slug}` com verificação de slug e soft delete em `./data/.archived/` em `_reversa_forward/023-crud-instituicoes-master-chef/regression-watch.md`
- `W005`: Suíte automatizada `tests/test_platform_tenants_api.py` mantendo 100% de aprovação em `_reversa_forward/023-crud-instituicoes-master-chef/regression-watch.md`

## Fontes

- `_reversa_forward/023-crud-instituicoes-master-chef/requirements.md`
- `_reversa_forward/023-crud-instituicoes-master-chef/roadmap.md`
- `_reversa_forward/023-crud-instituicoes-master-chef/actions.md`
- `_reversa_forward/023-crud-instituicoes-master-chef/legacy-impact.md`
- `_reversa_forward/023-crud-instituicoes-master-chef/regression-watch.md`
