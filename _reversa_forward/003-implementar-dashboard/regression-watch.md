# Regression Watch: Implementar a interface visual occupancy-dashboard

> Identificador: `003-implementar-dashboard`  
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

Estes itens representam as funcionalidades implementadas a partir da especificação `occupancy-dashboard.md`. Eles devem ser convertidos em regras de regressão principal assim que a primeira rodada de descoberta do `/reversa` extrair e confirmar o código escrito como 🟢:

| ID | Origem da Spec | Requisito Esperado | Verificação Recomendada |
|----|----------------|--------------------|-------------------------|
| W001 | `_reversa_sdd/sdd/occupancy-dashboard.md#RF-01` | Renderização de cards de KPIs (Ocupação, Economia, Blocos, Conflitos). | Validar presença dos elementos com IDs na UI. |
| W002 | `_reversa_sdd/sdd/occupancy-dashboard.md#RF-02` | Extrato de auditoria de leilões e compensações de créditos das coordenações. | Verificar renderização das linhas de leilão na tabela. |
| W003 | `_reversa_sdd/sdd/occupancy-dashboard.md#RF-03` | Botão interativo para disparo do motor de alocação de salas em lote. | Clicar no botão e verificar início do processamento de status. |
| W004 | `_reversa_sdd/sdd/occupancy-dashboard.md#RF-04` | Visualização de Skeleton loading (Shimmer animation) em carregamento. | Verificar presença de classes CSS `shimmer` nos estados lentos. |
| W005 | `_reversa_sdd/sdd/occupancy-dashboard.md#RF-05` | Polling dinâmico para barramento de andamento da IA em execução. | Verificar atualização da largura da barra de progresso. |
