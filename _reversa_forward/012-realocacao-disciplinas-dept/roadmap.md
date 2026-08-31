# Roadmap: Realocação Departamental de Disciplinas por Novo Docente

> Identificador: `012-realocacao-disciplinas-dept`
> Data: `2026-08-10`
> Requirements: `_reversa_forward/012-realocacao-disciplinas-dept/requirements.md`
> Confidência: 🟢 CONFIRMADO, 🟡 INFERIDO, 🔴 LACUNA

## 1. Resumo da abordagem

A abordagem técnica consiste em adicionar um novo endpoint atômico e transacional `POST /api/v1/teachers/reallocate-subjects` na API FastAPI em `src/api/routes.py`, acompanhado de novos schemas Pydantic em `src/api/schemas.py`. O endpoint valida estritamente a homogeneidade de departamento (`teacher_source.department == teacher_target.department`). Caso a transferência esvazie o rol de disciplinas do docente doador, a requisição exige a indicação de uma disciplina substituta (`replacement_subject`). Todas as alocações vigentes (`Allocation`) associadas às disciplinas transferidas são migradas automaticamente em memória/banco de dados para o novo docente; caso ocorra conflito de horário ou limite de aulas consecutivas, a alocação é marcada como `"pending_arbitration"`. Na SPA (`src/api/static/index.html`), será adicionado um Modal de Realocação Rápida Departamental.

## 2. Princípios aplicados

| Princípio | Como a feature se relaciona | Status |
|-----------|------------------------------|--------|
| Iso-Department Consistency | Garante que disciplinas permaneçam isoladas entre docentes do mesmo departamento | respeita |
| Transacionalidade Atômica | A realocação de disciplinas e a migração de alocações ocorrem de forma conjunta tudo-ou-nada | respeita |

## 3. Decisões técnicas

| ID | Decisão | Justificativa | Alternativas descartadas | Confidência |
|----|---------|----------------|--------------------------|-------------|
| D-01 | Endpoint de realocação atômico `POST /api/v1/teachers/reallocate-subjects` | Garante atomicidade da troca de rol e reatribuição de alocações em uma única requisição HTTP | Múltiplas chamadas avulsas `PUT /teachers/{id}` | 🟢 |
| D-02 | Migração automática de alocações ativas para o docente receptor | Evita desalocação desnecessária e preserva a grade horária mantendo consistência no calendário | Excluir todas as alocações da disciplina | 🟢 |
| D-03 | Exigência de `replacement_subject` quando o doador fica sem matérias | Mantém o docente doador com no mínimo 1 disciplina lecionável (regra mandatória do legado) | Permitir docente doador com 0 disciplinas | 🟢 |
| D-04 | Modal de Realocação Rápida na SPA `index.html` | Oferece visualização clara por departamento e seleção ágil de docentes e disciplinas | Wizard de múltiplos passos | 🟢 |

## 4. Premissas

Nenhuma premissa não confirmada. Todas as dúvidas foram esclarecidas e integradas via `/reversa-clarify`.

## 5. Delta arquitetural

| Componente | Arquivo de origem no legado | Tipo de mudança | Resumo |
|------------|------------------------------|-----------------|--------|
| `academic-space-manager` | `src/api/routes.py` | contrato-novo | Adiciona endpoint `POST /api/v1/teachers/reallocate-subjects` |
| `academic-space-manager` | `src/api/schemas.py` | contrato-novo | Adiciona schemas Pydantic `ReallocateSubjectsRequest` e `ReallocateSubjectsResponse` |
| `painel-ocupacao` | `src/api/static/index.html` | componente-novo | Adiciona modal visual `#reallocateModal` e script de integração na SPA |
| `core-allocation-engine` | `src/engine/core.py` | regra-alterada | Reavalia alocações migradas marcando conflitos com status `"pending_arbitration"` |

## 6. Delta no modelo de dados

- Resumo das mudanças: Nenhuma nova tabela ou coluna é criada no banco relacional. A operação manipula o campo JSON `subjects` na entidade `Teacher` e atualiza a coluna `teacher_id` na entidade `Allocation`.
- Detalhe completo em: `_reversa_forward/012-realocacao-disciplinas-dept/data-delta.md`

## 7. Delta de contratos externos

| Contrato | Tipo | Arquivo de detalhe |
|----------|------|--------------------|
| Realocação Departamental de Disciplinas | HTTP REST | `_reversa_forward/012-realocacao-disciplinas-dept/interfaces/reallocate-subjects-api.md` |

## 8. Plano de migração

1. Aplicar atualizações de schemas Pydantic e endpoint REST em `src/api/routes.py`.
2. Atualizar funções de manipulação de alocações vigentes em `src/api/routes.py` / `worker.py`.
3. Inserir componente visual Modal e handlers JavaScript em `src/api/static/index.html`.
4. Executar suíte de testes automatizados com `pytest`.

## 9. Riscos e mitigações

| Risco | Impacto | Probabilidade | Mitigação |
|-------|---------|---------------|-----------|
| Transferência indevida entre departamentos distintos | Alto | Baixo | Validação mandatória no backend retornando HTTP `422 Unprocessable Entity` se `source.department != target.department` |
| Conflito horário ou excesso de aulas seguidas no novo docente | Médio | Médio | Marcador automático de status `"pending_arbitration"` e notificação no resultado da API |
| Docente doador ficar com rol de disciplinas vazio | Médio | Baixo | Validação atômica exigindo o parâmetro `replacement_subject` se a lista de disciplinas remanescente for vazia |

## 10. Critério de pronto

- [ ] Todas as ações do `actions.md` marcadas `[X]`
- [ ] Endpoint `POST /api/v1/teachers/reallocate-subjects` implementado e testado
- [ ] Validações de departamento e disciplina substituta cobertas por testes automatizados
- [ ] Modal visual no `index.html` funcionando perfeitamente

## 11. Histórico de alterações

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-08-10 | Versão inicial gerada por `/reversa-plan` | reversa |
