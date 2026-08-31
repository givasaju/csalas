# Impacto no Legado: Gestão de Restrições de Horários por Professor e Alertas de Conflitos

> Identificador: `006-restricoes-horarios-docentes`  
> Data: `2026-08-08`  

---

## 1. Mapeamento de Arquivos Tocados

| Arquivo afetado | Componente (`_reversa_sdd/architecture.md`) | Tipo | Severidade | Justificativa |
|-----------------|---------------------------------------------|------|------------|---------------|
| `src/api/routes.py` | API REST / Router | `contrato-alterado` | MEDIUM | Adição de endpoints GET por docente e DELETE por ID de restrição |
| `src/engine/core.py` | Motor de Alocação (Core Engine) | `regra-alterada` | HIGH | Incorporação de Hard Constraint para rejeitar alocações em slots indisponíveis |
| `src/api/static/index.html` | SPA Web Dashboard | `componente-novo` | LOW | Interface visual de matriz de indisponibilidade docente |

---

## 2. Diff Conceitual por Componente

### API REST (`src/api/routes.py`)
Expansão dos contratos da API para suportar consulta por docente (`GET /api/v1/teachers/{teacher_id}/restrictions`) e remoção pontual (`DELETE /api/v1/allocation/restrictions/{restriction_id}`).

### Motor de IA (`src/engine/core.py`)
No ciclo de alocação inicial, o motor agora valida se a turma em processamento possui restrição docente para o dia/slot. Caso positivo, impede a atribuição da sala/slot e encaminha a turma para pendência/realocação alternativa.

---

## 3. Regras de Negócio Preservadas

- `_reversa_sdd/domain.md#2.10`: Validação de dias da semana (1-7) e slots `M1-N2` com retorno `422`.
- `_reversa_sdd/domain.md#2.10`: Proibição de restrições duplicadas para o mesmo professor no mesmo dia/slot (`409 Conflict`).
- `_reversa_sdd/domain.md#2.10`: Reset semestral limpando todas as indisponividades (`DELETE /api/v1/allocation/restrictions`).

---

## 4. Regras de Negócio Modificadas

- `_reversa_sdd/domain.md#2.10`: Adicionado comportamento de Hard Constraint no motor de IA para recusar alocações em slots de professores indisponíveis.
