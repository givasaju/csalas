# Addendum: Gestão e Controle Privativo de Informações entre Instituições (Deploy Isolado Multi-Tenant)

> Identificador: `021-gestao-privativa-instituicoes`
> Data: `2026-09-07`
> Cenário: Legado (`_reversa_sdd/architecture.md` e `domain.md`)

## Vigência

Vigente desde 2026-09-07.

## Resumo da entrega

Implementação da arquitetura de isolamento físico e controle privativo de informações entre múltiplas instituições clientes na plataforma ClassSync AI através do modelo de instâncias dedicadas (Single-Tenant por container/ambiente com banco e volumes desacoplados). A entrega contemplou a parametrização dinâmica de banco via `DATABASE_URL` em `src/database.py`, suporte dinâmico a `SECRET_KEY` em `src/api/auth.py` para isolamento criptográfico de tokens JWT, endpoint de diagnóstico e identificação de tenant `GET /api/v1/health`, template `Dockerfile` multi-stage, `docker-compose.yml`, `.env.example`, scripts automatizados de provisionamento em Bash e PowerShell (`scripts/deploy-institution.sh` e `.ps1`), configuração corporativa de Proxy Reverso Nginx (`nginx/nginx.conf`), scripts centralizados de backup de volumes (`scripts/backup-institutions.sh` e `.ps1`) e a suíte de testes automatizados `tests/test_multi_tenant_isolation.py` com 100% de aprovação (70/70 testes passando com zero regressões no legado).
Total de ações executadas: 11 de 11 (100% concluído).

## Impacto por artefato da extração

| Artefato | Seção | Tipo de impacto | Delta |
|----------|-------|-----------------|-------|
| `_reversa_sdd/architecture.md` | `#database` | `regra-alterada` | Conexão de banco aceita `DATABASE_URL` dinâmica do ambiente (SQLite local montado ou PostgreSQL) com criação automática de diretórios e fallback seguro. |
| `_reversa_sdd/architecture.md` | `#jwt-auth-service` | `regra-alterada` | `SECRET_KEY` obtida dinamicamente do ambiente, garantindo que tokens emitidos por um tenant sejam sumariamente rejeitados por outro. |
| `_reversa_sdd/architecture.md` | `#web-app-api` | `contrato-novo` | Endpoint `GET /api/v1/health` e rota `/health` retornando conectividade do banco, status da API e o slug do tenant ativo. |
| `_reversa_sdd/architecture.md` | `#infra-container` | `componente-novo` | Containerização multi-stage (`Dockerfile`), orquestração Compose (`docker-compose.yml`) e template de ambiente (`.env.example`). |
| `_reversa_sdd/architecture.md` | `#infra-automation` | `componente-novo` | Scripts multiplataforma de provisionamento de novas instituições piloto e backups centralizados em `scripts/`. |
| `_reversa_sdd/architecture.md` | `#infra-network` | `componente-novo` | Template Nginx de Proxy Reverso corporativo mapeando subdomínios institucionais com headers de segurança. |
| `_reversa_sdd/domain.md` | `#governanca-e-privacidade` | `regra-nova` | Princípio de segregação física e inviolabilidade de dados entre organizações clientes para atendimento integral à LGPD. |

## Regras sob vigilância

- `W001`: Conexão em `src/database.py` respeitando `DATABASE_URL` com fallback seguro em `_reversa_forward/021-gestao-privativa-instituicoes/regression-watch.md`
- `W002`: Obtenção dinâmica da `SECRET_KEY` em `src/api/auth.py` para isolamento criptográfico em `_reversa_forward/021-gestao-privativa-instituicoes/regression-watch.md`
- `W003`: Endpoint `GET /api/v1/health` respondendo 200 OK com metadados de tenant em `_reversa_forward/021-gestao-privativa-instituicoes/regression-watch.md`
- `W004`: Suíte de testes `test_multi_tenant_isolation.py` com segregação de banco e tokens em `_reversa_forward/021-gestao-privativa-instituicoes/regression-watch.md`

## Fontes

- `_reversa_forward/021-gestao-privativa-instituicoes/requirements.md`
- `_reversa_forward/021-gestao-privativa-instituicoes/roadmap.md`
- `_reversa_forward/021-gestao-privativa-instituicoes/actions.md`
- `_reversa_forward/021-gestao-privativa-instituicoes/legacy-impact.md`
- `_reversa_forward/021-gestao-privativa-instituicoes/regression-watch.md`
