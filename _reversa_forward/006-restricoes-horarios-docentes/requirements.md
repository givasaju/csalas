# Requirements: Gestão de Restrições de Horários por Professor e Alertas de Conflitos

> Identificador: `006-restricoes-horarios-docentes`  
> Data: `2026-08-08`  
> Pasta da extração reversa: `_reversa_sdd/`  
> Confidência: 🟢 CONFIRMADO, 🟡 INFERIDO, 🔴 LACUNA / DÚVIDA  

---

## 1. Resumo executivo

Esta feature implementa a gestão completa de restrições horárias de indisponibilidade docente e a detecção em tempo real de conflitos de alocação no ClassSync AI. Ela permite cadastrar, consultar e remover restrições de horários por professor, oferecendo suporte a reset semestral e emitindo alertas visuais e estruturados quando o motor de alocação de IA detectar turmas alocadas em slots bloqueados pelo docente.

---

## 2. Contexto a partir do legado

| Fonte | Trecho relevante | Confidência |
|-------|------------------|-------------|
| `_reversa_sdd/domain.md#2.10` | Validação de restrições de indisponibilidade docente (slots M1-N2, dias 1 a 7, unicidade por professor) | 🟢 |
| `_reversa_sdd/domain.md#2.5` | Realocação de turmas e mediação de conflitos de alocação no motor | 🟢 |
| `_reversa_sdd/addenda/005-cadastro-docentes.md#Resumo da entrega` | Cadastro e gestão de docentes via API e SPA (`models.Teacher`) | 🟢 |
| `_reversa_sdd/architecture.md#Componentes` | Backend FastAPI (`routes.py`) integrando com SQLAlchemy (`models.Restriction`) e SPA Web | 🟢 |

---

## 3. Personas e cenários de uso

| Persona | Objetivo | Cenário-chave |
|---------|----------|---------------|
| Coordenador Acadêmico | Cadastrar e gerenciar as indisponividades dos professores do departamento | Acessar a aba de docentes/restrições na interface web, definir os slots bloqueados do professor e salvar com validação imediata |
| Administrador do Sistema | Executar a limpeza semestral de restrições e acompanhar relatórios de alocação | Acionar a ação de reset semestral de restrições e visualizar alertas de conflitos de professores nas simulações de alocação |
| Motor de IA / Worker | Respeitar as restrições docentes durante o leilão e otimização predial | Consultar a lista consolidada de restrições antes de alocar a turma em um slot de horário |

---

## 4. Regras de negócio novas ou alteradas

1. **RN-01 (Validação de Slot e Dia):** O cadastro de restrições deve aceitar apenas dias da semana de 1 (Segunda) a 7 (Domingo) e slots `M1`, `M2`, `T1`, `T2`, `N1`, `N2`. 🟢
   - Origem no legado: `_reversa_sdd/domain.md#2.10`
   - Tipo: confirmada / mantida

2. **RN-02 (Impedimento de Restrição Duplicada):** Não é permitido cadastrar mais de uma restrição para o mesmo professor no mesmo dia da semana e mesmo slot de horário. Tentativas duplicadas devem retornar erro `409 Conflict`. 🟢
   - Origem no legado: `_reversa_sdd/domain.md#2.10`
   - Tipo: confirmada / mantida

3. **RN-03 (Bloqueio Rígido de Alocação em Slot Indisponível):** As restrições docentes atuam como *hard constraint* no motor de IA; turmas atreladas a um docente nunca serão alocadas em slots bloqueados por sua restrição horária. 🟢
   - Origem no legado: `_reversa_sdd/domain.md#2.10`
   - Tipo: confirmada / alinhada via clarify

4. **RN-04 (Exclusão Unitária de Restrição):** Deve ser possível remover uma restrição específica de um professor via `DELETE /api/v1/allocation/restrictions/{restriction_id}` sem efetuar a limpeza geral de todas as restrições do sistema. 🟡
   - Origem no legado: `_reversa_sdd/architecture.md#APIs`
   - Tipo: nova

5. **RN-05 (Bloqueio de Exclusão de Docente com Restrições):** A exclusão de docente (`DELETE /api/v1/teachers/{teacher_id}`) mantém a regra de segurança legada, proibindo a operação com `409 Conflict` enquanto existirem restrições cadastradas para o docente. 🟢
   - Origem no legado: `_reversa_sdd/domain.md#2.10` e `routes.py:146-150`
   - Tipo: confirmada / alinhada via clarify

---

## 5. Requisitos Funcionais

| ID | Requisito | Prioridade | Critério de aceite | Confidência |
|----|-----------|------------|--------------------|-------------|
| RF-01 | Cadastro unitário de restrições docentes via API e Web UI | Must | `POST /api/v1/allocation/restrictions` valida existência do professor, slot e dia, retornando `201 Created` | 🟢 |
| RF-02 | Listagem e consulta de restrições por professor | Must | `GET /api/v1/teachers/{teacher_id}/restrictions` retorna array de restrições ativas | 🟡 |
| RF-03 | Remoção de restrição específica por ID | Must | `DELETE /api/v1/allocation/restrictions/{restriction_id}` remove a restrição e retorna status `200 OK` | 🟡 |
| RF-04 | Reset semestral de todas as restrições | Should | `DELETE /api/v1/allocation/restrictions` limpa todas as indisponibilidades ativas e informa a quantidade removida | 🟢 |
| RF-05 | Respeito estrito (Hard Constraint) às restrições docentes pelo motor de IA | Must | Motor recusa alocação em slot bloqueado pelo docente e aciona realocação/pendência de mediação | 🟢 |
| RF-06 | Interface gráfica para gestão de grade horária de indisponibilidades | Should | Matriz reativa de dias (Seg-Dom) × slots (M1-N2) na página do professor com alteração por clique | 🟡 |

---

## 6. Requisitos Não Funcionais

| Tipo | Requisito | Evidência ou justificativa | Confidência |
|------|-----------|----------------------------|-------------|
| Desempenho | A verificação de conflitos de restrições durante a alocação de 100+ turmas deve executar em menos de 100ms | O processamento do motor roda em worker em background com pool de 2 threads (`_reversa_sdd/domain.md#2.11`) | 🟡 |
| Integridade | Erros de integridade referencial ao associar restrição a professor inexistente devem retornar `404 Not Found` | `_reversa_sdd/domain.md#2.10` e `routes.py:278` | 🟢 |
| Usabilidade | A grade visual na interface deve destacar claramente os horários bloqueados em vermelho/laranja e exibir contadores de alertas de conflito | Experiência de usuário reativa da SPA (`_reversa_sdd/addenda/005-cadastro-docentes.md`) | 🟡 |

---

## 7. Critérios de Aceitação

```gherkin
Cenário: Cadastro com sucesso de restrição horária para docente
  Dado que existe um professor com ID "prof-claudio" cadastrado no sistema
  Quando o usuário envia POST /api/v1/allocation/restrictions com dia_of_week=1 e time_slot_id="M1"
  Então a resposta deve ser 201 Created contendo o ID da restrição gerada
  E a restrição deve constar na listagem de indisponibilidades do professor

Cenário: Tentativa de cadastrar restrição para professor inexistente
  Dado que não existe docente com ID "prof-inexistente"
  Quando o usuário envia POST /api/v1/allocation/restrictions para este ID
  Então a API deve retornar erro 404 Not Found com a mensagem "Professor com ID prof-inexistente não encontrado."

Cenário: Garantia de Hard Constraint na alocação de turma em horário bloqueado pelo docente
  Dado que o professor "prof-isabela" possui restrição cadastrada na Terça (dia 2), slot T2
  E uma turma vinculada à "prof-isabela" tenta ser alocada na Terça, slot T2
  Quando o motor de alocação processa a grade
  Então o motor deve impedir a alocação no slot T2 e buscar uma sala/horário alternativo compatível
```

---

## 8. Prioridade MoSCoW

| Item | MoSCoW | Justificativa |
|------|--------|---------------|
| RF-01 (Cadastro unitário de restrição) | Must | Funcionalidade primária necessária para alimentar as indisponibilidades no backend |
| RF-02 (Consulta de restrições por professor) | Must | Necessário para renderizar a grade horária na interface web |
| RF-03 (Exclusão unitária de restrição) | Must | Permite ajustar indisponibilidades pontuais sem precisar limpar todo o banco |
| RF-05 (Hard Constraint no Motor de IA) | Must | Atende ao objetivo principal de não alocar docentes em slots indisponíveis |
| RF-04 (Reset semestral de restrições) | Should | Manutenção periódica da base de dados no início do período letivo |
| RF-06 (Grade interativa na Web UI) | Should | Melhora expressiva da experiência do usuário no dashboard web |

---

## 9. Esclarecimentos

### Sessão 2026-08-08

- **Q:** O motor de alocação de IA deve tratar o horário indisponível como bloqueio rígido (*hard constraint*) ou apenas penalizar a alocação com alerta (*soft constraint*)?  
  **R:** Bloqueio rígido (*hard constraint*): a turma nunca será alocada no slot de horário bloqueado pelo professor.

- **Q:** Como a API deve se comportar ao tentar excluir um docente (`DELETE /api/v1/teachers/{teacher_id}`) que possui restrições horárias vinculadas?  
  **R:** Manter regra de segurança: proibir a exclusão e retornar erro `409 Conflict` enquanto existirem restrições cadastradas.

---

## 10. Lacunas

Nenhuma lacuna pendente. Todas as dúvidas foram esclarecidas na sessão de 2026-08-08.

---

## 11. Histórico de alterações

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-08-08 | Versão inicial gerada por `/reversa-requirements` | reversa |
| 2026-08-08 | Dúvidas esclarecidas e integradas via `/reversa-clarify` | reversa |
