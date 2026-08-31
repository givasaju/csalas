# Adendo: Cadastro de Disciplinas Lecionáveis por Docente

> Identificador: `009-disciplinas-docentes`  
> Data: `2026-08-09`  
> Cenário: Legado  

---

## Vigência

Vigente desde 2026-08-09.

---

## Resumo da entrega

Esta feature entregou a funcionalidade de cadastro e gestão de disciplinas lecionáveis (de 1 a 6 disciplinas) por docente no ClassSync AI. Foram atualizados a tabela ORM `Teacher`, os schemas REST Pydantic `TeacherCreate` e `TeacherResponse`, as rotas REST `POST /api/v1/teachers` e `POST /api/v1/teachers/import-csv` (com parsing de disciplinas separadas por `;`), a simulação de dados em memória no `worker.py`, além do formulário e badges visuais na SPA web. Foram concluídas 7 de 7 ações planejadas no pipeline TDD.

---

## Impacto por artefato da extração

| Artefato | Seção | Tipo de impacto | Delta |
|----------|-------|-----------------|-------|
| `_reversa_sdd/architecture.md` | `#3-modelo-de-entidade-relacionamento-erd` | `delta-de-dados` | Adiciona a coluna JSON `subjects` no modelo `Teacher` em `src/models.py`. |
| `_reversa_sdd/architecture.md` | `#1-visao-geral-do-sistema` | `delta-de-contrato-externo` | Schemas REST `TeacherCreate` e `TeacherResponse` passam a incluir a lista de disciplinas `subjects` (exigindo de 1 a 6 disciplinas). |
| `_reversa_sdd/domain.md` | `#210-restricoes-de-indisponibilidade-docente` | `regra-alterada` | O cadastro de docentes passa a exigir obrigatoriamente a inclusão de no mínimo 1 e no máximo 6 disciplinas lecionáveis. |
| `_reversa_sdd/domain.md` | `#27-importacao-transacional-de-salas-tudo-ou-nada` | `regra-alterada` | O endpoint de importação CSV de docentes `POST /api/v1/teachers/import-csv` aceita a coluna `disciplinas` (delimitada por `;`) validando a regra atômica tudo-ou-nada. |
| `_reversa_sdd/painel-ocupacao/requirements.md` | `#visão-geral` | `componente-novo` | Adiciona o campo de entrada de disciplinas no formulário de docente e a exibição de badges na tabela de docentes na SPA (`index.html` e `index.css`). |

---

## Regras sob vigilância

Os watch items de regressão criados nesta feature estão registrados no seguinte arquivo:
* [regression-watch.md](file:///c:/csalas/_reversa_forward/009-disciplinas-docentes/regression-watch.md) (Watch IDs: `W001`, `W002`, `W003`)

---

## Fontes

- `_reversa_forward/009-disciplinas-docentes/requirements.md`
- `_reversa_forward/009-disciplinas-docentes/actions.md`
- `_reversa_forward/009-disciplinas-docentes/legacy-impact.md`
- `_reversa_forward/009-disciplinas-docentes/regression-watch.md`
