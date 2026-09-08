# Actions: Gestão e Controle Privativo de Informações entre Instituições (Deploy Isolado Multi-Tenant)

> Identificador: `021-gestao-privativa-instituicoes`
> Data: `2026-09-07`
> Roadmap: `_reversa_forward/021-gestao-privativa-instituicoes/roadmap.md`

## Resumo

| Métrica | Valor |
|---------|-------|
| Total de ações | 11 |
| Paralelizáveis (`[//]`) | 4 |
| Maior cadeia de dependência | 6 |

## Fase 1, Preparação

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T001 | Atualizar `src/database.py` para suportar a variável de ambiente `DATABASE_URL` (com fallback seguro para SQLite) e configuração dinâmica de engine SQLAlchemy | - | - | `src/database.py` | 🟢 | `[X]` |
| T002 | Atualizar `src/api/auth.py` para carregar `SECRET_KEY` a partir de variável de ambiente com geração de fallback seguro para isolamento criptográfico de tokens | - | `[//]` | `src/api/auth.py` | 🟢 | `[X]` |
| T003 | Criar a pasta de dados persistentes `./data/` e configurar `data/.gitignore` para garantir o isolamento local dos bancos SQLite de clientes sem versionamento | - | `[//]` | `data/.gitignore` | 🟢 | `[X]` |

## Fase 2, Testes

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T004 | Criar a suíte de testes automatizados `tests/test_multi_tenant_isolation.py` cobrindo segregação de banco, ausência de vazamento de dados de salas/turmas e rejeição cruzada de JWTs | T001, T002 | - | `tests/test_multi_tenant_isolation.py` | 🟢 | `[X]` |

## Fase 3, Núcleo

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T005 | Implementar o endpoint `GET /api/v1/health` em `src/api/routes.py` retornando status de saúde, conectividade do banco e o metadado `tenant_name` da instituição | T001 | - | `src/api/routes.py` | 🟢 | `[X]` |
| T006 | Criar o `Dockerfile` otimizado multi-stage para empacotar a aplicação ClassSync AI (FastAPI, dependências e frontend estático) em imagem leve | T001, T005 | - | `Dockerfile` | 🟢 | `[X]` |
| T007 | Criar o manifesto `docker-compose.yml` e o template `.env.example` com parametrização completa de portas, volumes e credenciais para execução de instâncias dedicadas | T006 | - | `docker-compose.yml` | 🟢 | `[X]` |

## Fase 4, Integração

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T008 | Desenvolver os scripts de provisionamento automatizado de novas instituições `scripts/deploy-institution.sh` e `scripts/deploy-institution.ps1` com geração de `.env` e subida de container | T007 | - | `scripts/deploy-institution.ps1` | 🟢 | `[X]` |
| T009 | Criar a configuração modelo de Proxy Reverso Nginx em `nginx/nginx.conf` mapeando subdomínios institucionais para os containers dedicados com headers de segurança | T007 | `[//]` | `nginx/nginx.conf` | 🟢 | `[X]` |

## Fase 5, Polimento

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T010 | Desenvolver os scripts de backup consolidado `scripts/backup-institutions.sh` e `scripts/backup-institutions.ps1` para compactação e snapshots dos volumes das instituições ativas | T008 | - | `scripts/backup-institutions.ps1` | 🟢 | `[X]` |
| T011 | Executar a suíte de testes `test_multi_tenant_isolation.py` e a suíte completa de regressão do projeto (`pytest`) para validar 100% de integridade | T004, T005 | `[//]` | `tests/test_multi_tenant_isolation.py` | 🟢 | `[X]` |

## Notas de execução

Todas as 11 tarefas (T001 a T011) foram implementadas e homologadas com sucesso.
A suíte completa de testes automatizados com `pytest` obteve 100% de aprovação (70/70 testes aprovados, incluindo testes de segregação de banco, incompatibilidade de tokens e endpoint de saúde).

## Histórico de alterações

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-09-07 | Versão inicial gerada por `/reversa-to-do` | reversa |
