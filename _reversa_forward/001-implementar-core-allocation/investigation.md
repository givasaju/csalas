# Investigation: core-allocation-engine

## 1. Pesquisa de fundo

O problema de alocação de salas (Classroom Assignment Problem - CAP) é uma variante bem conhecida de coloração de grafos e satisfação de restrições, classificada como NP-difícil. Em ambientes institucionais reais, o maior desafio não é apenas matemático, mas político: as coordenações possuem preferências e rivalidades históricas quanto a determinados blocos e salas de aula. 

Para resolver isso, adotamos uma modelagem de **Sistemas Multiagentes (SMA)** integrada a um **Leilão Cooperativo**. O protocolo escolhido é baseado no *Contract Net Protocol (CNP)*, onde os agentes submetem propostas de alocação. Em caso de conflito de salas, o Agente Mediador (AMR) organiza um leilão de lances fechados usando créditos acumulados como peso moderador.

## 2. Alternativas avaliadas

### Alternativa A: Programação Linear Inteira Misturada (MILP)
*   *Descrição:* Resolução global utilizando um solver como Pulp ou Google OR-Tools.
*   *Prós:* Garante a otimalidade teórica global absoluta de salas alocadas.
*   *Contras:* Complexo de depurar quando as restrições são contraditórias (o solver apenas retorna "inviável", sem explicar o culpado predial). Não oferece um mecanismo natural de negociação justa (como os créditos) que faça sentido para os coordenadores.

### Alternativa B: Sistemas Multiagentes com Leilão de Créditos (Adotado)
*   *Descrição:* Cada coordenação possui um ACC que defende seus interesses, e o leilão é conduzido de forma isolada para cada conflito residual pós-alocação inicial do AAC.
*   *Prós:* Modularidade total de regras, facilidade de auditoria (sabemos exatamente porque um curso perdeu a sala Y) e alto realismo na dinâmica acadêmica de compensação por créditos.
*   *Contras:* Pode levar a ótimos ligeiramente locais em vez do ótimo matemático absoluto global, contudo é amplamente aceitável e computacionalmente muito mais rápido.

---

## 3. Padrões aplicáveis

*   **FIPA Contract Net Interaction Protocol:** Padrão clássico de interação multiagente para distribuição de tarefas e recursos concorrentes.
*   **Asynchronous Task Queue (Fila Assíncrona):** Padrão produtor-consumidor para processar a computação em segundo plano sem travar a thread de requisições de controle.
