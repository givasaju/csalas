# Roadmap: Tabela de Alocações por Docente no Relatório de Ocupação

> Identificador: `010-tabela-docentes-relatorio`  
> Data: `2026-08-09`  
> Requirements: `_reversa_forward/010-tabela-docentes-relatorio/requirements.md`  

---

## 1. Arquitetura da solução

Expandir as funções de geração de relatório em `src/api/reports.py` (`generate_pdf_report` e `generate_excel_report`) e a rota de montagem de dados em `src/api/routes.py` para incluir a listagem consolidada de docentes, suas disciplinas lecionáveis, a sala física ocupada, o turno e o sub-slot da aula, ordenada alfabeticamente pelo nome do docente.

---

## 2. Componentes afetados

1. `src/api/reports.py`:
   - Atualizar a assinatura de `filter_data`, `generate_pdf_report` e `generate_excel_report` para aceitar a lista de docentes e alocações detalhadas.
   - Adicionar geração da Seção 3 ("Ocupação por Docente (Ordem A-Z)") no PDF utilizando ReportLab.
   - Adicionar geração da Aba 3 ("Alocações por Docente") na planilha Excel utilizando OpenPyXL.
2. `src/api/routes.py`:
   - Atualizar as rotas `GET /api/v1/reports/occupancy/pdf` e `GET /api/v1/reports/occupancy/excel` para consultar docentes e alocações no banco SQLite (`models.Teacher`, `models.Allocation`, `models.Room`) e repassar aos relatórios.
3. `tests/test_reports_api.py`:
   - Adicionar suíte de testes verificando a presença da nova tabela/aba de docentes em ordem A-Z nos relatórios PDF e Excel.

---

## 3. Matriz de Rastreabilidade

| Requisito | Ação Técnica | Arquivo afetado |
|-----------|--------------|-----------------|
| RF-01 | Implementar tabela de docentes A-Z no PDF | `src/api/reports.py` |
| RF-02 | Implementar aba de docentes A-Z no Excel | `src/api/reports.py` |
| RF-03 | Buscar e cruzar dados de alocações e docentes nas rotas REST | `src/api/routes.py` |
