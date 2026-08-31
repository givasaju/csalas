# Modelo de Domínio e Regras de Negócio: ClassSync AI (balcao)

Este documento contém o glossário de termos e as regras de negócio implícitas e explícitas mapeadas a partir do código do ClassSync AI.

---

## 1. Glossário de Termos

*   **ClassSync AI**: Nome do sistema legado responsável pelo gerenciamento de salas físicas e otimização inteligente de alocação de turmas acadêmicas.
*   **Sala Física (Room)**: Espaço físico do campus onde as turmas são alocadas. Possui capacidade de alunos, tipo (`common`, `lab`, `auditorium`), acessibilidade física (`is_accessible`) e recursos adicionais (`features`, como projetores ou computadores).
*   **Turma / Disciplina (Class)**: Uma unidade de ensino de um curso que requer uma sala física compatível em um slot de horário específico.
*   **Coordenação de Curso (Coordination)**: Departamento acadêmico responsável por um conjunto de turmas. Cada coordenação possui um saldo em créditos acadêmicos para competir por salas de aula.
*   **Créditos Acadêmicos (Credits)**: Moeda interna do sistema utilizada pelas coordenações de curso para disputar salas físicas concorridas.
*   **Urgência Acadêmica (Urgency)**: Prioridade de alocação de uma turma (escala de 1 a 5), que influencia o lance de créditos no leilão.
*   **Agente Coordenador de Curso (ACC)**: Agente de IA que atua em nome de uma coordenação para calcular lances e disputar salas no leilão.
*   **Agente Mediador e Reputação (AMR)**: Agente de IA central que arbitra os conflitos por salas físicas no mesmo horário, executando a cobrança dos vencedores e distribuição de compensações aos perdedores.
*   **Leilão Cooperativo**: Mecanismo de arbitragem onde as coordenações concorrentes dão lances por uma sala. O vencedor paga o lance ao perdedor como compensação, garantindo um rebalanceamento de créditos para futuras rodadas.
*   **Consolidação Predial (Building Optimization)**: Algoritmo guloso executado pelo `BuildingOptimizer` para remanejar turmas de blocos subutilizados (ocupação < 20%) para blocos ativos, visando desativar blocos vazios e reduzir gastos com energia.
*   **Bloco Predial (Block)**: Estrutura física do campus que agrupa salas de aula.
*   **Indisponibilidade Docente (Teacher Restriction)**: Cadastro que impede a alocação de disciplinas de um determinado docente em slots específicos de dia e horário.
*   **Tarefa de Alocação (AllocationTask)**: Processo em background gerenciado de forma assíncrona por uma thread do worker para executar o motor de IA e gerar a alocação de salas.

---

## 2. Regras de Negócio

### 2.1 Regra de Cálculo do Lance do ACC
*   **Descrição**: O lance de créditos de uma coordenação para disputar uma sala é proporcional à urgência da turma e limitado a no máximo 20% do seu saldo de créditos atual.
*   **Fórmula**: 
    $$\text{Lance} = \max\left(1, \left\lfloor \text{Créditos Atuais} \times 0.20 \times \frac{\text{Urgência}}{5} \right\rfloor\right)$$
*   Se o saldo de créditos for menor ou igual a zero, o lance retornado é zero.
*   **Status**: 🟢 **CONFIRMADO** (implementado em [agents.py:17-27](file:///c:/csalas/src/engine/agents.py#L17-L27)).

### 2.2 Arbitragem de Conflitos e Compensação Cooperativa (AMR)
*   **Descrição**: Quando há colisão de mais de uma turma no mesmo slot de horário e sala física, o `AMR` concede a sala ao maior lance de créditos do ACC. O vencedor tem os créditos deduzidos de sua carteira, e os perdedores recebem esse mesmo valor do lance vencedor dividido como compensação para restaurar o seu poder de compra em disputas futuras.
*   **Status**: 🟢 **CONFIRMADO** (implementado em [agents.py:44-83](file:///c:/csalas/src/engine/agents.py#L44-L83)).

### 2.3 Resolução de Empate no Leilão
*   **Descrição**: Se duas ou mais coordenações derem lances idênticos na disputa de uma sala, o `AMR` usa o saldo de créditos total acumulado de cada coordenação como critério de desempate: a coordenação com maior saldo acumulado no momento vence.
*   **Status**: 🟢 **CONFIRMADO** (implementado em [agents.py:58-63](file:///c:/csalas/src/engine/agents.py#L58-L63)).

### 2.4 Limite de Iterações do Leilão
*   **Descrição**: O loop de detecção e mediação de colisões de alocação de salas executa no máximo 5 iterações para mitigar o risco de loops infinitos causados por desalocações consecutivas.
*   **Status**: 🟢 **CONFIRMADO** (implementado em [core.py:83](file:///c:/csalas/src/engine/core.py#L83)).

### 2.5 Realocação de Turmas Pós-Derrota
*   **Descrição**: A turma desalocada de uma sala física após perder um leilão de concorrência tenta ser alocada imediatamente em qualquer sala alternativa livre do campus que atenda às suas restrições obrigatórias. Se não houver sala física compatível disponível no mesmo slot de tempo, a alocação da turma é marcada com status `"pending_arbitration"` e a sala é definida como `None` (pendente de mediação física manual).
*   **Status**: 🟢 **CONFIRMADO** (implementado em [core.py:121-144](file:///c:/csalas/src/engine/core.py#L121-L144)).

### 2.6 Otimização e Consolidação Predial
*   **Descrição**: Um bloco predial é classificado como subutilizado se sua taxa de ocupação for inferior a 20% da capacidade total de slots do bloco (definida como $\text{Quantidade de Salas} \times 6\text{ turnos}$). O `BuildingOptimizer` tenta migrar as turmas desses blocos para salas livres em blocos ativos, desde que atendam às restrições mandatórias (capacidade, tipo de sala, acessibilidade e recursos adicionais) e que o bloco de destino não seja também um bloco subutilizado. Blocos que terminam com zero turmas alocadas são sinalizados como desativados para economia de energia.
*   **Status**: 🟢 **CONFIRMADO** (implementado em [optimization.py:14-133](file:///c:/csalas/src/engine/optimization.py#L14-L133)).

### 2.7 Importação Transacional de Salas (Tudo ou Nada)
*   **Descrição**: O processamento de arquivos CSV de salas de aula utiliza uma política transacional estrita: se houver falha sintática no cabeçalho ou erro de validação em qualquer registro do arquivo (como bloco/sala vazios, capacidade $\le 0$, ou tipo de sala diferente de `common`, `lab` ou `auditorium`), toda a importação é revertida e nenhuma alteração é persistida no inventário.
*   **Status**: 🟢 **CONFIRMADO** (implementado em [routes.py:56-138](file:///c:/csalas/src/api/routes.py#L56-L138)).

### 2.8 Restrição de Cadastro de Salas Duplicadas
*   **Descrição**: Não é permitido cadastrar mais de uma sala física com o mesmo nome (`name`) dentro do mesmo bloco predial (`block_id`). Tentativas geram erro `409 Conflict`.
*   **Status**: 🟢 **CONFIRMADO** (implementado em [routes.py:37-40](file:///c:/csalas/src/api/routes.py#L37-L40)).

### 2.9 Bloqueio de Exclusão de Salas em Execução (RNF-02)
*   **Descrição**: Para garantir a consistência das execuções do motor de IA, é proibido excluir salas físicas do inventário se houver alguma rodada de alocação ativa (com status `"queued"` ou `"running"`) no worker em background. Tentativas de exclusão retornam erro `409 Conflict`.
*   **Status**: 🟢 **CONFIRMADO** (implementado em [routes.py:224-231](file:///c:/csalas/src/api/routes.py#L224-L231)).

### 2.10 Restrições de Indisponibilidade Docente
*   **Descrição**: O cadastro de restrições exige que o professor informado exista na base de dados. O slot de tempo deve ser um dos seguintes: `M1`, `M2`, `T1`, `T2`, `N1`, `N2`. O dia da semana deve ser de 1 (Segunda) a 7 (Domingo). Não são permitidas indisponibilidades duplicadas para o mesmo professor no mesmo dia e slot.
*   **Status**: 🟢 **CONFIRMADO** (implementado em [routes.py:139-174](file:///c:/csalas/src/api/routes.py#L139-L174)).

### 2.11 Limite de Concorrência de Threads do Motor
*   **Descrição**: O processador de tarefas em background do worker utiliza um pool de threads limitado a 2 execuções concorrentes simultâneas.
*   **Status**: 🟢 **CONFIRMADO** (implementado em [worker.py:36](file:///c:/csalas/src/api/worker.py#L36)).

---

## 3. Segurança e Autenticação

*   **Validação JWT**: As requisições para os endpoints protegidos devem incluir o cabeçalho `Authorization` no formato `Bearer <token>`.
*   **Políticas de Acesso**:
    *   Token ausente ou mal-formatado: gera erro `401 Unauthorized` com a mensagem `"Token de autorização ausente ou mal-formatado."`.
    *   Token igual a `"invalid-token"`: gera erro `401 Unauthorized` com a mensagem `"Token de autenticação inválido."`.
    *   Qualquer outro token Bearer é aceito e validado como sucesso.
*   **Status**: 🟢 **CONFIRMADO** (implementado em [routes.py:16-26](file:///c:/csalas/src/api/routes.py#L16-L26)).

---

## 4. Lacunas de Negócio e Inconsistências Críticas

### 4.1 Endpoints Inexistentes de Execução e Status da Alocação
*   **Descrição**: O dashboard frontend (`index.html`) faz chamadas Ajax para disparar a alocação (`POST /api/v1/allocation/run`) e monitorar o status do processamento (`GET /api/v1/allocation/status/{task_id}`). Contudo, estas rotas **não estão implementadas** em `routes.py`. Embora o `worker.py` defina funções como `enqueue_allocation_run()` para essa finalidade, elas nunca são expostas pela API FastAPI.
*   **Status**: 🔴 **LACUNA CRÍTICA** (identificado em [routes.py](file:///c:/csalas/src/api/routes.py)).

### 4.2 Desacoplamento da Persistência Relacional SQL
*   **Descrição**: Embora haja um DDL de migrations (`db/migrations.sql`) definindo as tabelas relacionais `AllocationTask` e `AuctionBid` para armazenar as tarefas e as auditorias de lances do leilão, todo o backend da aplicação persiste e lê dados de coleções locais em memória (`db_rooms`, `db_tasks`, etc.) declaradas no arquivo `worker.py`. A base de dados PostgreSQL relacional nunca é integrada de fato.
*   **Status**: 🔴 **LACUNA** (identificado em [migrations.sql](file:///c:/csalas/db/migrations.sql) e [worker.py](file:///c:/csalas/src/api/worker.py)).
