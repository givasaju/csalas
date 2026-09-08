# Actions: CRUD de Gestão de Instituições e Master-Chef

> Identificador: `023-crud-instituicoes-master-chef`
> Data: `2026-09-07`
> Roadmap: `_reversa_forward/023-crud-instituicoes-master-chef/roadmap.md`

## Resumo

| Métrica | Valor |
|---------|-------|
| Total de ações | 10 |
| Paralelizáveis (`[//]`) | 3 |
| Maior cadeia de dependência | 7 |

## Fase 1, Preparação

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T001 | Criar os esquemas Pydantic em `src/api/schemas.py` para consulta detalhada, atualização cadastral, reset de master-chef e exclusão assistida (`MasterChefInfo`, `TenantDetailResponse`, `TenantUpdateRequest`, `MasterChefResetRequest`, `MasterChefResetResponse`, `TenantDeleteRequest`, `TenantDeleteResponse`) | - | `[//]` | `src/api/schemas.py` | 🟢 | `[X]` |
| T002 | Implementar em `src/api/routes.py` funções utilitárias internas para inspeção de banco SQLite do tenant (`_get_tenant_master_chef_info`), sincronização cadastral (`_update_tenant_metadata`) e rotação de credenciais com `must_change_password=True` (`_reset_tenant_master_chef`) | T001 | - | `src/api/routes.py` | 🟢 | `[X]` |

## Fase 2, Testes

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T003 | Expandir a suíte `tests/test_platform_tenants_api.py` com cenários de teste cobrindo detalhe de tenant, atualização de dados cadastrais, geração de senha provisória de master-chef, soft delete com arquivamento e bloqueio 403 para usuários comuns | T001, T002 | `[//]` | `tests/test_platform_tenants_api.py` | 🟢 | `[X]` |

## Fase 3, Núcleo

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T004 | Implementar o endpoint `GET /api/v1/platform/tenants/{slug}` restrito a `doctor-chef`, retornando os metadados cadastrais, porta TCP, status do container e dados de identificação do master-chef | T002 | - | `src/api/routes.py` | 🟢 | `[X]` |
| T005 | Implementar o endpoint `PUT /api/v1/platform/tenants/{slug}` restrito a `doctor-chef`, atualizando nome de exibição e e-mail de contato do master-chef com imutabilidade estrita de porta e slug | T004 | - | `src/api/routes.py` | 🟢 | `[X]` |
| T006 | Implementar o endpoint `POST /api/v1/platform/tenants/{slug}/master-chef/reset` para redefinição de senha do master-chef com suporte a senha manual ou aleatória e ativação obrigatória de `must_change_password=True` | T004 | - | `src/api/routes.py` | 🟢 | `[X]` |
| T007 | Implementar o endpoint `DELETE /api/v1/platform/tenants/{slug}` com validação mandatória de confirmação de slug, finalização de container Docker, liberação de porta TCP e arquivamento em `./data/.archived/` | T004 | - | `src/api/routes.py` | 🟢 | `[X]` |

## Fase 4, Integração

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T008 | Integrar a interface gráfica na SPA (`src/api/static/index.html` e `index.css`) com botões de ação na tabela de instituições e modais de Edição Cadastral, Redefinição de Master-Chef e Exclusão Assistida com confirmação de slug | T005, T006, T007 | - | `src/api/static/index.html` | 🟢 | `[X]` |
| T009 | Implementar no frontend JavaScript os handlers de submissão assíncrona para os endpoints de CRUD, cópia segura de credenciais para clipboard e re-renderização imediata de tabela e KPIs sem recarregar a página | T008 | - | `src/api/static/index.html` | 🟢 | `[X]` |

## Fase 5, Polimento

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T010 | Executar a suíte de testes com `pytest` (garantindo 100% de aprovação e zero regressão no sistema legado) e validar a conformidade de ponta a ponta dos novos fluxos de governança | T003, T007, T009 | `[//]` | `tests/` | 🟢 | `[X]` |

## Notas de execução

Nenhuma observação no momento da criação do plano.

## Histórico de alterações

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-09-07 | Versão inicial gerada por `/reversa-to-do` a partir do roadmap 023 | reversa |
