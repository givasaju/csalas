# Adendo: UI Moderna de Entrada de Dados do ClassSync AI

> Identificador: `004-ui-entrada-dados`  
> Data: `2026-08-07`  
> Cenário: Legado  

---

## Vigência

Vigente desde 2026-08-07.
Superado pela re-extração de 2026-08-09.

---

## Resumo da entrega

Esta feature entregou a interface moderna de entrada de dados para o ClassSync AI. Foram implementadas 4 abas funcionais (Cadastrar Sala, Importação CSV, Restrições Docentes, Inventário de Salas) com formulários reativos, upload de arquivos por Drag and Drop com validação tudo-ou-nada (status 422), matriz interativa de indisponibilidade docente por slot de tempo, modal de reset semestral e suporte a feedback com Toasts animados. Foram concluídas 10 ações de 10 mapeadas.

---

## Impacto por artefato da extração

| Artefato | Seção | Tipo de impacto | Delta |
|----------|-------|-----------------|-------|
| `_reversa_sdd/architecture.md` | `# Componentes` | `regra-nova` | A SPA HTML/CSS foi expandida com formulários de entrada de dados e componentes reativos em JavaScript nativo sem dependências de frameworks. |
| `_reversa_sdd/domain.md` | `# Regras de Negócio` | `regra-nova` | Implementadas validações client-side e integrações com REST APIs para cadastro unitário (POST /api/v1/rooms), importação atômica em lote (POST /api/v1/rooms/import-csv) e gerenciamento de restrições (POST/DELETE /api/v1/allocation/restrictions). |

---

## Regras sob vigilância

Os watch items de regressão criados nesta feature estão registrados no seguinte arquivo:
* [regression-watch.md](file:///c:/csalas/_reversa_forward/004-ui-entrada-dados/regression-watch.md) (Watch IDs: `W001`, `W002`, `W003`)

---

## Fontes

- `_reversa_forward/004-ui-entrada-dados/requirements.md`
- `_reversa_forward/004-ui-entrada-dados/roadmap.md`
- `_reversa_forward/004-ui-entrada-dados/actions.md`
- `_reversa_forward/004-ui-entrada-dados/legacy-impact.md`
- `_reversa_forward/004-ui-entrada-dados/regression-watch.md`
