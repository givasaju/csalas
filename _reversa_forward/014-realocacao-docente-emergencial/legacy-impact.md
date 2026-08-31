# Legacy Impact: Realocação Docente Emergencial

> Identificador: `014-realocacao-docente-emergencial`
> Data: `2026-08-13`
> Requirements: `_reversa_forward/014-realocacao-docente-emergencial/requirements.md`

---

## 1. Mapeamento de Arquivos Tocados x Componentes do Legado

| Arquivo afetado | Componente | Tipo de impacto | Severidade | Justificativa |
|-----------------|------------|-----------------|------------|---------------|
| `src/engine/core.py` | `core-allocation-engine` | `regra-nova` | LOW | Adição do método `calculate_emergency_reallocation` sem alterar os métodos existentes |
| `src/api/schemas.py` | `academic-space-manager` | `regra-nova` | LOW | Schemas Pydantic adicionados para request/response de realocação emergencial |
| `src/api/worker.py` | `academic-space-manager` | `regra-nova` | LOW | Estrutura de persistência e gravação de logs de auditoria emergencial |
| `src/api/routes.py` | `academic-space-manager` | `delta-de-contrato-externo` | LOW | Novos endpoints REST `/emergency-reallocations/calculate` e `/commit` |
| `src/api/static/index.html` | `occupancy-dashboard` | `componente-novo` | LOW | Nova aba de navegação e modal de homologação em Modo Assistido vs. Modo Delegado |
| `db/migrations.sql` | `academic-space-manager` | `delta-de-dados` | LOW | Criação das tabelas `emergency_reallocation_logs` e `emergency_reallocation_details` |

---

## 2. Diff Conceitual por Componente

### `core-allocation-engine`
- Adicionada capacidade de cálculo emergencial isolado para cobrir licenças médicas sem refazer a alocação completa do campus.
- Ranqueamento por menor impacto mantido e expansão de busca para docentes de coordenações correlatas habilitada.

### `academic-space-manager`
- Exposição das rotas REST de cálculo e efetivação de realocação emergencial.
- Persistência estruturada em log de auditoria com data, responsável, modo de homologação (assistido vs. delegado) e detalhamento de substitutos.

### `occupancy-dashboard`
- Interface visual intuitiva integrada ao dashboard de ocupação, com alternância simples de modo de operação para a coordenação.

---

## 3. Regras Preservadas no Legado

- 🟢 **RN-AlocacaoInicial:** Permanece intocada em `src/engine/core.py` (AAC).
- 🟢 **RN-LeilaoCooperativo:** Permanece intocada em `src/engine/core.py` (`ACC`/`AMR`).
- 🟢 **RN-ConsolidacaoPredial:** Permanece intocada em `src/engine/optimization.py` (`BuildingOptimizer`).
- 🟢 **RN-ValidaçãoRestrições:** Restrições horárias dos docentes continuam sendo verificadas em O(1) via `is_teacher_restricted`.

---

## 4. Regras Modificadas no Legado

- 🟢 Nenhum comportamento ou regra pré-existente no legado foi quebrada ou alterada destructivamente. Todas as modificações foram aditivas.
