# Adendo: Implementar o motor de alocação core-allocation-engine

> Identificador: `001-implementar-core-allocation`  
> Data: `2026-08-07`  
> Cenário: Greenfield  

---

## Vigência

Vigente desde 2026-08-07.
Superado pela re-extração de 2026-08-09.

---

## Resumo da entrega

Esta feature entregou a implementação do motor de inteligência artificial de alocação de salas `core-allocation-engine` para o ClassSync AI. Ele processa as restrições acadêmicas e prediais das coordenações, executa um leilão de lances fechados cooperativo (utilizando créditos) para mediação automática de concorrência por salas e implementa heurísticas prediais para consolidação e esvaziamento de blocos de baixa ocupação predial. Foram concluídas 13 ações de 13 mapeadas.

---

## Impacto por artefato da extração

| Artefato | Seção | Tipo de impacto | Delta |
|----------|-------|-----------------|-------|
| `_reversa_sdd/prd.md` | `#4. Escopo (in)` | `componente-novo` | O motor core-allocation-engine foi completamente implementado em Python e exposto via API REST FastAPI. |
| `_reversa_sdd/sdd/core-allocation-engine.md` | `#6. Requisitos Funcionais` | `componente-novo` | Implementados os requisitos funcionais RF-01 (restrições mandatórias), RF-02 (otimização predial), RF-03 (leilão multiagente) e RF-04 (suspensão e arbitragem física). |

---

## Regras sob vigilância

Os watch items de regressão criados nesta feature estão registrados no seguinte arquivo:
*   [regression-watch.md](file:///c:/csalas/_reversa_forward/001-implementar-core-allocation/regression-watch.md) (Watch IDs: `W001`, `W002`, `W003`, `W004`, `W005`)

---

## Fontes

- `_reversa_forward/001-implementar-core-allocation/requirements.md`
- `_reversa_forward/001-implementar-core-allocation/roadmap.md`
- `_reversa_forward/001-implementar-core-allocation/legacy-impact.md`
- `_reversa_forward/001-implementar-core-allocation/regression-watch.md`
