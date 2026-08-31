# Pre-Spec: landing-page-apresentacao-login

> Selo 🟡 PLANEJADO. Insumo de entrada para o próximo pipeline, não é uma spec.

## Problema
🟡 Ausência de uma interface pública moderna e responsiva de apresentação da plataforma e de um fluxo estruturado de onboarding (cadastro e login), dificultando a apresentação institucional e exigindo controle de acesso granular às funcionalidades do sistema com base no perfil definido pelo gestor.

## Caminho escolhido
🟡 **Opção A: Landing Page Institucional Integrada com Auth Nativa e RBAC Local**, disponibilizando uma landing page pública moderna com formulários de login/cadastro e controle de acesso por perfis gerenciado localmente no backend FastAPI.

## Escopo mínimo da primeira entrega
🟡
1. **Landing Page Institucional**: Interface elegante e totalmente responsiva contendo Hero Section com proposta de valor, apresentação dos recursos de IA de alocação de salas, benefícios de otimização de espaços e chamadas para ação (CTA).
2. **Autenticação e Cadastro**: Componentes modais ou painel para Login e Auto-Cadastro (Sign-up) com validação de dados e emissão de token JWT.
3. **Controle de Acesso por Perfil (RBAC)**: Direcionamento pós-login e controle de visibilidade das funcionalidades conforme o papel do usuário (Gestor, Coordenador, Docente) definido pelo gestor.
4. **Segurança de Rotas no Backend**: Implementação de dependência/middleware de autenticação e autorização por role nas rotas protegidas da API FastAPI.

## Não-objetivos
🟡
- Integração com provedores corporativos externos de Single Sign-On (SAML/OAuth2/Google/Microsoft) nesta fatia inicial.
- Fluxo complexo de recuperação de senha por envio de e-mails transacionais via SMTP externo.
- Modificação dos algoritmos centrais do motor de alocação de salas (ACC/AMR/BuildingOptimizer).

## Restrições ativas
🟡 Manter a compatibilidade com a stack arquitetural do projeto (Python/FastAPI no backend, HTML/CSS responsivo/JS no frontend, SQLite como banco relacional).

## Critério de pronto
🟡 Qualquer visitante consegue acessar a URL pública da plataforma no navegador (desktop ou mobile), visualizar a apresentação institucional moderna, realizar cadastro e login com sucesso, e acessar exclusivamente os módulos do sistema correspondentes ao seu perfil de usuário atribuído pelo gestor.

## Premissa a validar primeiro
🟡 Criar e validar a dependência FastAPI de verificação de permissões (`require_roles`) no backend e verificar a responsividade fluida da grade visual no mobile.

## Riscos herdados
🟡 Assegurar armazenamento criptográfico de senhas com algoritmo robusto (bcrypt) e garantir que a proteção de dados seja estrita no backend (`src/api/routes.py`), não apenas por ocultação de abas no frontend.

## Âncoras no legado
🟡
- `_reversa_sdd/c4-context.md`: Mapeia as personas (Coordenador de Curso, Diretora de Infraestrutura) e o serviço JWT.
- `_reversa_sdd/domain.md`: Estrutura de papéis e regras de operação do ClassSync AI.
- `_reversa_sdd/architecture.md`: Estrutura de rotas FastAPI e frontend SPA.
- `_reversa_sdd/inventory.md`: Endpoints existentes em `src/api/routes.py`.

## Dúvidas abertas
- [DÚVIDA] 🟡 Qual será o perfil atribuído por padrão no momento do auto-cadastro (ex.: perfil com permissões de visualizador/docente até que o gestor eleve para coordenador/admin)?
- [DÚVIDA] 🟡 Quais seções visuais complementares na landing page são prioritárias (ex.: estatísticas de salas otimizadas, demonstração interativa ou FAQ)?

---
Gerado por reversa-pre-spec em 2026-08-26T18:10:40-03:00
Sessão: 003-landing-page-apresentacao-login
Destino sugerido: /reversa-requirements
