# Risks: landing-page-apresentacao-login

> Selo 🟡 PLANEJADO em todos os itens. Documento adversarial por design.

## Premortem
🟡 **Manchete 1:** Nova landing page é lançada, mas o fluxo de cadastro trava a operação porque a liberação de perfis virou um gargalo manual do gestor em períodos de matrícula (causa raiz: ausência de política clara de perfil padrão inicial no auto-cadastro).
🟡 **Manchete 2:** Interface visual moderna esconde brechas na validação de permissões e docentes conseguem visualizar e disparar alocações de salas de outros departamentos (causa raiz: autorização implementada apenas como ocultação visual no frontend sem validação estrita de RBAC nas rotas FastAPI).
🟡 **Manchete 3:** Landing page atrativa é ignorada pela comunidade acadêmica devido a formulários quebrados no mobile e ausência de feedback claro de erro no login (causa raiz: falta de testes de responsividade e tratamento pobre de estados de erro na UI).

**Manchete que mais assusta o usuário:** 🟡 Manchete 2 (Falha de segurança e vazamento de permissões entre perfis operacionais).

---

## Opção A, Landing Page Institucional Integrada com Auth Nativa e RBAC Local
- **Premissa que mata:** 🟡 O controle de perfil (RBAC) ser implementado de forma superficial apenas no frontend, permitindo que requisições diretas via API acessem módulos protegidos sem validação no backend.
- **Teste barato da premissa:** 🟡 Criar uma dependência FastAPI de verificação de papel (`require_roles(["gestor", "coordenador"])`) e disparar uma requisição curl com token de perfil não autorizado em 1 hora.
- **Custo escondido:** 🟡 Implementação de ciclo seguro de senhas (hashing com bcrypt/argon2, geração/validação de JWT com expiração) e sanitização contra ataques XSS/CSRF em `src/api/routes.py` e `src/api/static/index.html`.
- **Ponto sem volta:** 🟡 Definição do schema local de usuários, roles e tokens no banco de dados SQLite.

## Opção B, Portal Multi-Páginas com Onboarding Guiado e Painel de Aprovação de Perfis
- **Premissa que mata:** 🟡 O gestor da plataforma ter tempo e disponibilidade contínua para aprovar individualmente dezenas de novos cadastros de docentes antes do início das aulas.
- **Teste barato da premissa:** 🟡 Mapear com o gestor quanto tempo diário ele dispõe para triagem de usuários e simular uma fila com 10 cadastros simultâneos.
- **Custo escondido:** 🟡 Sobrecarga de desenvolvimento de telas administrativas dedicadas de gestão de usuários, estados intermediários de aprovação e envio de notificações/e-mails de status.
- **Ponto sem volta:** 🟡 Acoplamento do fluxo de negócios a um processo manual de autorização prévia de contas.

## Opção C, Não construir (Acesso Direto e Informal)
- **Premissa que mata:** 🟡 A instituição de ensino tolerar que qualquer pessoa na rede interna tenha acesso irrestrito às ferramentas de alocação de salas sem registro de auditoria nem identificação de quem realizou alterações.
- **Teste barato da premissa:** 🟡 Questionar a diretoria se a ausência de controle de acesso atende às exigências mínimas de conformidade e governança institucional.
- **Custo escondido:** 🟡 Risco de corrupção acidental de dados de turmas/salas e impossibilidade de auditar conflitos gerados por múltiplos usuários simultâneos.
- **Ponto sem volta:** 🟡 Inexistente (nenhum impacto de código).

## Opção D, Usar algo pronto (Template + Provedor de Autenticação Externo)
- **Premissa que mata:** 🟡 A infraestrutura do campus permitir dependência obrigatória de serviços de autenticação em nuvem (ex.: Auth0/Supabase) ou a equipe de TI local aceitar manter um container Keycloak dedicado.
- **Teste barato da premissa:** 🟡 Realizar um teste de latência e conectividade com a API do provedor em nuvem a partir do ambiente de deploy do campus.
- **Custo escondido:** 🟡 Indisponibilidade do login local em caso de oscilações de conexão externa com a internet e custos recorrentes de planos de autenticação conforme o crescimento do número de usuários ativos.
- **Ponto sem volta:** 🟡 Dependência estrutural do SDK de terceiros e migração complexa caso haja necessidade de internalizar as credenciais futuramente.

---

## Riscos transversais
🟡 **Segurança e Validação de Perfis (RBAC):** É obrigatório que a restrição de acesso por perfil (Gestor, Coordenador, Docente) seja validada tanto na interface visual quanto nas rotas HTTP do backend (`src/api/routes.py`).
🟡 **Responsividade e Design Mobile:** A landing page institucional e os modais de login/cadastro precisam de adaptação fluida para dispositivos móveis e desktops de diferentes resoluções.
🟡 **Bootstrap e Usuário Inicial:** O sistema precisa garantir o provisionamento automático de um usuário gestor/administrador padrão inicial para evitar bloqueio no primeiro deploy.

## O que precisa ser respondido antes de decidir
1. 🟡 Ao se auto-cadastrar, o usuário deve receber automaticamente um perfil padrão inicial (ex.: "Visitante" ou "Docente") ou aguardar ativação do gestor?
2. 🟡 Quais são os perfis de acesso fundamentais (ex.: `Gestor/Admin`, `Coordenador`, `Docente`, `Visualizador`)?
3. 🟡 A landing page deve conter quais blocos de apresentação (Hero Section, Apresentação da IA, Diferenciais de Ocupação Predial, Depoimentos, Chamada para Ação / CTA)?

---
Gerado por reversa-challenger em 2026-08-26T18:07:00-03:00
Sessão: 003-landing-page-apresentacao-login
