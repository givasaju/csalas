# Actions: Realocação Departamental de Disciplinas por Novo Docente

> Identificador: `012-realocacao-disciplinas-dept`
> Data: `2026-08-10`
> Roadmap: `_reversa_forward/012-realocacao-disciplinas-dept/roadmap.md`

---

## Resumo

| Métrica | Valor |
|---------|-------|
| Total de ações | 7 |
| Paralelizáveis (`[//]`) | 4 |
| Maior cadeia de dependência | 5 |

---

## Fase 1, Preparação

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T001 | Definir os schemas Pydantic `ReallocateSubjectsRequest` e `ReallocateSubjectsResponse` em `src/api/schemas.py` | - | `[//]` | `src/api/schemas.py` | 🟢 | `[x]` |

---

## Fase 2, Testes

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T002 | Criar arquivo de teste automatizado `tests/test_api_reallocate_subjects.py` com cenários de sucesso e caso negativo de departamentos distintos | T001 | `[//]` | `tests/test_api_reallocate_subjects.py` | 🟢 | `[x]` |

---

## Fase 3, Núcleo

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T003 | Implementar lógica de validação de departamento homogêneo e exigência de `replacement_subject` em `src/api/routes.py` | T001 | - | `src/api/routes.py` | 🟢 | `[x]` |
| T004 | Implementar endpoint `POST /api/v1/teachers/reallocate-subjects` em `src/api/routes.py` com migração automática de alocações vigentes e sinalização de conflitos | T003 | - | `src/api/routes.py` | 🟢 | `[x]` |

---

## Fase 4, Integração

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T005 | Adicionar estrutura HTML do Modal de Realocação Rápida `#reallocateModal` em `src/api/static/index.html` | T004 | `[//]` | `src/api/static/index.html` | 🟢 | `[x]` |
| T006 | Implementar funções JavaScript `openReallocateModal()` e `handleReallocateSubjects()` no `src/api/static/index.html` para integração com a API | T005 | - | `src/api/static/index.html` | 🟢 | `[x]` |

---

## Fase 5, Polimento

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T007 | Adicionar logs de auditoria estruturados `[SUBJECT_REALLOCATION]` e executar validação final da suíte com `pytest` | T004, T006 | `[//]` | `tests/test_api_reallocate_subjects.py` | 🟢 | `[x]` |

---

## Notas de execução

Todas as 7 ações T001 a T007 concluídas e validadas com 100% de aprovação nos testes automatizados.

---

## Histórico de alterações

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-08-10 | Versão inicial gerada por `/reversa-to-do` | reversa |
| 2026-08-10 | Conclusão de todas as ações T001 a T007 | reversa |
