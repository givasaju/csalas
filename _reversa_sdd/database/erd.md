# ERD completo do banco de dados

`mermaid
erDiagram
    AllocationTask {
        UUID id PK
        VARCHAR status
        TIMESTAMP created_at
        TIMESTAMP updated_at
        INTEGER progress
        TEXT error_log
        JSONB result_summary
    }
    AuctionBid {
        UUID id PK
        UUID task_id FK
        UUID room_id
        VARCHAR time_slot
        UUID winner_coordination_id
        UUID loser_coordination_id
        INTEGER credits_spent
        TIMESTAMP timestamp
    }
    Coordination {
        INTEGER credits
    }
    AllocationTask ||--o{ AuctionBid :  has
    Coordination ||--o{ AuctionBid : winner/loser
`
