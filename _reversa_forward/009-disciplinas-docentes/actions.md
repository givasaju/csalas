# Actions: Cadastro de Disciplinas Lecionáveis por Docente

> Identificador: `009-disciplinas-docentes`  
> Data: `2026-08-09`  
> Roadmap: `_reversa_forward/009-disciplinas-docentes/roadmap.md`  

---

## Resumo

| Métrica | Valor |
|---------|-------|
| Total de ações | 7 |
| Paralelizáveis (`[//]`) | 3 |
| Maior cadeia de dependência | 4 |

---

## Fase 1, Preparação

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T001 | Adicionar campo `subjects` (Column JSON) ao modelo `Teacher` em `src/models.py` e schemas Pydantic `TeacherCreate` e `TeacherResponse` com `min_items=1` e `max_items=6` em `src/api/schemas.py` | - | `[//]` | `src/models.py` | 🟢 | `[X]` |

---

## Fase 2, Testes

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T002 | Criar arquivo de testes automatizados em `tests/test_api_teacher_subjects.py` cobrindo cadastro unitário com disciplinas, rejeição sem disciplinas ou >6 disciplinas e importação CSV | T001 | `[//]` | `tests/test_api_teacher_subjects.py` | 🟢 | `[X]` |

---

## Fase 3, Núcleo

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T003 | Atualizar rotas REST `POST /api/v1/teachers` e `POST /api/v1/teachers/import-csv` em `src/api/routes.py` para incluir parsing da coluna de disciplinas (delimitadas por `;`) e validação de 1 a 6 disciplinas | T001 | - | `src/api/routes.py` | 🟢 | `[X]` |
| T004 | Atualizar armazenamento em memória e inicializador de docentes em `src/api/worker.py` para suportar a chave `subjects` | T001 | `[//]` | `src/api/worker.py` | 🟢 | `[X]` |

---

## Fase 4, Integração

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T005 | Adicionar campo de inserção de disciplinas e renderização de badges na tabela de docentes na SPA web | T003 | - | `src/api/static/index.html` | 🟢 | `[X]` |
| T006 | Adicionar estilos visuais CSS `.badge-subject` para exibição formatada das disciplinas na SPA web | T005 | - | `src/api/static/index.css` | 🟢 | `[X]` |

---

## Fase 5, Polimento

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T007 | Adicionar tratamento de erros e mensagens explicativas em `src/api/routes.py` para requisições de disciplinas malformatadas, vazias ou com mais de 6 itens | T003 | - | `src/api/routes.py` | 🟢 | `[X]` |

---

## Notas de execução

Nenhuma observação no momento.

---

## Histórico de alterações

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-08-09 | Versão inicial gerada por `/reversa-to-do` | reversa |
