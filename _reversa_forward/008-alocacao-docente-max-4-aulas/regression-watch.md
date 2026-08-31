# Regression Watch: Entrada de Alocação de Aulas (50 min) e Limite de 4 Aulas Consecutivas

> Identificador da feature: `008-alocacao-docente-max-4-aulas`  
> Data de criação: `2026-08-08`  

---

## 1. Watch Items de Regressão

| ID | Origem (arquivo, seção) | Regra esperada após mudança | Tipo de verificação | Sinal de violação |
|----|-------------------------|-----------------------------|---------------------|-------------------|
| W001 | `_reversa_forward/008-alocacao-docente-max-4-aulas/requirements.md#RN-02` | Tentativas de alocação que resultem em 5 ou mais aulas consecutivas no mesmo turno para o docente devem ser rejeitadas com erro HTTP 409 Conflict | presença | Aceitação de 5 ou mais aulas seguidas no mesmo turno sem exceção |
| W002 | `_reversa_forward/008-alocacao-docente-max-4-aulas/requirements.md#RF-01` | Rota `POST /api/v1/allocations` deve persistir a alocação de aula de 50 min e retornar HTTP 201 Created para até 4 aulas seguidas | presença | Falha ou recusa em alocar a 4ª aula consecutiva no turno |
| W003 | `_reversa_forward/008-alocacao-docente-max-4-aulas/requirements.md#RF-03` | O motor de alocação de IA em `core.py` deve tratar o limite de 4 aulas seguidas por turno como Hard Constraint mandatória | presença | Alocação de turmas pela IA violando o limite de 4 aulas seguidas |

---

## 2. Histórico de re-extrações

*Nenhuma re-extração registrada ainda.*

---

## 3. Arquivadas

*Nenhum item arquivado.*

---

## 4. Observações

- A verificação de consecutividade é realizada por turno (`M`, `T`, `N`) em uma janela de 5 sub-slots de 50 minutos.
