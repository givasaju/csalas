# Regression Watch: Implementar o gerenciador acadêmico academic-space-manager

> Identificador: `002-implementar-space-manager`  
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

Estes itens representam as funcionalidades implementadas a partir da especificação `academic-space-manager.md`. Eles devem ser convertidos em regras de regressão principal assim que a primeira rodada de descoberta do `/reversa` extrair e confirmar o código escrito como 🟢:

| ID | Origem da Spec | Requisito Esperado | Verificação Recomendada |
|----|----------------|--------------------|-------------------------|
| W001 | `_reversa_sdd/sdd/academic-space-manager.md#RF-01` | CRUD de salas com dados de tipo, acessibilidade e recursos. | Chamar POST `/api/v1/rooms` e verificar inserção. |
| W002 | `_reversa_sdd/sdd/academic-space-manager.md#RF-02` | Validação de capacidade de salas > 0. | Testar inserção com capacidade 0 ou menor e verificar HTTP 422. |
| W003 | `_reversa_sdd/sdd/academic-space-manager.md#RF-03` | Importação em lote transacional Tudo ou Nada de arquivos CSV. | Submeter arquivo com erro e confirmar que nada é persistido. |
| W004 | `_reversa_sdd/sdd/academic-space-manager.md#RF-04` | Reset semestral de todas as restrições docentes cadastradas. | Chamar DELETE `/api/v1/allocation/restrictions` e validar limpeza. |
| W005 | `_reversa_sdd/sdd/academic-space-manager.md#RF-05` | Endpoint GET `/api/v1/allocation/input-data` contendo insumos consolidados. | Chamar rota e verificar se o JSON traz a tipagem e dados corretos. |
