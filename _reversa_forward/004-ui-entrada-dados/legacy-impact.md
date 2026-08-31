# Impacto no Legado: UI Moderna de Entrada de Dados do ClassSync AI

> Identificador: `004-ui-entrada-dados`  
> Data: `2026-08-07`  
> Âncora: Legado (`_reversa_sdd/architecture.md` + `_reversa_sdd/domain.md`)  

---

## Mapeamento de Impacto por Arquivo

| Arquivo afetado | Componente | Tipo | Severidade | Justificativa |
|-----------------|------------|------|------------|---------------|
| `src/api/static/index.html` | Frontend SPA | `regra-nova` | LOW | Adição de painéis de formulários para cadastro de sala, importação CSV, restrições e inventário |
| `src/api/static/index.css` | Design System CSS | `regra-nova` | LOW | Adição de estilos de formulários, drag-and-drop, matrizes e suporte a animações de Toast |
| `tests/test_ui_input_routes.py` | Testes de Integração | `regra-nova` | LOW | Adição de cobertura automatizada de rotas e interações de UI |

---

## Diff Conceitual por Componente

### Frontend SPA (`src/api/static/index.html`, `src/api/static/index.css`)
- **Antes:** O frontend possuía apenas o Dashboard principal de ocupação e visualização de leilões.
- **Depois:** Integração de 4 novas abas funcionais (Cadastrar Sala, Importação CSV, Restrições Docentes, Inventário de Salas) conectadas aos endpoints `/api/v1/rooms`, `/api/v1/rooms/import-csv` e `/api/v1/allocation/restrictions`.

---

## Regras Preservadas (Intactas)

- 🟢 **RF-001 / RN-001 (Alocação Inteligente):** O motor de otimização e leilões de créditos continua operando intacto.
- 🟢 **RN-002 (Validação de Capacidade):** As salas cadastradas ou importadas respeitam as restrições de tipo e acessibilidade.
- 🟢 **RN-003 (Política Tudo ou Nada no CSV):** A importação em lote mantém rejeição atômica status 422 em caso de erro.
- 🟢 **RN-004 (Reset Semestral):** Limpeza em lote de restrições via `DELETE /api/v1/allocation/restrictions` mantida intacta.

---

## Regras Modificadas

Nenhuma regra 🟢 de domínio legado foi removida ou violada. As alterações consistem em extensões não-destrutivas de interface de usuário.
