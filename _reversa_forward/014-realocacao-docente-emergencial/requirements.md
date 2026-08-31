# Requirements: Realocação Docente Emergencial

> Identificador: `014-realocacao-docente-emergencial`
> Data: `2026-08-13`
> Pasta da extração reversa: `_reversa_sdd/`
> Confidência: 🟢 CONFIRMADO, 🟡 INFERIDO, 🔴 LACUNA / DÚVIDA

## 1. Resumo executivo

Permite à coordenação acadêmica gerenciar afastamentos não planejados de professores (licenças de saúde, cursos, aposentadorias) durante o período letivo de forma emergencial. A solução gera alternativas automatizadas de realocação de disciplinas e horários por meio do motor de IA (`core-allocation-engine`), oferecendo ao coordenador um modo duplo de operação no `occupancy-dashboard`: seleção assistida de alternativas ou delegação para homologação automática pelo agente de IA.

## 2. Contexto a partir do legado

| Fonte | Trecho relevante | Confidência |
|-------|------------------|-------------|
| `_reversa_sdd/architecture.md#1.1-módulos-principais` | Estrutura dos módulos `core-allocation-engine`, `academic-space-manager` e `occupancy-dashboard` | 🟢 |
| `_reversa_sdd/domain.md#entidades-e-regras` | Entidades `Teacher`, `Restriction`, `Class`, `Coordination` e `AllocationTask` | 🟢 |
| `_reversa_sdd/code-analysis.md#1.3-fluxo-de-controle` | Algoritmo de alocação inicial, leilão multiagente (`ACC`/`AMR`) e consolidação predial (`BuildingOptimizer`) em `src/engine/core.py` | 🟡 |

## 3. Personas e cenários de uso

| Persona | Objetivo | Cenário-chave |
|---------|----------|---------------|
| Coordenador de Curso (Cláudio) | Reorganizar a grade e substituir docente afastado emergencialmente | Registra o afastamento no painel e escolhe entre homologar manualmente uma opção ou delegar a escolha ao agente de IA |
| Professor Substituto | Assumir a turma/disciplina em horário compatível | Recebe a nova atribuição de aulas e salas atualizada na grade acadêmica |
| Aluno | Dar continuidade às aulas sem interrupção no semestre | Tem as aulas mantidas com mínima alteração de horário/espaço físico |

## 4. Regras de negócio novas ou alteradas

1. **RN-01:** A realocação emergencial de disciplinas deve buscar professores substitutos pertencentes prioritariamente à mesma coordenação do docente afastado. 🟢
   - Origem no legado: `_reversa_sdd/domain.md#Coordination`
   - Tipo: nova
2. **RN-02:** O motor de IA deve calcular e ranquear até 3 alternativas de realocação emergencial priorizando menor impacto (mínimo de substituições encadeadas em turmas terceiras e sem conflito de `Restriction`). 🟢
   - Origem no legado: `_reversa_sdd/code-analysis.md#1.3-fluxo-de-controle`
   - Tipo: nova
3. **RN-03:** O sistema deve prover alternância dinâmica de modo de homologação para o coordenador: Modo Assistido (revisão e clique manual) ou Modo Delegado (aprovação/efetivação automática pelo agente de IA). 🟢
   - Origem no legado: `_reversa_sdd/brainstorms/001-realocacao-docente-emergencial/decision.md`
   - Tipo: nova
4. **RN-04:** A execução do motor `CoreAllocationEngine` (`src/engine/core.py`) deve permitir recálculos parciais focados no subconjunto de turmas e horários diretamente afetados pelo afastamento. 🟡
   - Origem no legado: `_reversa_sdd/architecture.md#core-allocation-engine`
   - Tipo: alterada
5. **RN-05:** No Modo Delegado, a realocação é efetivada imediatamente no sistema acadêmico assim que aprovada pelo agente de IA, e o docente substituto é notificado da nova atribuição. 🟢
   - Origem: Esclarecimento da sessão 2026-08-13 (Q1)
   - Tipo: nova
6. **RN-06:** Caso o motor de IA não encontre professores substitutos livres na mesma coordenação, a busca é expandida automaticamente para coordenações correlatas antes de marcar como pendente. 🟢
   - Origem: Esclarecimento da sessão 2026-08-13 (Q2)
   - Tipo: nova

## 5. Requisitos Funcionais

| ID | Requisito | Prioridade | Critério de aceite | Confidência |
|----|-----------|------------|--------------------|-------------|
| RF-01 | Notificação de Afastamento Emergencial: Registrar licença de docente informando o período de ausência e as turmas afetadas | Must | Formulário permite selecionar o docente e marca as turmas com status de realocação pendente | 🟢 |
| RF-02 | Geração de Alternativas via IA: Calcular opções de realocação emergencial pelo motor de IA sem gerar conflitos de horários, expandindo para coordenações correlatas se necessário | Must | O motor retorna até 3 combinações viáveis com o índice de impacto de cada uma | 🟢 |
| RF-03 | Visualização no Painel: Exibir no `occupancy-dashboard` o resumo de cada alternativa calculada e os docentes substitutos sugeridos | Must | Painel exibe cards das opções com lista de horários/professores envolvidos | 🟢 |
| RF-04 | Escolha Dinâmica de Modo: Permitir ao coordenador alternar entre Modo Assistido (aprovação manual) e Modo Delegado (aprovação/efetivação imediata via IA) | Must | O coordenador pode clicar para homologar uma opção ou ativar o botão 'Delegar ao Agente de IA' | 🟢 |
| RF-05 | Efetivação e Atualização de Grade: Persistir as novas atribuições de docentes, turmas e salas na base de dados acadêmica e emitir notificação de atribuição | Must | As turmas passam para o novo docente e os horários/salas ficam atualizados na API REST | 🟢 |

## 6. Requisitos Não Funcionais

| Tipo | Requisito | Evidência ou justificativa | Confidência |
|------|-----------|----------------------------|-------------|
| Desempenho | O cálculo de alternativas de realocação emergencial via IA deve responder em menos de 5 segundos | Rationale: Evitar tempo de espera excessivo durante o atendimento no painel administrativo | 🟢 |
| Segurança / Auditoria | Registrar log de auditoria estruturado contendo timestamp, coordenador responsável, docente substituído e modo de homologação (assistido vs. delegado) | Rationale: Garantir rastreabilidade jurídica das alterações de atribuição docente | 🟢 |
| Usabilidade | Destacar claramente em vermelho/amarelo qualquer impacto secundário em turmas de terceiros antes da confirmação final | Rationale: Evitar aprovação inadvertida de substituições encadeadas | 🟡 |

## 7. Critérios de Aceitação

```gherkin
Cenário: Notificação e realocação emergencial em Modo Assistido
  Dado que o docente "Dr. Silva" precise se afastar por 60 dias
  E o coordenador "Cláudio" acesse o painel no Modo Assistido
  Quando acionar a realocação emergencial para as turmas do Dr. Silva
  Então o sistema exibe 3 opções de substituição calculadas pela IA
  E ao selecionar a Opção 1 e confirmar, as turmas são atribuídas aos novos docentes na grade sem gerar conflitos.

Cenário: Realocação emergencial em Modo Delegado pelo Agente de IA
  Dado que o coordenador "Cláudio" selecione o Modo Delegado
  Quando o afastamento do docente for registrado no sistema
  Então o agente de IA escolhe e efetiva automaticamente a alternativa de menor impacto no sistema acadêmico
  E o status da realocação é atualizado para "Concluído via Agente de IA" e o docente substituto é notificado.

Cenário: Expansão para coordenações correlatas
  Dado que não existam professores substitutos livres na mesma coordenação do docente ausente
  Quando o motor de IA calcular as alternativas emergenciais
  Então a busca é expandida automaticamente para docentes de coordenações correlatas compatíveis.
```

## 8. Prioridade MoSCoW

| Item | MoSCoW | Justificativa |
|------|--------|---------------|
| RF-01 (Notificação de Afastamento) | Must | Requisito essencial para disparar o fluxo de contingência |
| RF-02 (Geração via IA + Expansão) | Must | Núcleo da inteligência de realocação emergencial |
| RF-03 (Visualização no Painel) | Must | Transparência necessária para a tomada de decisão |
| RF-04 (Escolha Dinâmica de Modo) | Must | Alinhado com a decisão do brainstorm (Opção A + Opção B) |
| RF-05 (Efetivação de Grade) | Must | Necessário para persistir a nova atribuição |
| RNF de Desempenho (< 5s) | Should | Garante excelente experiência no painel administrativo |
| RNF de Auditoria | Must | Essencial para rastreabilidade trabalhista/acadêmica |

## 9. Esclarecimentos

### Sessão 2026-08-13
- **Q:** O sistema deve exigir confirmação/aceite explícito do professor substituto antes de efetivar a realocação no banco acadêmico quando o modo delegado for acionado?
  **R:** Não. No Modo Delegado, a realocação é efetivada imediatamente no sistema acadêmico, e o professor substituto é apenas notificado da nova atribuição.
- **Q:** Caso o motor de IA não encontre nenhuma combinação de professor substituto livre dentro da mesma coordenação, como a plataforma deve se comportar?
  **R:** Expandir a busca de professores substitutos para coordenações correlatas antes de declarar falta de docentes.

## 10. Lacunas

> Nenhuma lacuna ou dúvida pendente nesta versão.

## 11. Histórico de alterações

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-08-13 | Versão inicial gerada por `/reversa-requirements` | reversa |
| 2026-08-13 | Resolução de 2 dúvidas via `/reversa-clarify` | reversa |
