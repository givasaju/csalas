# Addendum: Grade de Horário Individual do Docente com Exportação PDF

> Identificador: `019-grade-horario-individual-docente-pdf`
> Data: `2026-08-14`

## Vigência

Vigente desde 2026-08-14.

## Resumo da entrega

Adicionada a funcionalidade interativa de consulta e exportação de grade horária individual por docente. Na seção **Relatório de Grade & Carga Horária Docente (Individual)** da aba Relatórios, clicar em qualquer linha de professor abre o modal `#teacherScheduleModal` exibindo a matriz semanal completa (Segunda a Sábado x Turnos M1..N5) com disciplinas e salas alocadas. O modal possui o botão **📄 Gerar PDF do Horário** que aciona o endpoint `GET /api/v1/reports/teacher/{teacher_id}/pdf` para download direto.

## Impacto por artefato da extração

| Artefato | Seção | Tipo de impacto | Delta |
|----------|-------|-----------------|-------|
| `_reversa_sdd/architecture.md` | `#academic-space-manager` | `contrato-novo` | Endpoint REST `GET /api/v1/reports/teacher/{teacher_id}/pdf` em `src/api/routes.py` e gerador PDF `generate_teacher_pdf_report` em `src/api/reports.py`. |
| `_reversa_sdd/architecture.md` | `#occupancy-dashboard` | `componente-novo` | Modal `#teacherScheduleModal` com matriz semanal e evento de clique na tabela em `src/api/static/index.html`. |

## Regras sob vigilância

- `W001`: Vigilância de funcionamento do endpoint `GET /api/v1/reports/teacher/{teacher_id}/pdf`
- `W002`: Vigilância de clique interativo e abertura do modal `#teacherScheduleModal`

## Fontes

- `_reversa_forward/019-grade-horario-individual-docente-pdf/requirements.md`
- `_reversa_forward/019-grade-horario-individual-docente-pdf/roadmap.md`
- `_reversa_forward/019-grade-horario-individual-docente-pdf/actions.md`
- `_reversa_forward/019-grade-horario-individual-docente-pdf/legacy-impact.md`
- `_reversa_forward/019-grade-horario-individual-docente-pdf/regression-watch.md`
