# Roadmap: Gestão de Restrições de Horários por Professor e Alertas de Conflitos

> Identificador: `006-restricoes-horarios-docentes`  
> Data: `2026-08-08`  
> Requirements: `_reversa_forward/006-restricoes-horarios-docentes/requirements.md`  
> Confidência: 🟢 CONFIRMADO, 🟡 INFERIDO, 🔴 LACUNA  

---

## 1. Resumo da abordagem

A solução implementa o suporte completo às restrições horárias de professores no backend FastAPI e na SPA web do ClassSync AI. Expandiremos a API com o endpoint `GET /api/v1/teachers/{teacher_id}/restrictions` para listagem por docente e `DELETE /api/v1/allocation/restrictions/{restriction_id}` para remoção pontual de restrição. No motor de alocação de IA (`src/engine/core.py`), a checagem de restrições atuará como uma trava rígida (*hard constraint*), impedindo a atribuição da sala/horário bloqueado ao professor responsável pela turma. Na interface SPA, a aba de Docentes será enriquecida com uma matriz de disponibilidade semanal clicável (Seg-Dom × M1-N2).

---

## 2. Princípios aplicados

| Princípio | Como a feature se relaciona | Status |
|-----------|------------------------------|--------|
| Sem princípios registrados (`.reversa/principles.md` ausente) | n/a | respeita |

---

## 3. Decisões técnicas

| ID | Decisão | Justificativa | Alternativas descartadas | Confidência |
|----|---------|----------------|--------------------------|-------------|
| D-01 | Implementar checagem de restrições docentes como Hard Constraint no leilão | Garantir que nenhum professor seja alocado em horário em que declarou estar indisponível | Soft constraint com penalização de pontos | 🟢 |
| D-02 | Expor rota `GET /api/v1/teachers/{teacher_id}/restrictions` | Permitir a renderização reativa do grid semanal de indisponibilidade na UI por professor | Carregar todas as restrições globais de uma só vez na UI | 🟢 |
| D-03 | Suportar remoção unitária por ID da restrição | Permitir correção de restrição cadastrada por engano sem apagar todo o banco | Permitir apenas reset semestral total | 🟢 |
| D-04 | Atualizar a SPA com componente visual de matriz horária | Proporcionar UX intuitiva de clique para bloquear/desbloquear slots | Entrada manual via formulário de select box | 🟡 |

---

## 4. Premissas

Nenhuma premissa adotada. Todas as dúvidas do `requirements.md` foram resolvidas no `/reversa-clarify`.

---

## 5. Delta arquitetural

| Componente | Arquivo de origem no legado | Tipo de mudança | Resumo |
|------------|------------------------------|-----------------|--------|
| `API Router` | `_reversa_sdd/architecture.md#Componentes` (`routes.py`) | contrato-alterado | Adição de endpoints GET por professor e DELETE por ID de restrição |
| `Motor de Alocação (Core Engine)` | `_reversa_sdd/architecture.md#Componentes` (`core.py`) | regra-alterada | Inclusão de filtro rígido de restrição docente no loop de alocação de salas |
| `Dashboard Web / SPA` | `_reversa_sdd/architecture.md#Componentes` (`index.html`) | componente-novo | Adição do componente de matriz horária interativa para indisponibilidade docente |

---

## 6. Delta no modelo de dados

- Resumo das mudanças: Nenhuma migration necessária no modelo de banco relacional, pois a tabela `Restriction` (`models.Restriction`) já possui os campos `id`, `teacher_id`, `day_of_week` e `time_slot_id`.
- Detalhe completo em: `_reversa_forward/006-restricoes-horarios-docentes/data-delta.md`

---

## 7. Delta de contratos externos

| Contrato | Tipo | Arquivo de detalhe |
|----------|------|--------------------|
| Restrictions API | HTTP | `_reversa_forward/006-restricoes-horarios-docentes/interfaces/restrictions-api.md` |

---

## 8. Plano de migração

1. Executar atualizações no código backend `src/api/routes.py` (novas rotas) e `src/engine/core.py` (validação no engine).
2. Atualizar a SPA `src/api/static/endpoints.html` / `src/api/static/index.html` com a matriz de restrições.
3. Não são necessárias alterações de schema de banco relacional (backward compatible).

---

## 9. Riscos e mitigações

| Risco | Impacto | Probabilidade | Mitigação |
|-------|---------|---------------|-----------|
| Incompatibilidade de horários gerando turmas sem sala (*pending_arbitration*) | Médio | Médio | O motor mantem o fluxo de realocação para salas secundárias e sinaliza pendência quando não houver salas em slots livres |
| Desempenho ao consultar restrições em laços do leilão | Baixo | Baixo | Pré-carregar todas as restrições em dicionário indexado por `(teacher_id, day, slot)` antes do leilão |

---

## 10. Critério de pronto

- [ ] Todas as ações do `actions.md` marcadas `[X]`
- [ ] Testes automatizados cobrindo as novas rotas e a validação do motor executando sem falhas
- [ ] `regression-watch.md` gerado
- [ ] Adendo de convergência gerado em `_reversa_sdd/addenda/006-restricoes-horarios-docentes.md`

---

## 11. Histórico de alterações

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-08-08 | Versão inicial gerada por `/reversa-plan` | reversa |
