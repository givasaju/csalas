-- DDL para criação das tabelas adicionais e delta de dados da alocação de salas

-- Alteração da tabela Coordination (Coordenação de Curso) para incluir créditos
ALTER TABLE Coordination ADD COLUMN IF NOT EXISTS credits INTEGER DEFAULT 1000;

-- Tabela de tarefas assíncronas de alocação (AllocationTask)
CREATE TABLE IF NOT EXISTS AllocationTask (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    status VARCHAR(50) NOT NULL DEFAULT 'queued', -- queued, running, completed, failed, pending_arbitration
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    progress INTEGER DEFAULT 0,
    error_log TEXT,
    result_summary JSONB
);

-- Tabela de auditoria de transações do leilão cooperativo (AuctionBid)
CREATE TABLE IF NOT EXISTS AuctionBid (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    task_id UUID REFERENCES AllocationTask(id) ON DELETE CASCADE,
    room_id UUID NOT NULL,
    time_slot VARCHAR(10) NOT NULL,
    winner_coordination_id UUID NOT NULL,
    loser_coordination_id UUID NOT NULL,
    credits_spent INTEGER NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de subslots de horários e intervalos de aulas (subslot_time_intervals)
CREATE TABLE IF NOT EXISTS subslot_time_intervals (
    id VARCHAR(36) PRIMARY KEY,
    code VARCHAR(10) UNIQUE NOT NULL,
    shift VARCHAR(20) NOT NULL,
    class_number INTEGER,
    start_time VARCHAR(5) NOT NULL,
    end_time VARCHAR(5) NOT NULL,
    is_interval BOOLEAN DEFAULT FALSE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Seed de horários padrão (Matutino, Vespertino, Noturno)
INSERT INTO subslot_time_intervals (id, code, shift, class_number, start_time, end_time, is_interval) VALUES
('subslot-m1', 'M1', 'matutino', 1, '07:00', '07:50', FALSE),
('subslot-m2', 'M2', 'matutino', 2, '07:50', '08:40', FALSE),
('subslot-m3', 'M3', 'matutino', 3, '08:40', '09:30', FALSE),
('subslot-m-int', 'M_INT', 'matutino', NULL, '09:30', '09:45', TRUE),
('subslot-m4', 'M4', 'matutino', 4, '09:45', '10:35', FALSE),
('subslot-m5', 'M5', 'matutino', 5, '10:35', '11:25', FALSE),
('subslot-m6', 'M6', 'matutino', 6, '11:25', '12:15', FALSE),

('subslot-t1', 'T1', 'vespertino', 1, '13:00', '13:50', FALSE),
('subslot-t2', 'T2', 'vespertino', 2, '13:50', '14:40', FALSE),
('subslot-t3', 'T3', 'vespertino', 3, '14:40', '15:30', FALSE),
('subslot-t-int', 'T_INT', 'vespertino', NULL, '15:30', '15:45', TRUE),
('subslot-t4', 'T4', 'vespertino', 4, '15:45', '16:35', FALSE),
('subslot-t5', 'T5', 'vespertino', 5, '16:35', '17:25', FALSE),
('subslot-t6', 'T6', 'vespertino', 6, '17:25', '18:15', FALSE),

('subslot-n1', 'N1', 'noturno', 1, '19:00', '19:50', FALSE),
('subslot-n2', 'N2', 'noturno', 2, '19:50', '20:40', FALSE),
('subslot-n3', 'N3', 'noturno', 3, '20:40', '21:30', FALSE),
('subslot-n-int', 'N_INT', 'noturno', NULL, '21:30', '21:45', TRUE),
('subslot-n4', 'N4', 'noturno', 4, '21:45', '22:35', FALSE),
('subslot-n5', 'N5', 'noturno', 5, '22:35', '23:25', FALSE),
('subslot-n6', 'N6', 'noturno', 6, '23:25', '00:15', FALSE)
ON CONFLICT (code) DO NOTHING;

-- Tabela de logs de realocação emergencial de docentes (emergency_reallocation_logs)
CREATE TABLE IF NOT EXISTS emergency_reallocation_logs (
    id VARCHAR(36) PRIMARY KEY,
    absent_teacher_id VARCHAR(50) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    mode VARCHAR(20) NOT NULL, -- 'assisted' ou 'delegated'
    selected_option_index INT,
    affected_classes_count INT NOT NULL,
    expanded_coordinations BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(100) DEFAULT 'coordinative_user'
);

-- Tabela de detalhamento de substituição de turmas (emergency_reallocation_details)
CREATE TABLE IF NOT EXISTS emergency_reallocation_details (
    id VARCHAR(36) PRIMARY KEY,
    log_id VARCHAR(36) NOT NULL,
    class_id VARCHAR(50) NOT NULL,
    substitute_teacher_id VARCHAR(50) NOT NULL,
    time_slot VARCHAR(20) NOT NULL,
    room_id VARCHAR(36),
    FOREIGN KEY (log_id) REFERENCES emergency_reallocation_logs(id)
);


