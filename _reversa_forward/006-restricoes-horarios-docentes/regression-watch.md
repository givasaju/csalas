# Regression Watch: Gestão de Restrições de Horários por Professor

> Identificador: `006-restricoes-horarios-docentes`  
> Data: `2026-08-08`  

---

## 1. Itens sob Vigilância de Regressão

| ID | Origem (arquivo, seção) | Regra esperada após mudança | Tipo de verificação | Sinal de violação |
|----|-------------------------|-----------------------------|---------------------|-------------------|
| W001 | `_reversa_sdd/domain.md#2.10` | Motor de IA recusa alocação de turma em slot bloqueado pelo professor (Hard Constraint) | presença | Turma alocada com sucesso em sala no horário indisponível do seu docente |
| W002 | `_reversa_sdd/domain.md#2.10` | API `GET /api/v1/teachers/{teacher_id}/restrictions` retorna array de restrições do docente | presença | Erro 404/500 ao consultar restrições de docente existente |
| W003 | `_reversa_sdd/domain.md#2.10` | API `DELETE /api/v1/allocation/restrictions/{id}` remove restrição isolada | presença | Remoção de restrição por ID falhando ou deletando todas as restrições indevidamente |

---

## 2. Histórico de re-extrações

*Nenhuma re-extração executada após esta entrega.*

---

## 3. Arquivadas

*Nenhum item arquivado.*
