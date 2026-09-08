# Actions: Ocultação do Super Administrador Geral na Gestão de Usuários das Instâncias

> Identificador: `024-ocultar-superadmin-instancias`
> Data: `2026-09-08`
> Roadmap: `_reversa_forward/024-ocultar-superadmin-instancias/roadmap.md`

## Resumo

| Métrica | Valor |
|---------|-------|
| Total de ações | 6 |
| Paralelizáveis (`[//]`) | 2 |
| Maior cadeia de dependência | 6 |

## Fase 1, Preparação

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T001 | Mapear e preparar a estrutura de cenários de teste em `tests/test_auth_rbac.py` cobrindo o isolamento da conta `doctor-chef` na rota de usuários | - | `[//]` | `tests/test_auth_rbac.py` | 🟢 | `[X]` |

## Fase 2, Testes

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T002 | Implementar cenários de testes automatizados em `tests/test_auth_rbac.py` validando que `GET /api/v1/users` omite `doctor-chef` e que `PATCH /api/v1/users/{id}/status` responde 403 Forbidden | T001 | - | `tests/test_auth_rbac.py` | 🟢 | `[X]` |

## Fase 3, Núcleo

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T003 | Atualizar o endpoint `GET /api/v1/users` em `src/api/routes.py` para aplicar filtro excluindo usuários com a role `doctor-chef` do retorno | T002 | - | `src/api/routes.py` | 🟢 | `[X]` |
| T004 | Implementar trava de proteção em `src/api/routes.py` no endpoint `PATCH /api/v1/users/{user_id}/status` retornando HTTP 403 Forbidden para tentativas de alteração em contas `doctor-chef` | T003 | - | `src/api/routes.py` | 🟢 | `[X]` |

## Fase 4, Integração

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T005 | Implementar filtragem defensiva client-side no método `loadUsersList()` em `src/api/static/index.html` para omitir `doctor-chef` da tabela visual do modal de usuários | T004 | `[//]` | `src/api/static/index.html` | 🟢 | `[X]` |

## Fase 5, Polimento

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T006 | Executar a suíte de testes com `pytest` assegurando 100% de aprovação e ausência de regressões no legado | T005 | - | `tests/` | 🟢 | `[X]` |

## Notas de execução

Nenhuma observação no momento da criação do plano.

## Histórico de alterações

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-09-08 | Versão inicial gerada por `/reversa-to-do` a partir do roadmap 024 | reversa |
