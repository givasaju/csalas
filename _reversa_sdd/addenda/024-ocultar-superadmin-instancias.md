# Addendum: Ocultação do Super Administrador Geral na Gestão de Usuários das Instâncias

> Identificador: `024-ocultar-superadmin-instancias`
> Data: `2026-09-08`
> Cenário: Legado (`_reversa_sdd/architecture.md` e `_reversa_sdd/domain.md`)

## Vigência

Vigente desde 2026-09-08.

## Resumo da entrega

Implementação do isolamento institucional e proteção de credenciais para a conta do Super Administrador Geral (`doctor-chef`) na gestão de usuários das instâncias locais da plataforma. No backend (`src/api/routes.py`), o endpoint `GET /api/v1/users` passa a aplicar filtro explícito tanto na consulta ORM quanto na serialização de saída, omitindo a conta `doctor@classsync.ai` e a role `doctor-chef` da listagem exposta aos gestores locais. Adicionalmente, o endpoint `PATCH /api/v1/users/{user_id}/status` introduziu uma trava de segurança que bloqueia com `HTTP 403 Forbidden` qualquer tentativa de desativação (`is_active: false`) ou alteração de papel (`role`) direcionada à conta do superadministrador. No frontend SPA (`src/api/static/index.html`), o método `loadUsersList()` adicionou filtragem defensiva client-side pré-renderização para garantir integridade visual no modal de usuários (`#usersModal`). A integridade da regra e ausência de regressões foram validadas através da expansão da suíte `tests/test_auth_rbac.py`, atingindo 100% de aprovação (85/85 testes passando no repositório com zero regressões no sistema legado).
Total de ações executadas: 6 de 6 (100% concluído).

## Impacto por artefato da extração

| Artefato | Seção | Tipo de impacto | Delta |
|----------|-------|-----------------|-------|
| `_reversa_sdd/architecture.md` | `#web-app-api` | `regra-alterada` | Endpoint `GET /api/v1/users` omite contas com role `doctor-chef` e email `doctor@classsync.ai` dos resultados retornados a gestores locais. |
| `_reversa_sdd/architecture.md` | `#web-app-api` | `regra-nova` | Endpoint `PATCH /api/v1/users/{user_id}/status` retorna `HTTP 403 Forbidden` contra tentativas de alterar status ou papel de contas `doctor-chef`. |
| `_reversa_sdd/architecture.md` | `#frontend-spa` | `regra-alterada` | Função `loadUsersList()` em `index.html` aplica filtragem defensiva prévia à renderização da tabela do modal `#usersModal`. |
| `_reversa_sdd/domain.md` | `#3-seguranca-e-autenticacao` | `regra-alterada` | Regra de RBAC e segregação multi-tenant: contas de governança global (`doctor-chef`) são imutáveis e invisíveis na gestão de usuários das instâncias locais de clientes. |

## Regras sob vigilância

- `W001`: Endpoint `GET /api/v1/users` omitindo `doctor-chef` e `doctor@classsync.ai` na listagem de instâncias locais em `_reversa_forward/024-ocultar-superadmin-instancias/regression-watch.md`
- `W002`: Endpoint `PATCH /api/v1/users/{user_id}/status` respondendo `HTTP 403 Forbidden` para tentativas de mutação da conta do Super Administrador Geral em `_reversa_forward/024-ocultar-superadmin-instancias/regression-watch.md`

## Fontes

- `_reversa_forward/024-ocultar-superadmin-instancias/requirements.md`
- `_reversa_forward/024-ocultar-superadmin-instancias/roadmap.md`
- `_reversa_forward/024-ocultar-superadmin-instancias/actions.md`
- `_reversa_forward/024-ocultar-superadmin-instancias/progress.jsonl`
- `_reversa_forward/024-ocultar-superadmin-instancias/legacy-impact.md`
- `_reversa_forward/024-ocultar-superadmin-instancias/regression-watch.md`
