# Adendo: Exportação de relatórios de ocupação das salas em PDF/Excel

> Identificador: `007-export-relatorios-pdf-excel`  
> Data: `2026-08-08`  
> Cenário: Legado  

---

## Vigência

Vigente desde 2026-08-08.
Superado pela re-extração de 2026-08-09.

---

## Resumo da entrega

Esta feature entregou a funcionalidade de exportação de relatórios consolidados de ocupação de salas nos formatos PDF e Excel (XLSX). Ela permite que diretores de infraestrutura e coordenadores acadêmicos gerem documentos formatados para impressão limpa ou planilhas analíticas filtradas por bloco predial ou turno. Foram concluídas 9 ações de 9 mapeadas no pipeline TDD.

---

## Impacto por artefato da extração

| Artefato | Seção | Tipo de impacto | Delta |
|----------|-------|-----------------|-------|
| `_reversa_sdd/architecture.md` | `#1.-visao-geral-do-sistema` | `contrato-novo` | Expõe endpoints REST `GET /api/v1/reports/occupancy/pdf` e `excel` em `src/api/routes.py`. |
| `_reversa_sdd/architecture.md` | `#1.-visao-geral-do-sistema` | `componente-novo` | Adiciona o módulo `src/api/reports.py` para geração de relatórios em memória (PDF/XLSX). |
| `_reversa_sdd/painel-ocupacao/requirements.md` | `#visão-geral` | `componente-novo` | Adiciona botões de exportação "Exportar PDF" e "Exportar Excel" na barra de ações da SPA em `src/api/static/index.html`. |
| `_reversa_sdd/domain.md` | `#3.-seguranca-e-autenticacao` | `regra-nova` | Aplica validação de token JWT para autorizar o download dos relatórios. |

---

## Regras sob vigilância

Os watch items de regressão criados nesta feature estão registrados no seguinte arquivo:
* [regression-watch.md](file:///c:/csalas/_reversa_forward/007-export-relatorios-pdf-excel/regression-watch.md) (Watch IDs: `W001`, `W002`, `W003`)

---

## Fontes

- `_reversa_forward/007-export-relatorios-pdf-excel/requirements.md`
- `_reversa_forward/007-export-relatorios-pdf-excel/roadmap.md`
- `_reversa_forward/007-export-relatorios-pdf-excel/legacy-impact.md`
- `_reversa_forward/007-export-relatorios-pdf-excel/regression-watch.md`
