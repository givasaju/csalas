# Adendo: Gestão de Restrições de Horários por Professor e Alertas de Conflitos

> Identificador: `006-restricoes-horarios-docentes`  
> Data: `2026-08-08`  
> Cenário: Legado  

---

## Vigência

Vigente desde 2026-08-07.
Superado pela re-extração de 2026-08-09.

---

## Resumo da entrega

Esta feature entregou a gestão completa de restrições de horários por professor e a aplicação de bloqueio rígido (*hard constraint*) no motor de alocação de IA do ClassSync AI. Foram implementadas as rotas `GET /api/v1/teachers/{teacher_id}/restrictions` (listagem por docente) e `DELETE /api/v1/allocation/restrictions/{restriction_id}` (exclusão unitária de restrição). O motor de alocação de salas (`core.py`) foi atualizado para recusar alocações em slots indisponíveis para o docente responsável e a SPA Web foi integrada. Foram concluídas 9 de 9 ações planejadas no `actions.md`.

---

## Impacto por artefato da extração

| Artefato | Seção | Tipo de impacto | Delta |
|----------|-------|-----------------|-------|
| `_reversa_sdd/architecture.md` | `# Componentes` | `contrato-alterado` | A API REST foi expandida com rotas de busca de restrições por docente e exclusão unitária por ID. |
| `_reversa_sdd/architecture.md` | `# Componentes` | `regra-alterada` | O Motor de Alocação (`core.py`) agora valida a matriz de indisponibilidade docente e recusa alocações em horários bloqueados. |
| `_reversa_sdd/domain.md` | `# Regras de Negócio` | `regra-alterada` | A regra de indisponibilidade docente (2.10) atua como Hard Constraint no leilão/alocação de turmas. |

---

## Regras sob vigilância

Os watch items de regressão criados nesta feature estão registrados no seguinte arquivo:
* [regression-watch.md](file:///c:/csalas/_reversa_forward/006-restricoes-horarios-docentes/regression-watch.md) (Watch IDs: `W001`, `W002`, `W003`)

---

## Fontes

- `_reversa_forward/006-restricoes-horarios-docentes/requirements.md`
- `_reversa_forward/006-restricoes-horarios-docentes/actions.md`
- `_reversa_forward/006-restricoes-horarios-docentes/legacy-impact.md`
- `_reversa_forward/006-restricoes-horarios-docentes/regression-watch.md`
