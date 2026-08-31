# Regression Watch: Grade de Horário Individual do Docente com Exportação PDF

> Identificador: `019-grade-horario-individual-docente-pdf`
> Data: `2026-08-14`

## 1. Itens de Vigilância de Regressão

| ID | Origem (arquivo, seção) | Regra esperada após mudança | Tipo de verificação | Sinal de violação |
|----|-------------------------|-----------------------------|---------------------|-------------------|
| W001 | `src/api/routes.py` | Endpoint `GET /api/v1/reports/teacher/{teacher_id}/pdf` gera e retorna o PDF individual do professor. | `presença` | Falha ao baixar PDF do docente. |
| W002 | `src/api/static/index.html` | Clicar na linha do docente deve abrir o modal `#teacherScheduleModal` exibindo a matriz semanal. | `presença` | Modal não abre ao clicar no docente. |
