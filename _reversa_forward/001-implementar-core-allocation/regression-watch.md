# Regression Watch: Implementar o motor de alocação core-allocation-engine

> Identificador: `001-implementar-core-allocation`  
> Cenário: Greenfield (sem regras 🟢 extraídas previamente do legado)  

---

## 1. Watch Principal (Verificações de Regressão)

| ID | Origem (arquivo, seção) | Regra esperada após mudança | Tipo de verificação | Sinal de violação |
|----|-------------------------|-----------------------------|---------------------|-------------------|
| - | - | Nenhuma regra extraída do legado para vigiar nesta feature greenfield. | - | - |

---

## 2. Histórico de re-extrações

*   *(Seção vazia, a ser populada pelas próximas extrações do `/reversa`)*

---

## 3. Arquivadas

*   *(Seção vazia)*

---

## 4. Observações (Requisitos da Spec SDD a serem vigiados após a re-extração)

Estes itens representam as funcionalidades implementadas a partir da especificação `core-allocation-engine.md`. Eles devem ser convertidos em regras de regressão principal assim que a primeira rodada de descoberta do `/reversa` extrair e confirmar o código escrito como 🟢:

| ID | Origem da Spec | Requisito Esperado | Verificação Recomendada |
|----|----------------|--------------------|-------------------------|
| W001 | `_reversa_sdd/sdd/core-allocation-engine.md#RF-01` | Respeito estrito de restrições mandatórias (acessibilidade, capacidade, recursos). | Validar se nenhuma turma é alocada fora dessas restrições. |
| W002 | `_reversa_sdd/sdd/core-allocation-engine.md#RF-02` | Heurística de fitness predial e esvaziamento de blocos subocupados (< 20%). | Validar agrupamento de blocos. |
| W003 | `_reversa_sdd/sdd/core-allocation-engine.md#RF-03` | Arbitragem de conflitos concorrentes via leilão com lances de créditos das coordenações. | Validar transferência/compensação de saldos. |
| W004 | `_reversa_sdd/sdd/core-allocation-engine.md#RF-04` | Suspensão e status de arbitragem física (`pending_arbitration`) após 5 rodadas de empate. | Validar limite máximo de iterações do loop. |
| W005 | `_reversa_sdd/sdd/core-allocation-engine.md#RF-05` | Endpoints de rotas de disparo assíncrono e consulta de status. | Validar respostas da API HTTP. |
