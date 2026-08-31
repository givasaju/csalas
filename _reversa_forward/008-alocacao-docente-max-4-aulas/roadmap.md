# Roadmap: Entrada de Alocação de Aulas Docentes (50 min) e Limite de 4 Aulas Consecutivas

> Identificador: `008-alocacao-docente-max-4-aulas`
> Data: `2026-08-08`
> Requirements: `_reversa_forward/008-alocacao-docente-max-4-aulas/requirements.md`
> Confidência: 🟢 CONFIRMADO, 🟡 INFERIDO, 🔴 LACUNA

## 1. Resumo da abordagem

A abordagem técnica expande o modelo relacional em `src/models.py` com a tabela `Allocation` e fornece os endpoints REST `POST /api/v1/allocations`, `GET /api/v1/allocations` e `DELETE /api/v1/allocations/{id}` em `src/api/routes.py`. A regra de consecutividade (no máximo 4 aulas de 50 minutos seguidas por turno) é implementada como uma função de validação de janela deslizante determinística no backend antes de persistir o registro. No motor de alocação de IA (`src/engine/core.py`), essa mesma regra é integrada como uma *Hard Constraint* mandatória. Na SPA web (`src/api/static/index.html`), é adicionada a aba "Alocação de Aulas" com formulário interativo de agendamento por sub-slots de 50 min.

## 2. Princípios aplicados

Não há arquivo `.reversa/principles.md` registrado no projeto.

| Princípio | Como a feature se relaciona | Status |
|-----------|------------------------------|--------|
| N/A | Nenhum princípio cadastrado em `.reversa/principles.md`. | respeita |

## 3. Decisões técnicas

| ID | Decisão | Justificativa | Alternativas descartadas | Confidência |
|----|---------|----------------|--------------------------|-------------|
| D-01 | Mapeamento de 5 sub-slots de 50 min por turno (`shift`: `M`, `T`, `N`; `sub_slot`: `1`..`5`) | Mantém compatibilidade com a estrutura de turnos existente do legado enquanto atende a granularidade de 50 minutos informada no esclarecimento. | Alterar todo o schema de slots legados para timestamps em minutos inteiros | 🟢 |
| D-02 | Validação de consecutividade via Janela Deslizante no Backend | Avalia os sub-slots alocados do docente no turno (ex: sub-slots `[1, 2, 3, 4, 5]`) e rejeita se houver 5 consecutivos sem interrupção. | Delegar a verificação apenas para o JavaScript no frontend | 🟢 |
| D-03 | Integração como Hard Constraint no loop do `core.py` | Garante que o motor autônomo de IA nunca aloque turmas que sobrecarreguem o professor além do limite de 4 aulas seguidas por turno. | Tratar o limite como Soft Constraint sujeita a penalidade de créditos | 🟢 |
| D-04 | Persistência relacional via tabela `Allocation` SQLAlchemy | Garante rastreabilidade, consulta por docente/sala e integridade referencial com `Teacher` e `Room`. | Armazenar alocações em JSON bruto não-relacional | 🟢 |

## 4. Premissas

Nenhuma premissa pendente. Todas as lacunas foram resolvidas na sessão `/reversa-clarify`.

| Premissa | Origem (`requirements.md` seção) | Risco se errada |
|----------|----------------------------------|-----------------|
| N/A | `## 9. Esclarecimentos` | N/A |

## 5. Delta arquitetural

| Componente | Arquivo de origem no legado | Tipo de mudança | Resumo |
|------------|------------------------------|-----------------|--------|
| `academic-space-manager` | `_reversa_sdd/architecture.md#1.-visao-geral-do-sistema` | delta-de-dados | Adiciona a tabela `Allocation` em `src/models.py` e schemas em `src/api/schemas.py`. |
| `academic-space-manager` | `_reversa_sdd/architecture.md#1.-visao-geral-do-sistema` | contrato-novo | Adiciona as rotas `POST /api/v1/allocations`, `GET /api/v1/allocations` e `DELETE /api/v1/allocations/{id}` em `src/api/routes.py`. |
| `core-allocation-engine` | `_reversa_sdd/architecture.md#1.-visao-geral-do-sistema` | regra-alterada | Incorpora a verificação de no máximo 4 aulas consecutivas por turno como Hard Constraint no loop do `src/engine/core.py`. |
| `occupancy-dashboard` | `_reversa_sdd/architecture.md#1.-visao-geral-do-sistema` | componente-novo | Adiciona a aba "Alocação de Aulas" e controle de sub-slots no `src/api/static/index.html`. |

## 6. Delta no modelo de dados

- Resumo das mudanças: Criação da tabela `Allocation` (`id`, `teacher_id`, `room_id`, `day_of_week`, `shift`, `sub_slot`, `created_at`).
- Detalhe completo em: `_reversa_forward/008-alocacao-docente-max-4-aulas/data-delta.md`

## 7. Delta de contratos externos

| Contrato | Tipo | Arquivo de detalhe |
|----------|------|--------------------|
| `allocations-api` | HTTP | `_reversa_forward/008-alocacao-docente-max-4-aulas/interfaces/allocations-api.md` |

## 8. Plano de migração

1. Executar a criação da tabela `Allocation` via SQLAlchemy metadata (`Base.metadata.create_all(bind=engine)`).
2. Nenhuma alteração destrutiva em tabelas legadas ("n/a").

## 9. Riscos e mitigações

| Risco | Impacto | Probabilidade | Mitigação |
|-------|---------|---------------|-----------|
| Tentativa de agendamento concorrente excedendo 4 aulas consecutivas | médio | baixo | Aplicar verificação transacional com lock ou validação rigorosa antes do `db.commit()`. |
| Incompatibilidade de turno em solicitações fora da faixa `M`, `T`, `N` | baixo | baixo | Validar enums com Pydantic em `schemas.py` retornando HTTP 422 para valores inválidos. |

## 10. Critério de pronto

- [ ] Todas as ações do `actions.md` marcadas `[X]`
- [ ] `cross-check.md` (se executado) sem CRITICAL nem HIGH
- [ ] `regression-watch.md` gerado
- [ ] Suíte de testes automatizados com cobertura de 1 a 4 aulas seguidas (sucesso) e tentativa da 5ª aula (erro 409 Conflict)

## 11. Histórico de alterações

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-08-08 | Versão inicial gerada por `/reversa-plan` | reversa |
