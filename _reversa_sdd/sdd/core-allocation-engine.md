# Spec: core-allocation-engine

**Versão:** 1.0  
**Status:** Rascunho  
**Autor:** reversa-spec-sdd  
**Data:** 2026-08-07  
**Reviewers:** N/A  

---

## 1. Resumo

O `core-allocation-engine` é o motor de inteligência artificial do ClassSync AI. Ele é responsável por processar as grades de horários e demandas acadêmicas, calcular a distribuição otimizada das salas de aula no campus através de restrições e preferências prediais, e mediar disputas entre coordenações via leilão cooperativo baseado em créditos de prioridade.

---

## 2. Contexto e Motivação

**Problema:**  
A alocação de salas é um problema de otimização combinatória NP-difícil. Coordenações disputam os mesmos espaços físicos, gerando impasses que atrasam o semestre e causam ociosidade de salas especiais (ex: laboratórios) ao mesmo tempo que causam custos energéticos altos por manter blocos inteiros abertos para poucas turmas.

**Evidências:**  
Semestre letivo iniciando com atrasos nas grades de horários e reconfigurações manuais constantes de salas devido a conflitos não detectados previamente.

**Por que agora:**  
A instituição precisa cortar custos operacionais com infraestrutura (energia, limpeza) e centralizar a distribuição de salas sem sobrecarregar as coordenações com negociações manuais exaustivas.

---

## 3. Goals (Objetivos)

- [ ] G-01: 🟡 Resolver 100% dos conflitos de salas e horários antes do início das aulas.
- [ ] G-02: 🟡 Maximizar a eficiência operacional agrupando turmas no menor número de blocos físicos possíveis.
- [ ] G-03: 🟡 Garantir a satisfação das coordenações por meio de uma negociação baseada em regras justas de crédito.

**Métricas de sucesso:**  
| Métrica | Baseline atual | Target | Prazo |
|---------|---------------|--------|-------|
| 🟡 Ociosidade de assentos | 40% de assentos vazios | < 15% de assentos vazios | 3 meses |
| 🟡 Tempo de convergência | Dias de negociação manual | < 10 minutos de processamento | Início do semestre |
| 🟡 Blocos abertos desnecessariamente | 4 blocos com baixa ocupação | < 1 bloco de baixa ocupação | 3 meses |

---

## 4. Non-Goals (Fora do Escopo)

- NG-01: 🟡 Gerenciamento financeiro ou cálculo de salários dos professores.
- NG-02: 🟡 Integração física ou conexão em tempo real com sensores IoT prediais (a eficiência é estimada e declarada logicamente).
- NG-03: 🟡 Controle e marcação de presença dos alunos.

---

## 5. Usuários e Personas

**Usuário primário:** 🟡 Cláudio (Coordenador de Curso), que submete demandas e participa das reallocações automáticas.  
**Usuário secundário:** 🟡 Isabela (Diretora de Infraestrutura), que define as metas operacionais de economia energética do campus.  

**Jornada atual (sem a feature):**  
1. 🟡 O coordenador envia sua grade ideal por e-mail para a equipe de infraestrutura.  
2. 🟡 A infraestrutura descobre conflitos de salas manualmente em planilhas Excel.  
3. 🟡 Os coordenadores realizam reuniões exaustivas para decidir quem cede a sala.  
4. 🟡 As salas são alocadas de forma estática e ineficiente, deixando blocos abertos quase vazios.  

**Jornada futura (com a feature):**  
1. 🟡 O coordenador submete suas restrições e demandas no sistema ClassSync AI.  
2. 🟡 O motor de alocação de IA roda o algoritmo e detecta conflitos concorrentes.  
3. 🟡 Os agentes dos coordenadores (ACC) negociam salas via leilão mediado pelo AMR de forma automática.  
4. 🟡 O sistema consolida as turmas em blocos eficientes e apresenta a alocação final sem conflitos.  

---

## 6. Requisitos Funcionais

### 6.1 Requisitos Principais

| ID | Requisito | Prioridade | Critério de Aceite |
|----|-----------|-----------|-------------------|
| RF-01 | 🟡 O sistema deve processar restrições mandatórias (capacidade da sala, laboratório especializado, acessibilidade) como prioridade absoluta. | Must | 🟡 Verificar se nenhuma turma foi alocada em sala menor que seu tamanho ou sem acessibilidade obrigatória. |
| RF-02 | 🟡 O sistema deve calcular uma função de aptidão (fitness) predial para agrupar turmas no menor número de blocos prediais ativos possíveis. | Must | 🟡 Validar se turmas de horários com baixa densidade são aglutinadas no mesmo bloco. |
| RF-03 | 🟡 O sistema deve permitir que os agentes de coordenação (ACC) negociem salas concorrentes usando créditos acadêmicos como moeda. | Must | 🟡 Testar leilão concorrente: a coordenação com mais créditos e maior urgência ganha a sala desejada, enquanto a outra recebe créditos compensatórios. |
| RF-04 | 🟡 O sistema deve permitir a arbitragem manual pela diretoria de infraestrutura se a negociação dos agentes falhar após o número limite de iterações. | Must | 🟡 Gerar um conflito irreconciliável de prioridades iguais e verificar se o sistema notifica a diretoria para arbitragem. |
| RF-05 | 🟡 O sistema deve recalcular dinamicamente a alocação de uma sala específica caso ocorra um imprevisto reportado (ex: ar-condicionado quebrado). | Should | 🟡 Simular falha de sala no sistema e verificar se as turmas daquela sala são reallocadas automaticamente sem alterar o resto da grade consolidada. |

### 6.2 Fluxo Principal (Happy Path)

1. 🟡 O sistema recebe o sinal de início de processamento de alocação semestral.  
2. 🟡 O Agente Alocador Central (AAC) lê as demandas e restrições de todos os cursos.  
3. 🟡 O AAC calcula uma alocação inicial baseada em restrições mandatórias.  
4. 🟡 Para cada conflito de concorrência de sala, os ACCs iniciam um leilão automático mediado pelo AMR.  
5. 🟡 Os ACCs resolvem os conflitos usando créditos de prioridade acumulada.  
6. 🟡 O sistema consolida as salas, otimiza o uso energético (agrupando por blocos) e salva a grade final.  

### 6.3 Fluxos Alternativos

**Fluxo Alternativo A — Conflito Empatado Sem Créditos:**  
1. 🟡 Dois ACCs disputam a mesma sala com prioridades e créditos idênticos.  
2. 🟡 O Agente Mediador (AMR) detecta empate após 3 rodadas de oferta.  
3. 🟡 O AMR congela a sala e gera uma pendência de arbitragem manual para a Diretora de Infraestrutura.  

---

## 7. Requisitos Não-Funcionais

| ID | Requisito | Valor alvo | Observação |
|----|-----------|-----------|------------|
| RNF-01 | Performance | 🟡 Tempo de processamento < 10 minutos | Para uma instituição com 500 turmas e 100 salas de aula concorrentes. |
| RNF-02 | Escalabilidade | 🟡 Suportar alocação de até 2000 turmas | Simula universidades de grande porte. |
| RNF-03 | Segurança | 🟡 Autenticação e autorização rígidas | Apenas coordenadores autorizados podem iniciar leilões ou alterar restrições. |

---

## 8. Design e Interface

**Componentes afetados:**  
- API de Processamento de IA (`/api/v1/allocation/run`)  
- Módulo de Mensageria e Eventos Multiagente (WebSockets / Filas de Mensagens internas)  

**Comportamento esperado:**  
- 🟡 O motor emite eventos de progresso durante o cálculo ("Alocando salas...", "Negociando conflitos...", "Otimizando consumo predial...") para que o frontend exiba uma barra de carregamento dinâmica.  
- 🟡 Em caso de erro na execução do algoritmo, o motor retorna um status de falha detalhado apontando a restrição contraditória que causou o travamento.  

---

## 9. Modelo de Dados

**Entidades novas ou modificadas:**  
```
AllocationRun {
  id: string              // Identificador único da rodada
  status: string          // running, completed, failed, pending_arbitration
  started_at: datetime
  completed_at: datetime
  optimized_blocks: list  // IDs dos blocos otimizados/ativos
}

AuctionTransaction {
  id: string
  room_id: string
  winner_acc_id: string
  loser_acc_id: string
  credits_spent: integer
  timestamp: datetime
}
```

---

## 10. Integrações e Dependências

| Dependência | Tipo | Impacto se indisponível |
|-------------|------|------------------------|
| Banco de dados de Gestão Acadêmica (Space Manager) | Obrigatória | O motor não inicia, pois precisa carregar as turmas, salas e restrições. |

---

## 11. Edge Cases e Tratamento de Erros

| Cenário | Trigger | Comportamento esperado |
|---------|---------|----------------------|
| EC-01: 🟡 Restrição impossível de resolver | Duas turmas com requisitos mandatórios incompatíveis (ex: ambas precisam da única sala acessível do campus no mesmo horário) | 🟡 O sistema suspende a alocação dessas duas turmas, marca status `pending_arbitration` e notifica o administrador, prosseguindo com as outras. |
| EC-02: 🟡 Loop de negociação infinita | ACCs programados de forma competitiva agressiva não cedem em rodadas sucessivas | 🟡 O AMR interrompe o leilão após a 5ª rodada de lances empatados, divide a sala ao meio (se viável) ou envia para decisão da reitoria (arbitragem manual). |
| EC-03: 🟡 Timeout / Indisponibilidade de Integração | Falha de conexão ou timeout na comunicação com o banco do Space Manager ao iniciar | 🟡 O motor suspende a execução, registra log de erro detalhado com o status da tentativa, e emite alerta visual de falha de conexão na tela de Isabela. |
| EC-04: 🟡 Payload / Input de dados inválido | Dados de turma contendo número de alunos negativo ou campos nulos obrigatórios | 🟡 O motor valida os dados na entrada, rejeita o registro problemático gerando um alerta de dados corrompidos para a coordenação responsável e prossegue com as demais turmas saudáveis. |

---

## 12. Segurança e Privacidade

- **Autenticação:** 🟡 Acesso ao motor via chaves de API restritas ao backend administrativo do ClassSync AI.  
- **Autorização:** 🟡 Apenas a Diretora de Infraestrutura (Isabela) pode acionar o motor de otimização global.  

---

## 13. Plano de Rollout

- **Estratégia:** 🟡 Rollout em ambiente de simulação (sandbox) usando dados históricos do semestre anterior para validar a eficiência da alocação de IA antes de aplicar em produção.  

---

## 14. Open Questions

| # | Pergunta | Impacto | Dono | Prazo |
|---|---------|---------|------|-------|
| OQ-01 | 🟡 Qual o limite máximo aceitável de créditos que um ACC pode acumular ou gastar por rodada? | Médio | IA Architect | Início do desenvolvimento |

---

## 15. Decisões Tomadas (Decision Log)

| Decisão | Alternativas consideradas | Racional |
|---------|--------------------------|---------|
| 🟡 Uso de leilão de créditos acadêmicos para mediação | Alocação pura por ordem de chegada ou força bruta centralizada | Evita privilégios arbitrários e simula uma negociação humana mais justa e flexível. |

---

## Avaliação de Qualidade

```
============================================================
  SPEC QUALITY REPORT
  Arquivo: _reversa_sdd/sdd/core-allocation-engine.md
============================================================

  SCORE TOTAL: 100.0/100  —  ⭐ Excelente — Pronta para implementação

  BREAKDOWN POR DIMENSÃO:
  Dimensão             Score      Peso     Contribuição
  --------------------------------------------------
  Completude           100%       30%     30.0/pt
  Testabilidade        100%       25%     25.0/pt
  Clareza              100%       20%     20.0/pt
  Escopo               100%       15%     15.0/pt
  Edge Cases           100%       10%     10.0/pt

  ✅ PONTOS FORTES:
     ✅ Seção 1 (Resumo) presente e preenchida
     ✅ Seção 2 (Contexto) presente e preenchida
     ✅ Seção 3 (Goals) presente e preenchida
     ✅ Seção 4 (Non-Goals) presente e preenchida
     ✅ Seção 5 (Usuários) presente e preenchida
     ✅ Cobertura adequada de edge cases
============================================================
```

