# Análise Técnica do Sistema Legado: balcao (ClassSync AI)

Este documento contém a escavação arqueológica do código do ClassSync AI, detalhando os fluxos de controle, algoritmos, dicionário de dados e regras de negócio extraídos diretamente do código-fonte.

---

## 1. Módulo: core-allocation-engine

### 1.1 Propósito e Escopo
Este módulo é o coração do ClassSync AI. Ele coordena o processo de alocação de turmas às salas de aula físicas em três etapas integradas:
1. **Alocação Inicial (AAC)**: Realiza uma alocação preliminar gulosa baseada em restrições estritas (capacidade, tipo de sala, recursos requeridos e acessibilidade).
2. **Mediação de Conflitos (Leilão Multiagente)**: Arbitra colisões de horários e salas físicas através de lances de créditos cooperativos disputados pelos Agentes Coordenadores de Curso (ACC) e mediados pelo Agente Mediador e Reputação (AMR).
3. **Consolidação Predial (BuildingOptimizer)**: Otimiza a ocupação do campus realocando turmas para esvaziar blocos prediais subutilizados (ocupação < 20%), permitindo o seu desligamento para economia energética.

---

### 1.2 Estrutura do Código
*   [`src/engine/core.py`](file:///c:/csalas/src/engine/core.py): Orquestrador principal (`CoreAllocationEngine`).
*   [`src/engine/agents.py`](file:///c:/csalas/src/engine/agents.py): Classes dos agentes `ACC` e `AMR`.
*   [`src/engine/optimization.py`](file:///c:/csalas/src/engine/optimization.py): Módulo de consolidação de blocos (`BuildingOptimizer`).

---

### 1.3 Fluxo de Controle e Execução
O fluxo de alocação de ponta a ponta ocorre dentro do método `CoreAllocationEngine.run_allocation()`:

1.  **Fase 1: Alocação Inicial**
    *   Itera sobre todas as turmas cadastradas (`self.classes`).
    *   Filtra as salas disponíveis (`self.rooms`) baseando-se nas seguintes restrições obrigatórias:
        *   **Capacidade**: A sala deve comportar a quantidade de alunos (`capacity >= students_count`).
        *   **Tipo de Sala**: O tipo da sala física deve corresponder ao solicitado (`room_type`).
        *   **Recursos**: A sala deve conter todos os recursos exigidos pela turma (`required_features`).
        *   **Acessibilidade**: Se a turma exigir acessibilidade (`require_accessibility`), a sala física deve ser acessível (`is_accessible == True`).
    *   As salas candidatas são ordenadas por capacidade em ordem crescente, e a turma é alocada temporariamente na menor sala compatível (capacidade mais justa) para evitar desperdício de espaço.
    *   Se nenhuma sala atender às restrições, um erro é registrado no log e a turma fica sem alocação.

2.  **Fase 2: Resolução de Conflitos (Leilão)**
    *   Roda em loop por no máximo 5 iterações para mitigar o risco de loops infinitos.
    *   Mapeia o uso de salas por slot de tempo para identificar colisões (duas ou mais turmas na mesma sala no mesmo horário).
    *   Para cada colisão encontrada:
        *   Obtém o lance (bid) de cada agente `ACC` concorrente.
        *   O `AMR` resolve a disputa: o maior lance vence. Em caso de empate, vence a coordenação que tiver o maior saldo total de créditos.
        *   O vencedor mantém a alocação na sala e paga o valor do lance (`winning_bid`), que é deduzido dos seus créditos.
        *   Os perdedores recebem o valor do lance (`winning_bid`) como compensação financeira (leilão cooperativo).
        *   Os perdedores são desalocados e o sistema tenta realocá-los imediatamente em qualquer sala alternativa compatível que esteja livre no mesmo slot.
        *   Se nenhuma sala alternativa estiver livre, a turma é marcada com status `"pending_arbitration"` e a sala física é definida como `None` (pendente de intervenção humana).

3.  **Fase 3: Otimização Predial**
    *   O `BuildingOptimizer` calcula a taxa de ocupação esperada de cada bloco do campus (considerando 6 slots por dia por sala física).
    *   Identifica blocos subutilizados (com taxa de ocupação `< 20%` e com pelo menos uma turma alocada).
    *   Para cada bloco subutilizado:
        *   Tenta mover as turmas alocadas nele para salas em blocos ativos (não subutilizados), respeitando todas as restrições obrigatórias e sem gerar novos conflitos de horário.
        *   Turmas não podem ser migradas para outros blocos também classificados como subutilizados.
    *   Retorna a distribuição final de alocações otimizadas e uma lista de blocos prediais totalmente desativados (com ocupação zerada).

---

### 1.4 Algoritmos e Lógicas Não-Triviais
*   **Fórmula do Lance do ACC**:
    ```python
    max_allocable = int(self.credits * 0.20)
    bid = int(max_allocable * (urgency / 5.0))
    return max(1, bid)
    ```
    O lance consome no máximo 20% do saldo de créditos atual da coordenação do curso, ponderado pela prioridade acadêmica (urgência) da turma em uma escala de 1 a 5. O lance mínimo é de 1 crédito.
*   **Resolução de Empate (AMR)**:
    Se dois ou mais lances possuírem o mesmo valor máximo de créditos, o `AMR` utiliza o saldo histórico total de créditos de cada coordenação como critério de desempate: a coordenação com mais créditos totais na carteira vence.
*   **Compensação de Créditos**:
    O leilão é estruturado de forma estritamente cooperativa: os créditos deduzidos da coordenação vencedora são somados diretamente ao saldo da coordenação perdedora. Isso garante redistribuição de poder de compra para rodadas ou conflitos futuros.

---

### 1.5 Dicionário de Dados Resumido (Fase 1 e 2)
Como o nível de documentação definido é **essencial**, as principais estruturas de dados consumidas e geradas pelo motor são descritas na tabela abaixo:

| Entidade | Campo | Tipo | Obrigatoriedade | Descrição / Regra de Negócio |
| :--- | :--- | :--- | :---: | :--- |
| **Class** | `id` | `string` | Sim | Identificador único da turma (ex: `"eng-101"`). |
| | `students_count` | `int` | Sim | Número de alunos matriculados na turma. |
| | `room_type` | `string` | Sim | Tipo de sala necessário: `"common"`, `"lab"`, `"auditorium"`. |
| | `time_slot` | `string` | Sim | Faixa de horário da aula: `"M1"`, `"M2"`, `"T1"`, `"T2"`, `"N1"`, `"N2"`. |
| | `coordination_id` | `string` | Sim | ID da coordenação responsável (`"eng"`, `"let"`, `"med"`). |
| | `urgency` | `int` | Sim | Nível de urgência da alocação de 1 (mínimo) a 5 (máximo). |
| | `require_accessibility` | `bool` | Não | Se a turma exige sala física com acessibilidade (default `False`). |
| **Room** | `id` | `string` | Sim | Identificador único gerado por UUID. |
| | `name` | `string` | Sim | Nome da sala (ex: `"Sala A1"`). Não pode haver duplicados no mesmo bloco. |
| | `block_id` | `string` | Sim | ID ou nome do bloco predial (ex: `"Bloco A"`). |
| | `capacity` | `int` | Sim | Capacidade física de alunos (deve ser `> 0`). |
| | `room_type` | `string` | Sim | Tipo de sala física: `"common"`, `"lab"`, `"auditorium"`. |
| | `is_accessible` | `bool` | Sim | Indica se a sala atende a normas de acessibilidade física. |
| | `features` | `List[string]` | Sim | Lista de recursos extras disponíveis (ex: `["projector", "computers"]`). |
| **Allocation** | `room_id` | `string` \| `None` | Sim | ID da sala física alocada. `None` se estiver em arbitragem. |
| | `time_slot` | `string` | Sim | Slot de tempo da alocação. |
| | `students_count` | `int` | Sim | Capacidade de alunos alocada. |
| | `coordination_id` | `string` | Sim | ID da coordenação que detém a alocação. |
| | `urgency` | `int` | Sim | Nível de urgência da turma alocada. |
| | `status` | `string` | Não | Estado da alocação, ex: `"pending_arbitration"`. |
| **Coordination** | `id` | `string` | Sim | ID único da coordenação. |
| | `name` | `string` | Sim | Nome do departamento/curso. |
| | `credits` | `int` | Sim | Saldo de créditos acadêmicos (inicia com 1000). |
| **AuctionBid** | `room_id` | `string` | Sim | ID da sala onde ocorreu o conflito de concorrência. |
| | `time_slot` | `string` | Sim | Slot do conflito. |
| | `winner_id` | `string` | Sim | ID da coordenação que venceu a arbitragem. |
| | `loser_id` | `string` | Sim | ID da coordenação que perdeu e recebeu compensação. |
| | `credits_spent` | `int` | Sim | Valor cobrado do vencedor e transferido ao perdedor. |

---

### 1.6 Escala de Confiança e Lacunas Identificadas
*   🟢 **CONFIRMADO**: A alocação por capacidade justa, leilões multiagente cooperativos (ACC + AMR), regras de transação e compensação de lances, e os filtros de consolidação predial de 20% da ocupação estão implementados e cobertos por testes unitários em `tests/`.
*   🔴 **LACUNA**: O sistema simulado em memória em [`src/api/worker.py`](file:///c:/csalas/src/api/worker.py) implementa controle de estado e threads assíncronas para tarefas de alocação que não possuem rotas correspondentes declaradas em [`src/api/routes.py`](file:///c:/csalas/src/api/routes.py). As rotas `/api/v1/allocation/run` e `/api/v1/allocation/status/{task_id}` chamadas pelo dashboard frontend simplesmente **não existem** no backend do projeto legado.

---

## 2. Módulo: academic-space-manager

### 2.1 Propósito e Escopo
Este módulo fornece a interface de comunicação HTTP (API REST) e a persistência em memória (simulação de banco) de todas as entidades que alimentam o motor de alocação. Ele permite cadastrar e remover salas, processar a importação em lote via arquivos CSV, definir e redefinir as restrições horárias de indisponibilidade dos docentes e expor os dados consolidados do campus.

---

### 2.2 Estrutura do Código
*   [`src/api/routes.py`](file:///c:/csalas/src/api/routes.py): Define as rotas REST do backend do FastAPI.
*   [`src/api/schemas.py`](file:///c:/csalas/src/api/schemas.py): Modelos de validação Pydantic.
*   [`src/api/worker.py`](file:///c:/csalas/src/api/worker.py): Banco de dados em memória simulado e pool de threads em background.
*   [`db/migrations.sql`](file:///c:/csalas/db/migrations.sql): Script DDL SQL relacional (PostgreSQL).

---

### 2.3 Fluxo de Controle e Operações Principais
A API expõe as seguintes rotas sob o prefixo `/api/v1`:

1.  **Criação de Sala (`POST /rooms`)**
    *   Valida credenciais JWT via mock (`check_jwt_auth`).
    *   Verifica duplicados: se já existir uma sala com o mesmo nome (`name`) dentro do mesmo bloco predial (`block_id`), rejeita com `409 Conflict`.
    *   Se válido, atribui um UUID único à sala e a insere em `db_rooms`.

2.  **Importação de Salas em Lote (`POST /rooms/import-csv`)**
    *   Recebe um arquivo no formato CSV.
    *   **Algoritmo Tudo ou Nada (Transacional)**:
        *   Valida a presença de linhas e se o cabeçalho é idêntico a: `bloco, sala, capacidade, tipo, acessivel, recursos`. Se divergente, rejeita com `400 Bad Request`.
        *   Varre todas as linhas do CSV antes de persistir qualquer dado. Valida se o bloco e sala não estão vazios, se a capacidade é um inteiro `> 0` e se o tipo está entre `common`, `lab` ou `auditorium`.
        *   Caso ocorra algum erro em qualquer linha, a operação inteira é abortada com `422 Unprocessable Entity` ou `400 Bad Request`.
        *   Apenas se todas as linhas forem consideradas 100% válidas, elas são adicionadas ao banco de dados (`db_rooms`).

3.  **Cadastro de Indisponibilidade Docente (`POST /allocation/restrictions`)**
    *   Valida autenticação JWT.
    *   Verifica se o professor correspondente existe no banco de dados. Se não, retorna `404 Not Found`.
    *   Valida se a faixa de horário informada está na lista permitida (`M1`, `M2`, `T1`, `T2`, `N1`, `N2`). Se não, rejeita com `422 Unprocessable Entity`.
    *   Verifica se a indisponibilidade já está cadastrada para o professor. Se duplicada, retorna `409 Conflict`.
    *   Atribui um UUID e persiste no `db_restrictions`.

4.  **Reset Semestral de Indisponibilidades (`DELETE /allocation/restrictions`)**
    *   Limpa a lista inteira de indisponibilidades dos professores (`db_restrictions`), sinalizando aviso no log. Retorna a contagem de restrições removidas.

5.  **Obtenção de Dados Consolidados (`GET /allocation/input-data`)**
    *   Consolida e retorna todas as salas, coordenações, turmas, professores e restrições cadastradas em memória para o consumo do motor de IA.

6.  **Remoção de Sala (`DELETE /rooms/{room_id}`)**
    *   Verifica se a sala física existe em `db_rooms`. Se não, retorna `404 Not Found`.
    *   **Garantia de Não-Interrupção (RNF-02)**: Verifica se existe alguma tarefa de alocação de IA ativa executando em background (`status` em `queued` ou `running` no `db_tasks`). Se houver, a exclusão é proibida retornando `409 Conflict`.
    *   Se livre, remove a sala física da lista.

---

### 2.4 Dicionário de Dados Resumido (Persistência)

As principais estruturas de dados utilizadas para persistência e validação no módulo são:

| Entidade | Campo | Tipo | Obrigatoriedade | Descrição / Regra de Negócio |
| :--- | :--- | :--- | :---: | :--- |
| **RoomCreate** | `block_id` | `string` | Sim | Mínimo 1 caractere. Nome/identificador do bloco predial. |
| | `name` | `string` | Sim | Mínimo 1 caractere. Nome da sala de aula física. |
| | `capacity` | `int` | Sim | Deve ser estritamente `> 0`. Capacidade máxima de alunos. |
| | `room_type` | `string` | Sim | Tipo de sala: `"common"`, `"lab"`, `"auditorium"`. |
| | `is_accessible` | `bool` | Não | Flag indicando se é acessível (default `True`). |
| | `features` | `List[string]` | Não | Recursos adicionais (default `[]`). |
| **RestrictionCreate**| `teacher_id` | `string` | Sim | ID único do professor solicitante. |
| | `day_of_week` | `int` | Sim | Dia da semana representado de 1 (Segunda) a 7 (Domingo). |
| | `time_slot_id` | `string` | Sim | ID da faixa de horário (`M1`, `M2`, `T1`, `T2`, `N1`, `N2`). |
| **Teacher** | `id` | `string` | Sim | Identificador único do docente (ex: `"prof-claudio"`). |
| | `name` | `string` | Sim | Nome completo do professor. |
| | `email` | `string` | Sim | Endereço de e-mail institucional. |

---

### 2.5 Escala de Confiança e Lacunas Identificadas
*   🟢 **CONFIRMADO**: As regras de validação Pydantic, restrições de unicidade de sala por bloco, autenticação simulada JWT via header e a lógica transacional Tudo ou Nada para CSV estão implementadas e validadas por testes unitários em `tests/`.
*   🔴 **LACUNA**: O script de migração relacional SQL [`db/migrations.sql`](file:///c:/csalas/db/migrations.sql) prevê tabelas físicas com UUID autogerado via `gen_random_uuid()` para auditoria de leilões e tarefas assíncronas, contudo, o código backend da API REST é acoplado a coleções locais em memória simuladas em [`src/api/worker.py`](file:///c:/csalas/src/api/worker.py) (`db_rooms`, `db_restrictions`, etc.), o que significa que o banco PostgreSQL relacional de produção ainda não está integrado de forma operacional com o servidor FastAPI legado.

---

## 3. Módulo: occupancy-dashboard

### 3.1 Propósito e Escopo
Este módulo fornece a interface gráfica do ClassSync AI. Consiste em uma aplicação web estática de página única (SPA) que permite aos administradores monitorar e disparar os leilões de créditos acadêmicos e a consolidação de ocupação dos blocos. A interface é projetada com uma estética moderna (Dark Mode, Glassmorphism, gradientes e animações de shimmer loading) utilizando CSS puro.

---

### 3.2 Estrutura do Código
*   [`src/api/static/index.html`](file:///c:/csalas/src/api/static/index.html): Estrutura HTML e scripts JavaScript de interação e consumo da API REST.
*   [`src/api/static/index.css`](file:///c:/csalas/src/api/static/index.css): Regras de estilo, paleta de cores e animações.

---

### 3.3 Fluxo de Controle e Interações do Dashboard
O comportamento interativo da interface baseia-se em quatro operações assíncronas:

1.  **Carregamento de Dados Iniciais (`loadInputData`)**
    *   No carregamento da página, realiza um `GET /api/v1/allocation/input-data` com cabeçalho de autenticação JWT mockado (`Bearer mock-token`).
    *   Atualiza os cartões de KPIs em tela:
        *   **Ocupação Geral (`kpiOccupancy`)**: Taxa média de preenchimento (estático mockado para `78.5%` caso existam salas).
        *   **Economia de Energia (`kpiEnergy`)**: Percentual estimado de economia de custos (estático mockado para `25.0%`).
        *   **Blocos Desativados (`kpiBlocks`)**: Lista de blocos prediais esvaziados (estático mockado para `"Bloco C"`).
        *   **Conflitos Resolvidos (`kpiConflicts`)**: Número de rodadas de arbitragem (estático mockado para `3`).
    *   Preenche a tabela de extrato de auditoria de leilões (`auctionsTableBody`) com três lances estáticos mockados em HTML de coordenações concorrentes se houver dados cadastrados no inventário.

2.  **Disparo de Nova Alocação (`triggerAllocation`)**
    *   Ao clicar no botão "Disparar Alocação de IA", envia um `POST /api/v1/allocation/run`.
    *   Se a API responder com `409 Conflict`, alerta o usuário que um processamento já está rodando.
    *   Se sucesso, obtém o ID da tarefa (`task_id`), altera o badge de status para `queued`, inicializa a barra de progresso em 0% e inicia um polling repetitivo (a cada 1000ms).

3.  **Polling de Status (`pollTaskStatus`)**
    *   Executa um `GET /api/v1/allocation/status/{taskId}` a cada segundo para acompanhar o processamento.
    *   **Transição de Estados**:
        *   Se status for `running`: Mantém o badge em `running`, atualiza a barra de progresso com o valor numérico e exibe mensagem de execução.
        *   Se status for `completed` ou `pending_arbitration`: Interrompe o polling (`clearInterval`), altera a barra para 100%, define o badge correspondente e dispara `loadInputData()` para recarregar a tabela e indicadores.
        *   Se status for `failed`: Interrompe o polling, define o badge como `failed` e exibe o log de erro no painel.

4.  **Estilos e Variáveis de Design**
    *   Design baseado em variáveis CSS no seletor `:root` facilitando a manutenibilidade do tema escuro:
        *   `--bg-primary`: Azul ardósia escuro (`#0f172a`).
        *   `--bg-card`: Translúcido com efeito blur (`rgba(30, 41, 59, 0.7)` e `backdrop-filter: blur(12px)`).
        *   `--color-accent` e `--color-success`: Indigo (`#6366f1`) e Verde Esmeralda (`#10b981`).
    *   Utiliza a fonte `Inter` via Google Fonts.
    *   Adiciona efeito shimmer (animação linear gradiente deslizante de 1.5s) em `.shimmer` para representar carregamentos pendentes de forma fluida.

---

### 3.4 Escala de Confiança e Lacunas Identificadas
*   🟢 **CONFIRMADO**: O código HTML e CSS de interface está estruturado, responsivo (com media-queries para mobile), e consome o endpoint `/api/v1/allocation/input-data` com o cabeçalho Bearer Token devidamente configurado.
*   🔴 **LACUNA (CRÍTICA)**: O frontend está totalmente desacoplado da lógica dinâmica de renderização de resultados e cálculo de KPIs após a conclusão da alocação assíncrona. Os endpoints `/api/v1/allocation/run` e `/api/v1/allocation/status/{taskId}` não existem no backend. Toda a exibição de resultados na tabela de leilões e os números de economia energética/ocupação em tela após o polling fechar são dados mockados estáticos codados diretamente nos scripts do `index.html`.
