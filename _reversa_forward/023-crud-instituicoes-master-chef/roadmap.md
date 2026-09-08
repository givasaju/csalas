# Roadmap: CRUD de Gestão de Instituições e Master-Chef

> Identificador: `023-crud-instituicoes-master-chef`
> Data: `2026-09-07`
> Requirements: `_reversa_forward/023-crud-instituicoes-master-chef/requirements.md`
> Confidência: 🟢 CONFIRMADO, 🟡 INFERIDO

## 1. Resumo da abordagem

Expansão das capacidades da camada de governança da plataforma ClassSync AI (`022-admin-geral-instituicoes`), evoluindo a interface de Administração Geral e o backend REST para suportar o ciclo de vida completo (CRUD) de instituições clientes e de seus gestores gerais ('master-chef').
A solução estabelece a inspeção individualizada de instituições com extração segura de metadados cadastrais do tenant e do gestor, edição controlada com preservação da estabilidade de infraestrutura (slug e portas TCP fixos), desativação e exclusão assistida com salvaguarda de arquivamento (soft delete movendo `./data/{slug}/` para `./data/.archived/` e liberação imediata de porta TCP) mediante confirmação estrita de slug, além de fluxo de suporte para redefinição de credenciais do master-chef com injeção direta de senha provisória e ativação de `must_change_password=True`. No frontend SPA (`src/api/static/`), adicionam-se modais reativos em Vanilla JavaScript integrados à visualização existente.

## 2. Princípios aplicados

| Princípio | Como a feature se relaciona | Status |
|-----------|------------------------------|--------|
| Segregação Física e Inviolabilidade de Dados | O superadministrador gerencia credenciais de acesso mas não inspeciona nem altera dados acadêmicos ou pedagógicos da instituição. | respeita |
| Não-destruição Irreversível de Histórico | A exclusão de tenants adota soft delete com arquivamento de volume em `./data/.archived/`, garantindo auditabilidade e recuperação de dados. | respeita |
| Princípio do Menor Privilégio e RBAC Estrito | Todos os novos endpoints de leitura, edição, exclusão e reset de credenciais são protegidos exclusivamente pela role `doctor-chef`. | respeita |
| Segurança de Credenciais e LGPD | Toda senha redefinida pelo operador da plataforma nasce temporária e força substituição imediata pelo titular da conta no primeiro acesso. | respeita |

## 3. Decisões técnicas

| ID | Decisão | Justificativa | Alternativas descartadas | Confidência |
|----|---------|----------------|--------------------------|-------------|
| D-01 | Desativação com Soft Delete / Arquivamento (`./data/.archived/{slug}`) na exclusão de tenants | Protege contra deleção acidental de dados de clientes, mantém histórico para compliance LGPD e libera a porta TCP para reuso seguro. | Hard delete com `rm -rf` imediato (risco severo de perda irreversível de dados); manter pasta no diretório ativo com flag em JSON (poluição do diretório de produção). | 🟢 |
| D-02 | Imutabilidade de Porta TCP e Slug na edição de instituições em operação | Evita interrupções de serviço, reconstrução complexa de containers Docker em tempo de execução e risco de conflitos de roteamento. | Permitir alteração de porta com restart automático do container (alto risco de indisponibilidade e inconsistência de DNS/proxy). | 🟢 |
| D-03 | Acesso Cross-Tenant Seguro ao SQLite para Reset do Master-Chef | O backend acessa pontualmente o banco isolado `./data/{slug}/classsync.db` para atualizar o hash do gestor sem necessitar de API externa exposta na instância. | Expor endpoint HTTP de administração interna dentro de cada container (maior superfície de ataque e dependência de rede interna). | 🟢 |
| D-04 | Modal de Exclusão com Confirmação Mandatória por Digitação de Slug | Previne acidentes operacionais humanos causados por cliques incorretos em botões de ação destrutiva. | Caixa de diálogo de alerta padrão do navegador (`confirm()`) ou simples botão de clique único (insuficientes para operações destrutivas de produção). | 🟢 |
| D-05 | Geração de Senha Provisória com Opção de Override Manual | Proporciona conveniência e alta entropia por padrão, permitindo que o administrador defina uma credencial específica quando houver exigência operacional. | Apenas digitação manual (propensa a senhas fracas); apenas geração automática rígida (reduz flexibilidade do suporte). | 🟢 |

## 4. Premissas

Nenhuma premissa pendente sob dúvida não resolvida. Todas as três dúvidas identificadas no requirements foram esclarecidas na sessão de `/reversa-clarify` e integradas ao escopo.

## 5. Delta arquitetural

| Componente | Arquivo de origem no legado | Tipo de mudança | Resumo |
|------------|------------------------------|-----------------|--------|
| `web-app-api` | `_reversa_sdd/architecture.md#web-app-api` | contrato-alterado | Adição dos endpoints de detalhe, edição e exclusão de tenants (`/api/v1/platform/tenants/{slug}`) e rota de reset de credencial (`/master-chef/reset`). |
| `platform-tenant-service` | `_reversa_sdd/architecture.md#web-app-api` | regra-alterada | Implementação da lógica de arquivamento físico de volumes, leitura/escrita pontual em banco SQLite isolado do tenant e liberação de portas. |
| `frontend-spa` | `_reversa_sdd/architecture.md#web-app-api` | componente-novo | Modais de Edição de Instituição, Redefinição de Master-Chef e Exclusão Assistida integrados à tabela da aba 'Administração Geral'. |
| `jwt-auth-service` | `_reversa_sdd/architecture.md#jwt-auth-service` | regra-alterada | Validação estrita da role `doctor-chef` nas novas rotas de governança de ciclo de vida. |

## 6. Delta no modelo de dados

- Resumo das mudanças: Não há alteração estrutural no modelo relacional do banco principal. No nível de esquemas da API (`src/api/schemas.py`), são criados modelos Pydantic para detalhamento de tenant (`TenantDetailResponse`), atualização de dados cadastrais (`TenantUpdateRequest`), requisição/resposta de reset de credenciais (`MasterChefResetRequest`, `MasterChefResetResponse`) e deleção assistida (`TenantDeleteRequest`). No sistema de arquivos, introduz-se a pasta de arquivamento `./data/.archived/`.
- Detalhe completo em: `_reversa_forward/023-crud-instituicoes-master-chef/data-delta.md`

## 7. Delta de contratos externos

| Contrato | Tipo | Arquivo de detalhe |
|----------|------|--------------------|
| `platform-tenants-crud-api` | HTTP (REST) | `_reversa_forward/023-crud-instituicoes-master-chef/interfaces/platform-tenants-api.md` |

## 8. Plano de migração

1. **Passo 1 (Criação do Diretório de Arquivamento):** Garantir a existência do diretório `./data/.archived/` no host com as mesmas permissões de leitura/escrita do diretório `./data/`.
2. **Passo 2 (Compatibilidade Retroativa):** Todos os tenants provisionados anteriormente na feature 022 continuam plenamente legíveis e compatíveis com as novas rotas de consulta, edição, reset e exclusão.
3. **Passo 3 (Verificação de Integridade de Bancos SQLite):** O helper de reset de credenciais inspeciona a tabela `User` do tenant-alvo; se a coluna `must_change_password` não existir (em bases anteriores à migração 022), o sistema executa automaticamente a migração da coluna no tenant.

## 9. Riscos e mitigações

| Risco | Impacto | Probabilidade | Mitigação |
|-------|---------|---------------|-----------|
| Bloqueio de arquivo no SQLite do tenant durante o reset de senha com o container rodando | Médio | Baixo | Utilização de conexão SQLite com timeout apropriado e modo WAL (Write-Ahead Logging) compatível com acessos concorrentes rápidos. |
| Exclusão acidental de instituição com dados acadêmicos ativos | Alto | Baixo | Dupla camada de segurança: exigência de digitação do slug exato na interface e adoção de soft delete / arquivamento em `./data/.archived/`. |
| Conflito de estado ao excluir container que já esteja parado ou removido | Baixo | Médio | Tratamento resiliente no comando Docker com checagem prévia de existência e captura segura de exceções sem abortar o arquivamento. |

## 10. Critério de pronto

- [ ] Todas as ações do `actions.md` marcadas `[X]`
- [ ] Endpoint `GET /api/v1/platform/tenants/{slug}` retornando dados detalhados da instituição e do master-chef
- [ ] Endpoint `PUT /api/v1/platform/tenants/{slug}` atualizando nome e contato com persistência
- [ ] Endpoint `DELETE /api/v1/platform/tenants/{slug}` parando container, movendo pasta para `.archived` e liberando porta TCP
- [ ] Endpoint `POST /api/v1/platform/tenants/{slug}/master-chef/reset` redefinindo credencial com flag `must_change_password=True`
- [ ] Modais de Edição, Exclusão e Reset operando na interface da SPA com feedback em tempo real
- [ ] Suíte de testes automatizados com 100% de aprovação cobrindo todos os fluxos positivos, negativos e de segurança

## 11. Histórico de alterações

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-09-07 | Versão inicial gerada por `/reversa-plan` a partir do requirements 023 | reversa |
