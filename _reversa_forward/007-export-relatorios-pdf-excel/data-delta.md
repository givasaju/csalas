# Delta no Modelo de Dados: Exportação de relatórios em PDF/Excel

> Identificador da feature: `007-export-relatorios-pdf-excel`  
> Data: `2026-08-08`  

---

## 1. Visão Geral

A funcionalidade de exportação de relatórios não insere, altera ou remove entidades persistidas no banco de dados do ClassSync AI. Trata-se de uma camada de **leitura e agregação de dados** em memória sobre o inventário de salas físicas (`Room`), turmas (`Class`) e o estado atual das alocações.

---

## 2. Estrutura dos Dados Agregados no Relatório (DTOs)

Para a compilação do relatório, o backend irá consolidar os seguintes DTOs em tempo de execução:

### 2.1 SummaryByBlockDTO (Resumo por Bloco Predial)
- `block_id` (str): Identificador do bloco predial (ex: `"BLOCO_A"`).
- `total_rooms` (int): Quantidade total de salas cadastradas no bloco.
- `total_capacity` (int): Soma das capacidades físicas de alunos do bloco.
- `occupied_slots` (int): Quantidade de turmas alocadas nos slots do bloco.
- `total_available_slots` (int): Slots totais teóricos do bloco ($\text{salas} \times 6$).
- `occupancy_rate` (float): Percentual de ocupação do bloco predial ($\frac{\text{slots ocupados}}{\text{slots totais}} \times 100$).

### 2.2 AllocationDetailDTO (Matriz Detalhada)
- `block_id` (str): Bloco predial.
- `room_name` (str): Nome/número da sala física.
- `capacity` (int): Capacidade da sala.
- `room_type` (str): Tipo da sala (`common`, `lab`, `auditorium`).
- `time_slot` (str): Slot de horário (`M1`, `M2`, `T1`, `T2`, `N1`, `N2`).
- `class_id` (str): Identificador da turma alocada (ou `"LIVRE"` se desocupada).
- `coordination_id` (str): Coordenação responsável pela turma.

---

## 3. Migrações e Scripts SQL

Nenhuma migração SQL é necessária para esta feature.
