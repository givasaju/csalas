# Roadmap: Implementar o gerenciador acadêmico academic-space-manager

> Identificador: `002-implementar-space-manager`  
> Data: `2026-08-07`  
> Requirements: `_reversa_forward/002-implementar-space-manager/requirements.md`  
> Confidência: 🟢 CONFIRMADO, 🟡 INFERIDO, 🔴 LACUNA  

---

## 1. Resumo da abordagem

A implementação do gerenciador acadêmico `academic-space-manager` estenderá o backend FastAPI. Forneceremos rotas CRUD para manipulação de salas de aula e recursos físicos, cadastro de indisponibilidade docente por dia da semana e faixa horária, e processamento de carga de arquivos CSV. 

O banco de dados simulado em memória (gerenciado no `worker.py`) será estruturado com validações rigorosas de dados via esquemas Pydantic para garantir consistência de entradas. O endpoint `/api/v1/allocation/input-data` reunirá e formatará de forma otimizada todos os insumos de salas, turmas e indisponibilidades, alimentando o motor de IA em um payload JSON unificado.

---

## 2. Princípios aplicados

Não há princípios específicos cadastrados no arquivo `.reversa/principles.md` deste projeto.

---

## 3. Decisões técnicas

| ID | Decisão | Justificativa | Alternativas descartadas | Confidência |
|----|---------|----------------|--------------------------|-------------|
| D-01 | **Validações via Esquemas Pydantic** | Garante que dados inconsistentes (capacidade negativa ou nula) sejam rejeitados automaticamente na entrada da rota com status HTTP 422. | Validações manuais imperativas com condicionais `if-else` no código de controle. | 🟢 |
| D-02 | **Reset automático semestral das restrições horárias** | Mantém o banco higienizado e livre de dados defasados que causariam erros nas alocações do novo período letivo. | Manutenção acumulada de indisponibilidades passadas com controle de flags de vigência. | 🟢 |
| D-03 | **Importação transacional de CSV de salas** | O upload do CSV é processado em lote sob política "tudo ou nada" (se houver erro em uma linha, toda a transação é revertida). | Importação incremental parcial de linhas corretas com descarte silencioso de linhas inválidas. | 🟡 |

---

## 4. Premissas

Nenhuma premissa sob dúvida ativa. Todas as questões levantadas no `requirements.md` foram completamente clarificadas.

---

## 5. Delta arquitetural

A arquitetura do projeto será expandida com a adição das definições do gerenciador acadêmico:

| Componente | Arquivo de origem no legado | Tipo de mudança | Resumo |
|------------|------------------------------|-----------------|--------|
| **academic-space-manager** | `_reversa_sdd/sdd/academic-space-manager.md` | componente-novo | Módulo de persistência física e acadêmica do ClassSync AI. |

---

## 6. Delta no modelo de dados

- Resumo das mudanças: Definição dos modelos Pydantic e estruturas de persistência para as entidades `Room`, `Teacher` e `TeacherRestriction`.
- Detalhe completo em: `_reversa_forward/002-implementar-space-manager/data-delta.md`

---

## 7. Delta de contratos externos

| Contrato | Tipo | Arquivo de detalhe |
|----------|------|--------------------|
| **space-manager-api** | HTTP | `_reversa_forward/002-implementar-space-manager/interfaces/space-manager-api.md` |

---

## 8. Plano de migração

Nenhuma migração aplicável (cenário greenfield).

---

## 9. Riscos e mitigações

| Risco | Impacto | Probabilidade | Mitigação |
|-------|---------|---------------|-----------|
| Travamentos e deadlocks em cadastros concorrentes de docentes no início do período | médio | média | Usar controle simples de travas em memória e processamento otimizado de escritas no dicionário global. |
| Inserção de dados inconsistentes via CSV (ex: cabeçalhos errados) | médio | alta | Validar a presença exata da primeira linha contendo `bloco,sala,capacidade,tipo,acessivel,recursos` antes de ler o conteúdo. |

---

## 10. Critério de pronto

- [ ] Todas as ações do `actions.md` marcadas `[X]`
- [ ] `regression-watch.md` gerado
- [ ] Testes de integração de APIs (CRUD de salas, carga de CSV e GET de inputs) passando com 100% de cobertura.

---

## 11. Histórico de alterações

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-08-07 | Versão inicial gerada por `/reversa-plan` | reversa |
