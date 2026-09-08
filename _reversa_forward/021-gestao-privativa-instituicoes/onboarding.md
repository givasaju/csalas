# Onboarding & Guia de Teste: Gestão Privativa e Deploy Isolado Multi-Tenant

> Identificador: `021-gestao-privativa-instituicoes`
> Data: `2026-09-07`

Este documento apresenta o passo a passo para testar e comprovar na prática o isolamento físico, a parametrização de containers e o sigilo de dados entre duas instituições clientes distintas.

---

## 1. Pré-Requisitos

- Docker e Docker Compose instalados no host (ou ambiente Python local para testar a suíte automatizada).
- Terminal PowerShell (Windows) ou Bash (Linux/macOS).

---

## 2. Passo a Passo de Teste e Validação

### Passo 1: Provisionar a Primeira Instituição ("Faculdade Alpha")
1. Execute o script de provisionamento indicando o nome e a porta desejada:
   ```bash
   # No Linux/macOS:
   ./scripts/deploy-institution.sh faculdade_alpha 8001
   
   # No Windows (PowerShell):
   .\scripts\deploy-institution.ps1 -Tenant "faculdade_alpha" -Port 8001
   ```
2. O script:
   - Cria o diretório de dados `./data/faculdade_alpha/`.
   - Gera um arquivo `.env.faculdade_alpha` com `SECRET_KEY` criptográfica única.
   - Sobe o container `classsync-faculdade_alpha` mapeado para a porta `8001`.

### Passo 2: Provisionar a Segunda Instituição ("Faculdade Beta")
1. Execute o script para a segunda instituição em porta separada:
   ```bash
   # No Linux/macOS:
   ./scripts/deploy-institution.sh faculdade_beta 8002
   
   # No Windows (PowerShell):
   .\scripts\deploy-institution.ps1 -Tenant "faculdade_beta" -Port 8002
   ```
2. Observe que ambas as instâncias passam a rodar simultaneamente de forma independente.

### Passo 3: Verificação de Health Check e Metadados
1. Abra no navegador ou terminal:
   - `curl http://localhost:8001/api/v1/health`
     - Resposta esperada: `{"status": "healthy", "tenant": "faculdade_alpha", "timestamp": "..."}`
   - `curl http://localhost:8002/api/v1/health`
     - Resposta esperada: `{"status": "healthy", "tenant": "faculdade_beta", "timestamp": "..."}`

### Passo 4: Cadastro e Validação da Barreira de Dados
1. Acesse a **Faculdade Alpha** em `http://localhost:8001/`.
   - Faça login com o administrador da Alpha (`admin@classsync.ai` / `admin123`).
   - Cadastre uma sala exclusiva: `Auditório Alpha Nobre (Capacidade: 200)`.
   - Cadastre um docente: `Dr. Roberto Silva (Departamento: Medicina)`.
2. Acesse a **Faculdade Beta** em `http://localhost:8002/`.
   - Faça login com o administrador da Beta (`admin@classsync.ai` / `admin123`).
   - Verifique o inventário de salas e docentes da Beta.
   - **Critério de Inviolabilidade:** O `Auditório Alpha Nobre` e o docente `Dr. Roberto Silva` **NÃO** existem e não aparecem em nenhuma lista, tela ou resposta da API da Faculdade Beta.

### Passo 5: Teste de Rejeição de Token JWT Cruzado
1. Obtenha o token de autenticação emitido pelo login da Faculdade Alpha (`http://localhost:8001/api/v1/auth/login`).
2. Tente usar esse mesmo token JWT no cabeçalho `Authorization: Bearer <TOKEN_ALPHA>` chamando a rota protegida da Faculdade Beta (`http://localhost:8002/api/v1/users`).
3. **Resultado esperado:** A Faculdade Beta rejeita a requisição imediatamente com código HTTP `401 Unauthorized` devido à chave secreta (`SECRET_KEY`) distinta.

### Passo 6: Execução do Script de Backup Centralizado
1. No host, execute o script consolidado de backup:
   ```bash
   # No Linux/macOS:
   ./scripts/backup-institutions.sh
   
   # No Windows (PowerShell):
   .\scripts\backup-institutions.ps1
   ```
2. Verifique que foi gerado na pasta `./backups/` um snapshot compactado `.tar.gz` para a `faculdade_alpha` e outro para a `faculdade_beta`, garantindo a integridade e independência das cópias de segurança.
