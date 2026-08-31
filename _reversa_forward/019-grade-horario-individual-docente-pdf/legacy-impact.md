# Legacy Impact: Grade de Horário Individual do Docente com Exportação PDF

> Identificador: `019-grade-horario-individual-docente-pdf`
> Data: `2026-08-14`

## 1. Arquivos Afetados

| Arquivo afetado | Componente | Tipo | Severidade | Justificativa |
|-----------------|------------|------|------------|---------------|
| `src/api/routes.py` | `academic-space-manager` | `contrato-novo` | LOW | Adição do endpoint `GET /api/v1/reports/teacher/{teacher_id}/pdf`. |
| `src/api/reports.py` | `academic-space-manager` | `componente-novo` | LOW | Adição de `generate_teacher_pdf_report`. |
| `src/api/static/index.html` | `occupancy-dashboard` | `componente-novo` | LOW | Modal `#teacherScheduleModal`, tabela semanal por slot e botão de exportação individual em PDF. |
