# Contrato de Interface: API e Configuração Multi-Tenant Isolada

> Identificador: `021-gestao-privativa-instituicoes`
> Protocolo: HTTP / REST (FastAPI) & Docker / Environment
> Formato: JSON / Env Var

---

## 1. Endpoints de Diagnóstico e Tenant

### 1.1 `GET /api/v1/health`
Retorna o status de saúde da instância, confirmação de conectividade com o banco de dados e metadados da instituição ativa.

- **Autenticação:** Pública (não requer token JWT)
- **Headers:** `Accept: application/json`
- **Response `200 OK`:**
```json
{
  "status": "healthy",
  "tenant": "faculdade_alpha",
  "version": "1.0.0",
  "database": "connected",
  "timestamp": "2026-09-07T13:25:00Z"
}
```
- **Response `503 Service Unavailable`:**
```json
{
  "status": "unhealthy",
  "tenant": "faculdade_alpha",
  "database": "disconnected",
  "error": "Could not connect to database"
}
```

---

## 2. Contrato de Variáveis de Ambiente da Instância (`.env`)

Cada container dedicado recebe as seguintes variáveis de ambiente injetadas no momento da inicialização:

| Variável | Tipo | Obrigatório? | Exemplo / Padrão | Descrição |
|----------|------|--------------|-------------------|-----------|
| `TENANT_NAME` | String | Sim | `faculdade_alpha` | Identificador slug da instituição cliente (usado em logs e health check) |
| `PORT` | Inteiro | Sim | `8001` | Porta TCP do host exposta para o container |
| `DATABASE_URL` | String | Sim | `sqlite:////app/data/classsync.db` | String de conexão SQLAlchemy (SQLite em volume `/app/data` ou PostgreSQL) |
| `SECRET_KEY` | String | Sim | *(64 hex chars)* | Chave criptográfica secreta exclusiva usada para assinar e validar tokens JWT da instituição |
| `APP_ENV` | String | Não | `production` | Ambiente de execução (`development`, `staging`, `production`) |
| `CORS_ORIGINS` | String | Não | `*` | Origens autorizadas para requisições cross-origin |

---

## 3. Contrato de Invocação dos Scripts de Automação

### 3.1 Script de Provisionamento (`deploy-institution.sh` / `.ps1`)

- **Assinatura Bash:**
  ```bash
  ./scripts/deploy-institution.sh <TENANT_NAME> <PORT> [DATABASE_URL]
  ```
- **Assinatura PowerShell:**
  ```powershell
  .\scripts\deploy-institution.ps1 -Tenant <TENANT_NAME> -Port <PORT> [-DatabaseUrl <DATABASE_URL>]
  ```
- **Comportamento:**
  1. Cria o diretório de dados persistentes `./data/<TENANT_NAME>/` se não existir.
  2. Gera arquivo `.env.<TENANT_NAME>` preenchendo chave segura `SECRET_KEY` aleatória.
  3. Executa `docker compose` subindo o container `classsync-<TENANT_NAME>`.
  4. Valida se o endpoint `GET /api/v1/health` respondeu `200 OK`.

### 3.2 Script de Backup Consolidado (`backup-institutions.sh` / `.ps1`)

- **Assinatura Bash:**
  ```bash
  ./scripts/backup-institutions.sh [DEST_DIR]
  ```
- **Assinatura PowerShell:**
  ```powershell
  .\scripts\backup-institutions.ps1 [-DestDir <DEST_DIR>]
  ```
- **Comportamento:**
  1. Localiza todos os diretórios dentro de `./data/`.
  2. Para cada tenant, gera um arquivo `./backups/backup-<TENANT_NAME>-YYYYMMDD-HHMMSS.tar.gz`.
  3. Registra log de saída com o hash e tamanho de cada arquivo de backup gerado.
