# Adendo SDD: Tabela de Subslots com Intervalos de Aula

> Identificador: `013-tabela-subslots-intervalos`
> Data: `2026-08-11`
> Cenário: Legado

## Vigência

Vigente desde 2026-08-11.

## Resumo da entrega

Esta feature cria a tabela relacional `subslot_time_intervals` no banco de dados e nos modelos FastAPI/SQLAlchemy/Pydantic, com carga inicial automática via migração/seed de 18 horários (5 aulas de 50m + 1 intervalo de 15m entre aula 3 e 4 nos turnos Matutino, Vespertino e Noturno). Disponibiliza rotas REST API (`GET`, `POST`, `PUT`, `DELETE /api/v1/subslots`) e integra a validação de indisponibilidade docente aos subslots cadastrados.

Ações concluídas: 7 de 7 (`T001` a `T007`).

## Impacto por artefato da extração

| Artefato | Seção | Tipo de impacto | Delta |
|----------|-------|-----------------|-------|
| `_reversa_sdd/architecture.md` | `#3-modelo-de-entidade-relacionamento-erd` | `componente-novo` | Adicionada a tabela relacional `subslot_time_intervals` no banco de dados. |
| `_reversa_sdd/architecture.md` | `#1-visao-geral-do-sistema` | `delta-de-contrato-externo` | Adicionados os endpoints REST API `/api/v1/subslots` para consulta e gerenciamento CRUD. |
| `_reversa_sdd/domain.md` | `#210-restricoes-de-indisponibilidade-docente` | `regra-alterada` | A validação de restrições docentes passou a consultar dinamicamente a tabela `subslot_time_intervals`, mantendo suporte a `M1`..`N5`. |
| `_reversa_sdd/inventory.md` | `#superficie-do-codigo` | `regra-nova` | Adicionado modelo ORM `SubslotTimeInterval` em `src/models.py`, schemas em `src/api/schemas.py` e rotas em `src/api/routes.py`. |

## Regras sob vigilância

- `W001`: `_reversa_forward/013-tabela-subslots-intervalos/regression-watch.md#W001`
- `W002`: `_reversa_forward/013-tabela-subslots-intervalos/regression-watch.md#W002`

## Fontes

- `_reversa_forward/013-tabela-subslots-intervalos/requirements.md`
- `_reversa_forward/013-tabela-subslots-intervalos/legacy-impact.md`
- `_reversa_forward/013-tabela-subslots-intervalos/regression-watch.md`
- `_reversa_forward/013-tabela-subslots-intervalos/actions.md`
