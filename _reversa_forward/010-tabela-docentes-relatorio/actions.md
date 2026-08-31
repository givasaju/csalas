# Actions: Tabela de Alocações por Docente no Relatório de Ocupação

> Identificador: `010-tabela-docentes-relatorio`  
> Data: `2026-08-09`  
> Roadmap: `_reversa_forward/010-tabela-docentes-relatorio/roadmap.md`  

---

## Resumo

| Métrica | Valor |
|---------|-------|
| Total de ações | 4 |
| Paralelizáveis (`[//]`) | 2 |
| Maior cadeia de dependência | 3 |

---

## Fase 1, Preparação

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T001 | Atualizar suíte de testes em `tests/test_reports_api.py` para validar a presença de docentes e disciplinas ordenados de A-Z nos relatórios PDF e Excel | - | `[//]` | `tests/test_reports_api.py` | 🟢 | `[x]` |

---

## Fase 2, Núcleo

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T002 | Atualizar `src/api/reports.py` para incluir a tabela "Ocupação por Docente (A-Z)" no PDF e a aba "Alocações por Docente" no Excel contendo Docente, Disciplinas, Sala, Turno e Subslot | T001 | - | `src/api/reports.py` | 🟢 | `[x]` |
| T003 | Atualizar rotas GET `/api/v1/reports/occupancy/pdf` e `/excel` em `src/api/routes.py` para consultar docentes e alocações no banco e repassar para os relatórios | T002 | `[//]` | `src/api/routes.py` | 🟢 | `[x]` |

---

## Fase 3, Polimento

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T004 | Executar suíte completa de testes automatizados com `pytest` garantindo 100% de sucesso nos relatórios | T003 | - | `tests/test_reports_api.py` | 🟢 | `[x]` |

---

## Notas de execução

Todas as ações concluídas e validadas via pytest com 100% de sucesso.

---

## Histórico de alterações

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-08-09 | Versão inicial gerada por `/reversa-to-do` | reversa |
| 2026-08-09 | Finalização de todas as ações T001 a T004 | reversa |
