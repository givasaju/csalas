# Investigation: Realocação Docente Emergencial

> Identificador: `014-realocacao-docente-emergencial`
> Data: `2026-08-13`
> Feature: `_reversa_forward/014-realocacao-docente-emergencial/requirements.md`

---

## 1. Contexto e Motivação

No sistema legado ClassSync AI (`balcao`), o motor de alocação `CoreAllocationEngine` (`src/engine/core.py`) executa o cálculo de distribuição de turmas em salas de aula para o semestre inteiro em 3 fases (Alocação Inicial AAC, Leilão Multiagente `ACC`/`AMR` e Consolidação Predial `BuildingOptimizer`).

Entretanto, quando ocorre uma licença médica ou afastamento não planejado de um docente (ex: licença de 60 dias), recriar a grade inteira do campus via leilão multiagente é inviável, pois desfaz alocações estáveis já acordadas com centenas de docentes.

Esta investigação avaliou estratégias para implementar o cálculo emergencial direcionado (localizado apenas no subconjunto de turmas afetadas), suportando o Modo Assistido e o Modo Delegado solicitados pela coordenação.

---

## 2. Alternativas Avaliadas

### Alternativa 1: Recálculo Global da Grade (Descartada)
- **Descrição:** Disparar o `CoreAllocationEngine.run_allocation()` completo para todo o campus após remover o docente ausente.
- **Desvantagens:** Alto risco de efeito dominó desnecessário, invalidando horários de dezenas de turmas e professores que não tinham relação com a licença.

### Alternativa 2: Busca Gulosa de Horários Livres (Descartada)
- **Descrição:** Simplesmente listar docentes da mesma coordenação com janelas vagas no mesmo horário e escolher o primeiro.
- **Desvantagens:** Não avalia o impacto em turmas em caso de necessidade de permuta, e falha quando não há vaga exata na mesma janela.

### Alternativa 3: Algoritmo de Realocação Emergencial Direcionada com Expansão de Coordenação (Escolhida)
- **Descrição:** Método dedicado `calculate_emergency_reallocation` no `src/engine/core.py`.
- **Funcionamento:**
  1. Mapeia as turmas do docente afastado.
  2. Busca docentes da mesma coordenação (`Coordination`) sem conflitos de `Restriction` no mesmo slot.
  3. Caso não haja docentes suficientes, expande a busca para docentes de coordenações correlatas.
  4. Gera até 3 opções ordenadas pelo menor `impact_score` (mínimo de deslocamentos e trocas de salas).
  5. Retorna as opções para aprovação manual no Modo Assistido ou autorização direta no Modo Delegado.

---

## 3. Padrões de Projeto e Arquitetura Recomendados

- **Estratégia de Homologação Dupla:** Padrão Strategy para alternar entre `AssistedApprovalStrategy` e `DelegatedApprovalStrategy`.
- **Log de Auditoria Estruturado:** Gravação imediata dos eventos de realocação em formato JSON estático/tabela no banco para atender requisitos de governança trabalhista.
