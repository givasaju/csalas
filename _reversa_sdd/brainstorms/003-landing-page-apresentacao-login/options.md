# Options: landing-page-apresentacao-login

> Selo 🟡 PLANEJADO em todos os itens. Nenhuma opção foi escolhida ainda.

## Problema de referência
🟡 Quando o usuário acessar a plataforma, eu quero que seja apresentada uma landing page elegante, moderna e responsiva com opção de login e cadastro de novo usuário, para conseguir que após login com sucesso o usuário tenha acesso seguro e direcionado às funcionalidades do sistema conforme seu perfil definido pelo gestor da plataforma.

## Restrições ativas
🟡 Nenhuma declarada pelo usuário.

---

## Opção A: Landing Page Institucional Integrada com Auth Nativa e RBAC Local
- **Em uma frase:** 🟡 Construir uma landing page responsiva integrada na rota raiz com seções de apresentação da plataforma, formulários modais de Login e Auto-Cadastro (Sign-up), e controle de navegação baseado no perfil (Role-Based Access Control) armazenado localmente.
- **Como resolve o problema:** 🟡 Cria uma fachada institucional atrativa e moderna para recepção dos usuários e direciona cada usuário para suas respectivas funcionalidades (coordenador, docente, infraestrutura) após autenticação via token.
- **Esforço:** 🟡 Médio , exige criação da interface da landing page, componentes modais de autenticação/cadastro e endpoints locais de persistência de credenciais e validação de papéis no backend FastAPI.
- **Impacto no legado:** 🟡 A rota raiz passa a servir a landing page pública; o painel operacional existente é protegido e exibido/filtrado conforme o perfil retornado na autenticação.
- **Reversibilidade:** 🟡 Fácil , a landing page e a camada de controle de acesso podem ser ajustadas ou reorganizadas sem afetar o motor de alocação de salas.
- **O que precisa ser verdade para funcionar:** 🟡 O backend precisa implementar a persistência de usuários com hash seguro de senhas e atribuição de perfis pelo gestor.

## Opção B: Portal Multi-Páginas com Onboarding Guiado e Painel de Aprovação de Perfis
- **Em uma frase:** 🟡 Desenvolver uma landing page institucional com página dedicada de autenticação (`/login` e `/cadastro`), fluxo de onboarding onde novos usuários aguardam ativação/atribuição de perfil, e um painel administrativo para o gestor gerenciar e aprovar permissões.
- **Como resolve o problema:** 🟡 Garante controle estrito de segurança institucional, assegurando que nenhum novo usuário acesse dados sensíveis antes de sua conta ser formalmente aprovada e classificada pelo gestor da plataforma.
- **Esforço:** 🟡 Alto , envolve desenvolvimento de páginas separadas, ciclo de vida de ativação de conta, notificações de cadastro e interface completa de gestão de usuários para o administrador.
- **Impacto no legado:** 🟡 Cria novas rotas no frontend, novas tabelas de controle de usuários no banco de dados e adiciona middlewares de verificação de status de conta ativa em todos os endpoints.
- **Reversibilidade:** 🟡 Cara , estabelece um ciclo de governança e aprovação acoplado à arquitetura de dados e regras de negócio de usuários.
- **O que precisa ser verdade para funcionar:** 🟡 É necessário que haja pelo menos um administrador master cadastrado para aprovar e definir os perfis de novos registros.

---

## Opção sempre presente, não construir
- **Em uma frase:** 🟡 Manter a aplicação acessível diretamente na interface operacional existente, gerenciando acessos apenas por links diretos ou senhas compartilhadas entre a equipe sem portal público nem tela de auto-cadastro.
- **Como resolve o problema:** 🟡 Os operadores continuam acessando as ferramentas de alocação e relatórios diretamente, dispensando esforço de desenvolvimento de fachada e controle de usuários.
- **Esforço:** 🟡 Baixo , zero desenvolvimento de código.
- **Impacto no legado:** 🟡 Nenhum.
- **Reversibilidade:** 🟡 Fácil , sem alterações no repositório.
- **O que precisa ser verdade para funcionar:** 🟡 A plataforma ser de uso estritamente restrito a um grupo fixo e reduzido de operadores internos que não demandam autoatendimento nem portal institucional.

## Opção sempre presente, usar algo pronto
- **Em uma frase:** 🟡 Utilizar um template de landing page moderno de mercado e integrar a autenticação e gestão de perfis a um provedor de identidade pronto (ex.: Supabase Auth, Keycloak, Auth0 ou Firebase Auth).
- **Como resolve o problema:** 🟡 Transfere para uma plataforma de autenticação consolidada a responsabilidade por cadastro, segurança de senhas, recuperação de acesso e controle de perfis (RBAC), focando o trabalho local na integração visual.
- **Esforço:** 🟡 Médio , requer adaptação do template da landing page e configuração do middleware de validação de tokens JWT do provedor externo no backend.
- **Impacto no legado:** 🟡 Inclusão de cliente SDK de autenticação e validação de claims externas em `src/api/routes.py`.
- **Reversibilidade:** 🟡 Média , desacoplar um provedor de autenticação externo exige reescrever o armazenamento e emissão de credenciais no banco local.
- **O que precisa ser verdade para funcionar:** 🟡 O ambiente de infraestrutura permitir comunicação e dependência com o provedor de identidade externo ou suportar o serviço conteinerizado.

---
Gerado por reversa-explorer em 2026-08-26T18:04:00-03:00
Sessão: 003-landing-page-apresentacao-login
Nenhuma recomendação emitida por design. Convergência é papel de /reversa-arbiter.
