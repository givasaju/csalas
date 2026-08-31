# Legacy Impact: Entrada de Alocação de Aulas (50 min) e Limite de 4 Aulas Consecutivas

> Identificador da feature: `008-alocacao-docente-max-4-aulas`  
> Data: `2026-08-08`  
> Âncora de contexto: Legado (`_reversa_sdd/architecture.md` + `_reversa_sdd/domain.md`)  

---

## 1. Arquivos Afetados e Impacto no Legado

| Arquivo afetado | Componente | Tipo | Severidade | Justificativa |
|-----------------|------------|------|------------|---------------|
| `src/models.py` | `academic-space-manager` | `delta-de-dados` | LOW | Adiciona o modelo ORM `Allocation` para persistência relacional das aulas. |
| `src/api/schemas.py` | `academic-space-manager` | `contrato-novo` | LOW | Adiciona os schemas Pydantic `AllocationCreate` e `AllocationResponse`. |
| `src/api/allocation_validator.py` | `academic-space-manager` | `componente-novo` | MEDIUM | Módulo do algoritmo de janela deslizante para cálculo de consecutividade. |
| `src/api/routes.py` | `academic-space-manager` | `contrato-novo` | MEDIUM | Endpoints REST `POST`, `GET` e `DELETE /api/v1/allocations`. |
| `src/engine/core.py` | `core-allocation-engine` | `regra-alterada` | HIGH | Incorpora a verificação de no máximo 4 aulas consecutivas por turno como Hard Constraint. |
| `src/api/static/index.html` | `occupancy-dashboard` | `componente-novo` | LOW | Adiciona a aba "🎓 Alocação de Aulas (50 min)" e o formulário interativo de sub-slots. |
| `src/api/static/index.css` | `occupancy-dashboard` | `componente-novo` | LOW | Adiciona estilos `.form-group`, `.form-control` e alertas visuais de trava de aulas. |

---

## 2. Diff Conceitual por Componente

### 2.1 academic-space-manager (`src/models.py`, `src/api/routes.py`, `src/api/allocation_validator.py`)
- **Resumo**: Foi introduzida a estrutura de dados e rotas REST para agendamento de aulas por sub-slots de 50 minutos. Tentativas de alocação que resultem na 5ª aula consecutiva para o mesmo docente no mesmo turno são bloqueadas com exceção `HTTP 409 Conflict`.

### 2.2 core-allocation-engine (`src/engine/core.py`)
- **Resumo**: O loop de alocação do motor de IA passou a verificar a trava de 4 aulas consecutivas por turno antes de confirmar a alocação de salas para uma turma docente.

### 2.3 occupancy-dashboard (`src/api/static/index.html` e `index.css`)
- **Resumo**: A interface gráfica foi expandida com uma aba dedicada ao agendamento de aulas de 50 minutos e tabela interativa de alocações ativas no campus.

---

## 3. Regras de Negócio Preservadas

- **RN-2.10 (Indisponibilidade Docente)**: A verificação de restrições horárias pré-cadastradas continua sendo executada em conjunto com a nova trava de consecutividade. 🟢
- **RN-3 (Segurança e Autenticação JWT)**: Todas as novas rotas em `/api/v1/allocations` exigem token Bearer válido. 🟢

---

## 4. Regras de Negócio Modificadas

Nenhuma regra legada foi revogada; a regra de restrição docente foi expandida para cobrir a trava de no máximo 4 aulas consecutivas no turno.
