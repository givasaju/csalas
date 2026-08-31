# Adendo: Realocação Departamental de Disciplinas por Novo Docente

> Identificador: `012-realocacao-disciplinas-dept`  
> Data: `2026-08-10`  
> Cenário: Legado  

---

## Vigência

Vigente desde 2026-08-10.

---

## Resumo da entrega

Esta feature entregou a funcionalidade de realocação e transferência de disciplinas lecionáveis entre docentes do mesmo departamento acadêmico no ClassSync AI. Foram adicionados os Pydantic schemas `ReallocateSubjectsRequest` e `ReallocateSubjectsResponse` em `src/api/schemas.py`, a rota REST atômica `POST /api/v1/teachers/reallocate-subjects` em `src/api/routes.py` (com validação Iso-Department, migração automática de alocações ativas e exigência de disciplina substituta caso o doador fique com 0 matérias), o botão **"🔄 Realocação Departamental"** e o modal `#reallocateModal` na SPA web (`index.html`), além de 4 testes automatizados em `tests/test_api_reallocate_subjects.py`. Foram concluídas 7 de 7 ações planejadas.

---

## Impacto por artefato da extração

| Artefato | Seção | Tipo de impacto | Delta |
|----------|-------|-----------------|-------|
| `_reversa_sdd/architecture.md` | `#1-visao-geral-do-sistema` | `contrato-novo` | Adiciona os schemas REST `ReallocateSubjectsRequest` e `ReallocateSubjectsResponse`. |
| `_reversa_sdd/architecture.md` | `#3-modelo-de-entidade-relacionamento-erd` | `delta-de-dados` | Mutação atômica das colunas `subjects` (JSON) na entidade `Teacher` e `teacher_id` na entidade `Allocation`. |
| `_reversa_sdd/domain.md` | `#210-restricoes-de-indisponibilidade-docente` | `regra-alterada` | O rol de disciplinas passa a permitir transferência entre docentes do mesmo departamento (Iso-Department), exigindo `replacement_subject` se o doador zerar matérias e limitando receptor a 6. |
| `_reversa_sdd/painel-ocupacao/requirements.md` | `#visão-geral` | `componente-novo` | Adiciona botão e modal de realocação departamental na SPA (`index.html`). |

---

## Regras sob vigilância

Os watch items de regressão criados nesta feature estão registrados no seguinte arquivo:
* [regression-watch.md](file:///c:/csalas/_reversa_forward/012-realocacao-disciplinas-dept/regression-watch.md) (Watch IDs: `W001`, `W002`, `W003`, `W004`)

---

## Fontes

- `_reversa_forward/012-realocacao-disciplinas-dept/requirements.md`
- `_reversa_forward/012-realocacao-disciplinas-dept/actions.md`
- `_reversa_forward/012-realocacao-disciplinas-dept/legacy-impact.md`
- `_reversa_forward/012-realocacao-disciplinas-dept/regression-watch.md`
