# Requirements: Entrada de Alocação de Aulas Docentes (50 min) e Limite de 4 Aulas Consecutivas

> Identificador: `008-alocacao-docente-max-4-aulas`
> Data: `2026-08-08`
> Pasta da extração reversa: `_reversa_sdd/`
> Confidência: 🟢 CONFIRMADO, 🟡 INFERIDO, 🔴 LACUNA / DÚVIDA

## 1. Resumo executivo

Esta feature estabelece a interface de entrada de dados para agendamento e alocação de aulas de professores em salas físicas, definindo a duração padrão de 50 minutos por aula (mapeadas em até 5 aulas de 50 minutos por slot). Ela introduz a regra de negócio rígida (*hard constraint*) de ergonomia docente que limita a no máximo 4 aulas seguidas (consecutivas) para um mesmo professor dentro de um mesmo turno (Manhã, Tarde ou Noite), prevenindo sobrecarga de ensino e garantindo conformidade regulatória acadêmica no motor de IA e na API REST.

## 2. Contexto a partir do legado

| Fonte | Trecho relevante | Confidência |
|-------|------------------|-------------|
| `_reversa_sdd/architecture.md#1.-visao-geral-do-sistema` | O `academic-space-manager` gerencia cadastros, turmas e alocações de salas via FastAPI. | 🟢 |
| `_reversa_sdd/domain.md#2.10-restricoes-de-indisponibilidade-docente` | Cadastro e validação de disponibilidade e slots horários dos professores. | 🟢 |
| `_reversa_sdd/addenda/006-restricoes-horarios-docentes.md#resumo-da-entrega` | O motor de alocação (`core.py`) valida restrições docentes como Hard Constraints. | 🟢 |
| `_reversa_sdd/domain.md#1.-glossario-de-termos` | Definição de slots de horário acadêmicos (`M1`, `M2`, `T1`, `T2`, `N1`, `N2`). | 🟢 |

## 3. Personas e cenários de uso

| Persona | Objetivo | Cenário-chave |
|---------|----------|---------------|
| Cláudio (Coordenador de Curso) | Cadastrar o agendamento de aulas de um docente em determinada sala e período de 50 minutos. | Cláudio seleciona o professor, a sala física e os períodos de aula de 50 min na interface e salva a alocação. |
| Isabela (Diretora de Infraestrutura) | Garantir que nenhum professor seja alocado com mais de 4 aulas seguidas no mesmo turno. | O motor de alocação recusa automaticamente tentativas de alocação que gerem a 5ª aula consecutiva para o docente no turno. |

## 4. Regras de negócio novas ou alteradas

1. **RN-01: Duração Padrão do Período de Aula** 🟢
   - Origem no legado: N/A (nova)
   - Tipo: nova
   - Cada período de aula cadastrado possui duração nominal de 50 minutos. Cada slot principal do legado mapeia até 5 sub-períodos/aulas de 50 minutos.

2. **RN-02: Limite Rígido de Aulas Consecutivas por Turno (Max 4 Aulas Seguidas)** 🟢
   - Origem no legado: `_reversa_sdd/domain.md#2.10-restricoes-de-indisponibilidade-docente`
   - Tipo: alterada
   - É proibido alocar mais de 4 aulas consecutivas (seguidas) para um mesmo professor dentro do mesmo turno (Manhã, Tarde ou Noite). A tentativa de cadastrar a 5ª aula seguida no mesmo turno gera erro `409 Conflict` na API e bloqueio no motor de IA.

3. **RN-03: Validação de Conflito de Sala e Horário** 🟢
   - Origem no legado: `_reversa_sdd/domain.md#2.8-restricao-de-cadastro-de-salas-duplicadas`
   - Tipo: alterada
   - Uma mesma sala física não pode ser ocupada por mais de uma turma/professor no mesmo período de 50 minutos.

4. **RN-04: Autenticação das Operações de Agendamento** 🟢
   - Origem no legado: `_reversa_sdd/domain.md#3.-seguranca-e-autenticacao`
   - Tipo: preservada
   - Todas as operações de entrada de dados de alocação requerem o cabeçalho `Authorization: Bearer <token>` válido.

## 5. Requisitos Funcionais

| ID | Requisito | Prioridade | Critério de aceite | Confidência |
|----|-----------|------------|--------------------|-------------|
| RF-01 | Formulário e endpoint REST `POST /api/v1/allocations` para entrada de dados de aula (professor, sala, dia e sub-período de 50 min). | Must | Receber payload com `teacher_id`, `room_id`, `day_of_week`, `shift` e `sub_slot` (1..5), persistindo a alocação. | 🟢 |
| RF-02 | Validação de limite de no máximo 4 aulas seguidas no mesmo turno para um docente. | Must | Retornar erro `409 Conflict` quando a requisição resultar em >4 aulas consecutivas para o docente no turno. | 🟢 |
| RF-03 | Integração da validação de limite de 4 aulas seguidas por turno no motor de IA (`core.py`). | Must | O loop de alocação de IA deve considerar o limite por turno de 4 aulas seguidas como Hard Constraint inviolável. | 🟢 |
| RF-04 | Interface web (SPA) para formulário interativo de agendamento de aulas por professor. | Must | Disponibilizar aba ou modal no `occupancy-dashboard` permitindo selecionar docente, sala e sub-períodos de 50 min por turno. | 🟢 |
| RF-05 | Exibição de alertas visuais no frontend ao atingir 4 aulas seguidas no turno. | Should | Destacar visualmente na UI que o docente atingiu o limite de 4 aulas contínuas no turno. | 🟢 |

## 6. Requisitos Não Funcionais

| Tipo | Requisito | Evidência ou justificativa | Confidência |
|------|-----------|----------------------------|-------------|
| Desempenho | A verificação de consecutividade de aulas docentes por turno deve ser executada em menos de 10ms por requisição. | Rationale de performance em `_reversa_sdd/architecture.md#4.4` | 🟢 |
| Usabilidade | O formulário deve impedir a submissão no frontend caso mais de 4 períodos consecutivos sejam marcados no mesmo turno. | Rationale de experiência de usuário | 🟢 |
| Confiabilidade | Falhas na validação não devem corromper alocações previamente confirmadas. | Evidência em `_reversa_sdd/domain.md#2.7` | 🟢 |

## 7. Critérios de Aceitação

```gherkin
Cenário: Agendamento bem-sucedido de até 4 aulas seguidas para um professor no mesmo turno
  Dado que o professor "prof-01" possui 3 aulas consecutivas agendadas no turno da Manhã
  Quando o coordenador cadastra a 4ª aula consecutiva para "prof-01" no mesmo turno
  Então a API responde com status 201 Created
  E a alocação da aula é confirmada no sistema.

Cenário: Rejeição ao tentar cadastrar a 5ª aula seguida para o mesmo professor no mesmo turno
  Dado que o professor "prof-01" já possui 4 aulas consecutivas agendadas no turno da Manhã
  Quando o coordenador tenta agendar a 5ª aula no mesmo turno
  Então a API recusa a requisição com status 409 Conflict
  E exibe a mensagem "Limite máximo de 4 aulas seguidas no mesmo turno atingido para o docente."

Cenário: Rejeição por conflito de sala física ocupada
  Dado que a sala "A101" já está ocupada na aula 1 do turno Manhã em uma segunda-feira
  Quando outro agendamento é solicitado para a sala "A101" na mesma aula e turno
  Então o sistema retorna erro 409 Conflict.
```

## 8. Prioridade MoSCoW

| Item | MoSCoW | Justificativa |
|------|--------|---------------|
| RF-01 | Must | Requisito base de entrada de dados de alocação de aula. |
| RF-02 | Must | Regra crítica para limitar no máximo 4 aulas seguidas por turno. |
| RF-03 | Must | Garantir que o motor autônomo de IA respeite a Hard Constraint por turno. |
| RF-04 | Must | Interface de entrada para coordenadores no dashboard web. |
| RF-05 | Should | Alerta preventivo na UI melhora a usabilidade e previne erros humanos. |

## 9. Esclarecimentos

### Sessão 2026-08-08

- **Q:** Como os períodos de aula de 50 minutos se correlacionam com a estrutura de horários?  
  **R:** Cada slot principal do legado representa 5 sub-períodos/aulas de 50 minutos.
- **Q:** Como deve ser aplicado o limite de até 4 aulas seguidas para o mesmo professor?  
  **R:** Limite por turno: Máximo de 4 aulas seguidas dentro do mesmo turno (Manhã, Tarde ou Noite).

## 10. Lacunas

Nenhuma lacuna pendente nesta versão.

## 11. Histórico de alterações

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-08-08 | Versão inicial gerada por `/reversa-requirements` | reversa |
| 2026-08-08 | Resolução de dúvidas via `/reversa-clarify` (mapeamento 5 aulas por slot e limite por turno) | reversa |
