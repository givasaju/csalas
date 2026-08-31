# Roadmap: Grade de Horário Individual do Docente com Exportação PDF

> Identificador: `019-grade-horario-individual-docente-pdf`
> Data: `2026-08-14`
> Requirements: `_reversa_forward/019-grade-horario-individual-docente-pdf/requirements.md`

## 1. Resumo da abordagem

1. **Backend**:
   - Criar o endpoint `GET /api/v1/reports/teacher/{teacher_id}/pdf` em `src/api/routes.py` utilizando o ReportLab para gerar o PDF da grade semanal individual do professor.
2. **Frontend**:
   - Adicionar o modal `#teacherScheduleModal` em `src/api/static/index.html`.
   - Adicionar efeito hover e evento `onclick="openTeacherScheduleModal('${t.teacher_id}')"` nas linhas da tabela de docentes (`#reportTeachersTableBody`).
   - Criar a função JavaScript `renderTeacherScheduleMatrix(teacherData)` para desenhar a grade semanal (Segunda a Sábado x M1..N6).
   - Adicionar o botão `📄 Gerar PDF do Horário` no modal para disparar a rota de download do PDF individual.

## 2. Decisões técnicas

| ID | Decisão | Justificativa | Confidência |
|----|---------|----------------|-------------|
| D-01 | Modal Glassmorphic para a grade individual | Permite visualização focada sem perder o contexto da aba de relatórios | 🟢 |
| D-02 | Endpoint `GET /api/v1/reports/teacher/{teacher_id}/pdf` dedicado | Permite que o download do PDF seja reutilizável e com layout limpo por docente | 🟢 |

## 3. Delta Arquitetural

| Componente | Arquivo de origem | Tipo | Resumo |
|------------|-------------------|------|--------|
| `occupancy-dashboard` | `src/api/static/index.html` | `componente-novo` | Adição de `#teacherScheduleModal` e clique nas linhas da tabela de docentes. |
| `academic-space-manager` | `src/api/routes.py` | `contrato-novo` | Endpoint `GET /api/v1/reports/teacher/{teacher_id}/pdf`. |
