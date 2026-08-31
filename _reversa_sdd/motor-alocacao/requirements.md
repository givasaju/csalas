# Unit: motor-alocacao (Motor de Alocação de IA)

> Especificação de requisitos para a unidade central de alocação e otimização de salas do campus.

## Visão Geral
Este componente é o núcleo inteligente do ClassSync AI. Ele realiza a alocação inicial de turmas às salas físicas sob restrições mandatórias, resolve colisões de horários em salas concorridas através de um leilão multiagente de créditos cooperativos e otimiza a eficiência predial agrupando turmas para desativar blocos subutilizados.

## Responsabilidades
- Executar a alocação preliminar baseada em capacidade, acessibilidade, tipo de sala e recursos obrigatórios.
- Arbitrar conflitos concorrenciais por salas físicas no mesmo horário utilizando leilões cooperativos entre agentes autônomos de coordenação.
- Consolidar a ocupação das salas remanejando turmas de blocos subutilizados para desativar blocos prediais vazios e poupar energia.

## Regras de Negócio

*   **RN-01: Alocação Inicial por Restrições (AAC)**: As turmas devem ser alocadas somente em salas físicas que atendam a todos os seguintes critérios obrigatórios:
    *   *Capacidade*: A capacidade da sala deve ser maior ou igual ao número de alunos (`capacity >= students_count`). 🟢 (Evidência: `src/engine/core.py:48-49`)
    *   *Tipo*: O tipo da sala deve ser idêntico ao solicitado pela turma (`room_type`). 🟢 (Evidência: `src/engine/core.py:50-52`)
    *   *Recursos*: A sala deve conter todos os recursos/features obrigatórios listados pela turma (`required_features`). 🟢 (Evidência: `src/engine/core.py:53-55`)
    *   *Acessibilidade*: Se a turma exigir acessibilidade, a sala física deve ser acessível (`is_accessible == True`). 🟢 (Evidência: `src/engine/core.py:56-58`)
*   **RN-02: Minimização de Desperdício de Espaço**: Em caso de múltiplas salas candidatas que atendam a todas as restrições rígidas, o sistema deve ordenar as salas por capacidade física e alocar a turma na menor sala compatível (capacidade mais justa). 🟢 (Evidência: `src/engine/core.py:67-68`)
*   **RN-03: Limitação de Lance do ACC**: O lance (bid) máximo de um Agente Coordenador de Curso (ACC) é limitado a no máximo 20% do seu saldo atual de créditos acadêmicos. O lance é ponderado pela urgência acadêmica da turma (escala de 1 a 5). Se o saldo de créditos for `<= 0`, o lance é `0`; caso contrário, o lance mínimo é `1` crédito. 🟢 (Evidência: `src/engine/agents.py:22-27`)
*   **RN-04: Arbitragem de Disputa por Maior Lance**: Quando duas ou mais turmas concorrem pela mesma sala física no mesmo slot de tempo, o Agente Mediador e Reputação (AMR) concede a sala à turma representada pelo ACC que der o maior lance de créditos. 🟢 (Evidência: `src/engine/agents.py:54-55`)
*   **RN-05: Critério de Desempate por Saldo Histórico**: Se houver um empate de lances máximos concorrentes, o AMR deve conceder a sala à coordenação que possuir o maior saldo de créditos total disponível em carteira no momento. 🟢 (Evidência: `src/engine/agents.py:58-63`)
*   **RN-06: Compensação Cooperativa de Créditos**: O valor cobrado do vencedor da disputa (`winning_bid`) é deduzido de sua carteira e redistribuído integralmente para a carteira dos perdedores do leilão, reequilibrando seu poder de compra para rodadas futuras. 🟢 (Evidência: `src/engine/agents.py:65-72`)
*   **RN-07: Mitigação de Loops no Leilão**: O ciclo de detecção e mediação de colisões deve rodar no máximo 5 iterações para evitar desvios infinitos por desalocações sucessivas. 🟢 (Evidência: `src/engine/core.py:83`)
*   **RN-08: Realocação Pós-Derrota**: A turma perdedora do leilão deve ser imediatamente realocada em qualquer sala livre compatível no mesmo horário. Se não houver sala física alternativa livre, a turma deve ser marcada com o status `"pending_arbitration"` e sua sala definida como `None` (aguardando mediação manual humana). 🟢 (Evidência: `src/engine/core.py:121-144`)
*   **RN-09: Identificação de Bloco Subutilizado**: Um bloco predial é subutilizado se sua taxa de ocupação esperada for inferior a 20% (sendo a capacidade total do bloco definida por `Salas do Bloco * 6 slots por dia`) e se houver ao menos uma alocação ativa nele. 🟢 (Evidência: `src/engine/optimization.py:44-52`)
*   **RN-10: Consolidação de Blocos e Restrição de Destino**: O otimizador de blocos deve tentar migrar as turmas de blocos subutilizados para salas livres em blocos ativos que atendam a todas as restrições rígidas da turma. Não é permitido migrar uma turma para uma sala localizada em outro bloco que também esteja classificado como subutilizado. 🟢 (Evidência: `src/engine/optimization.py:84-88`)

---

## Requisitos Funcionais

| ID | Requisito | Prioridade | Critério de Aceite |
|----|-----------|-----------|-------------------|
| RF-01 | Alocação Inicial (AAC) baseada em restrições mandatórias. | Must | Validar que turmas são alocadas em salas com capacidade justa, atendendo acessibilidade, tipo e recursos obrigatórios. |
| RF-02 | Arbitragem de colisões via leilão multiagente cooperativo. | Must | Validar que colisões de salas/horários são resolvidas em favor do maior lance, deduzindo créditos do vencedor e compensando os perdedores. |
| RF-03 | Realocação automática imediata de turmas derrotadas no leilão. | Must | Validar que a turma perdedora é alocada em outra sala livre compatível no mesmo slot de tempo, ou marcada em arbitragem se o campus estiver cheio. |
| RF-04 | Otimização predial para consolidação energética (BuildingOptimizer). | Should | Validar que turmas em blocos com <20% de ocupação são movidas para blocos ativos e os blocos de origem são desativados. |

---

## Requisitos Não Funcionais

| Tipo | Requisito inferido | Evidência no código | Confiança |
|------|--------------------|---------------------|-----------|
| Performance | Limitação de processamento a no máximo 5 iterações para mitigar gargalo algorítmico. | `src/engine/core.py:83` | 🟢 |
| Observabilidade | Emissão de logs detalhados de auditoria em formato padronizado a cada alocação, leilão e migração de blocos. | `src/engine/core.py:7-8` | 🟢 |

---

## Critérios de Aceitação

```gherkin
Dado que há duas turmas cadastradas para o mesmo slot de tempo "M1" requerendo a mesma sala "sala-a1"
Quando a engine executa o processo de alocação de turmas
Então o sistema deve disparar o leilão, conceder a sala ao maior lance de créditos, deduzir o saldo do vencedor, compensar o perdedor e tentar realocar o perdedor em uma sala compatível livre.

Dado que o Bloco C possui apenas 1 sala ativa com 1 turma alocada no slot "M1" (ocupação esperada de 16.6% - inferior a 20%)
Quando a otimização predial (BuildingOptimizer) é executada
Então o sistema deve migrar a turma do Bloco C para uma sala livre compatível no Bloco A (bloco ativo), e sinalizar o Bloco C como desativado.

Dado que uma turma com exigência de acessibilidade física está em processo de alocação inicial
Quando o motor de alocação busca salas candidatas
Então a sala "sala-b1" (que não possui acessibilidade) deve ser sumariamente ignorada no filtro de salas para esta turma.
```

---

## Prioridade (MoSCoW)

| Requisito | MoSCoW | Justificativa |
|-----------|--------|---------------|
| Alocação Inicial (AAC) | Must | Funcionalidade mandatória sem a qual o sistema não realiza o mapeamento básico. |
| Resolução de Colisões (Leilão) | Must | Processo crítico de negócio para desfazer colisões de salas no mesmo horário. |
| Realocação Pós-Derrota | Must | Evita que turmas perdedoras fiquem desalocadas se houver espaço no campus. |
| Consolidação Predial | Should | Importante para economia energética, mas secundário à alocação básica sem conflitos. |

---

## Rastreabilidade de Código

| Arquivo | Função / Classe | Cobertura |
|---------|-----------------|-----------|
| [`src/engine/core.py`](file:///c:/csalas/src/engine/core.py) | `CoreAllocationEngine` | 🟢 |
| [`src/engine/agents.py`](file:///c:/csalas/src/engine/agents.py) | `ACC`, `AMR` | 🟢 |
| [`src/engine/optimization.py`](file:///c:/csalas/src/engine/optimization.py) | `BuildingOptimizer` | 🟢 |
