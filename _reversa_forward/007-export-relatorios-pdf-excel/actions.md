# Actions: Exportação de relatórios de ocupação das salas em PDF/Excel

> Identificador: `007-export-relatorios-pdf-excel`  
> Data: `2026-08-08`  
> Roadmap: `_reversa_forward/007-export-relatorios-pdf-excel/roadmap.md`  

---

## Resumo

| Métrica | Valor |
|---------|-------|
| Total de ações | 9 |
| Paralelizáveis (`[//]`) | 4 |
| Maior cadeia de dependência | 5 |

---

## Fase 1, Preparação

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T001 | Adicionar `reportlab` e `openpyxl` ao `requirements.txt` e criar scaffolding do módulo `src/api/reports.py` | - | `[//]` | `src/api/reports.py` | 🟢 | `[X]` |
| T002 | Criar fixtures de salas, alocações e turmas para os testes de relatórios | - | `[//]` | `tests/conftest.py` | 🟢 | `[X]` |

---

## Fase 2, Testes

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T003 | Criar testes automatizados integrados para as rotas `GET /api/v1/reports/occupancy/pdf` e `excel` | T001, T002 | `[//]` | `tests/test_reports_api.py` | 🟢 | `[X]` |

---

## Fase 3, Núcleo

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T004 | Implementar a compilação e renderização de PDF em estilo Impressão Limpa em `src/api/reports.py` | T001 | - | `src/api/reports.py` | 🟢 | `[X]` |
| T005 | Implementar a compilação e renderização de planilha Excel (.xlsx) com múltiplas abas em `src/api/reports.py` | T004 | - | `src/api/reports.py` | 🟢 | `[X]` |
| T006 | Implementar os endpoints REST `GET /api/v1/reports/occupancy/pdf` e `excel` em `src/api/routes.py` | T004, T005 | - | `src/api/routes.py` | 🟢 | `[X]` |

---

## Fase 4, Integração

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T007 | Integrar botões de exportação (PDF e Excel) com manipuladores de download Blob na SPA web | T006 | - | `src/api/static/index.html` | 🟢 | `[X]` |
| T008 | Adicionar estilos visuais para os botões de exportação e regras de impressão CSS | T007 | - | `src/api/static/index.css` | 🟢 | `[X]` |

---

## Fase 5, Polimento

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T009 | Adicionar logs estruturados para auditoria de download de relatórios | T006 | `[//]` | `src/api/routes.py` | 🟢 | `[X]` |

---

## Notas de execução

Nenhuma observação no momento.

---

## Histórico de alterações

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-08-08 | Versão inicial gerada por `/reversa-to-do` | reversa |
