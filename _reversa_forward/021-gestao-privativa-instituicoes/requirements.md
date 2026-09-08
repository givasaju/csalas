# Requirements: Gestão e Controle Privativo de Informações entre Instituições (Deploy Isolado Multi-Tenant)

> Identificador: `021-gestao-privativa-instituicoes`
> Data: `2026-09-07`
> Pasta da extração reversa: `_reversa_sdd/` (proveniente do Brainstorm Session 004 `pre-spec.md`)
> Confidência: 🟢 CONFIRMADO, 🟡 INFERIDO, 🔴 LACUNA / DÚVIDA

## 1. Resumo executivo

Estabelecer uma arquitetura de isolamento físico e privativo para a plataforma ClassSync AI entre diferentes instituições clientes, garantindo que usuários autenticados acessem estritamente os dados e informações da sua própria organização. A solução adota o modelo de instâncias dedicadas (Single-Tenant por container/ambiente com banco e volumes desacoplados), provendo templates Docker e Docker Compose parametrizáveis por variáveis de ambiente (`.env`), automação de scripts de provisionamento de novas instituições piloto, rotina centralizada de backup de volumes e configuração de proxy reverso com suporte híbrido a portas locais e subdomínios de produção, eliminando qualquer risco de contaminação cruzada ou vazamento de dados acadêmicos sem alterar o motor de alocação de salas legado.

## 2. Contexto a partir do legado

| Fonte | Trecho relevante | Confidência |
|-------|------------------|-------------|
| `_reversa_sdd/architecture.md#web-app-api` | Estrutura de rotas da API FastAPI (`src/main.py`, `src/api/routes.py`) e entrega dos arquivos estáticos da SPA (`src/api/static/index.html`). | 🟢 |
| `_reversa_sdd/domain.md#glossario` | Estrutura de domínios, coordenações acadêmicas, restrições docentes e regras de alocação que foram modeladas em escopo de campus único. | 🟢 |
| `_reversa_sdd/inventory.md#src/api/routes.py` | Superfície do código, endpoints REST, persistência do banco relacional e inicialização de banco de dados (`src/database.py`). | 🟢 |
| `_reversa_sdd/addenda/020-landing-page-login-rbac.md` | Implementação do fluxo de autenticação com senhas protegidas, emissão de token JWT e autorização por perfis (RBAC). | 🟢 |
| `_reversa_sdd/brainstorms/004-gestao-privativa-instituicoes/pre-spec.md` | Especificação de ideação com aprovação da Opção B (Deploy isolado com containers e volumes independentes). | 🟢 |

## 3. Personas e cenários de uso

| Persona | Objetivo | Cenário-chave |
|---------|----------|---------------|
| Administrador de TI / DevOps da Plataforma | Provisionar rapidamente uma nova instituição cliente com total isolamento | Executa o script de provisionamento informando o identificador da instituição; o sistema cria a pasta de dados, gera chaves criptográficas exclusivas e sobe a instância dedicada pronta para uso. |
| Gestor da Instituição Cliente (ex.: Faculdade A) | Administrar usuários, salas, turmas e docentes da sua instituição com garantia de sigilo | Acessa a URL ou subdomínio exclusivo da sua instituição, efetua login como gestor e gerencia o campus sabendo que nenhum dado seu é compartilhado com concorrentes. |
| Coordenador / Docente da Instituição | Visualizar e registrar dados acadêmicos de sua unidade de ensino | Conecta-se ao portal de sua faculdade, realiza login seguro e interage apenas com as coordenações, salas e grades vinculadas à sua instituição. |

## 4. Regras de negócio novas ou alteradas

1. **RN-01: Segregação Física de Dados e Armazenamento Híbrido:** 🟢
   - Cada instituição possui seu próprio banco de dados persistente em volume desacoplado no host (`/data/{TENANT_NAME}/`).
   - A aplicação suporta configuração transparente via variável `DATABASE_URL`, utilizando SQLite em arquivo montado como padrão leve e suporte direto a PostgreSQL para ambientes de alta concorrência.
2. **RN-02: Isolamento Criptográfico de Tokens (JWT):** 🟢
   - Cada instância de instituição utiliza uma chave de assinatura secreta (`SECRET_KEY`) própria e gerada aleatoriamente no provisionamento.
   - Tokens emitidos pela Instituição A são sumariamente rejeitados como inválidos pela Instituição B.
3. **RN-03: Parametrização Integral por Variáveis de Ambiente:** 🟢
   - Nenhuma informação de porta, caminhos de montagem ou segredos fica hardcoded no código.
   - Toda a parametrização da instância é injetada via arquivo de variáveis de ambiente (`.env`).
4. **RN-04: Provisionamento Automatizado Padronizado:** 🟢
   - O provisionamento de uma nova instituição piloto é executado através de script único (`deploy-institution.sh` / `.ps1`), sem dependência de passos manuais.
5. **RN-05: Roteamento Privativo e Flexível (Local e Produção):** 🟢
   - Em ambiente local e homologação, cada instituição expõe uma porta HTTP dedicada (ex.: `:8001`, `:8002`).
   - Em produção, um proxy reverso (Nginx/Caddy) mapeia subdomínios (ex.: `{tenant}.classsync.ai`) para os respectivos containers sem sobreposição de sessões.
6. **RN-06: Rotinas Centralizadas de Backup:** 🟢
   - O administrador do host pode executar um script consolidado de backup para gerar snapshots arquivados e compactados dos volumes de todas as instituições de forma não disruptiva.

## 5. Requisitos Funcionais

| ID | Requisito | Prioridade | Critério de aceite | Confidência |
|----|-----------|------------|--------------------|-------------|
| RF-01 | Criar `Dockerfile` otimizado e multi-stage para empacotar a aplicação ClassSync AI (FastAPI + dependências + frontend estático). | Must | Imagem construída com sucesso, leve e executável de forma autônoma com suporte a `DATABASE_URL`. | 🟢 |
| RF-02 | Criar template `docker-compose.yml` e arquivo de configuração modelo `.env.example` com variáveis parametrizáveis (`TENANT_NAME`, `PORT`, `DATA_DIR`, `SECRET_KEY`, `DATABASE_URL`, `APP_ENV`). | Must | Permite instanciar o serviço apontando para portas e volumes isolados no host. | 🟢 |
| RF-03 | Desenvolver scripts de provisionamento automatizado (`scripts/deploy-institution.sh` e `deploy-institution.ps1`) para criação de novas instituições. | Must | Comando único cria o diretório de dados, gera `.env` com segredos seguros e inicializa a instância via Docker Compose. | 🟢 |
| RF-04 | Configurar template de Proxy Reverso (Nginx / Caddy) para roteamento de tráfego institucional com suporte a subdomínios e portas locais. | Must | O proxy encaminha requisições do subdomínio correto para a respectiva porta do container com headers de segurança (`X-Forwarded-For`, `X-Forwarded-Proto`). | 🟢 |
| RF-05 | Criar suíte de testes de validação de isolamento multi-instituição (`tests/test_multi_tenant_isolation.py`). | Must | Testes automatizados confirmam que dados criados na Instância A não existem na Instância B e que tokens JWT são incompatíveis entre instâncias. | 🟢 |
| RF-06 | Implementar endpoint de health check e identificação da instância (`GET /health` ou `GET /api/v1/health`). | Should | Retorna o status da aplicação e o identificador configurado da instituição em formato JSON. | 🟢 |
| RF-07 | Desenvolver scripts de backup e restauração (`scripts/backup-institutions.sh` e `backup-institutions.ps1`). | Should | Script executa no host, compacta os volumes de dados de cada instituição ativa e armazena em pasta de snapshots com timestamp. | 🟢 |

## 6. Requisitos Não Funcionais

| Tipo | Requisito | Evidência ou justificativa | Confidência |
|------|-----------|----------------------------|-------------|
| Segurança e Privacidade | Isolamento estrito de dados e conformidade com LGPD; credenciais e tokens segregados por cliente. | `_reversa_sdd/brainstorms/004-gestao-privativa-instituicoes/risks.md` | 🟢 |
| Desempenho e Eficiência | Cada container deve ter consumo balanceado de recursos e suporte a concorrência assíncrona com Uvicorn. | `_reversa_sdd/architecture.md#web-app-api` | 🟢 |
| Portabilidade | Capacidade de rodar de forma idêntica em servidores locais de desenvolvimento e em provedores de nuvem (AWS/GCP/DigitalOcean). | `_reversa_sdd/brainstorms/004-gestao-privativa-instituicoes/decision.md` | 🟢 |
| Manutenibilidade | Zero impacto nas rotas de negócio e no motor de alocação de salas (`core-allocation-engine`), mantendo o código da aplicação single-tenant. | `_reversa_sdd/brainstorms/004-gestao-privativa-instituicoes/decision.md` | 🟢 |

## 7. Critérios de Aceitação

```gherkin
Cenário: Inicialização e isolamento de dados entre duas instituições distintas
  Dado que foram provisionadas a "Faculdade Alpha" na porta 8001 e a "Faculdade Beta" na porta 8002
  Quando o gestor da "Faculdade Alpha" cadastra uma turma "Engenharia de Software 101"
  E o gestor da "Faculdade Beta" consulta a listagem de turmas da sua instituição
  Então a turma "Engenharia de Software 101" não deve ser retornada na resposta da "Faculdade Beta"
  E o banco de dados da "Faculdade Beta" não deve conter nenhum registro da "Faculdade Alpha"

Cenário: Rejeição de token JWT cruzado entre instituições
  Dado que um usuário obteve um token de autenticação válido na "Faculdade Alpha"
  Quando esse mesmo token for enviado no cabeçalho Authorization para um endpoint protegido da "Faculdade Beta"
  Então a requisição deve ser rejeitada com código HTTP 401 Unauthorized

Cenário: Execução do script centralizado de backup
  Dado que existem duas instituições com dados cadastrados
  Quando o administrador executar o script de backup no host
  Então deve ser gerado um arquivo de snapshot compactado para cada instituição com integridade preservada
```

## 8. Prioridade MoSCoW

| Item | MoSCoW | Justificativa |
|------|--------|---------------|
| RF-01 (Dockerfile Otimizado) | Must | Base fundamental para empacotamento e execução padronizada. |
| RF-02 (Docker Compose Parametrizado) | Must | Permite rodar múltiplas instâncias sem colisão de portas ou volumes. |
| RF-03 (Script de Provisionamento) | Must | Garante repetibilidade, criação de segredos e agilidade operacional. |
| RF-04 (Proxy Reverso de Roteamento) | Must | Ponto de entrada unificado e flexível para clientes institucionais. |
| RF-05 (Testes de Isolamento) | Must | Comprovação técnica obrigatória de ausência de vazamento de dados. |
| RF-06 (Health Check e Identificação) | Should | Facilita o monitoramento contínuo das instâncias ativas. |
| RF-07 (Scripts de Backup Centralizado) | Should | Assegura continuidade de negócios e proteção contra perda de dados. |

## 9. Esclarecimentos

### Sessão 2026-09-07

- **Q:** Como deve ser estruturado o roteamento de rede para as instituições?
  **R:** Suporte flexível e desacoplado: portas diretas configuráveis via `.env` para execução e testes locais (ex.: `:8001`, `:8002`) e suporte a proxy reverso com roteamento por subdomínios (ex.: `*.classsync.ai`) para ambientes de produção.
- **Q:** Qual mecanismo de banco de dados deve ser utilizado em cada instância institucional?
  **R:** Arquitetura híbrida e parametrizável via `DATABASE_URL`: SQLite em volume persistente dedicado como padrão leve e zero-configuração (para desenvolvimento, testes e pilotos com consumo mínimo de recursos), com suporte transparente a instâncias PostgreSQL em produção apenas alterando a string de conexão.
- **Q:** Como devem ser organizadas as rotinas de backup e restauração dos dados?
  **R:** Script centralizado executado no host (`scripts/backup-institutions.sh` e `backup-institutions.ps1`) capaz de iterar sobre os diretórios de dados de todas as instituições provisionadas e gerar snapshots compactados dos volumes de dados de forma consistente.

## 10. Lacunas

Nenhuma dúvida pendente. Todas as lacunas técnicas e de escopo foram esclarecidas na sessão de 2026-09-07.

## 11. Histórico de alterações

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-09-07 | Versão inicial gerada por `/reversa-requirements` a partir do Brainstorm Session 004 | reversa |
| 2026-09-07 | Resolução das 3 dúvidas técnicas via `/reversa-clarify` (roteamento flexível, persistência híbrida e backups centralizados) | reversa |
