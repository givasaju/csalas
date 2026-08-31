# Unit: motor-alocacao, Design Técnico

> Especificação de design técnico detalhando como a unidade de alocação inteligente é construída e opera.

## Interface

Esta unit é implementada como uma biblioteca/módulo em Python puro, consumida de forma assíncrona pelo worker da API. Suas classes principais possuem as seguintes assinaturas:

### Classes e Funções Principais

| Símbolo | Assinatura | Retorno | Observação |
|---------|-----------|---------|------------|
| `CoreAllocationEngine.__init__` | `(rooms: List[Dict], coordinations: List[Dict], classes: List[Dict])` | `None` | Instancia a engine e inicializa os agentes `ACC` de cada coordenação. |
| `CoreAllocationEngine.run_allocation` | `()` | `Tuple[Dict, List[str], List[Dict]]` | Orquestra a execução completa: AAC, leilão e otimização predial. Retorna alocações finais, blocos fechados e histórico de lances. |
| `ACC.__init__` | `(id_coord: str, name: str, credits: int)` | `None` | Inicializa o agente da coordenação de curso com um saldo de créditos. |
| `ACC.make_bid` | `(class_id: str, room_id: str, urgency: int)` | `int` | Calcula o valor do lance de créditos baseado na urgência (1-5) e no saldo. |
| `AMR.resolve_dispute` | `(room_id: str, time_slot: str, competitor_bids: Dict[ACC, int])` | `ACC` | Executa a mediação, transfere créditos, registra a auditoria e retorna o vencedor. |
| `BuildingOptimizer.optimize_building_occupancy` | `(allocations: Dict, rooms: List, blocks: List)` | `Tuple[Dict, List[str]]` | Analisa a ocupação predial, realiza migrações para esvaziar blocos e retorna alocações otimizadas. |

---

## Fluxo Principal

O fluxo de processamento de alocação de turmas ocorre em três grandes fases sequenciais no método `run_allocation()`:

1.  **Fase 1: Alocação Inicial (AAC)**:
    *   Filtra as salas candidatas que atendem às restrições rígidas (capacidade, tipo, recursos e acessibilidade) da turma (`src/engine/core.py:44-60`).
    *   Ordena as candidatas por capacidade de forma crescente (`src/engine/core.py:67`).
    *   Aloca a turma na primeira sala compatível (menor tamanho justo para evitar desperdício de espaço) (`src/engine/core.py:68-76`).
2.  **Fase 2: Resolução de Conflitos (Leilão Multiagente)**:
    *   Executa um loop de arbitragem de conflitos limitado a no máximo 5 iterações (`src/engine/core.py:83-85`).
    *   Identifica salas físicas com mais de uma turma alocada no mesmo slot de tempo (`src/engine/core.py:90-96`).
    *   Coleta o lance (bid) do ACC de cada coordenação concorrente no conflito (`src/engine/core.py:104-111`).
    *   O AMR arbitra e declara o vencedor com base no maior lance (em caso de empate, vence a coordenação com maior saldo total) (`src/engine/agents.py:53-63`).
    *   O vencedor mantém a alocação e paga os créditos. Os perdedores são compensados com os créditos pagos e são desalocados da sala física (`src/engine/agents.py:65-72`).
    *   As turmas perdedoras tentam ser realocadas imediatamente em qualquer sala livre compatível. Caso contrário, sua sala é definida como `None` e o status da alocação passa a ser `"pending_arbitration"` (`src/engine/core.py:121-144`).
3.  **Fase 3: Consolidação Predial (BuildingOptimizer)**:
    *   Calcula a taxa de ocupação esperada de todos os blocos prediais (`src/engine/optimization.py:23-42`).
    *   Identifica blocos subutilizados com ocupação `< 20%` (`src/engine/optimization.py:44-52`).
    *   Para cada bloco subutilizado, tenta migrar as turmas alocadas para salas livres em blocos ativos (não subutilizados) respeitando todas as restrições rígidas (`src/engine/optimization.py:69-120`).
    *   Retorna a distribuição de alocações otimizada predialmente e a lista de blocos desativados (`src/engine/optimization.py:121-133`).

---

## Fluxos Alternativos

*   **Nenhuma sala atende às restrições rígidas da turma na alocação inicial**: A turma é ignorada do mapeamento inicial, registrando-se um erro no log (`src/engine/core.py:62-64`).
*   **Empate de lances no leilão cooperativo**: O AMR avalia o saldo total dos agentes concorrentes e favorece o ACC com maior saldo geral de créditos (`src/engine/agents.py:57-63`).
*   **Derrota no leilão sem salas livres compatíveis disponíveis**: A alocação da turma perdedora é marcada com status `"pending_arbitration"` e a propriedade `room_id` é redefinida como `None` (`src/engine/core.py:140-144`).
*   **Inexistência de salas compatíveis em blocos ativos para consolidação predial**: A turma permanece alocada no bloco subutilizado original; a otimização desse bloco específico é abortada mantendo a segurança acadêmica (`src/engine/optimization.py:113-120`).

---

## Dependências

Esta unit é autocontida e não depende de APIs ou bibliotecas externas complexas, importando apenas módulos da biblioteca padrão do Python (`logging`, `typing`, `uuid`). Ela é instanciada e orquestrada de fora pelo worker assíncrono do FastAPI (`src/api/worker.py`).

---

## Decisões de Design Identificadas

| Decisão | Evidência no código | Confiança |
|---------|---------------------|-----------|
| **Leilão Multiagente Cooperativo**: Compensação dos perdedores com os créditos gastos pelo vencedor para garantir reequilíbrio futuro. | `src/engine/agents.py:65-72` | 🟢 |
| **Otimização predial por limite rígido de 20%**: Esvaziamento de blocos subutilizados e desativação predial baseada em limite numérico configurável de slots. | `src/engine/optimization.py:51` | 🟢 |
| **Mitigação de loop infinito**: Limitação de no máximo 5 iterações no loop de colisão do leilão para evitar estouro de processamento. | `src/engine/core.py:83` | 🟢 |
| **Alocação Gulosa por Tamanho Justo**: Escolha sistemática da sala física compatível de menor capacidade para conservar espaço no campus. | `src/engine/core.py:67-68` | 🟢 |

---

## Estado Interno

*   **Créditos do ACC (`ACC.credits`)**: Tipo `int`. Mantém o saldo ativo de créditos da coordenação do curso (iniciando em 1000). Modificado após leilões por dedução/compensação.
*   **Histórico de Lances (`AMR.bids_history`)**: Tipo `List[Dict]`. Registra transações do leilão contendo dados de `room_id`, `time_slot`, `winner_id`, `loser_id` e `credits_spent`.

---

## Observabilidade

*   **Logs da Engine**: Emite logs informativos detalhados descrevendo o progresso das fases, conflitos encontrados, lances oferecidos, vencedores declarados e migrações prediais no logger `core-allocation-engine` (`src/engine/core.py:7-8`).

---

## Riscos e Lacunas

*   🔴 **LACUNA CRÍTICA DE PERSISTÊNCIA**: Os créditos das coordenações e o histórico de transações de lances do leilão são alterados e armazenados apenas na memória volátil do processo Python. Não há nenhuma integração com banco de dados físico (como previsto no script `db/migrations.sql`). Ao reiniciar a aplicação, todos os saldos e auditorias de leilões são completamente perdidos.
