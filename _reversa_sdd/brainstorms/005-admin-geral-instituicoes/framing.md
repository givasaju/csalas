# Framing, admin-geral-instituicoes

> Selo 🟡 PLANEJADO em todos os itens, sujeito a validação.

## Classificação da entrada
🟡 Solução disfarçada de problema: o usuário solicita a construção de uma interface administrativa central com papéis hierárquicos específicos ('doctor-chef' e 'master-chef') para resolver o atrito de onboarding manual e governança de instâncias institucionais.

## Problema
🟡 Ausência de uma interface visual administrativa e centralizada (SaaS SuperAdmin) para criação e delegação de instâncias institucionais. Atualmente, o provisionamento depende de rotinas técnicas de terminal e scripts no host, impedindo que o administrador geral da plataforma ('doctor-chef') cadastre novas instituições de forma amigável e delegue a gestão inicial para o responsável institucional ('master-chef').

## Quem sente
🟡 O administrador global da plataforma ('doctor-chef'), que precisa operar tarefas de infraestrutura sem uma interface visual centralizada, e o gestor geral da instituição ('master-chef'), que depende de processos manuais para receber seu acesso e começar a governar os administradores e coordenadores de sua instituição.

## Quando dói
🟡 No momento do onboarding de novos clientes (instituições de ensino) e na transferência da governança administrativa, quando é necessário instanciar a unidade e vincular o seu primeiro gestor responsável.

## Custo de não fazer
🟡 Gargalo operacional direto e incapacidade de escalar a plataforma ClassSync AI como produto SaaS para múltiplas instituições; dependência permanente de intervenção manual da equipe de infraestrutura para criar instâncias e cadastrar gestores; risco de erros humanos em configurações e morosidade no início de operação dos clientes.

## Job to be done
🟡 Quando o usuário 'doctor-chef' logar na plataforma, ele quer acessar uma UI de gestão de instituições para cadastrar uma nova instituição e definir o login do usuário 'master-chef', para conseguir delegar a governança e gestão da respectiva instância institucional de forma amigável, autônoma e segura.

## Fora de escopo declarado
🟡 A gestão operacional e acadêmica interna da instituição (distribuição de turmas, docentes e alocação de salas), que permanece sob responsabilidade estrita dos usuários locais ('master-chef', gestores locais, coordenadores e docentes) no ecossistema isolado de cada instituição.

## Âncoras no legado
🟡
- _reversa_sdd/addenda/021-gestao-privativa-instituicoes.md: Estabeleceu o modelo de isolamento físico multi-tenant (Single-Tenant por container/ambiente com banco e volumes desacoplados), provisionado via scripts em scripts/deploy-institution.ps1 e .sh.
- _reversa_sdd/addenda/020-landing-page-login-rbac.md e src/api/auth.py: Definiu a autenticação JWT e perfis de usuário (gestor, coordenador, docente). O perfil 'doctor-chef' representa uma camada de superadministração global da plataforma.
- _reversa_sdd/architecture.md#web-app-api: Arquitetura de rotas FastAPI e interface SPA via arquivos estáticos (src/api/static/).

---
Gerado por reversa-framer em 2026-09-07T16:20:00-03:00
Sessão: 005-admin-geral-instituicoes
