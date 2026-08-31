# Delta no Modelo de Dados: Tabela de Subslots com Intervalos de Aula

> Identificador: `013-tabela-subslots-intervalos`
> Data: `2026-08-11`

## 1. Novas Tabelas Relacionais

### Tabela: `subslot_time_intervals`

Armazena a definição formal de cada subslot de aula e intervalo de descanso por turno acadêmico.

| Atributo | Tipo de Dado | Nulável | Chave / Restrição | Descrição |
|----------|--------------|---------|-------------------|-----------|
| `id` | VARCHAR(36) | Não | PK | Identificador único UUID do subslot |
| `code` | VARCHAR(10) | Não | UNIQUE | Código de referência rápida (ex: `M1`, `M2`, `M_INT`, `T1`, etc.) |
| `shift` | VARCHAR(20) | Não | - | Turno acadêmico (`matutino`, `vespertino`, `noturno`) |
| `class_number` | INTEGER | Sim | - | Número sequencial da aula no turno (1 a 5). Nulo se for intervalo |
| `start_time` | VARCHAR(5) | Não | - | Horário de início no formato HH:MM (ex: `07:00`) |
| `end_time` | VARCHAR(5) | Não | - | Horário de término no formato HH:MM (ex: `07:50`) |
| `is_interval` | BOOLEAN | Não | DEFAULT FALSE | Indica se o subslot é um intervalo de descanso (15 min) |
| `created_at` | TIMESTAMP | Não | DEFAULT CURRENT_TIMESTAMP | Data/hora de inserção do registro |

---

## 2. Carga Inicial de Dados (Seed Data)

A migração SQL de carga inicial insere os 18 registros padrão distribuídos nos 3 turnos:

### Turno Matutino (Início 07:00)
- `M1`: `07:00` às `07:50` (is_interval: false, class_number: 1)
- `M2`: `07:50` às `08:40` (is_interval: false, class_number: 2)
- `M3`: `08:40` às `09:30` (is_interval: false, class_number: 3)
- `M_INT`: `09:30` às `09:45` (is_interval: true, class_number: null) — *Intervalo de 15 min*
- `M4`: `09:45` às `10:35` (is_interval: false, class_number: 4)
- `M5`: `10:35` às `11:25` (is_interval: false, class_number: 5)

### Turno Vespertino (Início 13:00)
- `T1`: `13:00` às `13:50` (is_interval: false, class_number: 1)
- `T2`: `13:50` às `14:40` (is_interval: false, class_number: 2)
- `T3`: `14:40` às `15:30` (is_interval: false, class_number: 3)
- `T_INT`: `15:30` às `15:45` (is_interval: true, class_number: null) — *Intervalo de 15 min*
- `T4`: `15:45` às `16:35` (is_interval: false, class_number: 4)
- `T5`: `16:35` às `17:25` (is_interval: false, class_number: 5)

### Turno Noturno (Início 19:00)
- `N1`: `19:00` às `19:50` (is_interval: false, class_number: 1)
- `N2`: `19:50` às `20:40` (is_interval: false, class_number: 2)
- `N3`: `20:40` às `21:30` (is_interval: false, class_number: 3)
- `N_INT`: `21:30` às `21:45` (is_interval: true, class_number: null) — *Intervalo de 15 min*
- `N4`: `21:45` às `22:35` (is_interval: false, class_number: 4)
- `N5`: `22:35` às `23:25` (is_interval: false, class_number: 5)

---

## 3. Índices Recomendados

- `idx_subslots_shift`: Índice no atributo `shift` para agilizar filtros por turno.
- `idx_subslots_code`: Índice UNIQUE no atributo `code` para buscas diretas.
