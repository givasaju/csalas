# Legacy Impact: Implementar o gerenciador acadêmico academic-space-manager

> Data: `2026-08-07`  
> Identificador: `002-implementar-space-manager`  
> Tipo: Feature greenfield, sem legado pré-existente. Âncora: prd.md + specs SDD.  

---

## 1. Arquivos Criados e Mapeamento de Componentes

| Arquivo Criado | Componente Spec | Tipo de Impacto | Severidade | Justificativa |
|----------------|-----------------|-----------------|------------|---------------|
| `src/api/schemas.py` | `academic-space-manager` | `componente-novo` | LOW | Modelos Pydantic de validação dos payloads das rotas de salas e restrições. |
| `src/api/routes.py` | `academic-space-manager` | `componente-novo` | HIGH | Implementação de rotas FastAPI CRUD de salas, importação CSV, indisponibilidades e reset. |
| `tests/test_api_rooms.py` | `academic-space-manager` | `componente-novo` | MEDIUM | Testes integrados de validação das APIs de gerenciamento físico de salas. |
| `tests/test_api_csv.py` | `academic-space-manager` | `componente-novo` | MEDIUM | Testes integrados de validação da importação CSV sob política Tudo ou Nada. |
| `tests/test_api_restrictions.py` | `academic-space-manager` | `componente-novo` | MEDIUM | Testes integrados das lógicas de restrição e reset de indisponibilidades. |

---

## 2. Diff Conceitual por Componente

*   **academic-space-manager:** Criação de todo o subsistema de gerenciamento do inventário de salas do campus e restrições docentes, com integridade concorrente sob transações Tudo ou Nada para CSV.

---

## 3. Preservadas

*   N/A (Nenhuma regra ou código existente alterado; feature greenfield).

---

## 4. Modificadas

*   N/A (Nenhuma regra ou código existente alterado; feature greenfield).
