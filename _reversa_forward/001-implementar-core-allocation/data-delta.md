# Data Delta: core-allocation-engine

Este documento apresenta as novas entidades e modificações necessárias no modelo de dados conceitual em relação à especificação inicial para suportar a funcionalidade de alocação multiagente.

---

## 1. Novas Entidades

### `AllocationTask`
Persiste o status de execução assíncrona do motor em background.

```
AllocationTask {
  id: uuid                  // Chave primária
  status: string            // queued, running, completed, failed, pending_arbitration
  created_at: timestamp
  updated_at: timestamp
  progress: integer         // Porcentagem (0 a 100) de progresso
  error_log: text           // Log de erro caso status == failed
  result_summary: jsonb     // Estatísticas resumidas da alocação final
}
```

### `AuctionBid`
Armazena a auditoria dos lances dados em leilões concorrentes de salas.

```
AuctionBid {
  id: uuid
  task_id: uuid             // FK para AllocationTask
  room_id: uuid             // Sala disputada
  time_slot: string         // Horário da concorrência
  winner_coordination_id: uuid
  loser_coordination_id: uuid
  credits_spent: integer    // Créditos debitados do vencedor e compensados ao perdedor
  timestamp: timestamp
}
```

---

## 2. Entidades Modificadas

### `Coordination` (Coordenação de Curso)
Adição de campo para controle de saldo de créditos para o leilão.

```diff
 Coordination {
   id: uuid
   name: string
+  credits: integer         // Saldo atual de créditos (inicializado com 1000)
 }
```

### `AllocationRun` (Rodada de Alocação)
Vínculo com a tarefa assíncrona executada.

```diff
 AllocationRun {
   id: uuid
   status: string
   started_at: datetime
   completed_at: datetime
+  task_id: uuid            // FK opcional para AllocationTask
   optimized_blocks: list
 }
```

---

## 3. Migrações e Inicializações

1. Criar tabelas `AllocationTask` e `AuctionBid`.
2. Adicionar a coluna `credits` com valor padrão `1000` na tabela de Coordenação.
3. Adicionar coluna `task_id` na tabela de Rodada de Alocação.
