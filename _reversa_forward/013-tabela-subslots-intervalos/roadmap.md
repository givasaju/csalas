# Roadmap: Tabela de Subslots com Intervalos de Aula

> Identificador: `013-tabela-subslots-intervalos`
> Data: `2026-08-11`
> Requirements: `_reversa_forward/013-tabela-subslots-intervalos/requirements.md`
> Confidência: 🟢 CONFIRMADO, 🟡 INFERIDO, 🔴 LACUNA

## 1. Resumo da abordagem

A implementação consiste na criação da tabela relacional `subslot_time_intervals` no banco de dados e nos schemas FastAPI/Pydantic, populando-a via seed DDL com 18 registros padrão (5 aulas de 50 minutos e 1 intervalo de 15 minutos entre a 3ª e 4ª aula para os turnos Matutino, Vespertino e Noturno). Além da carga automática via migração, a API exporá rotas REST CRUD para permitir consulta e gerenciamento dinâmico dos subslots. Os códigos de identificação (`M1`..`M5`, `T1`..`T5`, `N1`..`N5`) garantem compatibilidade direta com a entidade de restrições docentes (`TeacherRestriction`).

## 2. Princípios aplicados

| Princípio | Como a feature se relaciona | Status |
|-----------|------------------------------|--------|
| Integridade e Consistência Temporal | Garante que os intervalos de aulas de 50 minutos e descansos de 15 minutos sejam respeitados e validados no banco | respeita |
| Transparência de Contratos REST API | Mantém padrão RESTful nos schemas e endpoints de subslots | respeita |

## 3. Decisões técnicas

| ID | Decisão | Justificativa | Alternativas descartadas | Confidência |
|----|---------|----------------|--------------------------|-------------|
| D-01 | Tabela relacional `subslot_time_intervals` com colunas `id`, `code`, `shift`, `class_number`, `start_time`, `end_time`, `is_interval` | Permite estruturar horários e intervalos de forma relacional no banco de dados | Coleção fixa apenas em dicionário Python em memória | 🟢 |
| D-02 | Carga inicial determinística via script SQL/seed de migração (18 registros) | Garante que o ambiente suba com a grade padrão do campus imediatamente | Exigir cadastro manual de todos os horários via interface | 🟢 |
| D-03 | Rotas REST API para CRUD completo (`GET`, `POST`, `PUT`, `DELETE /api/v1/subslots`) | Permite a administradores consultar e alterar subslots sem reiniciar o servidor | Apenas script SQL estático sem API | 🟢 |
| D-04 | Mapeamento explícito de códigos de restrição (`M1`..`M5`, `T1`..`T5`, `N1`..`N5`) na coluna `code` | Mantém interoperabilidade imediata com o módulo de restrições de professores | Alterar o formato de IDs de indisponibilidade em toda a aplicação | 🟢 |

## 4. Premissas

> Nenhuma premissa sob dúvida pendente. Todas as decisões foram confirmadas no alinhamento de requisitos.

## 5. Delta arquitetural

| Componente | Arquivo de origem no legado | Tipo de mudança | Resumo |
|------------|------------------------------|-----------------|--------|
| `academic-space-manager` | `_reversa_sdd/architecture.md#1-visao-geral-do-sistema` | contrato-novo | Adição de schemas Pydantic e rotas REST para subslots em `src/api/routes.py` e `src/api/schemas.py` |
| Modelo Relacional SQL | `_reversa_sdd/architecture.md#3-modelo-de-entidade-relacionamento-erd` | componente-novo | Adição da tabela `subslot_time_intervals` e script de seed em `db/migrations.sql` e gerenciadores de persistência |

## 6. Delta no modelo de dados

- Resumo das mudanças: Criação da tabela `subslot_time_intervals` com 8 atributos e restrição UNIQUE no atributo `code`. Carga inicial com 15 aulas e 3 intervalos de descanso.
- Detalhe completo em: `_reversa_forward/013-tabela-subslots-intervalos/data-delta.md`

## 7. Delta de contratos externos

| Contrato | Tipo | Arquivo de detalhe |
|----------|------|--------------------|
| Subslots API | HTTP | `_reversa_forward/013-tabela-subslots-intervalos/interfaces/subslots-api.md` |

## 8. Plano de migração

1. Criar e executar a migração DDL de criação da tabela `subslot_time_intervals` e inserção dos 18 registros padrão (Seed) em `db/migrations.sql`.
2. Adicionar o modelo de dados e repositório de persistência correspondente no backend Python.
3. Expor os schemas Pydantic e os endpoints `/api/v1/subslots` na API FastAPI.

## 9. Riscos e mitigações

| Risco | Impacto | Probabilidade | Mitigação |
|-------|---------|---------------|-----------|
| Sobreposição inadvertida de horários em subslots alterados via API | médio | baixa | Validação de colisão de horários no backend (`start_time` < `end_time` e sem interseção com mesmo turno) |
| Código de subslot duplicado | alto | baixa | Constraint `UNIQUE(code)` no banco de dados e validação Pydantic |

## 10. Critério de pronto

- [ ] Todas as ações do `actions.md` marcadas `[X]`
- [ ] `cross-check.md` (se executado) sem CRITICAL nem HIGH
- [ ] `regression-watch.md` gerado
- [ ] Re-extração reversa executada e sem regressão vermelha

## 11. Histórico de alterações

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-08-11 | Versão inicial gerada por `/reversa-plan` | reversa |
