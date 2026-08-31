# Impacto no Legado: Realocação Departamental de Disciplinas por Novo Docente

> Identificador: `012-realocacao-disciplinas-dept`  
> Data: `2026-08-10`  
> Cenário: Legado (âncora em `_reversa_sdd/architecture.md` e `domain.md`)  

---

## 1. Resumo do Impacto nos Arquivos

| Arquivo afetado | Componente | Tipo | Severidade | Justificativa |
|-----------------|------------|------|------------|---------------|
| `src/api/schemas.py` | `academic-space-manager` | `contrato-novo` | LOW | Adiciona schemas Pydantic `ReallocateSubjectsRequest` e `ReallocateSubjectsResponse`. |
| `src/api/routes.py` | `academic-space-manager` | `regra-nova` / `contrato-novo` | HIGH | Implementa endpoint `POST /api/v1/teachers/reallocate-subjects` com validação de departamento e migração de alocações. |
| `src/api/static/index.html` | `painel-ocupacao` | `componente-novo` | MEDIUM | Adiciona botão e modal de realocação departamental de disciplinas na SPA web. |
| `tests/test_api_reallocate_subjects.py` | `academic-space-manager` | `componente-novo` | LOW | Adiciona testes automatizados TDD para o contrato de realocação. |

---

## 2. Diff Conceitual por Componente

### Academic Space Manager (`src/api/routes.py` e `src/api/schemas.py`)
Adicionado contrato de API `POST /api/v1/teachers/reallocate-subjects` que permite transferir disciplinas entre docentes do mesmo departamento. O componente valida estritamente se `source_teacher.department == target_teacher.department` (rejeitando com erro HTTP `422 Unprocessable Entity` se forem de departamentos distintos). Valida também a exigência de uma disciplina substituta (`replacement_subject`) para impedir que o docente doador fique com 0 matérias, e limita o docente receptor a no máximo 6 disciplinas no rol. Alocações ativas vinculadas às disciplinas transferidas têm seu `teacher_id` atualizado para o docente de destino.

### Painel de Ocupação (`src/api/static/index.html`)
Adicionado o Modal `#reallocateModal` com seleção dinâmica de departamento, docente doador, docente de destino e checklist de disciplinas. Permite que coordenadores efetuem realocações rapidamente através da interface visual da SPA.

---

## 3. Regras Preservadas

As seguintes regras de negócio confirmadas do legado continuam intactas:
- **`domain.md#28-restricao-de-cadastro-de-salas-duplicadas`**: Permanece inalterada.
- **`domain.md#27-importacao-transacional-de-salas-tudo-ou-nada`**: Permanece inalterada.
- **`domain.md#29-bloqueio-de-exclusao-de-salas-em-execucao`**: Permanece inalterada.
- **`domain.md#3-seguranca-e-autenticacao`**: Validação Bearer JWT mantida rigorosamente no novo endpoint.

---

## 4. Regras Modificadas

- **`domain.md#210-restricoes-de-indisponibilidade-docente`** / **Adendo 009**: O rol de disciplinas do docente continua exigindo de 1 a 6 disciplinas. A regra foi alterada para permitir a transferência entre docentes do mesmo departamento, adicionando a exigência de uma disciplina substituta caso a transferência esvazie o rol do docente doador.
