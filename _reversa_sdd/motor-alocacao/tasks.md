# Unit: motor-alocacao, Tarefas de Implementação

> Roteiro de tarefas sequenciais para a reconstrução/implementação da unidade do motor de alocação.

## Pré-requisitos
- Ambientes e interpretador Python 3 configurados no projeto.
- Dicionário de dados mapeado para as entidades `Class`, `Room`, `Coordination` e `AuctionBid`.
- Dependência do logger configurada conforme RNF-03 de Observabilidade.

## Tarefas

- [ ] **T-01: Implementação das classes ACC e AMR**
  - **Origem no legado**: [`src/engine/agents.py:6-83`](file:///c:/csalas/src/engine/agents.py#L6-L83)
  - **Critério de pronto**: Criar as classes `ACC` (Agente Coordenador de Curso) e `AMR` (Agente Mediador e Reputação) com as lógicas de lances proporcionais (teto de 20% do saldo), dedução/compensação cooperativa e desempate por saldo total.
  - **Confiança**: 🟢
- [ ] **T-02: Implementação do BuildingOptimizer**
  - **Origem no legado**: [`src/engine/optimization.py:6-133`](file:///c:/csalas/src/engine/optimization.py#L6-L133)
  - **Critério de pronto**: Criar o método estático `optimize_building_occupancy` que calcula taxas de ocupação predial, identifica blocos com `< 20%` de utilização e realiza o remanejamento condicional das turmas respeitando as restrições rígidas.
  - **Confiança**: 🟢
- [ ] **T-03: Implementação da orquestração principal (CoreAllocationEngine)**
  - **Origem no legado**: [`src/engine/core.py:10-158`](file:///c:/csalas/src/engine/core.py#L10-L158)
  - **Critério de pronto**: Criar a classe `CoreAllocationEngine` integrando a alocação gulosa por tamanho justo, o loop de colisões do leilão limitado a 5 iterações, realocação em caso de derrota e consolidação predial de blocos.
  - **Confiança**: 🟢

---

## Tarefas de Teste

- [ ] **TT-01: Teste do happy path da alocação inicial (AAC)**
  - **Origem no legado**: [`tests/test_constraints.py`](file:///c:/csalas/tests/test_constraints.py)
  - **Critério de pronto**: Testar que turmas são alocadas com sucesso respeitando todas as restrições rígidas (capacidade, tipo, acessibilidade e recursos).
- [ ] **TT-02: Teste da arbitragem por leilão**
  - **Origem no legado**: [`tests/test_auction.py`](file:///c:/csalas/tests/test_auction.py)
  - **Critério de pronto**: Forçar um conflito de horário e validar se o AMR resolve a disputa em favor do maior lance, deduz créditos do vencedor, recompensa o perdedor e tenta realocá-lo.
- [ ] **TT-03: Teste da otimização predial (BuildingOptimizer)**
  - **Origem no legado**: [`tests/test_building_optimization.py`](file:///c:/csalas/tests/test_building_optimization.py)
  - **Critério de pronto**: Validar se turmas em blocos com baixa ocupação são migradas corretamente e se o bloco de origem é listado como desativado.

---

## Ordem Sugerida
1. **T-01** (Agentes) e **T-02** (Otimizador) por serem unidades de lógica isoladas.
2. **T-03** (Engine) para orquestrar as unidades implementadas.
3. Testes automatizados (**TT-01**, **TT-02**, **TT-03**).

---

## Lacunas Pendentes (🔴)
- **Persistência de Transações e Tarefas**: O legado não possui integração com banco relacional para gravar o histórico de leilões (`AuctionBid`) e o estado do worker (`AllocationTask`), operando somente em memória volátil. Decidir a forma de persistência real antes de iniciar o desenvolvimento.
