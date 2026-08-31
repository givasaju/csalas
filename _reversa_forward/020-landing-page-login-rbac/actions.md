# Actions: Landing Page de Apresentação Institucional, Auto-Cadastro e Login com RBAC

> Identificador: `020-landing-page-login-rbac`
> Data: `2026-08-26`
> Roadmap: `_reversa_forward/020-landing-page-login-rbac/roadmap.md`

## Resumo

| Métrica | Valor |
|---------|-------|
| Total de ações | 8 |
| Paralelizáveis (`[//]`) | 1 |
| Maior cadeia de dependência | 7 |

## Fase 1, Preparação

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T001 | Adicionar o modelo `User` em `src/models.py` e implementar a rotina de criação de tabela e seed inicial do gestor (`admin@classsync.ai`) em `src/database.py` | - | - | `src/models.py` | 🟢 | `[X]` |

## Fase 2, Testes

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T002 | Criar a suíte de testes `tests/test_auth_rbac.py` cobrindo cadastro pendente, login, geração de JWT e proteção de rotas por perfil | T001 | `[//]` | `tests/test_auth_rbac.py` | 🟢 | `[X]` |

## Fase 3, Núcleo

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T003 | Atualizar `src/api/auth.py` com hashing seguro de senhas com bcrypt, geração/validação de tokens JWT com claims de role e a dependência `require_roles` | T001 | - | `src/api/auth.py` | 🟢 | `[X]` |
| T004 | Implementar em `src/api/routes.py` os endpoints `POST /api/v1/auth/register`, `POST /api/v1/auth/login`, `GET /api/v1/auth/me`, `GET /api/v1/users` e `PATCH /api/v1/users/{user_id}/status` | T003 | - | `src/api/routes.py` | 🟢 | `[X]` |

## Fase 4, Integração

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T005 | Criar em `src/api/static/index.html` a estrutura visual da Landing Page pública institucional (Navbar, Hero com CTA, Recursos de IA, Estatísticas e Rodapé) | T004 | - | `src/api/static/index.html` | 🟢 | `[X]` |
| T006 | Implementar em `src/api/static/index.html` os modais de Login e Auto-Cadastro com validações, integração assíncrona com os endpoints de autenticação e feedback | T005 | - | `src/api/static/index.html` | 🟢 | `[X]` |
| T007 | Implementar no frontend SPA o controle de visibilidade das abas por perfil (RBAC), cabeçalho com identificação do usuário/logout e a interface de Gestão de Usuários para o Gestor | T006 | - | `src/api/static/index.html` | 🟢 | `[X]` |

## Fase 5, Polimento

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T008 | Executar a suíte de testes automatizados `pytest` e validar o fluxo completo de cadastro, aprovação, login e proteção de rotas | T007 | - | `tests/test_auth_rbac.py` | 🟢 | `[X]` |

## Notas de execução

Todas as 8 tarefas (T001 a T008) foram implementadas e validadas com sucesso. A suíte completa de testes automatizados `pytest` obteve 100% de aprovação (67/67 testes aprovados).

## Histórico de alterações

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-08-26 | Versão inicial gerada por `/reversa-to-do` | reversa |
| 2026-08-26 | Conclusão e homologação de todas as 8 ações por `/reversa-coding` | reversa |
| 2026-08-26 | Inclusão e conclusão da emenda E001 por `/reversa-add` | reversa |

## Emendas

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| E001 | Restringir abas de gestão e exibir grade semanal de horários completa do docente no Dashboard | - | - | `src/api/static/index.html` | 🟢 | `[X]` |

