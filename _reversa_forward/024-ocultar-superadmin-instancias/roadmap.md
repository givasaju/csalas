# Roadmap: Ocultação do Super Administrador Geral na Gestão de Usuários das Instâncias

> Identificador: `024-ocultar-superadmin-instancias`
> Data: `2026-09-08`
> Requirements: `_reversa_forward/024-ocultar-superadmin-instancias/requirements.md`
> Confidência: 🟢 CONFIRMADO, 🟡 INFERIDO, 🔴 LACUNA

## 1. Resumo da abordagem

A solução implementa o isolamento visual e de dados entre a governança global da plataforma e as instâncias dedicadas de clientes por meio do princípio de defesa em profundidade. No backend (`src/api/routes.py`), a consulta `GET /api/v1/users` passa a aplicar filtro explícito excluindo usuários com a role `doctor-chef` (`models.User.role != "doctor-chef"`), e o endpoint de mutação de status (`PATCH /api/v1/users/{user_id}/status`) introduz validação de segurança que bloqueia com `HTTP 403 Forbidden` qualquer tentativa de desativação ou alteração de papel da conta de superadministrador. No frontend SPA (`src/api/static/index.html`), o método `loadUsersList()` adiciona filtro reativo defensivo pré-renderização para assegurar integridade visual caso um payload anômalo seja retornado. O comportamento é coberto por testes automatizados em `tests/`.

## 2. Princípios aplicados

| Princípio | Como a feature se relaciona | Status |
|-----------|------------------------------|--------|
| I. Segregação e Isolamento Multi-Tenant | Respeita a separação estrita de privilégios entre operadores da plataforma SaaS e gestores acadêmicos locais. | respeita |
| II. Defesa em Profundidade | Aplica filtragem tanto na camada de consulta da API quanto na camada de renderização do cliente. | respeita |
| III. Preservação do Bundle Nativo | Mantém todas as alterações em Vanilla JS e CSS puro, sem introduzir bibliotecas externas. | respeita |

## 3. Decisões técnicas

| ID | Decisão | Justificativa | Alternativas descartadas | Confidência |
|----|---------|----------------|--------------------------|-------------|
| D-01 | Filtrar contas `doctor-chef` na consulta ORM do endpoint `GET /api/v1/users` | Impede que dados da conta central trafeguem na rede ou sejam inspecionados no DevTools do navegador. | Filtrar exclusivamente no JavaScript da SPA (vulnerável a inspeção de rede). | 🟢 |
| D-02 | Responder `HTTP 403 Forbidden` com detalhe explicativo ao tentar alterar o status da conta `doctor-chef` | Sinaliza categoricamente a violação de privilégio e preserva a imutabilidade da credencial global. | Responder `HTTP 404` (gera ambiguidade técnica) ou falhar silenciosamente. | 🟢 |
| D-03 | Aplicar filtro redundante no JavaScript (`loadUsersList`) em `index.html` | Garante tolerância a falhas na interface do usuário contra respostas de cache ou versões anteriores. | Confiar apenas na filtragem do backend. | 🟢 |
| D-04 | Criar testes automatizados dedicados em `tests/test_auth_rbac.py` | Assegura que o filtro de isolamento e o bloqueio 403 permaneçam protegidos contra regressões. | Testar apenas manualmente na interface. | 🟢 |

## 4. Premissas

Nenhuma premissa pendente. Todas as dúvidas foram elucidadas na sessão de esclarecimentos do `/reversa-clarify`.

## 5. Delta arquitetural

| Componente | Arquivo de origem no legado | Tipo de mudança | Resumo |
|------------|------------------------------|-----------------|--------|
| `web-app-api` | `_reversa_sdd/architecture.md#web-app-api` | contrato-alterado | Endpoint `GET /api/v1/users` suprime `doctor-chef` e `PATCH /api/v1/users/{id}/status` bloqueia com HTTP 403. |
| `frontend-spa` | `_reversa_sdd/architecture.md#frontend-spa` | componente-alterado | Método `loadUsersList()` em `index.html` filtra registros `doctor-chef` antes de montar a tabela. |
| `test-suite` | `_reversa_sdd/inventory.md#3-pontos-de-entrada` | componente-novo | Testes automatizados para verificação do filtro de listagem e rejeição de alteração de privilégio. |

## 6. Delta no modelo de dados

- Resumo das mudanças: Nenhuma modificação no schema, colunas ou tabelas do banco de dados SQLite. As entidades `User` permanecem inalteradas.
- Detalhe completo em: `_reversa_forward/024-ocultar-superadmin-instancias/data-delta.md`

## 7. Delta de contratos externos

| Contrato | Tipo | Arquivo de detalhe |
|----------|------|--------------------|
| `users-management-api` | HTTP | `_reversa_forward/024-ocultar-superadmin-instancias/interfaces/users-management-api.md` |

## 8. Plano de migração

Não há migração de banco de dados ou conversão de arquivos necessária (`n/a`). As instâncias locais e a plataforma master aplicam a nova regra imediatamente no boot da aplicação.

## 9. Riscos e mitigações

| Risco | Impacto | Probabilidade | Mitigação |
|-------|---------|---------------|-----------|
| Ocultação acidental de gestores acadêmicos locais legítimos | alto | baixa | O filtro compara estritamente o papel `u.role.lower() == "doctor-chef"` e e-mail `doctor@classsync.ai`, preservando papéis `gestor`, `coordenador` e `docente`. |
| Bloqueio do superadministrador ao tentar gerenciar instituições | médio | baixa | O fluxo de governança de instituições ocorre na aba exclusiva de Administração Geral (`/platform/tenants/*`), que não depende de `/api/v1/users`. |

## 10. Critério de pronto

- [ ] Ação T001 implementada e aprovada em testes unitários/integrados
- [ ] Endpoint `GET /api/v1/users` nunca retorna contas `doctor-chef`
- [ ] Endpoint `PATCH /api/v1/users/{id}/status` retorna HTTP 403 Forbidden para alvos `doctor-chef`
- [ ] Modal `#usersModal` na interface gráfica exibe somente contas acadêmicas locais
- [ ] Suíte de testes automatizados com 100% de aprovação (zero regressões nas 83 aprovações existentes)

## 11. Histórico de alterações

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-09-08 | Versão inicial gerada por `/reversa-plan` | reversa |
