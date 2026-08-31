# Addendum 010: Tabela de Alocações por Docente no Relatório de Ocupação

> Data de sincronização: `2026-08-09`  
> Origem: `_reversa_forward/010-tabela-docentes-relatorio/`  

---

## 1. Contexto da Evolução

Adicionada uma nova tabela/aba dedicada ao detalhamento de alocações por docente nos relatórios de ocupação de salas gerados em formato PDF e Excel (.xlsx).

---

## 2. Resumo da Entrega

- **`src/api/reports.py`**:
  - Atualizadas as funções `generate_pdf_report()` e `generate_excel_report()` para aceitarem o parâmetro `teacher_allocations`.
  - No PDF, adicionada a Seção 3 ("Ocupação por Docente (Ordem A-Z)") formatada em estilo *Impressão Limpa*.
  - No Excel, adicionada a Aba 3 ("Alocações por Docente") contendo as colunas: `Nome do Docente`, `Disciplinas Lecionáveis`, `Sala Ocupada`, `Turno` e `Sub-slot`.
  - Aplicada a ordenação estritamente alfabética (A-Z) por nome do docente.
- **`src/api/routes.py`**:
  - Atualizadas as rotas `GET /api/v1/reports/occupancy/pdf` e `GET /api/v1/reports/occupancy/excel` para realizarem os cruzamentos necessários no SQLite (`models.Allocation`, `models.Teacher`, `models.Room`) e repassarem a lista estruturada aos geradores de relatórios.
- **`tests/test_reports_api.py`**:
  - Incluídos testes unitários e de integração `test_generate_pdf_with_teacher_allocations` e `test_generate_excel_with_teacher_allocations`, validados com 100% de sucesso.
