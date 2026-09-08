# Pre-Spec: gestao-privativa-instituicoes

> Selo 🟡 PLANEJADO. Insumo de entrada para o próximo pipeline, não é uma spec.

## Problema
🟡 Ausência de isolamento estrito e controle privativo de informações entre diferentes instituições na plataforma, gerando risco de visualização não autorizada, vazamento de dados estratégicos/pessoais (professores, horários, salas, turmas) e quebra de confidencialidade entre organizações distintas.

## Caminho escolhido
🟡 Opção B: Instâncias dedicadas por instituição (Deploy isolado / Single-tenant), garantindo segregação física total de dados e infraestrutura via containers e volumes desacoplados, sem necessidade de refatorar os algoritmos do motor do ClassSync AI.

## Escopo mínimo da primeira entrega
🟡
1. **Template Docker e Compose Parametrizado:** Criação de `Dockerfile` otimizado e `docker-compose.yml` parametrizável por arquivo `.env` para instanciar o ClassSync AI (FastAPI + Frontend + Banco) com portas, volumes e credenciais isoladas.
2. **Script de Provisionamento Automatizado:** Script (Bash/PowerShell) para subir uma nova instituição piloto com um comando, configurando nome do tenant, porta, segredos JWT (`SECRET_KEY`) e diretório de dados persistentes.
3. **Roteamento Básico / Proxy:** Configuração de proxy reverso (Nginx/Caddy/Traefik) para direcionar o tráfego de cada instituição para seu respectivo container dedicado.

## Não-objetivos
🟡
- Painel web self-service para auto-criação de tenants e onboarding automático de novas instituições sem intervenção técnica.
- Módulo financeiro de faturamento, split de pagamentos ou cobrança de assinaturas por cartão/PIX.
- Refatoração profunda do modelo relacional interno para multi-tenancy lógico unificado na mesma tabela de banco.

## Restrições ativas
🟡
- Stack baseada em Docker e Docker Compose como padrão de empacotamento e orquestração inicial.
- Segregação física de dados: cada instituição deve possuir seu próprio banco de dados e volume de armazenamento estritamente desacoplado.
- Chaves criptográficas de autenticação JWT independentes por instituição cliente.

## Critério de pronto
🟡 Duas instâncias operacionais em paralelo (ex.: `faculdade-a` e `faculdade-b`), com dados cadastrados de turmas/docentes/salas em cada uma, onde um usuário logado na `faculdade-a` é comprovadamente incapaz de acessar, visualizar ou alterar qualquer registro pertencente à `faculdade-b`.

## Premissa a validar primeiro
🟡 Realizar simulação orçamentária em planilha dos custos de nuvem para hospedar instâncias dedicadas (5, 10 e 20 clientes) e testar a inicialização concorrente de 2 instâncias em máquina local sem conflito de portas ou dados.

## Riscos herdados
🟡
- Sobrecarga de DevOps para gerenciar e monitorar dezenas de containers e bancos de dados separados no longo prazo.
- Risco de drift de configuração entre instâncias se as atualizações de versão não forem orquestradas por pipelines centralizados.

## Âncoras no legado
🟡
- `_reversa_sdd/architecture.md`: Arquitetura do monolito FastAPI e frontend estático SPA do ClassSync AI.
- `_reversa_sdd/inventory.md`: Dependências de ambiente e pontos de persistência atuais.
- `_reversa_sdd/addenda/020-landing-page-login-rbac.md`: Mecanismo de autenticação e RBAC que rodará isolado dentro de cada instância institucional.

## Dúvidas abertas
- [DÚVIDA] 🟡 O roteamento de entrada entre as instituições deve priorizar subdomínios (ex.: `faculdade1.classsync.ai`) ou portas/prefixos de caminho (ex.: `:8001`, `:8002` ou `/faculdade1`)?
- [DÚVIDA] 🟡 O banco de dados de cada instância dedicada continuará com SQLite em arquivo desacoplado ou já iniciará com um container PostgreSQL dedicado por tenant?
- [DÚVIDA] 🟡 As rotinas de backup e restore dos volumes devem ser centralizadas em um script do servidor hospedeiro ou gerenciadas dentro de cada container?

---
Gerado por reversa-pre-spec em 2026-09-07T12:43:00-03:00
Sessão: 004-gestao-privativa-instituicoes
Destino sugerido: /reversa-requirements
