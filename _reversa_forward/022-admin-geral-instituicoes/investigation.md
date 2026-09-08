# Investigation: Interface do Administrador Geral para Gestão e Delegação de Instituições

> Identificador: `022-admin-geral-instituicoes`
> Data: `2026-09-07`

## 1. Contexto e Pesquisa de Fundo

A evolução da arquitetura do ClassSync AI a partir da entrega `021-gestao-privativa-instituicoes` consolidou o isolamento físico multi-tenant por meio de containers dedicados e volumes desacoplados (`./data/{tenant}`). No entanto, a criação de novas instituições permaneceu dependente da execução manual de scripts no host (`scripts/deploy-institution.ps1` e `.sh`), exigindo que o operador da plataforma tivesse acesso direto ao terminal do servidor.
A necessidade atual é elevar esse processo para o nível da aplicação web, provendo uma interface amigável para o superadministrador (`doctor-chef`) sem comprometer a segurança da infraestrutura.

## 2. Padrões Arquiteturais Avaliados

### 2.1. Acesso Direto ao Docker Socket (`/var/run/docker.sock`) vs. Executor Desacoplado
- **Cenário A (Socket Docker no Web Backend):** Montar o socket do Docker dentro do container web principal para permitir que a API dispare `docker run` ou `docker compose` diretamente via SDK do Docker.
  - *Problema:* É uma falha crítica de segurança (CVEs clássicas de Container Breakout). Se a aplicação web sofrer uma vulnerabilidade de Remote Code Execution (RCE) ou injeção, o invasor ganha controle total do host como root.
- **Cenário B (FastAPI `BackgroundTasks` com Wrapper Seguro):** O backend recebe a requisição autenticada com role `doctor-chef`, valida os parâmetros em esquema Pydantic restrito (sem caracteres de escape de shell) e aciona um worker assíncrono interno via `BackgroundTasks` que orquestra a criação de arquivos de ambiente e invoca o CLI do Docker sob controle de concorrência.
  - *Vantagem:* Rápido, assíncrono (não bloqueia a resposta HTTP que retorna `202 Accepted`) e mantém a execução protegida.

## 3. Alocação Automática de Portas TCP e Prevenção de Colisão

Para garantir que novas instituições não colidam em portas já alocadas:
1. O sistema faz a varredura dos arquivos `.env.*` e das pastas ativas em `./data/` para identificar todas as portas já atribuídas.
2. Realiza um teste de bind em socket local (`socket.socket(socket.AF_INET, socket.SOCK_STREAM)`) para confirmar se a porta candidata está fisicamente desocupada no sistema operacional.
3. Sugere a próxima porta sequencial livre a partir de 8001 (ex.: 8001, 8002, 8003...).
4. O `doctor-chef` pode visualizar e, se necessário, customizar a porta antes de submeter o formulário.

## 4. Conformidade com a LGPD e Governança de Senhas

Ao provisionar o `master-chef`, o `doctor-chef` define um e-mail corporativo e uma senha provisória inicial.
Para assegurar que o operador do SaaS não retenha acesso aos dados acadêmicos privativos da instituição cliente:
- O usuário é inserido com o atributo `must_change_password=True`.
- No primeiro login do `master-chef` na URL dedicada, o token JWT gerado contém a claim `{"must_change_password": true}`.
- O frontend e a API interceptam requisições e exigem que o usuário submeta uma nova senha via `POST /api/v1/auth/change-password` antes de liberar acesso aos módulos de salas, turmas e alocações.

## 5. Referências e Padrões
- OWASP Docker Top 10: *D01 - Secure Host Configuration & Avoiding Docker Socket Exposure*.
- LGPD (Lei Geral de Proteção de Dados - Lei nº 13.709/2018): Princípios de necessidade, segurança e segregação de acesso.
- FastAPI Documentation: *Background Tasks and Asynchronous Workers*.

