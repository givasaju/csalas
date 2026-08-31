# Addendum: Landing Page de Apresentação Institucional, Auto-Cadastro e Login com RBAC

> Identificador: `020-landing-page-login-rbac`
> Data: `2026-08-26`
> Cenário: Legado (`_reversa_sdd/architecture.md` e `domain.md`)

## Vigência

Vigente desde 2026-08-26.

## Resumo da entrega

Implementação da Landing Page institucional pública na rota raiz `/`, apresentação moderna com Hero Section dos diferenciais da plataforma ClassSync AI (resolução cooperativa de conflitos por leilão multiagente AMR/ACC, consolidação predial de energia, conformidade de acessibilidade e relatórios), modais de Auto-Cadastro com governança (contas nascem pendentes de aprovação) e Login institucional com emissão de JWT criptografado e controle de acesso baseado em papéis (RBAC - Gestor, Coordenador e Docente) com painel administrativo para aprovação e atualização de papéis.
Total de ações executadas: 8 de 8 (100% concluído).

## Impacto por artefato da extração

| Artefato | Seção | Tipo de impacto | Delta |
|----------|-------|-----------------|-------|
| `_reversa_sdd/architecture.md` | `#database` | `delta-de-dados` | Adição da entidade `User` em `src/models.py` e rotina `seed_users()` em `src/database.py`. |
| `_reversa_sdd/architecture.md` | `#jwt-auth-service` | `componente-alterado` | Hashing seguro de senhas com PBKDF2/SHA256, geração de tokens JWT com claims de papel e middleware `require_roles` em `src/api/auth.py`. |
| `_reversa_sdd/architecture.md` | `#web-app-api` | `contrato-novo` | Endpoints `/api/v1/auth/register`, `/api/v1/auth/login`, `/api/v1/auth/me`, `/api/v1/users` e `/api/v1/users/{id}/status` em `src/api/routes.py`. |
| `_reversa_sdd/architecture.md` | `#frontend-spa` | `componente-alterado` | Landing page pública institucional `#landingPageSection`, modais de autenticação e gestão de usuários `#usersModal` em `src/api/static/index.html`. |
| `_reversa_sdd/domain.md` | `#autenticacao-e-governanca` | `regra-nova` | Auto-cadastro com aprovação manual pelo Gestor e segmentação de visibilidade de abas por perfil RBAC. |

## Regras sob vigilância

- `W001`: Vigilância de carregamento da Landing Page pública na rota `/` em `_reversa_forward/020-landing-page-login-rbac/regression-watch.md`
- `W002`: Vigilância de funcionamento dos contratos de autenticação `/api/v1/auth/*` em `_reversa_forward/020-landing-page-login-rbac/regression-watch.md`
- `W003`: Vigilância de persistência da entidade `User` e seed inicial em `_reversa_forward/020-landing-page-login-rbac/regression-watch.md`
- `W004`: Vigilância de integridade das restrições de privilégio (403 para não-gestores) em `_reversa_forward/020-landing-page-login-rbac/regression-watch.md`

## Fontes

- `_reversa_forward/020-landing-page-login-rbac/requirements.md`
- `_reversa_forward/020-landing-page-login-rbac/roadmap.md`
- `_reversa_forward/020-landing-page-login-rbac/actions.md`
- `_reversa_forward/020-landing-page-login-rbac/legacy-impact.md`
- `_reversa_forward/020-landing-page-login-rbac/regression-watch.md`

## Atualização 2026-08-26 (Emenda E001)

- **Resumo do Delta:** Ajuste na segmentação da interface para o papel `docente`. Ao autenticar, o docente visualiza diretamente no Dashboard sua Grade Semanal Completa de Aulas e Salas com botão de exportação em PDF, mantendo as demais abas administrativas restritas.
- **Impacto:** `_reversa_sdd/architecture.md#frontend-spa` (`regra-alterada`).
- **Ações:** 1 emenda concluída (`E001`).

