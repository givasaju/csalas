# Requirements: Tabela de Subslots com Intervalos de Aula

> Identificador: `013-tabela-subslots-intervalos`
> Data: `2026-08-11`
> Pasta da extração reversa: `_reversa_sdd/`
> Confidência: 🟢 CONFIRMADO, 🟡 INFERIDO, 🔴 LACUNA / DÚVIDA

## 1. Resumo executivo

Esta feature cria a tabela relacional `subslot_time_intervals` para mapear os subslots de horários acadêmicos no banco de dados, associando cada subslot de aula ao seu intervalo exato de tempo (duração de 50 minutos) dentro dos turnos Matutino (07:00), Vespertino (13:00) e Noturno (19:00). Cada turno contempla até 5 aulas com um intervalo de 15 minutos entre a 3ª e a 4ª aula. A solução contempla carga inicial via migration e rotas CRUD na API, mantendo compatibilidade com códigos de restrição docente (`M1`..`N5`).

## 2. Contexto a partir do legado

| Fonte | Trecho relevante | Confidência |
|-------|------------------|-------------|
| `_reversa_sdd/architecture.md#3-modelo-de-entidade-relacionamento-erd` | Entidades relacionais do sistema e necessidade de persistência SQL relacional | 🟢 |
| `_reversa_sdd/domain.md#210-restricoes-de-indisponibilidade-docente` | Mapeamento legado de slots de tempo (`M1`, `M2`, `T1`, `T2`, `N1`, `N2`) | 🟢 |
| `_reversa_sdd/code-analysis.md#academic-space-manager` | Estrutura de endpoints FastAPI e persistência de restrições em memória | 🟡 |

## 3. Personas e cenários de uso

| Persona | Objetivo | Cenário-chave |
|---------|----------|---------------|
| Isabela (Diretora de Infraestrutura) | Consultar e padronizar os horários de início e término das aulas no campus | Visualiza a grade oficial de subslots e intervalos por turno no sistema. |
| Cláudio (Coordenador de Curso) | Alocar disciplinas e cadastrar indisponibilidades docentes ancoradas em subslots reais | Associa turmas a subslots de 50 minutos com intervalos oficiais de 15 minutos. |

## 4. Regras de negócio novas ou alteradas

1. **RN-01: Estrutura da Grade de Turnos e Subslots** 🟢
   - Origem no legado: `_reversa_sdd/domain.md#210`
   - Tipo: nova
   - Descrição: O dia acadêmico é dividido em três turnos fixos: Matutino (início às 07:00), Vespertino (início às 13:00) e Noturno (início às 19:00).
2. **RN-02: Duração das Aulas e Quantidade Máxima por Turno** 🟢
   - Origem no legado: N/A
   - Tipo: nova
   - Descrição: Cada turno permite no máximo 5 subslots de aula. Cada aula tem duração estrita de 50 minutos.
3. **RN-03: Intervalo Obrigatório Intra-turno** 🟢
   - Origem no legado: N/A
   - Tipo: nova
   - Descrição: Entre a aula-3 e a aula-4 de cada turno, deve haver obrigatoriamente um intervalo de 15 minutos.
4. **RN-04: Mapeamento Exato dos Horários por Turno** 🟢
   - Origem no legado: N/A
   - Tipo: nova
   - Descrição:
     - Matutino: Aula 1 (07:00–07:50), Aula 2 (07:50–08:40), Aula 3 (08:40–09:30), Intervalo (09:30–09:45), Aula 4 (09:45–10:35), Aula 5 (10:35–11:25).
     - Vespertino: Aula 1 (13:00–13:50), Aula 2 (13:50–14:40), Aula 3 (14:40–15:30), Intervalo (15:30–15:45), Aula 4 (15:45–16:35), Aula 5 (16:35–17:25).
     - Noturno: Aula 1 (19:00–19:50), Aula 2 (19:50–20:40), Aula 3 (20:40–21:30), Intervalo (21:30–21:45), Aula 4 (21:45–22:35), Aula 5 (22:35–23:25).
5. **RN-05: Codificação e Compatibilidade Docente** 🟢
   - Origem no legado: `_reversa_sdd/domain.md#210`
   - Tipo: nova
   - Descrição: Os subslots são codificados como `M1`..`M5`, `T1`..`T5` e `N1`..`N5` no atributo `code`, assegurando compatibilidade direta com os cadastros de `TeacherRestriction`.

## 5. Requisitos Funcionais

| ID | Requisito | Prioridade | Critério de aceite | Confidência |
|----|-----------|------------|--------------------|-------------|
| RF-01 | Criar a tabela relacional `subslot_time_intervals` para armazenamento dos subslots | Must | A tabela no banco de dados contém os atributos `id`, `code`, `shift`, `class_number`, `start_time`, `end_time` e `is_interval`. | 🟢 |
| RF-02 | Executar carga inicial via migration/seed SQL dos 15 subslots de aula e 3 intervalos nos 3 turnos | Must | A consulta à tabela pós-migração retorna 5 aulas de 50 min e 1 intervalo de 15 min entre aula 3 e 4 para cada turno. | 🟢 |
| RF-03 | Disponibilizar endpoints REST API para consulta (`GET /api/v1/subslots`) e gerenciamento CRUD | Should | Os endpoints permitem listar por turno e realizar operações de criação/edição/exclusão. | 🟢 |
| RF-04 | Garantir mapeamento dos códigos `code` (`M1`..`N5`) para interoperabilidade com restrições docentes | Must | Os registros contêm os códigos `M1`..`M5`, `T1`..`T5` e `N1`..`N5` preenchidos. | 🟢 |

## 6. Requisitos Não Funcionais

| Tipo | Requisito | Evidência ou justificativa | Confidência |
|------|-----------|----------------------------|-------------|
| Desempenho | Consultas à tabela de subslots devem responder em menos de 10ms | Tabela pequena e estática (15 a 18 registros), com índice em `shift` e `code`. | 🟢 |
| Integridade | Impedir a sobreposição de horários entre subslots do mesmo turno no banco de dados | Constraint de validação de horário no banco/migration. | 🟢 |
| Manutenibilidade | Migrations SQL declarativas e reproduzíveis | Alinhado com o DDL relacional em `db/migrations.sql`. | 🟢 |

## 7. Critérios de Aceitação

```gherkin
Cenário: Carga inicial de subslots do turno matutino
  Dado que a migração do banco de dados foi executada com sucesso
  Quando eu consulto os subslots cadastrados para o turno "matutino"
  Então a aula M1 inicia às 07:00 e termina às 07:50
  E a aula M3 inicia às 08:40 e termina às 09:30
  E o intervalo de 15 minutos ocorre das 09:30 às 09:45
  E a aula M4 inicia às 09:45 e termina às 10:35
  E a aula M5 inicia às 10:35 e termina às 11:25

Cenário: Validação de horário no turno vespertino
  Dado que os subslots do turno vespertino foram gerados
  Quando eu verifico o horário da aula T4 do turno vespertino
  Então o horário de início deve ser exatamente 15:45 e o término 16:35

Cenário: Tentativa de inserção de subslot com horário sobreposto
  Dado que a tabela subslot_time_intervals possui restrições de integridade
  Quando houver uma tentativa de inserir um subslot que se sobreponha aos horários oficiais
  Então a operação deve falhar com erro de restrição no banco de dados
```

## 8. Prioridade MoSCoW

| Item | MoSCoW | Justificativa |
|------|--------|---------------|
| RF-01 | Must | Tabela essencial para estruturar os horários no modelo relacional. |
| RF-02 | Must | Carga dos horários padrão do campus (5 aulas de 50m + intervalo de 15m por turno). |
| RF-03 | Should | Endpoints REST API para consulta e gerenciamento de subslots. |
| RF-04 | Must | Compatibilidade direta com códigos de indisponibilidade docente (`M1`..`N5`). |
| RNF de Integridade | Must | Garante consistência temporal absoluta dos horários. |

## 9. Esclarecimentos

### Sessão 2026-08-11

- **Q:** Qual deve ser o nome oficial da nova tabela relacional de subslots no banco de dados e nos modelos da aplicação?
  **R:** `subslot_time_intervals`.

- **Q:** Como deve ser realizada a populagem/carga inicial dos subslots padrão (5 aulas + 1 intervalo por turno)?
  **R:** Carga inicial via Migration SQL/seed de banco de dados + disponibilidade de endpoints CRUD via API para gerenciamento.

- **Q:** Como as restrições de disponibilidade docente (`TeacherRestriction`) que hoje usam códigos legados (`M1`..`N2`) se integram à nova tabela?
  **R:** Os códigos `M1` a `M5`, `T1` a `T5` e `N1` a `N5` serão mantidos na coluna `code` da nova tabela para compatibilidade direta com a entidade de restrições.

## 10. Lacunas

> Nenhuma lacuna pendente. Todas as dúvidas iniciais foram esclarecidas na sessão de 2026-08-11.

## 11. Histórico de alterações

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-08-11 | Versão inicial gerada por `/reversa-requirements` | reversa |
| 2026-08-11 | Esclarecimento de dúvidas via `/reversa-clarify` (tabela `subslot_time_intervals`, seed+CRUD e códigos `M1`..`N5`) | reversa |
