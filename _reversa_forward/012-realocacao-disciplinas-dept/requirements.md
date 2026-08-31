# Requirements: Realocação Departamental de Disciplinas por Novo Docente

> Identificador: `012-realocacao-disciplinas-dept`
> Data: `2026-08-10`
> Pasta da extração reversa: `_reversa_sdd/`
> Confidência: 🟢 CONFIRMADO, 🟡 INFERIDO, 🔴 LACUNA / DÚVIDA

## 1. Resumo executivo

Esta feature introduz a capacidade de realocação e transferência de disciplinas lecionáveis entre docentes pertencentes ao **mesmo departamento acadêmico**. O objetivo é permitir que um docente recém-contratado assuma disciplinas previamente ministradas por outros professores do departamento, mantendo a integridade do rol de disciplinas, validação de restrições horárias e reatribuição de alocações vigentes.

## 2. Contexto a partir do legado

| Fonte | Trecho relevante | Confidência |
|-------|------------------|-------------|
| `_reversa_sdd/domain.md#210-restricoes-de-indisponibilidade-docente` | Cadastro e validação de docentes e indisponibilidades | 🟢 |
| `_reversa_sdd/addenda/009-disciplinas-docentes.md#resumo-da-entrega` | Rol de disciplinas lecionáveis por docente (`subjects` de 1 a 6 itens) e departamento (`department`) | 🟢 |
| `_reversa_sdd/addenda/011-disciplina-alocacao-aula.md#resumo-da-entrega` | Associação da disciplina (`subject`) na entidade `Allocation` vinculada ao docente | 🟢 |
| `_reversa_sdd/architecture.md#1-visao-geral-do-sistema` | Rotas REST FastAPI e validações Pydantic | 🟢 |

## 3. Personas e cenários de uso

| Persona | Objetivo | Cenário-chave |
|---------|----------|---------------|
| Coordenador de Departamento | Atribuir disciplinas ao novo professor contratado | Selecionar um novo docente do departamento e transferir disciplinas de um docente veterano para ele |
| Administrador Acadêmico | Reequilibrar carga horária do departamento | Visualizar o rol de disciplinas por departamento e realizar a realocação entre docentes do mesmo departamento |

## 4. Regras de negócio novas ou alteradas

1. **RN-01 (Validação de Departamento Homogêneo):** A realocação/transferência de disciplinas só é permitida entre docentes pertencentes ao **mesmo departamento** (`teacher_source.department == teacher_target.department`). Tentativas de transferência entre departamentos distintos devem ser rejeitadas com erro `422 Unprocessable Entity`. 🟢
   - Origem no legado: `_reversa_sdd/addenda/009-disciplinas-docentes.md`
   - Tipo: nova

2. **RN-02 (Respeito aos Limites do Rol e Substituição Obrigatória):** O docente de destino (`teacher_target`) pode ter no máximo 6 disciplinas em seu rol após a transferência. Caso a transferência deixe o docente de origem (`teacher_source`) com 0 disciplinas no rol, o sistema exige a indicação ou cadastro de uma nova disciplina substituta para o docente doador no momento da operação. 🟢
   - Origem no legado: `_reversa_sdd/domain.md#210-restricoes-de-indisponibilidade-docente`
   - Tipo: alterada

3. **RN-03 (Migração Automática de Alocações Vigentes):** Ao transferir uma disciplina, todas as alocações de horários existentes dessa matéria são migradas automaticamente para o novo docente de destino. 🟢
   - Origem no legado: `_reversa_sdd/addenda/011-disciplina-alocacao-aula.md`
   - Tipo: nova

4. **RN-04 (Tratamento de Conflito de Horário e Consecutividade):** Se a migração automática de uma alocação gerar conflito com a restrição de indisponibilidade ou limite de 4 aulas seguidas no mesmo turno do novo docente, essa alocação específica é sinalizada com status `"pending_arbitration"`. 🟢
   - Origem no legado: `_reversa_sdd/domain.md#25-realocacao-de-turmas-pos-derrota`
   - Tipo: nova

## 5. Requisitos Funcionais

| ID | Requisito | Prioridade | Critério de aceite | Confidência |
|----|-----------|------------|--------------------|-------------|
| RF-01 | Endpoint de realocação de disciplinas entre docentes do mesmo departamento | Must | `POST /api/v1/teachers/reallocate-subjects` aceita `source_teacher_id`, `target_teacher_id`, `subjects` e opcional `replacement_subject`. Valida pertencimento ao mesmo departamento. | 🟢 |
| RF-02 | Validação de limites e exigência de substituta para o doador | Must | Impede que o docente doador fique com 0 disciplinas exigindo `replacement_subject`, e limita o receptor a no máximo 6 disciplinas. | 🟢 |
| RF-03 | Migração automática de alocações vigentes com arbitragem em conflito | Must | Atualiza `teacher_id` nas alocações vigentes das disciplinas transferidas, atribuindo status `"pending_arbitration"` se houver conflito de horário/turno. | 🟢 |
| RF-04 | Modal de transferência rápida na SPA | Should | Adicionar modal rápido na SPA permitindo filtrar departamento, docente de origem, docente de destino e selecionar disciplinas com campo de disciplina substituta se necessário. | 🟢 |

## 6. Requisitos Não Funcionais

| Tipo | Requisito | Evidência ou justificativa | Confidência |
|------|-----------|----------------------------|-------------|
| Desempenho | Operação de realocação atômica em menos de 300ms | A alteração de rol e atualização de alocações em memória/banco deve executar de forma síncrona transacional. | 🟢 |
| Integridade | Consistência de Departamento (Iso-Department) | Nenhum docente pode receber disciplinas de departamentos distintos ao seu sem atualização explícita de departamento. | 🟢 |
| Observabilidade | Log de auditoria de realocação | Registrar log estruturado `[SUBJECT_REALLOCATION]` contendo departamento, origem, destino e disciplinas migradas. | 🟢 |

## 7. Critérios de Aceitação

```gherkin
Cenário: Realocação bem-sucedida de disciplina para novo docente do mesmo departamento
  Dado que o docente "prof-veterano" e o docente "prof-novo" pertencem ao departamento "Computação"
  E que "prof-veterano" possui as disciplinas ["Banco de Dados", "Compiladores"]
  E que "prof-novo" possui a disciplina ["Algoritmos"]
  Quando a coordenação solicita a transferência da disciplina "Compiladores" de "prof-veterano" para "prof-novo"
  Então o sistema atualiza o rol de "prof-novo" para ["Algoritmos", "Compiladores"]
  E atualiza o rol de "prof-veterano" para ["Banco de Dados"]
  E reatribui todas as alocações da disciplina "Compiladores" para "prof-novo"
  E retorna HTTP status 200 OK

Cenário: Realocação de todas as disciplinas com fornecimento de disciplina substituta
  Dado que o docente "prof-veterano" possui apenas a disciplina ["Cálculo I"]
  Quando a coordenação transfere "Cálculo I" para "prof-novo" informando a disciplina substituta "Álgebra Linear"
  Então o rol de "prof-veterano" passa a ser ["Álgebra Linear"]
  E a disciplina "Cálculo I" é atribuída a "prof-novo" com sucesso

Cenário: Rejeição de realocação entre docentes de departamentos diferentes
  Dado que o docente "prof-eng" pertence ao departamento "Engenharia"
  E que o docente "prof-mat" pertence ao departamento "Matemática"
  Quando o usuário tenta transferir a disciplina "Cálculo I" de "prof-mat" para "prof-eng"
  Então o sistema recusa a transferência
  E retorna HTTP status 422 Unprocessable Entity com a mensagem "Realocação permitida apenas entre docentes do mesmo departamento"
```

## 8. Prioridade MoSCoW

| Item | MoSCoW | Justificativa |
|------|--------|---------------|
| RF-01 (Endpoint de realocação no mesmo departamento) | Must | Funcionalidade core exigida para integrar recém-contratados |
| RF-02 (Validação de limites e disciplina substituta) | Must | Preserva regra mandatória de negócio do cadastro de docentes |
| RF-03 (Migração automática de alocações vigentes) | Must | Mantém a grade de aulas consistente e sinaliza conflitos imediatamente |
| RF-04 (Modal de transferência rápida na SPA) | Should | Melhora a usabilidade da coordenação para realizar trocas visuais |
| RNF de Integridade de Departamento | Must | Impede inconsistência cadastral entre docentes e áreas |

## 9. Esclarecimentos

### Sessão 2026-08-10

- **Q:** Ao transferir uma disciplina para o novo docente contratado, como devem ser tratadas as alocações de horários já existentes no calendário?
  **R:** Migrar automaticamente as alocações existentes para o novo docente, sinalizando como 'pending_arbitration' caso ocorra conflito horário ou de aulas seguidas.
- **Q:** Como tratar o docente de origem (doador) caso ele repasse todas as suas disciplinas para o novo contratado?
  **R:** Solicitar o cadastro de uma nova disciplina substituta para o docente doador durante a transferência.
- **Q:** Qual deve ser o modelo visual na interface web (SPA) para realizar a realocação de disciplinas?
  **R:** Modal de transferência rápida na SPA com seleção de departamento, docente de origem, docente de destino e disciplinas.

## 10. Lacunas

> Nenhuma lacuna ou dúvida pendente.

## 11. Histórico de alterações

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-08-10 | Versão inicial gerada por `/reversa-requirements` | reversa |
| 2026-08-10 | Dúvidas esclarecidas e integradas via `/reversa-clarify` | reversa |
