# Actions: Grade de Horário Individual do Docente com Exportação PDF

> Identificador: `019-grade-horario-individual-docente-pdf`
> Data: `2026-08-14`

## Fase 1, Preparação

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T001 | Implementar o endpoint `GET /api/v1/reports/teacher/{teacher_id}/pdf` em `src/api/routes.py` para gerar o PDF da grade semanal do professor | - | `[//]` | `src/api/routes.py` | 🟢 | `[x]` |

## Fase 3, Núcleo

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T002 | Adicionar o HTML do modal `#teacherScheduleModal` em `src/api/static/index.html` com o botão de download de PDF | T001 | - | `src/api/static/index.html` | 🟢 | `[x]` |
| T003 | Adicionar cursor pointer, hover visual e o evento `onclick` nas linhas da tabela de docentes e implementar `openTeacherScheduleModal()` | T002 | - | `src/api/static/index.html` | 🟢 | `[x]` |

## Fase 5, Polimento

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T004 | Testar a abertura do modal e a geração de PDF via suíte de testes `pytest` e teste de integração no navegador | T003 | `[//]` | `tests/test_reports_api.py` | 🟢 | `[x]` |

## Notas de execução

Todas as 4 ações T001 a T004 foram executadas com sucesso e validadas pela suíte de testes (63/63 passed).
