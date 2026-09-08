# Roadmap: Interface do Administrador Geral para Gestão e Delegação de Instituições

> Identificador: `022-admin-geral-instituicoes`
> Data: `2026-09-07`
> Requirements: `_reversa_forward/022-admin-geral-instituicoes/requirements.md`
> Confidência: 🟢 CONFIRMADO, 🟡 INFERIDO

## 1. Resumo da abordagem

Implementação da camada administrativa de alto nível (SuperAdmin) para a plataforma ClassSync AI, viabilizando que o operador global ('doctor-chef') provisione de forma visual, amigável e segura novas instituições clientes com seus respectivos gestores gerais ('master-chef').
A abordagem preserva o isolamento físico multi-tenant (Single-Tenant por container/ambiente), estendendo o modelo de permissões RBAC com a role `doctor-chef`, expondo endpoints REST protegidos `/api/v1/platform/tenants`, acionando a orquestração assíncrona de deploy via `BackgroundTasks` da FastAPI (sem expor o socket Docker diretamente ao processo web), alocando portas TCP automaticamente a partir de 8001 e criando o 'master-chef' na base do novo tenant com obrigatoriedade de redefinição de senha no primeiro login para cumprimento da LGPD. Na interface SPA existente (`src/api/static/`), adiciona-se a visão dedicada de 'Administração Geral'.

## 2. Princípios aplicados

| Princípio | Como a feature se relaciona | Status |
|-----------|------------------------------|--------|
| Segregação Física e Inviolabilidade de Dados | Mantém cada instituição em volume e banco próprios em `./data/{tenant}` e chave JWT exclusiva, impedindo qualquer vazamento cruzado. | respeita |
| Não-bloqueio de Event Loop | Utiliza `BackgroundTasks` assíncrono para operações pesadas de deploy no host, mantendo tempo de resposta da API abaixo de 300ms. | respeita |
| Princípio do Menor Privilégio (PoLP) | O 'doctor-chef' apenas provisiona e delega o 'master-chef', sem acesso visual aos dados pedagógicos internos da instituição após o handover. | respeita |

## 3. Decisões técnicas

| ID | Decisão | Justificativa | Alternativas descartadas | Confidência |
|----|---------|----------------|--------------------------|-------------|
| D-01 | Adição da role global `doctor-chef` em `src/api/auth.py` | Permite controle de acesso estrito (RBAC) aos endpoints de criação de instituições sem alterar as roles locais dos tenants (`gestor`, `coordenador`, `docente`). | Criar app de login totalmente separada para o SuperAdmin (alto custo desnecessário para o MVP). | 🟢 |
| D-02 | Orquestração assíncrona de deploy via FastAPI `BackgroundTasks` | Responde imediatamente com HTTP 202 Accepted para a UI, executando a criação de arquivos `.env`, diretório `./data/{tenant}` e subida de container sem travar o worker web. | Webhook runner externo dedicado ou container daemon (maior complexidade operacional); execução síncrona (travaria a requisição por dezenas de segundos). | 🟢 |
| D-03 | Alocação incremental de portas TCP iniciando em 8001 com override manual | Garante previsibilidade e automação, evitando colisões de portas locais através de checagem em tempo de execução, mantendo flexibilidade para o 'doctor-chef'. | Alocação manual obrigatória (atrito operacional); alocação aleatória (dificuldade de mapeamento de proxy). | 🟢 |
| D-04 | Obrigação de troca de senha no primeiro acesso do 'master-chef' (`must_change_password=True`) | Conformidade integral com a LGPD e privacidade contratual, garantindo que o operador da plataforma não conheça a senha em uso da instituição. | Permitir senha definitiva cadastrada pelo 'doctor-chef' (risco de privacidade); envio obrigatório de link SMTP externo (dependência de gateway de e-mail). | 🟢 |
| D-05 | Interface nativa SPA em Vanilla JS e CSS em `src/api/static/` | Preserva a simplicidade arquitetural do frontend existente sem adicionar bundlers ou frameworks pesados (React/Vue). | Desenvolver frontend em React/Next.js (incompatível com a restrição de manter o bundle leve e homogêneo). | 🟢 |

## 4. Premissas

Nenhuma premissa sob dúvida não resolvida. Todas as 3 dúvidas originais foram esclarecidas e incorporadas no `requirements.md` via `/reversa-clarify`.

## 5. Delta arquitetural

| Componente | Arquivo de origem no legado | Tipo de mudança | Resumo |
|------------|------------------------------|-----------------|--------|
| `jwt-auth-service` | `_reversa_sdd/architecture.md#jwt-auth-service` | regra-alterada | Reconhecimento da role `doctor-chef`, verificação da claim `must_change_password` e rota de troca de senha. |
| `platform-tenant-api` | `_reversa_sdd/architecture.md#web-app-api` | contrato-novo | Endpoints `GET` e `POST /api/v1/platform/tenants` para governança global de instâncias. |
| `infra-automation` | `_reversa_sdd/architecture.md#infra-automation` | regra-alterada | Helper Python de orquestração interna disparando rotinas de provisionamento com injeção do 'master-chef'. |
| `frontend-spa` | `_reversa_sdd/architecture.md#web-app-api` | componente-novo | Seção 'Administração Geral' na SPA com tabela de instituições, modal de criação e feedback de deploy. |

## 6. Delta no modelo de dados

- Resumo das mudanças: Adição do campo booleano `must_change_password` (default=False) na tabela `User` em `src/models.py`, com sanitização automática de esquema SQLite em `src/database.py`. No nível de plataforma, os metadados dos tenants são geridos a partir dos volumes e arquivos `.env.*` em disco, sem acoplar bancos entre instâncias.
- Detalhe completo em: `_reversa_forward/022-admin-geral-instituicoes/data-delta.md`

## 7. Delta de contratos externos

| Contrato | Tipo | Arquivo de detalhe |
|----------|------|--------------------|
| `platform-tenants-api` | HTTP (REST) | `_reversa_forward/022-admin-geral-instituicoes/interfaces/platform-tenants-api.md` |

## 8. Plano de migração

1. **Passo 1 (Esquema de Dados):** Atualizar `src/models.py` e `src/database.py` para injetar a coluna `must_change_password` em tabelas `User` existentes sem perda de dados (`ALTER TABLE User ADD COLUMN must_change_password BOOLEAN DEFAULT 0`).
2. **Passo 2 (Seed do SuperAdmin):** Inicializar conta padrão do 'doctor-chef' (`doctor@classsync.ai`) em ambiente principal caso não exista.
3. **Passo 3 (Compatibilidade com Tenants Legados):** Instâncias já ativas (como `faculdade_beta`) continuam operando normalmente sem impacto.

## 9. Riscos e mitigações

| Risco | Impacto | Probabilidade | Mitigação |
|-------|---------|---------------|-----------|
| Concorrência no provisionamento simultâneo de instâncias | Médio | Baixo | `BackgroundTasks` sequencial com trava de escrita baseada em arquivo de lock temporário. |
| Porta TCP em conflito com serviço externo do host | Alto | Baixo | Função utilitária de socket check antes da alocação que valida se a porta está realmente livre no SO. |
| 'Master-chef' tentar contornar a troca de senha inicial | Médio | Baixo | Middleware de autenticação JWT intercepta requisições de usuários com `must_change_password=True` e bloqueia endpoints acadêmicos até a redefinição. |

## 10. Critério de pronto

- [x] Todas as ações do `actions.md` marcadas `[X]`
- [x] Endpoint `GET /api/v1/platform/tenants` respondendo listagem de instâncias para `doctor-chef`
- [x] Endpoint `POST /api/v1/platform/tenants` provisionando nova instituição com sucesso em `BackgroundTasks`
- [x] Nova instituição acessível com login do 'master-chef' e tela forçada de troca de senha
- [x] Suíte de testes automatizados (`pytest`) cobrindo controle de acesso, criação assíncrona e troca de senha com 100% de aprovação


## 11. Histórico de alterações

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-09-07 | Versão inicial gerada por `/reversa-plan` a partir do requirements 022 | reversa |

