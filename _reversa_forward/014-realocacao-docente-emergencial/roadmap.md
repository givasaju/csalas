# Roadmap: Realocação Docente Emergencial

> Identificador: `014-realocacao-docente-emergencial`
> Data: `2026-08-13`
> Requirements: `_reversa_forward/014-realocacao-docente-emergencial/requirements.md`
> Confidência: 🟢 CONFIRMADO, 🟡 INFERIDO, 🔴 LACUNA

## 1. Resumo da abordagem

A feature introduz a funcionalidade de realocação docente emergencial no ClassSync AI para mitigar o impacto de ausências não planejadas de professores (licenças de saúde, cursos, aposentadorias). A solução estende o motor de IA em `src/engine/core.py` para calcular opções de substituição em segundos, ranqueadas por menor impacto no corpo docente e sem conflitos de `Restriction`. A API em `src/api/routes.py` passa a expor rotas para cálculo e efetivação da realocação, enquanto a interface SPA em `src/api/static/index.html` ganha suporte à escolha dinâmica do coordenador entre o Modo Assistido (seleção manual entre opções) e o Modo Delegado (aprovação/efetivação imediata via IA).

## 2. Princípios aplicados

| Princípio | Como a feature se relaciona | Status |
|-----------|------------------------------|--------|
| n/a | Nenhum princípio em `.reversa/principles.md` cadastrado | n/a |

## 3. Decisões técnicas

| ID | Decisão | Justificativa | Alternativas descartadas | Confidência |
|----|---------|----------------|--------------------------|-------------|
| D-01 | Recálculo emergencial isolado no `CoreAllocationEngine` | Evitar resetar a grade inteira do semestre; foca apenas nas turmas afetadas pelo docente ausente | Recalcular a alocação completa de todo o campus | 🟢 |
| D-02 | Ranqueamento de opções por índice de impacto | Garantir que a IA priorize opções que afetem o menor número possível de turmas terceiras | Seleção aleatória de professores livres | 🟢 |
| D-03 | Expansão de busca para coordenações correlatas quando necessário | Evitar deixar turmas desassistidas quando a coordenação titular não tiver docentes livres | Marcar a turma como pendente sem tentar coordenações vizinhas | 🟢 |
| D-04 | Homologação e Efetivação Imediata no Modo Delegado | Atender à especificação de resposta rápida e automatizada, gerando log de auditoria e notificando substitutos | Bloquear no Modo Delegado exigindo aceite por formulário do substituto | 🟢 |

## 4. Premissas

| Premissa | Origem (`requirements.md` seção) | Risco se errada |
|----------|----------------------------------|-----------------|
| Nenhuma premissa não resolvida | Todas as dúvidas foram esclarecidas no `/reversa-clarify` | Baixo |

## 5. Delta arquitetural

| Componente | Arquivo de origem no legado | Tipo de mudança | Resumo |
|------------|------------------------------|-----------------|--------|
| `core-allocation-engine` | `_reversa_sdd/architecture.md#1.1-módulos-principais` | regra-alterada | Adiciona o método `calculate_emergency_reallocation` em `src/engine/core.py` |
| `academic-space-manager` | `_reversa_sdd/architecture.md#1.1-módulos-principais` | contrato-novo | Adiciona endpoints `POST /api/v1/emergency-reallocations/calculate` e `commit` em `src/api/routes.py` |
| `occupancy-dashboard` | `_reversa_sdd/architecture.md#1.1-módulos-principais` | componente-novo | Adiciona modal de realocação emergencial com suporte a Modo Assistido e Modo Delegado no SPA |

## 6. Delta no modelo de dados

- Resumo das mudanças: Adição de tabelas `emergency_reallocation_logs` e `emergency_reallocation_options` em `db/migrations.sql`, novos modelos Pydantic em `src/api/schemas.py` e persistência no `src/api/worker.py`.
- Detalhe completo em: `_reversa_forward/014-realocacao-docente-emergencial/data-delta.md`

## 7. Delta de contratos externos

| Contrato | Tipo | Arquivo de detalhe |
|----------|------|--------------------|
| Realocação Docente API | HTTP / REST | `_reversa_forward/014-realocacao-docente-emergencial/interfaces/reallocate-teachers-api.md` |

## 8. Plano de migração

1. Executar a migração DDL de tabela em `db/migrations.sql` para criar `emergency_reallocation_logs`.
2. Atualizar o `src/api/worker.py` para carregar o histórico de realocações emergenciais na inicialização.
3. Implantar os novos endpoints REST em `src/api/routes.py` e a atualização da SPA em `src/api/static/index.html`.

## 9. Riscos e mitigações

| Risco | Impacto | Probabilidade | Mitigação |
|-------|---------|---------------|-----------|
| Efeito dominó de descarte de horários em docentes terceiros | Médio | Médio | Ponderação no algoritmo de IA penalizando trocas em cascata |
| Conflitos com restrições horárias (`Restriction`) | Alto | Baixo | Validação rigorosa das janelas de disponibilidade em `src/engine/core.py` |
| Sobrecarga no atendimento de coordenações correlatas | Médio | Baixo | Flag indicativo de "Busca Expandida" exibido no painel para transparência |

## 10. Critério de pronto

- [ ] Todas as ações do `actions.md` marcadas `[X]`
- [ ] `regression-watch.md` gerado e suíte de testes unitários passando em `pytest`
- [ ] Testes de integração dos novos endpoints `/api/v1/emergency-reallocations` validados

## 11. Histórico de alterações

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-08-13 | Versão inicial gerada por `/reversa-plan` | reversa |
