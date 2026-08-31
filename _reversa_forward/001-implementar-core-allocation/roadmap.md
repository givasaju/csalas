# Roadmap: Implementar o motor de alocação core-allocation-engine

> Identificador: `001-implementar-core-allocation`  
> Data: `2026-08-07`  
> Requirements: `_reversa_forward/001-implementar-core-allocation/requirements.md`  
> Confidência: 🟢 CONFIRMADO, 🟡 INFERIDO, 🔴 LACUNA  

---

## 1. Resumo da abordagem

A implementação do motor `core-allocation-engine` usará uma arquitetura multiagente cooperativa modelada em Python Puro (com POO estruturada). Cada coordenação de curso será controlada por um Agente Coordenador de Curso (ACC) e o campus será governado pelo Agente Alocador Central (AAC), sob a supervisão e arbitragem do Agente Mediador e Reputação (AMR). 

Os conflitos de concorrência por salas serão resolvidos através de um leilão de lances fechados em rodadas rápidas, utilizando créditos acadêmicos como moeda de barganha. O agrupamento físico de turmas em blocos eficientes utilizará uma heurística gulosa de agrupamento predial para otimizar os custos com energia elétrica do campus. O motor rodará em segundo plano de forma assíncrona, notificando o chamador ao finalizar.

---

## 2. Princípios aplicados

Não há princípios específicos cadastrados no arquivo `.reversa/principles.md` deste projeto.

---

## 3. Decisões técnicas

| ID | Decisão | Justificativa | Alternativas descartadas | Confidência |
|----|---------|----------------|--------------------------|-------------|
| D-01 | **Modelagem em POO Multiagente descentralizada** | Permite representar as coordenações como entidades autônomas com regras políticas e créditos de leilão individuais. | Solução determinística em bloco único via Programação Inteira Linear (Solver Pulp/GLPK). | 🟡 |
| D-02 | **Processamento em Fila Assíncrona** | Garante que requisições de universidades grandes com milhares de turmas não gerem timeouts na API, rodando em background. | Execução síncrona no corpo da requisição HTTP do painel de administração. | 🟢 |
| D-03 | **Mecanismo de Créditos Fixos Reajustados** | As coordenações iniciam com 1000 créditos a cada início de período letivo para equilibrar o poder de negociação de forma justa. | Acúmulo de créditos cumulativos históricos sem reset semestral. | 🟢 |

---

## 4. Premissas

Nenhuma premissa sob dúvida ativa. Todas as questões levantadas no `requirements.md` foram completamente clarificadas.

---

## 5. Delta arquitetural

A arquitetura do projeto será expandida com a adição das definições do motor de IA:

| Componente | Arquivo de origem no legado | Tipo de mudança | Resumo |
|------------|------------------------------|-----------------|--------|
| **core-allocation-engine** | `_reversa_sdd/sdd/core-allocation-engine.md` | componente-novo | Módulo em Python responsável pela IA multiagente e resolução de conflitos. |

---

## 6. Delta no modelo de dados

- Resumo das mudanças: Criação de tabelas para auditoria de transações do leilão e saldo de créditos das coordenações, além de tabela de controle de jobs assíncronos.
- Detalhe completo em: `_reversa_forward/001-implementar-core-allocation/data-delta.md`

---

## 7. Delta de contratos externos

| Contrato | Tipo | Arquivo de detalhe |
|----------|------|--------------------|
| **allocation-api** | HTTP | `_reversa_forward/001-implementar-core-allocation/interfaces/allocation-api.md` |

---

## 8. Plano de migração

Como o projeto opera sob contexto greenfield recém-criado, nenhuma migração de dados legados é aplicável.
1. Executar as DDLs de criação de tabelas iniciais.
2. Inserir dados de teste e inicialização (seed) contendo salas, professores e as coordenações com 1000 créditos cada.

---

## 9. Riscos e mitigações

| Risco | Impacto | Probabilidade | Mitigação |
|-------|---------|---------------|-----------|
| Lentidão de convergência em leilões concorrentes | médio | baixa | Limitar rodadas de ofertas de lances (bids) a no máximo 5 iterações por conflito predial. |
| Inconsistências temporárias de dados ao rodar assincronamente | médio | média | Bloquear edição de dados acadêmicos pelo Space Manager enquanto uma rodada de alocação estiver ativamente rodando. |

---

## 10. Critério de pronto

- [ ] Todas as ações do `actions.md` marcadas `[X]`
- [ ] `regression-watch.md` gerado
- [ ] Testes de integração simulando leilão e convergência passando com 100% de cobertura de cenários de concorrência.

---

## 11. Histórico de alterações

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-08-07 | Versão inicial gerada por `/reversa-plan` | reversa |
