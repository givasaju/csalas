# Legacy Impact: Cadastro de Disciplinas Lecionáveis por Docente

> Identificador: `009-disciplinas-docentes`  
> Data: `2026-08-09`  
> Extração ancorada: `_reversa_sdd/`  

---

## Resumo de Impacto no Legado

| Arquivo afetado | Componente (`architecture.md`) | Tipo de impacto | Severidade | Justificativa |
|-----------------|-------------------------------|-----------------|------------|---------------|
| [`src/models.py`](file:///c:/csalas/src/models.py) | `gerenciador-espacos` | `delta-de-dados` | LOW | Adição da coluna JSON `subjects` na tabela ORM `Teacher`. |
| [`src/api/schemas.py`](file:///c:/csalas/src/api/schemas.py) | `gerenciador-espacos` | `delta-de-dados` | LOW | Atualização dos schemas `TeacherCreate` e `TeacherResponse` com validação de 1 a 6 disciplinas (`min_items=1`, `max_items=6`). |
| [`src/api/routes.py`](file:///c:/csalas/src/api/routes.py) | `gerenciador-espacos` | `regra-alterada` | MEDIUM | Adição de obrigatoriedade e validação de 1 a 6 disciplinas em `POST /teachers` e parsing de disciplinas (separadas por `;`) no `POST /teachers/import-csv`. |
| [`src/api/worker.py`](file:///c:/csalas/src/api/worker.py) | `gerenciador-espacos` | `delta-de-dados` | LOW | Suporte à chave `subjects` na lista de inicialização `db_teachers`. |
| [`src/api/static/index.html`](file:///c:/csalas/src/api/static/index.html) | `painel-ocupacao` | `regra-alterada` | LOW | Adição do campo de disciplinas no formulário de cadastro unitário e renderização de badges na tabela de docentes da SPA. |
| [`src/api/static/index.css`](file:///c:/csalas/src/api/static/index.css) | `painel-ocupacao` | `componente-novo` | LOW | Inclusão de classe estilizada `.badge-subject` para tags visuais de disciplinas. |

---

## Diff Conceitual por Componente

### `gerenciador-espacos`
A entidade docente passou a exigir obrigatoriamente entre 1 e 6 disciplinas lecionáveis vinculadas a cada registro de professor no cadastro unitário e na importação em lote CSV.

### `painel-ocupacao`
A interface do painel web foi expandida para incluir a entrada de disciplinas lecionáveis e exibir badges visuais com as disciplinas lecionáveis cadastradas de cada docente.

---

## Regras Preservadas 🟢

- `_reversa_sdd/domain.md#210-restricoes-de-indisponibilidade-docente` — Restrições de horário por docente mantidas intactas.
- `_reversa_sdd/domain.md#27-importacao-transacional-de-salas-tudo-ou-nada` — Política transacional tudo-ou-nada para importação CSV mantida.

---

## Regras Modificadas 🟢

- `_reversa_sdd/addenda/005-cadastro-docentes.md#resumo-da-entrega` — O cadastro de docentes agora requer obrigatoriamente de 1 a 6 disciplinas lecionáveis vinculadas.
