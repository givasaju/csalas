# Requirements: Landing Page de Apresentação Institucional, Auto-Cadastro e Login com RBAC

> Identificador: `020-landing-page-login-rbac`
> Data: `2026-08-26`
> Pasta da extração reversa: `_reversa_sdd/` (proveniente do Brainstorm Session 003 `pre-spec.md`)
> Confidência: 🟢 CONFIRMADO, 🟡 INFERIDO, 🔴 LACUNA / DÚVIDA

## 1. Resumo executivo

Disponibilizar uma Landing Page pública, moderna e responsiva na rota inicial da plataforma ClassSync AI, apresentando os diferenciais do ecossistema de otimização de salas com IA e oferecendo opções de Auto-Cadastro e Login de usuários. Após o cadastro, a conta permanece em estado pendente até aprovação pelo Gestor. Após a autenticação com sucesso de uma conta aprovada, o sistema direciona o usuário e restringe o acesso às funcionalidades e rotas de acordo com seu perfil de permissão (RBAC: Gestor/Admin, Coordenador de Curso, Docente), com validação rigorosa de segurança no backend FastAPI e painel de gestão de contas para o administrador.

## 2. Contexto a partir do legado

| Fonte | Trecho relevante | Confidência |
|-------|------------------|-------------|
| `_reversa_sdd/c4-context.md#personas` | Mapeamento das personas centrais (Coordenador de Curso, Diretora de Infraestrutura) e Serviço de Autenticação JWT com Bearer Token. | 🟢 |
| `_reversa_sdd/domain.md#glossario` | Estrutura de domínios, coordenações acadêmicas, restrições docentes e regras operacionais do ClassSync AI. | 🟢 |
| `_reversa_sdd/architecture.md#web-app-api` | Estrutura de roteamento FastAPI (`src/main.py`, `src/api/routes.py`) e entrega dos arquivos estáticos da SPA (`src/api/static/index.html`). | 🟢 |
| `_reversa_sdd/inventory.md#src/api/auth.py` | Módulo de autenticação JWT existente (`TokenData`, `verify_token`, `get_current_user`, `get_current_admin_user`). | 🟢 |
| `_reversa_sdd/brainstorms/003-landing-page-apresentacao-login/pre-spec.md` | Especificação de entrada definindo a Opção A (Landing Page Integrada + Auth Nativa + RBAC Local). | 🟢 |

## 3. Personas e cenários de uso

| Persona | Objetivo | Cenário-chave |
|---------|----------|---------------|
| Visitante / Novo Usuário | Conhecer a plataforma institucional e realizar auto-cadastro | Acessa a rota pública (`/`), explora os diferenciais da plataforma no hero e seções de recursos, clica em "Cadastre-se", preenche seus dados e cria sua solicitação de conta. |
| Docente / Coordenador | Autenticar-se no sistema para gerenciar horários, salas ou disciplinas | Acessa a landing page, clica em "Entrar", informa e-mail/senha no modal de login, é autenticado via JWT e entra no painel operacional com visão adaptada ao seu perfil. |
| Gestor / Administrador | Gerenciar usuários, aprovar cadastros, alocações e permissões do sistema | Autentica-se com perfil administrativo, visualiza os módulos operacionais e acessa a seção de "Gestão de Usuários" para aprovar novos cadastros e definir papéis. |

## 4. Regras de negócio novas ou alteradas

1. **RN-01: Rota Pública Inicial (Landing Page):** 🟢
   - A rota raiz (`/`) deve exibir a Landing Page institucional moderna e responsiva quando o usuário não estiver autenticado.
   - Usuários com sessão/token válido ativo podem acessar diretamente o painel operacional da aplicação.
2. **RN-02: Auto-Cadastro e Ciclo de Aprovação de Contas:** 🟢
   - O formulário de cadastro coleta Nome, E-mail, Senha e Departamento/Curso.
   - A senha deve ser criptografada com algoritmo seguro (`bcrypt`).
   - Novos usuários são criados com status `pendente` (`is_active: false` ou `status: "pending"`). Tentativas de login com conta pendente informam amigavelmente que o acesso aguarda aprovação pelo Gestor.
3. **RN-03: Autenticação e Emissão de Token JWT:** 🟢
   - O endpoint de login valida credenciais e o status ativo da conta contra o banco SQLite, emitindo token JWT com claims `sub`, `name`, `role` (`gestor`, `coordenador`, `docente`).
4. **RN-04: Controle de Acesso Baseado em Papéis (RBAC):** 🟢
   - `gestor` / `admin`: Acesso irrestrito a todas as abas operacionais (Espaços, Docentes, Alocação IA, Relatórios) e ao painel/modal de **Gestão de Usuários** para aprovar contas e alterar papéis.
   - `coordenador`: Acesso à gestão de restrições de docentes, cadastro de turmas de seu departamento e relatórios de ocupação.
   - `docente`: Acesso à visualização de sua grade individual de horários e consulta de ocupação de salas.
5. **RN-05: Proteção de Endpoints no Backend:** 🟢
   - Todas as rotas de mutação e consulta restrita em `src/api/routes.py` devem validar os papéis permitidos via dependência `Depends(require_roles([...]))`.

## 5. Requisitos Funcionais

| ID | Requisito | Prioridade | Critério de aceite | Confidência |
|----|-----------|------------|--------------------|-------------|
| RF-01 | Construir a Landing Page responsiva com Navbar pública, Hero Section com proposta de valor, apresentação dos diferenciais da IA de Alocação, métricas de eficiência predial e rodapé institucional. | Must | A página carrega na rota raiz `/` com design limpo, moderno e fluído em desktop e mobile. | 🟢 |
| RF-02 | Implementar o modal de Login com validação de credenciais, tratamento de status de conta pendente e feedback amigável de erro. | Must | Usuário aprovado recebe token JWT e é redirecionado ao painel; usuário pendente recebe aviso de aguardo. | 🟢 |
| RF-03 | Implementar o modal de Auto-Cadastro (Sign-up) com criação da conta em status pendente no banco SQLite e mensagem de confirmação. | Must | O cadastro grava os dados com senha criptografada e notifica que o acesso aguarda aprovação do gestor. | 🟢 |
| RF-04 | Criar a entidade `User` no modelo SQLAlchemy (`src/models.py`) com campos `id`, `name`, `email`, `password_hash`, `role`, `department`, `is_active`, `created_at`. | Must | Tabela criada no SQLite com chave primária e unicidade no campo e-mail. | 🟢 |
| RF-05 | Implementar endpoints de autenticação e gestão de usuários: `POST /api/v1/auth/register`, `POST /api/v1/auth/login`, `GET /api/v1/auth/me`, `GET /api/v1/users`, `PATCH /api/v1/users/{user_id}/status`. | Must | Endpoints protegidos por JWT e validação de perfil de Gestor/Admin para gestão de contas. | 🟢 |
| RF-06 | Implementar o controle de visibilidade das abas e botões no frontend SPA conforme a role contida no payload do token JWT. | Must | Docentes e coordenadores visualizam apenas as abas autorizadas para seu papel. | 🟢 |
| RF-07 | Adicionar botão de Logout e identificador do usuário logado (Nome e Badges de Perfil) no cabeçalho do painel operacional. | Must | Clicar em Logout limpa o token local e retorna o usuário à Landing Page. | 🟢 |
| RF-08 | Implementar modal/seção de Gestão de Usuários exclusiva para o Gestor aprovar novos cadastros e alterar papéis de acesso. | Must | Gestor visualiza lista de usuários cadastrados, aprova contas pendentes e atualiza perfis com 1 clique. | 🟢 |

## 6. Requisitos Não Funcionais

| Tipo | Requisito | Evidência ou justificativa | Confidência |
|------|-----------|----------------------------|-------------|
| Usabilidade & Design | A Landing Page deve adotar estética moderna (paleta de cores tecnológica, glassmorphism, tipografia limpa, seções bem espaçadas) e layout 100% responsivo. | Diretrizes de excelência em UI/UX e identidade institucional | 🟢 |
| Segurança | Hashing criptográfico de senhas utilizando `bcrypt` e assinatura de tokens JWT com expiração configurada (`src/api/auth.py`). | Melhores práticas de segurança OWASP e proteção de credenciais | 🟢 |
| Desempenho | Tempo de resposta dos endpoints de autenticação e listagem inferior a 200ms e renderização rápida da interface sem travamentos. | Rationale de performance em FastAPI e frontend leve | 🟢 |

## 7. Critérios de Aceitação

```gherkin
Cenário: Acesso à Landing Page pública
  Dado que um visitante não autenticado acessa a URL raiz da plataforma
  Quando a página carrega
  Então a Landing Page institucional é exibida com Hero Section, recursos do ClassSync AI e botões de Login e Cadastro

Cenário: Auto-cadastro de novo usuário aguardando aprovação
  Dado que o visitante clica no botão "Cadastre-se" na Landing Page
  Quando ele preenche Nome, E-mail, Senha e Departamento e submete o formulário
  Então o usuário é cadastrado com status "pendente" e uma mensagem informa que a conta aguarda liberação pelo gestor

Cenário: Aprovação de usuário e definição de papel pelo Gestor
  Dado que o Gestor está autenticado e abre a seção "Gestão de Usuários"
  Quando ele clica em "Aprovar" e seleciona o perfil "Coordenador" para um cadastro pendente
  Então o usuário é ativado no banco de dados com o papel correspondente

Cenário: Login bem-sucedido e direcionamento por perfil
  Dado que o usuário com conta aprovada abre o modal de Login
  Quando ele informa seu e-mail e senha corretos
  Então o sistema emite o token JWT, fecha o modal e exibe o painel operacional adaptado às permissões do seu perfil

Cenário: Tentativa de login com conta ainda pendente
  Dado que um usuário recém-cadastrado tenta efetuar login antes da aprovação do gestor
  Quando ele submete suas credenciais válidas
  Então o sistema retorna HTTP 403 com a mensagem "Conta pendente de aprovação pelo gestor"
```

## 8. Prioridade MoSCoW

| Item | MoSCoW | Justificativa |
|------|--------|---------------|
| RF-01 (Landing Page Responsiva) | Must | Portal de entrada institucional essencial para apresentação da plataforma. |
| RF-02 (Modal de Login) | Must | Mecanismo fundamental de autenticação e emissão de credenciais. |
| RF-03 (Modal de Auto-Cadastro) | Must | Fluxo de onboarding de novos usuários com estado pendente. |
| RF-04 (Tabela User no SQLite) | Must | Estrutura de persistência segura de contas, status e perfis de acesso. |
| RF-05 (Endpoints de Auth e Usuários) | Must | Camada de API REST para registro, autenticação e aprovação de contas. |
| RF-06 (Controle RBAC no Frontend) | Must | Adequação da interface gráfica ao perfil do usuário conectado. |
| RF-07 (Logout e Header de Usuário) | Must | Gestão de encerramento de sessão e identificação visual do usuário. |
| RF-08 (Painel de Gestão de Usuários) | Must | Interface do Gestor para aprovar novos cadastros e gerenciar perfis. |

## 9. Esclarecimentos

### Sessão 2026-08-26
- **Q:** Como deve funcionar a liberação de acesso após o auto-cadastro do novo usuário?
  **R:** A conta fica no estado "Pendente" até que um Gestor/Admin aprove o acesso e defina/confirme o perfil no sistema.
- **Q:** Como o Gestor/Administrador deve alterar e gerenciar os perfis de acesso dos usuários?
  **R:** Incluir no painel do Gestor uma seção/modal de "Gestão de Usuários" para visualizar cadastros, aprovar acessos e alterar os papéis (Gestor, Coordenador, Docente).

## 10. Lacunas

Nenhuma lacuna ou `[DÚVIDA]` pendente. Todos os pontos de escopo e governança foram esclarecidos.

## 11. Histórico de alterações

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-08-26 | Versão inicial gerada por `/reversa-requirements` a partir da ideação 003 | reversa |
| 2026-08-26 | Atualização pós `/reversa-clarify`: ciclo de aprovação de contas e gestão de perfis pelo Gestor | reversa |

## Emendas

### E001, 2026-08-26

O que muda: O usuário com perfil `docente` passa a acessar exclusivamente a visão do Dashboard com exibição imediata e em destaque da sua grade semanal completa de aulas logo após o login, mantendo as demais abas de gestão administrativa (ambientes, docentes e IA) restritas.
Motivo: Solicitação do usuário ("o usuário com perfil docente deve acessar apenas o dashboard e visualizar sua grade de horario completa que deve ser exibida quando ele fizer seu login na plataforma").
Arquivos previstos: `src/api/static/index.html`

