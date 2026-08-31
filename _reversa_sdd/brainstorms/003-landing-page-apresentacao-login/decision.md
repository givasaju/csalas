# Decision: landing-page-apresentacao-login

> Selo 🟡 PLANEJADO. Decisão humana registrada, sujeita a revisão.

## Problema de referência
🟡 Quando o usuário acessar a plataforma, eu quero que seja apresentada uma landing page elegante, moderna e responsiva com opção de login e cadastro de novo usuário, para conseguir que após login com sucesso o usuário tenha acesso seguro e direcionado às funcionalidades do sistema conforme seu perfil definido pelo gestor da plataforma.

## Placar
| Opção | Job to be done | Esforço | Risco residual | Custo no legado | Total |
|---|---|---|---|---|---|
| **Opção A: Landing Page Integrada + Auth Nativa + RBAC Local** | 5 | 3 | 4 | 4 | **16** |
| **Opção B: Portal Multi-Páginas + Aprovação Manual de Perfis** | 4 | 2 | 2 | 2 | **10** |
| **Opção C: Não construir (Acesso Direto e Informal)** | 1 | 5 | 2 | 5 | **13** |
| **Opção D: Usar algo pronto (Template + Provedor Auth Externo)** | 4 | 3 | 3 | 3 | **13** |

🟡 Placar sem empates. A Opção A venceu com 16/20 pontos.

## Recomendação do Arbiter
🟡 **Opção A: Landing Page Institucional Integrada com Auth Nativa e RBAC Local**. Cria uma presença institucional moderna e responsiva na rota raiz, oferece formulários modais de onboarding (login e auto-cadastro) e estabelece controle de acesso baseado em papéis (RBAC) localmente no backend FastAPI sem dependências externas nem gargalos manuais.

## O que se perde ao escolher ela
🟡 Perde-se a governança manual rígida pré-ativação de conta (da Opção B) e a terceirização completa de serviços de credenciais/recuperação de senhas para a nuvem (da Opção D).

## Em que condição a recomendação muda
🟡 Se a instituição exigir obrigatoriamente que nenhuma conta seja criada sem aprovação formal e manual prévia de um comitê institucional, a Opção B passa à frente; ou se a TI do campus possuir um servidor central de Single Sign-On (Keycloak/SAML/OAuth2) já padronizado, a Opção D passa à frente.

## Decisão do usuário
🟡 **Opção A: Landing Page Institucional Integrada com Auth Nativa e RBAC Local**, decidido por **givas** em 2026-08-26T18:09:20-03:00.

## A validar antes de comprometer
🟡 Validar a dependência FastAPI de verificação de permissões (`require_roles`) no backend e testar a responsividade mobile do layout da landing page antes de integrar o formulário de cadastro final.

## Riscos aceitos conscientemente
🟡 Necessidade de manter a segurança e hashing de senhas localmente no banco SQLite/FastAPI; assegurar que as rotas da API protejam os dados com RBAC e não apenas a interface gráfica.

---
Gerado por reversa-arbiter em 2026-08-26T18:09:30-03:00
Sessão: 003-landing-page-apresentacao-login
