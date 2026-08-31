# Regression Watch: Realocação Departamental de Disciplinas por Novo Docente

> Identificador: `012-realocacao-disciplinas-dept`  
> Data: `2026-08-10`  

---

## 1. Regras Sob Vigilância de Regressão

| ID | Origem (arquivo, seção) | Regra esperada após mudança | Tipo de verificação | Sinal de violação |
|----|-------------------------|-----------------------------|---------------------|-------------------|
| W001 | `_reversa_sdd/domain.md#210-restricoes-de-indisponibilidade-docente` | A realocação de disciplinas é restrita a docentes do mesmo departamento (Iso-Department) | presença | Inclusão de disciplina de departamento distinto sem erro HTTP 422 |
| W002 | `_reversa_sdd/addenda/009-disciplinas-docentes.md` | O docente de origem não pode permanecer com 0 disciplinas sem indicação de `replacement_subject` | presença | Docente salvo com lista `subjects` vazia |
| W003 | `_reversa_sdd/addenda/009-disciplinas-docentes.md` | O docente de destino não pode ultrapassar o limite máximo de 6 disciplinas lecionáveis | presença | Docente receptor com mais de 6 disciplinas em `subjects` |
| W004 | `_reversa_sdd/addenda/011-disciplina-alocacao-aula.md` | As alocações vigentes das disciplinas transferidas devem ter seu `teacher_id` atualizado para o docente receptor | presença | Alocação da disciplina transferida permanecendo vinculada ao docente antigo |

---

## 2. Histórico de re-extrações

*(Esta seção será preenchida automaticamente quando uma nova re-extração `/reversa` for executada no futuro).*

---

## 3. Arquivadas

*(Nenhum item arquivado nesta versão).*
