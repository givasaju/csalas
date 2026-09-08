# Risks: gestao-privativa-instituicoes

> Selo 🟡 PLANEJADO em todos os itens. Documento adversarial por design.

## Premortem
🟡 **Manchete 1:** Vazamento de dados acadêmicos: Coordenador de uma faculdade visualiza restrições, horários e alocações de docentes de faculdade concorrente após esquecimento de filtro em uma rota nova (causa raiz: falha humana em multi-tenancy puramente lógico na camada de aplicação sem garantias no banco de dados).
🟡 **Manchete 2:** Custos de nuvem explodem e sobrecarga operacional de DevOps inviabiliza o negócio ao tentar gerenciar dezenas de servidores e bancos de dados isolados para cada campus cliente (causa raiz: complexidade operacional e subutilização de infraestrutura dedicada).
🟡 **Manchete 3:** Atualização de versão corrompe o banco de dados e paralisa as alocações ao falhar migrações estruturais do Alembic no meio da execução em múltiplos schemas dinâmicos (causa raiz: fragilidade de migrações em múltiplos schemas PostgreSQL).
🟡 **Manchete 4:** Plataforma fica inacessível no primeiro dia do semestre letivo devido a bloqueio de cota de requisições ou instabilidade do provedor de identidade em nuvem (causa raiz: dependência rígida de SaaS externo de autenticação/IAM).

**Manchete que mais assusta o usuário:** 🟡 Manchete 1 (Vazamento de dados acadêmicos entre faculdades concorrentes após esquecimento de filtro em uma rota/query - falha humana em multi-tenancy puramente lógico).

---

## Opção A, Multi-tenancy lógico com discriminador no banco e filtros de aplicação
- **Premissa que mata:** 🟡 A premissa de que desenvolvedores e novos endpoints nunca esquecerão de incluir `institution_id` nas cláusulas de busca, confiando apenas no código da aplicação sem travas estruturais de banco.
- **Teste barato da premissa:** 🟡 Criar uma rota de teste no FastAPI sem injetar o filtro de tenant e disparar uma requisição com usuário autenticado de outro tenant para comprovar se os dados vazam (teste executável em 2 horas).
- **Custo escondido:** 🟡 Implementação mandatória de Row-Level Security (RLS) no PostgreSQL para conter falhas humanas de query, auditoria contínua de endpoints e testes automatizados de invasão cruzada em `src/api/routes.py`.
- **Ponto sem volta:** 🟡 O momento em que o modelo relacional unificado entra em produção e dezenas de instituições passam a coexistir fisicamente nas mesmas tabelas relacionais (`_reversa_sdd/architecture.md`).

## Opção B, Instâncias dedicadas por instituição (Deploy isolado / Single-tenant)
- **Premissa que mata:** 🟡 O modelo financeiro da plataforma gerar receita suficiente para pagar os custos fixos de manter containers, instâncias de banco e balanceadores reservados para cada cliente individual.
- **Teste barato da premissa:** 🟡 Simular o custo mensal em nuvem para hospedar 20 e 50 instâncias separadas do ClassSync AI e confrontar com o valor de mensalidade/assinatura cobrado das instituições (1 dia de planilha/orçamento).
- **Custo escondido:** 🟡 Sobrecarga de manutenção de pipelines de CI/CD para deploy coordenado em dezenas de ambientes, monitoramento distribuído e orquestração de backups individuais (`_reversa_sdd/architecture.md`).
- **Ponto sem volta:** 🟡 Ultrapassar 15 clientes em instâncias separadas com risco de configurações ou versões de banco divergindo manualmente ("drift de infraestrutura").

## Opção C, Multi-tenancy por schemas separados no mesmo banco (PostgreSQL Schemas)
- **Premissa que mata:** 🟡 O SQLAlchemy e o pool assíncrono de conexões do FastAPI conseguirem alternar o `search_path` de forma 100% confiável sob alta concorrência sem "connection pollution" (uma requisição usar a conexão com o schema do tenant anterior).
- **Teste barato da premissa:** 🟡 Escrever um teste de estresse com 50 threads concorrentes alternando requisições entre schemas distintos e validar se houve contaminação cruzada no pool (teste executável em 1 dia).
- **Custo escondido:** 🟡 Scripts customizados do Alembic para iterar e migrar N schemas dinamicamente, além do crescimento de consumo de recursos do PostgreSQL pelo número elevado de tabelas no catálogo.
- **Ponto sem volta:** 🟡 Escalar além de 50 schemas no mesmo banco, tornando as migrações demoradas e as operações de backup/restore de todo o cluster lentas e arriscadas.

---

## Opção sempre presente, não construir
- **Premissa que mata:** 🟡 As instituições clientes aceitarem operar em um sistema mono-cliente, sem pretensão da plataforma de atuar como SaaS ou atender múltiplos campi/universidades.
- **Teste barato da premissa:** 🟡 Conversar com a diretoria/stakeholders e verificar se a ausência de multi-tenancy bloqueia contratos estratégicos em negociação (1 reunião).
- **Custo escondido:** 🟡 Perda irreparável de oportunidade comercial frente a soluções concorrentes que já oferecem operação multi-tenant nativa.
- **Ponto sem volta:** 🟡 Imediato: recusa de contratos por incapacidade arquitetural de segregação de clientes.

## Opção sempre presente, usar algo pronto
- **Premissa que mata:** 🟡 A plataforma de IAM B2B externa (Clerk, Auth0, Zitadel) fornecer os recursos necessários com latência aceitável e custos sustentáveis em moeda local.
- **Teste barato da premissa:** 🟡 Criar conta de avaliação, cadastrar duas organizações fictícias e validar o token JWT emitido em um interceptor FastAPI simples (1 dia de protótipo).
- **Custo escondido:** 🟡 Faturas em dólar que crescem com o volume de usuários ativos mensais (MAU) e falta de autonomia para resolver falhas caso o fornecedor fique indisponível.
- **Ponto sem volta:** 🟡 Acoplamento dos identificadores de usuários e organizações aos schemas proprietários do provedor SaaS externo.

---

## Riscos transversais
🟡 **Proteção de Dados e LGPD:** O sistema lida com dados sensíveis de professores (restrições médicas/pessoais, alocações, carga horária) e turmas; qualquer brecha de isolamento entre instituições caracteriza incidente de segurança grave reportável à ANPD.
🟡 **Evolução da Camada de Autenticação:** A solução adotada precisa se integrar ao fluxo de autenticação e perfis (RBAC) introduzido em `_reversa_sdd/addenda/020-landing-page-login-rbac.md`, adicionando a dimensão obrigatória de `Tenant` / `Institution`.
🟡 **Migração do Modelo Relacional:** Todas as tabelas mapeadas em `_reversa_sdd/architecture.md` (Coordination, Teacher, Room, Class, Restriction, AllocationTask) precisarão ser adaptadas para o modelo de isolamento escolhido.

## O que precisa ser respondido antes de decidir
1. 🟡 Qual é a projeção de escala para os próximos 12 a 24 meses (quantas instituições clientes ativas simultaneamente na plataforma)?
2. 🟡 As instituições aceitam isolamento lógico robusto com proteção no banco de dados (RLS) ou exigem isolamento físico de banco/infraestrutura por contrato?
3. 🟡 A equipe prefere manter o foco exclusivo no código da aplicação (FastAPI) ou possui capacidade de orquestrar infraestrutura de múltiplos containers/deploys?
4. 🟡 Há tolerância e orçamento para depender de um provedor SaaS de IAM B2B em nuvem ou a solução deve ser 100% autocontida/open-source?

---
Gerado por reversa-challenger em 2026-09-07T12:35:00-03:00
Sessão: 004-gestao-privativa-instituicoes
