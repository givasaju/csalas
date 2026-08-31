# Adendo: Entrada de Alocação de Aulas (50 min) e Limite de 4 Aulas Consecutivas

> Identificador: `008-alocacao-docente-max-4-aulas`  
> Data: `2026-08-08`  
> Cenário: Legado  

---

## Vigência

Vigente desde 2026-08-08.
Superado pela re-extração de 2026-08-09.

---

## Resumo da entrega

Esta feature entregou a funcionalidade de agendamento e entrada de dados de alocação de aulas de 50 minutos por professor e a regra de negócio rígida (*hard constraint*) que limita a no máximo 4 aulas seguidas (consecutivas) para um mesmo docente no mesmo turno (Manhã, Tarde ou Noite). Foram implementados a tabela ORM `Allocation`, as rotas REST `POST`, `GET` e `DELETE /api/v1/allocations`, a validação de janela deslizante, a Hard Constraint no motor de IA e a nova aba na SPA Web. Foram concluídas 9 de 9 ações planejadas no pipeline TDD.

---

## Impacto por artefato da extração

| Artefato | Seção | Tipo de impacto | Delta |
|----------|-------|-----------------|-------|
| `_reversa_sdd/architecture.md` | `#1.-visao-geral-do-sistema` | `delta-de-dados` | Adiciona a tabela ORM `Allocation` em `src/models.py`. |
| `_reversa_sdd/architecture.md` | `#1.-visao-geral-do-sistema` | `contrato-novo` | Expõe os endpoints REST `POST`, `GET` e `DELETE /api/v1/allocations` em `src/api/routes.py`. |
| `_reversa_sdd/architecture.md` | `#1.-visao-geral-do-sistema` | `regra-alterada` | O Motor de Alocação (`core.py`) recusa alocações que resultem em mais de 4 aulas consecutivas por turno para o docente. |
| `_reversa_sdd/painel-ocupacao/requirements.md` | `#visão-geral` | `componente-novo` | Adiciona a aba "Alocação de Aulas (50 min)" e formulário interativo em `src/api/static/index.html`. |
| `_reversa_sdd/domain.md` | `#2.10-restricoes-de-indisponibilidade-docente` | `regra-alterada` | Regra de restrição docente expandida com a trava de no máximo 4 aulas seguidas por turno. |

---

## Regras sob vigilância

Os watch items de regressão criados nesta feature estão registrados no seguinte arquivo:
* [regression-watch.md](file:///c:/csalas/_reversa_forward/008-alocacao-docente-max-4-aulas/regression-watch.md) (Watch IDs: `W001`, `W002`, `W003`)

---

## Fontes

- `_reversa_forward/008-alocacao-docente-max-4-aulas/requirements.md`
- `_reversa_forward/008-alocacao-docente-max-4-aulas/roadmap.md`
- `_reversa_forward/008-alocacao-docente-max-4-aulas/legacy-impact.md`
- `_reversa_forward/008-alocacao-docente-max-4-aulas/regression-watch.md`
