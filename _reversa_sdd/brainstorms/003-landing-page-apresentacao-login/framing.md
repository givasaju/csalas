# Framing: landing-page-apresentacao-login

> Selo 🟡 PLANEJADO em todos os itens, sujeito a validação.

## Classificação da entrada
🟡 Solução disfarçada de problema, a demanda solicita a criação de uma landing page com login, cadastro e controle por perfil (RBAC), cobrindo a dor de ausência de portal de entrada público/institucional e falta de segmentação segura de acessos no ClassSync AI.

## Problema
🟡 Ausência de uma interface pública moderna e responsiva de apresentação da plataforma e de um fluxo estruturado de onboarding (cadastro e login), dificultando a apresentação institucional e exigindo controle de acesso granular às funcionalidades do sistema com base no perfil definido pelo gestor.

## Quem sente
🟡 Novos usuários, coordenadores de curso, diretores de infraestrutura, docentes e administradores da plataforma que necessitam de uma porta de entrada clara, segura e adaptada às suas atribuições no sistema.

## Quando dói
🟡 No primeiro acesso à aplicação (descoberta e onboarding), no momento do cadastro de novos usuários e no login diário onde cada perfil precisa visualizar apenas os módulos e ações autorizados pelo gestor.

## Custo de não fazer
🟡 Barreiras de adoção da plataforma no campus, impressão de sistema incompleto ou inacessível ao público geral, falta de autoatendimento para novos usuários e risco de acesso indevido a funcionalidades operacionais críticas sem segmentação por perfil.

## Job to be done
🟡 Quando o usuário acessar a plataforma, eu quero que seja apresentada uma landing page elegante, moderna e responsiva com opção de login e cadastro de novo usuário, para conseguir que após login com sucesso o usuário tenha acesso seguro e direcionado às funcionalidades do sistema conforme seu perfil definido pelo gestor da plataforma.

## Fora de escopo declarado
🟡 Alterações nos algoritmos internos do motor de otimização de salas (ACC/AMR/BuildingOptimizer) e reformulação dos serviços de cálculo de alocação de IA (foco exclusivo na landing page institucional, onboarding/cadastro, autenticação e controle de acesso por perfis/RBAC).

## Âncoras no legado
🟡
- `_reversa_sdd/c4-context.md`: Mapeia as personas centrais do sistema (Coordenador de Curso e Diretora de Infraestrutura) e a integração com o Serviço de Autenticação JWT.
- `_reversa_sdd/domain.md`: Descreve os papéis de domínio, permissões operacionais e fluxos de gestão acadêmica do ClassSync AI.
- `_reversa_sdd/architecture.md`: Documenta os módulos do frontend, roteamento de páginas e a camada de API REST (FastAPI).
- `_reversa_sdd/inventory.md`: Mapeia os endpoints existentes em `src/api/routes.py` e o estado dos mocks e interceptadores de autenticação.

---
Gerado por reversa-framer em 2026-08-26T18:03:00-03:00
Sessão: 003-landing-page-apresentacao-login
