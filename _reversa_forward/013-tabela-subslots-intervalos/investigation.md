# Investigação Técnica: Tabela de Subslots com Intervalos de Aula

> Identificador: `013-tabela-subslots-intervalos`
> Data: `2026-08-11`

## 1. Contexto e Problema

No sistema legado ClassSync AI, a gestão de restrições de indisponibilidade docente (`TeacherRestriction`) utiliza códigos estáticos como `M1`, `M2`, `T1`, `T2`, `N1`, `N2`. No entanto, não havia uma representação relacional formal persistida no banco de dados para mapear o horário de início e término exato de cada aula de 50 minutos e seus respectivos intervalos de descanso de 15 minutos.

Esta investigação avaliou como modelar essa estrutura de forma declarativa e relacional sem quebrar as integrações existentes.

## 2. Alternativas Avaliadas

### Alternativa A: Dicionário estático em memória Python (Descartada)
- **Descrição:** Definir os horários em uma constante global Python (ex: `SLOTS_MAP = {...}`).
- **Prós:** Simples e sem necessidade de alteração de esquema de banco.
- **Contras:** Impede a personalização de horários por ambiente ou campus sem deploy de código; impede consultas SQL diretas em auditorias.

### Alternativa B: Tabela relacional `subslot_time_intervals` com Seed + CRUD REST (Escolhida)
- **Descrição:** Criar uma tabela relacional dedicada no banco de dados com migração DDL inicial e expor endpoints REST API.
- **Prós:** Total alinhamento com a arquitetura relacional, permite consultas flexíveis, auditoria, manutenção dinâmica via API e carga automática no bootstrap.
- **Contras:** Requer atualização nos scripts SQL de migração e criação de novas rotas API.

## 3. Padrões Aplicáveis

- **Database Seed Migration:** Padrão de migração relacional que cria a tabela e popula imediatamente com registros mestre (master data).
- **Domain Code Mapping:** Uso do campo `code` (ex: `M1`, `M2`... `N5`) como chave natural de leitura rápida para interoperabilidade com entidades dependentes.
