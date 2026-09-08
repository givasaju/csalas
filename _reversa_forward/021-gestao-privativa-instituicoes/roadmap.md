# Roadmap: Gestão e Controle Privativo de Informações entre Instituições (Deploy Isolado Multi-Tenant)

> Identificador: `021-gestao-privativa-instituicoes`
> Data: `2026-09-07`
> Requirements: `_reversa_forward/021-gestao-privativa-instituicoes/requirements.md`
> Confidência: 🟢 CONFIRMADO, 🟡 INFERIDO, 🔴 LACUNA

## 1. Resumo da abordagem

A implementação estabelece a segregação física e privativa de dados entre múltiplas instituições clientes na plataforma ClassSync AI através de containerização dedicada e automação de infraestrutura:
1. **Containerização Otimizada (`Dockerfile`)**: Empacotar a aplicação monolítica (API FastAPI + Frontend estático) em imagem Docker multi-stage leve com Python 3.11, configurando Uvicorn com inicialização assíncrona orientada a variáveis de ambiente (`PORT`, `DATABASE_URL`, `SECRET_KEY`, `TENANT_NAME`).
2. **Orquestração Parametrizada (`docker-compose.yml` e `.env.example`)**: Prover manifesto Docker Compose e arquivo modelo `.env` definindo portas configuráveis, injeção de segredos criptográficos exclusivos e montagem de volumes desacoplados no host (`./data/{TENANT_NAME}:/app/data`).
3. **Scripts de Automação de Provisionamento (`scripts/deploy-institution.sh` e `.ps1`)**: Desenvolver scripts em Bash e PowerShell para criar uma nova instituição com um único comando, criando o diretório de dados dedicado, gerando chaves JWT aleatórias e inicializando a instância de forma isolada.
4. **Roteamento e Proxy Reverso Flexível (`nginx/nginx.conf`)**: Configurar template de proxy reverso com suporte a roteamento de subdomínios (`{tenant}.classsync.ai`) para ambientes de produção, mantendo acesso direto por portas locais (`:8001`, `:8002`) para desenvolvimento.
5. **Rotinas Centralizadas de Backup (`scripts/backup-institutions.sh` e `.ps1`)**: Implementar scripts executados no servidor host para iterar sobre os diretórios de dados de todas as instituições e gerar snapshots compactados `.tar.gz` com carimbo de data/hora.
6. **Suíte de Testes Automatizados de Isolamento (`tests/test_multi_tenant_isolation.py`)**: Criar testes automatizados de integração que provisionam contextos de duas instituições simultâneas (`inst_alpha` e `inst_beta`), comprovando a incomunicabilidade de dados acadêmicos e a rejeição de tokens JWT cruzados.
7. **Endpoint de Health Check e Metadados (`GET /api/v1/health`)**: Rota leve retornando status de integridade da API, timestamp e identificador institucional configurado.

## 2. Princípios aplicados

| Princípio | Como a feature se relaciona | Status |
|-----------|------------------------------|--------|
| Isolamento Estrito e LGPD | Garante que cada cliente possua armazenamento e credenciais segregados por barreira física/processual. | respeita |
| Não-Destrutivo ao Legado | Mantém 100% intactos os algoritmos do motor de alocação cooperativa de salas (`core-allocation-engine`). | respeita |
| Infraestrutura como Código (IaC) | Todo o ciclo de vida das instâncias é automatizado e versionado em templates e scripts auditáveis. | respeita |
| Portabilidade e Simplicidade | Utiliza Docker/Docker Compose e suporte a SQLite/Postgres híbrido, viável tanto em ambiente local quanto em nuvem. | respeita |

## 3. Decisões técnicas

| ID | Decisão | Justificativa | Alternativas descartadas | Confidência |
|----|---------|----------------|--------------------------|-------------|
| D-01 | Adoção do modelo Single-Tenant por Container (Isolamento Físico de Instâncias) | Elimina por design qualquer possibilidade de vazamento de dados por query sem filtro e preserva o código legado | Multi-tenancy lógico com discriminador `institution_id` no mesmo banco compartilhado | 🟢 |
| D-02 | Persistência híbrida via `DATABASE_URL` (SQLite padrão em volume montado e suporte a PostgreSQL) | Permite custo zero e consumo mínimo de memória em pilotos locais, viabilizando transição transparente para PostgreSQL em clusters de produção | Forçar container PostgreSQL obrigatório para cada cliente localmente | 🟢 |
| D-03 | Geração de `SECRET_KEY` criptográfica única de 64 caracteres hexadecimais por tenant no provisionamento | Assegura que um token JWT emitido pela Instituição A seja criptograficamente rejeitado pela Instituição B | Compartilhar a mesma chave de assinatura de tokens entre todas as instituições | 🟢 |
| D-04 | Roteamento duplo: portas locais diretas para dev/testes e proxy reverso para subdomínios em produção | Oferece agilidade máxima no desenvolvimento e validação rápida sem necessidade de alterar arquivos de hosts locais, mantendo padrão corporativo em nuvem | Exigir obrigatoriamente DNS com subdomínios até para testes locais | 🟢 |
| D-05 | Scripts de provisionamento e backup disponíveis tanto em Bash (Linux/macOS) quanto em PowerShell (Windows) | Garante paridade multiplataforma de desenvolvimento e operação para toda a equipe | Fornecer scripts apenas para uma plataforma de terminal | 🟢 |

## 4. Premissas

Nenhuma premissa adotada a partir de dúvidas abertas. Todos os requisitos e diretrizes arquiteturais foram esclarecidos e confirmados na sessão de `/reversa-clarify`.

## 5. Delta arquitetural

| Componente | Arquivo de origem no legado | Tipo de mudança | Resumo |
|------------|------------------------------|-----------------|--------|
| `web-app-api` | `_reversa_sdd/architecture.md#web-app-api` | componente-alterado | Atualização da inicialização do banco (`src/database.py`) e rotas (`src/api/routes.py`) para consumir `DATABASE_URL`, `SECRET_KEY` e adicionar rota `GET /api/v1/health`. |
| `infra-docker` | n/a | componente-novo | Adição de `Dockerfile`, `docker-compose.yml`, `docker-compose.institution.yml` e `.env.example`. |
| `scripts-provisionamento` | n/a | componente-novo | Adição de `scripts/deploy-institution.sh`, `scripts/deploy-institution.ps1`, `scripts/backup-institutions.sh` e `scripts/backup-institutions.ps1`. |
| `reverse-proxy` | n/a | componente-novo | Template de roteamento com Nginx em `nginx/nginx.conf`. |
| `tests-isolation` | n/a | componente-novo | Criação de `tests/test_multi_tenant_isolation.py` cobrindo segregação de dados e tokens. |

## 6. Delta no modelo de dados

- Resumo das mudanças: O modelo de dados relacional interno das tabelas (`Coordination`, `Room`, `Teacher`, `Class`, `Restriction`, `AllocationTask`, `User`) permanece exatamente o mesmo. A mudança de dados reside no desacoplamento físico: cada tenant possui seu próprio arquivo `.db` (ou schema/banco PostgreSQL) armazenado em `./data/{TENANT_NAME}/classsync.db`.
- Detalhe completo em: `_reversa_forward/021-gestao-privativa-instituicoes/data-delta.md`

## 7. Delta de contratos externos

| Contrato | Tipo | Arquivo de detalhe |
|----------|------|--------------------|
| `multi-tenant-api` | HTTP (REST) | `_reversa_forward/021-gestao-privativa-instituicoes/interfaces/multi-tenant-api.md` |

## 8. Plano de migração

1. Criar a pasta raiz de dados persistentes `./data/` no projeto (com `.gitignore` adequado para não versionar bancos SQLite de clientes).
2. Manter a base legado existente intacta para execução direta via terminal local (`src/main.py`).
3. Ao subir uma instituição piloto (ex.: `faculdade_alfa`), o script de provisionamento gera o diretório `./data/faculdade_alfa/` e inicializa as tabelas automaticamente na primeira subida.
4. Para migrar dados existentes para um tenant específico, basta copiar o arquivo `classsync.db` legado para a pasta `./data/{TENANT_NAME}/classsync.db`.

## 9. Riscos e mitigações

| Risco | Impacto | Probabilidade | Mitigação |
|-------|---------|---------------|-----------|
| Conflito de portas HTTP entre instâncias | Médio | Baixa | O script de provisionamento valida se a porta solicitada está livre no host antes de inicializar o container. |
| Acúmulo de dados não compactados no host | Médio | Baixa | O script de backup gera arquivos compactados `.tar.gz` organizados por data e descarta arquivos temporários. |
| Injeção de variáveis de ambiente incompletas | Alto | Baixa | O script de provisionamento gera o arquivo `.env` a partir do template validado `.env.example` preenchendo todos os parâmetros obrigatórios. |
| Falha de conexão caso usuário informe `DATABASE_URL` inválida | Médio | Média | Fallback seguro e mensagem de erro clara no log do container durante a inicialização em `src/database.py`. |

## 10. Critério de pronto

- [ ] Todas as ações do `actions.md` marcadas `[X]`
- [ ] `Dockerfile` e `docker-compose.yml` criados e testados
- [ ] Scripts de provisionamento e backup (Bash e PowerShell) implementados e funcionais
- [ ] Configuração de proxy reverso Nginx documentada e validada
- [ ] Suíte de testes `test_multi_tenant_isolation.py` com 100% de aprovação
- [ ] `onboarding.md` testado por simulação de subida de 2 instâncias em paralelo

## 11. Histórico de alterações

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-09-07 | Versão inicial do plano gerada por `/reversa-plan` | reversa |
