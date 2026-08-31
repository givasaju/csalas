# Requirements: Implementar o motor de alocação core-allocation-engine

> Identificador: `001-implementar-core-allocation`  
> Data: `2026-08-07`  
> Pasta da extração reversa: `_reversa_sdd/`  
> Confidência: 🟢 CONFIRMADO, 🟡 INFERIDO, 🔴 LACUNA / DÚVIDA  

---

## 1. Resumo executivo

Esta feature entrega a implementação do motor de inteligência artificial de alocação de salas `core-allocation-engine` para o ClassSync AI. Ele processará as demandas de espaço e restrições horárias das coordenações, executará um algoritmo de leilão cooperativo multiagente (com créditos) para mediar concorrência e otimizará a ocupação predial agrupando turmas para reduzir custos de energia do campus. Não descreve a UI nem o banco de dados diretamente, focando exclusivamente na inteligência de alocação e mediação.

---

## 2. Contexto a partir do legado

As definições do motor de alocação baseiam-se diretamente nos documentos concebidos e especificados no refinamento greenfield de design de software:

| Fonte | Trecho relevante | Confidência |
|-------|------------------|-------------|
| `_reversa_sdd/prd.md#4. Escopo (in)` | O motor de inteligência artificial baseado em restrições e regras flexíveis. | 🟡 |
| `_reversa_sdd/sdd/core-allocation-engine.md#1. Resumo` | O motor é responsável por processar as restrições prediais e mediar disputas por leilão. | 🟡 |
| `_reversa_sdd/sdd/core-allocation-engine.md#6. Requisitos Funcionais` | Requisitos de validação de restrições rígidas, fitness predial e leilão de créditos. | 🟡 |

---

## 3. Personas e cenários de uso

| Persona | Objetivo | Cenário-chave |
|---------|----------|---------------|
| **Cláudio (Coordenador de Curso)** | Obter salas adequadas para suas disciplinas sem entrar em debates exaustivos. | Submeter as restrições horárias de seus docentes e verificar se a IA resolveu conflitos via leilão automático de créditos. |
| **Isabela (Diretora de Infraestrutura)** | Reduzir custos energéticos operacionais do campus agrupando turmas eficientemente. | Monitorar o fechamento de blocos acadêmicos ociosos com base na otimização predial gerada pela IA. |

---

## 4. Regras de negócio novas ou alteradas

1. **RN-01:** Prioridade absoluta a restrições mandatórias (hard constraints: acessibilidade, capacidade física mínima compatível com número de alunos, tipo de sala/laboratório). 🟡
   - Origem no legado: `_reversa_sdd/sdd/core-allocation-engine.md#6.1 Requisitos Principais (RF-01)`
   - Tipo: nova
2. **RN-02:** Otimização de eficiência energética predial (agrupamento de turmas no menor número de blocos prediais ativos possíveis). 🟡
   - Origem no legado: `_reversa_sdd/sdd/core-allocation-engine.md#6.1 Requisitos Principais (RF-02)`
   - Tipo: nova
3. **RN-03:** Resolução de concorrência e mediação automática via leilão de créditos de prioridade acadêmica acumulados. As coordenações iniciam com saldo igual de 1000 créditos a cada início de semestre acadêmico. 🟡
   - Origem no legado: `_reversa_sdd/sdd/core-allocation-engine.md#6.1 Requisitos Principais (RF-03)`
   - Tipo: nova

---

## 5. Requisitos Funcionais

| ID | Requisito | Prioridade | Critério de aceite | Confidência |
|----|-----------|------------|--------------------|-------------|
| RF-01 | O motor de IA deve validar que nenhuma alocação de sala viole as restrições mandatórias acadêmicas e prediais. | Must | Rodar simulações de teste e verificar se todas as turmas atendem a acessibilidade e recursos mínimos obrigatórios. | 🟡 |
| RF-02 | O algoritmo de alocação central deve agrupar as turmas para maximizar o fechamento temporário de blocos de baixa ocupação predial. | Must | Validar se blocos prediais com menos de 20% de ocupação esperada são esvaziados e consolidados em outros blocos ativos. | 🟡 |
| RF-03 | O sistema de leilão cooperativo deve decrementar os créditos de prioridade da coordenação vencedora e compensar/transferir créditos à perdedora. | Must | Executar leilão piloto entre Engenharia (mais créditos) e Letras; validar que Engenharia ganha a sala, e Letras recebe créditos compensatórios no final. | 🟡 |
| RF-04 | O motor deve suspender a negociação e emitir status de arbitragem manual se o conflito persistir após 5 rodadas do leilão automático. | Should | Rodar cenário com demandas idênticas e verificar se o motor interrompe o loop e gera status `pending_arbitration`. | 🟡 |

---

## 6. Requisitos Não Funcionais

| Tipo | Requisito | Evidência ou justificativa | Confidência |
|------|-----------|----------------------------|-------------|
| Desempenho | Tempo de convergência do algoritmo de alocação global < 10 minutos para 500 turmas e 100 salas concorrentes. Se o processamento exceder o tempo limite, ele deve ser executado de forma totalmente assíncrona em background. | Exigência operacional no início do semestre acadêmico. | 🟡 |
| Segurança | O motor de IA só deve ser acionável via conexões internas autenticadas de backend de administração. | Proteção da integridade das grades horárias acadêmicas contra alterações indevidas. | 🟡 |
| Observabilidade | Emissão de logs verbosos das rodadas de negociação, propostas (bids) de cada agente ACC e transações de créditos. | Essencial para fins de auditoria de decisões tomadas autonomamente pela IA. | 🟡 |

---

## 7. Critérios de Aceitação

```gherkin
Cenário: Alocação bem-sucedida e otimizada predialmente
  Dado que o campus possui 3 blocos prediais cadastrados e 50 turmas ativas
  Quando o motor de alocação de IA é executado
  Então o sistema deve alocar todas as salas sem conflitos e agrupar as disciplinas no menor número de blocos possíveis, indicando quais blocos podem ser fechados para economia predial.

Cenário: Empate persistente no leilão cooperativo de salas
  Dado que o curso de Direito e Engenharia disputam a mesma sala 202 com créditos zerados e restrições idênticas
  Quando a negociação atinge a 5ª rodada de lances empatados
  Então o motor de IA deve suspender a sala 202, atribuir o status "pending_arbitration" e acionar o alerta para Isabela.
```

---

## 8. Prioridade MoSCoW

| Item | MoSCoW | Justificativa |
|------|--------|---------------|
| RF-01 | Must | Mandatório para viabilizar as aulas básicas (professores/alunos e acessibilidade). |
| RF-02 | Must | Objetivo de negócio primário de redução de custos operacionais do campus. |
| RF-03 | Must | Base da mediação multiagente sem intervenção humana frequente. |
| RF-04 | Should | Importante para evitar loops infinitos de negociação na IA quando houver empates reais. |

---

## 9. Esclarecimentos

### Sessão 2026-08-07
- **Q:** Qual a estratégia de escalabilidade se o leilão demorar mais de 10 minutos para universidades grandes?
- **R:** Execução totalmente assíncrona (background) com fila de processamento e notificação ao finalizar.
- **Q:** Como devem ser inseridos os créditos de leilão históricos das coordenações no ClassSync AI?
- **R:** Carga automática: inicializar todas as coordenações com saldo igual (ex: 1000 créditos) a cada início de semestre.

---

## 10. Lacunas

Nenhuma pendência ou lacuna não resolvida.

---

## 11. Histórico de alterações

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-08-07 | Versão inicial gerada por `/reversa-requirements` | reversa |
| 2026-08-07 | Dúvidas de escalabilidade e créditos resolvidas em sessão de clarify | reversa |
