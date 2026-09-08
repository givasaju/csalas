# Options: gestao-privativa-instituicoes

> Selo 🟡 PLANEJADO em todos os itens. Nenhuma opção foi escolhida ainda.

## Problema de referência
🟡 Quando o usuário logar na plataforma, eu quero que ele acesse somente as informações referentes a sua instituição, para manter a privacidade das informações e dados.

## Restrições ativas
🟡 Nenhuma restrição rígida declarada pelo usuário até o momento.

---

## Opção A, Multi-tenancy lógico com discriminador no banco e filtros de aplicação
- **Em uma frase:** 🟡 Compartilhar o mesmo banco e API, adicionando a chave `institution_id` a todas as tabelas e aplicando filtros obrigatórios nas queries com base no token do usuário.
- **Como resolve o problema:** 🟡 No momento da autenticação, o token JWT do usuário carrega o identificador de sua instituição; a camada de backend intercepta e limita todas as consultas e mutações exclusivamente a esse escopo institucional.
- **Esforço:** 🟡 Médio, requer migração do modelo relacional em todas as entidades (adicionar `institution_id`), criação de índices compostos e implementação de middleware/dependência no FastAPI para injeção automática do filtro.
- **Impacto no legado:** 🟡 Modifica os modelos relacionais descritos em `_reversa_sdd/architecture.md` (Coordination, Room, Teacher, Class, AllocationTask) e exige revisão de todas as rotas e queries do motor de alocação.
- **Reversibilidade:** 🟡 Cara, remover a coluna discriminadora e desfazer a lógica de filtro transversal em todo o backend exigiria ampla refatoração.
- **O que precisa ser verdade para funcionar:** 🟡 As regras de filtragem devem ser infalíveis (ou garantidas por Row-Level Security no banco) para evitar qualquer brecha onde uma query sem filtro exponha dados entre instituições.

## Opção B, Instâncias dedicadas por instituição (Deploy isolado / Single-tenant)
- **Em uma frase:** 🟡 Manter o código da aplicação exatamente como está (mono-instituição) e provisionar uma instância de container e banco de dados separada para cada instituição cliente.
- **Como resolve o problema:** 🟡 Cada instituição recebe um subdomínio ou URL dedicada conectada a um banco fisicamente isolado; o isolamento é garantido na camada de rede e infraestrutura, eliminando possibilidade de acesso cruzado no nível de aplicação.
- **Esforço:** 🟡 Baixo no código da aplicação; Médio em infraestrutura e orquestração de deploy (CI/CD, Docker, ingress/proxy reverso).
- **Impacto no legado:** 🟡 Praticamente nenhum no código existente do ClassSync AI, preservando integralmente os módulos FastAPI e o motor de alocação.
- **Reversibilidade:** 🟡 Fácil, bancos individuais podem ser facilmente exportados, migrados ou consolidados posteriormente caso a estratégia mude.
- **O que precisa ser verdade para funcionar:** 🟡 A quantidade de instituições deve ser compatível com os custos operacionais e a capacidade da equipe de gerenciar múltiplos deploys.

## Opção C, Multi-tenancy por schemas separados no mesmo banco (PostgreSQL Schemas)
- **Em uma frase:** 🟡 Utilizar uma única instância de banco de dados relacional, mantendo schemas estruturais independentes (`schema_inst_a`, `schema_inst_b`) para cada instituição cliente.
- **Como resolve o problema:** 🟡 Após a validação do token do usuário na requisição, a aplicação define o contexto de busca (`search_path`) para o schema da respectiva instituição, mantendo isolamento lógico de tabelas sem duplicar servidores.
- **Esforço:** 🟡 Alto, exige suporte dinâmico a múltiplos schemas no SQLAlchemy e rotinas de migração (Alembic) que repliquem alterações estruturais para todos os schemas existentes.
- **Impacto no legado:** 🟡 Altera a camada de gerenciamento de sessões e conexões do banco de dados no backend, mantendo a estrutura interna das tabelas inalterada.
- **Reversibilidade:** 🟡 Média, cada schema pode ser individualmente extraído via dump ou transformado em banco independente.
- **O que precisa ser verdade para funcionar:** 🟡 O motor de banco de dados deve suportar schemas nativos (PostgreSQL) e o pool de conexões da API precisa isolar estritamente o contexto de schema entre requisições assíncronas concorrentes.

---

## Opção sempre presente, não construir
- **Em uma frase:** 🟡 Manter a plataforma estritamente dedicada a uma única instituição por instalação, resolvendo a segregação por acordos comerciais e processos operacionais.
- **Como resolve o problema:** 🟡 Evita o risco de vazamento de dados ao não permitir a coexistência de múltiplas organizações no mesmo ambiente operacional.
- **Esforço:** 🟡 Baixo, zero esforço de desenvolvimento e zero modificação de arquitetura.
- **Impacto no legado:** 🟡 Nenhum no código existente.
- **Reversibilidade:** 🟡 Fácil, o desenvolvimento de qualquer solução técnica de isolamento pode ser iniciado quando houver necessidade concreta de expansão.
- **O que precisa ser verdade para funcionar:** 🟡 O modelo de negócios da plataforma não depender de operação simultânea de várias faculdades/universidades em um mesmo serviço compartilhado.

## Opção sempre presente, usar algo pronto
- **Em uma frase:** 🟡 Adotar uma solução pronta de identidade e gerenciamento de organizações B2B (como Auth0 Organizations, Clerk B2B ou Zitadel) para governar o isolamento e tenant dos usuários.
- **Como resolve o problema:** 🟡 A plataforma de mercado gerencia os cadastros institucionais, convites de membros e atribuição de permissões, entregando no token JWT o identificador validado da instituição do usuário.
- **Esforço:** 🟡 Médio, envolve a contratação, configuração do serviço externo e integração do middleware/SDK de autenticação na API FastAPI.
- **Impacto no legado:** 🟡 Substitui o serviço mockado de autenticação JWT documentado na arquitetura, delegando a validação de identidade e organização ao provedor externo.
- **Reversibilidade:** 🟡 Média, trocar de provedor de identidade no futuro exige exportação de usuários e reconfiguração de tokens.
- **O que precisa ser verdade para funcionar:** 🟡 A instituição aceitar dependência de serviço externo (SaaS/nuvem de autenticação) e arcar com os custos de licenciamento por usuário ativo/organização.

---
Gerado por reversa-explorer em 2026-09-07T12:32:00-03:00
Sessão: 004-gestao-privativa-instituicoes
Nenhuma recomendação emitida por design. Convergência é papel de /reversa-arbiter.
