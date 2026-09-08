# Legacy Impact: Gestão e Controle Privativo de Informações entre Instituições (Deploy Isolado Multi-Tenant)

> Identificador: `021-gestao-privativa-instituicoes`
> Data: `2026-09-07`
> Política de Edição do Legado: `allowLegacyEdits: true` com caminhos autorizados em `allowedPaths` (`src/**`, `data/**`, `tests/**`, `scripts/**`, `nginx/**`, `Dockerfile`, `docker-compose.yml`, `.env.example`)

## 1. Arquivos Afetados

| Arquivo afetado | Componente | Tipo | Severidade | Justificativa |
|-----------------|------------|------|------------|---------------|
| `src/database.py` | `database-schema` (`_reversa_sdd/architecture.md#database`) | `regra-alterada` | LOW | Adição de suporte à variável de ambiente `DATABASE_URL` com criação automática de diretórios e fallback para SQLite. |
| `src/api/auth.py` | `jwt-auth-service` (`_reversa_sdd/c4-context.md#personas`) | `regra-alterada` | LOW | Obtenção dinâmica da `SECRET_KEY` a partir do ambiente para isolamento de assinatura JWT por instituição. |
| `src/api/routes.py` | `web-app-api` (`_reversa_sdd/architecture.md#web-app-api`) | `contrato-novo` | LOW | Implementação do endpoint de health check `GET /api/v1/health` com verificação de banco e identificação do tenant. |
| `src/main.py` | `web-app-api` (`_reversa_sdd/architecture.md#web-app-api`) | `componente-alterado` | LOW | Suporte a `HOST` dinâmico para execução em container e rota raiz `/health`. |
| `data/.gitignore` | `infra-storage` | `componente-novo` | LOW | Criação da pasta de volumes persistentes desacoplados para cada cliente, ignorando bancos no Git. |
| `tests/test_multi_tenant_isolation.py` | `test-suite` | `componente-novo` | LOW | Suíte de testes automatizados cobrindo segregação de banco, ausência de vazamento de dados e rejeição de JWT cruzado. |
| `Dockerfile` | `infra-container` | `componente-novo` | LOW | Imagem Docker multi-stage otimizada para o ClassSync AI baseada em Python 3.11-slim. |
| `docker-compose.yml` | `infra-container` | `componente-novo` | LOW | Orquestração parametrizada de instâncias dedicadas por variáveis de ambiente. |
| `.env.example` | `infra-container` | `componente-novo` | LOW | Template com documentação de todas as variáveis obrigatórias para provisionar um tenant. |
| `scripts/deploy-institution.sh` / `.ps1` | `infra-automation` | `componente-novo` | LOW | Automação multiplataforma para provisionar uma nova instituição em 1 comando. |
| `nginx/nginx.conf` | `infra-network` | `componente-novo` | LOW | Template de Proxy Reverso corporativo mapeando subdomínios institucionais com headers de segurança. |
| `scripts/backup-institutions.sh` / `.ps1` | `infra-automation` | `componente-novo` | LOW | Scripts centralizados no host para arquivamento e snapshots compactados dos dados dos clientes. |

## 2. Diff Conceitual por Componente

### `database-schema` & `infra-storage`
- **Isolamento Físico de Dados:** Em vez de poluir tabelas relacionais com chaves estrangeiras complexas de multi-tenancy lógico, cada instituição cliente ganha um banco de dados independente e volume isolado em `./data/{TENANT_NAME}/`.
- **Hibridismo de Banco:** `DATABASE_URL` permite que ambientes locais e pilotos usem SQLite em volume montado com zero custo, enquanto ambientes de nuvem corporativa conectam diretamente a bancos PostgreSQL alterando apenas a string de conexão.

### `jwt-auth-service`
- **Isolamento Criptográfico:** A `SECRET_KEY` exclusiva gerada para cada instituição impede categoricamente que credenciais ou tokens de uma faculdade sejam aceitos por outra, mesmo que ambas usem o mesmo software base.

### `web-app-api` & `test-suite`
- **Diagnóstico e Observabilidade:** Endpoint `/api/v1/health` permite que orquestradores de container, proxies reversos e administradores inspecionem instantaneamente a saúde da aplicação e qual organização aquele container está atendendo.
- **Validação de Inviolabilidade:** 70/70 testes aprovados no projeto, assegurando zero regressão nos algoritmos e modelos legados.

## 3. Regras Preservadas

| Regra | Arquivo no Legado | Status |
|-------|-------------------|--------|
| Motor multiagente de alocação de salas (ACC / AMR / BuildingOptimizer) | `_reversa_sdd/architecture.md#core-allocation-engine` | 100% Intacto |
| Módulo de Gestão de Docentes, Ambientes e Restrições | `_reversa_sdd/architecture.md#academic-space-manager` | 100% Intacto |
| Landing Page institucional, Cadastro, Login e RBAC local | `_reversa_forward/020-landing-page-login-rbac/` | 100% Intacto |
| Compatibilidade de testes com token estático `test-valid-token` | `src/api/auth.py` | Preservada |

## 4. Regras Modificadas

| Regra Original | Nova Regra | Justificativa |
|----------------|------------|---------------|
| Banco de dados SQLite fixo no caminho local `../db/project.db` | Caminho do banco configurável dinamicamente via `DATABASE_URL` | Viabilizar volumes desacoplados por instituição em containers dedicados. |
| Chave de token JWT estática fixa no código | `SECRET_KEY` lida dinamicamente do ambiente com geração aleatória no provisionamento | Garantir isolamento criptográfico e impossibilidade de acesso cruzado de tokens entre clientes. |
