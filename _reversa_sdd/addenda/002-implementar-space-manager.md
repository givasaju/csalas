# Adendo: Implementar o gerenciador acadêmico academic-space-manager

> Identificador: `002-implementar-space-manager`  
> Data: `2026-08-07`  
> Cenário: Greenfield  

---

## Vigência

Vigente desde 2026-08-07.
Superado pela re-extração de 2026-08-09.

---

## Resumo da entrega

Esta feature entregou a implementação do gerenciador acadêmico e predial `academic-space-manager` do ClassSync AI. Ele expõe endpoints CRUD seguros com validações declarativas Pydantic para gestão física de salas, cadastro e reset semestral de restrições de indisponibilidades docentes e upload de arquivos CSV sob política de importação transacional Tudo ou Nada. Além disso, fornece o payload consolidado unificado para consumo da inteligência artificial de alocação de salas. Foram concluídas 13 ações de 13 mapeadas.

---

## Impacto por artefato da extração

| Artefato | Seção | Tipo de impacto | Delta |
|----------|-------|-----------------|-------|
| `_reversa_sdd/prd.md` | `#4. Escopo (in)` | `componente-novo` | O gerenciador acadêmico e predial foi implementado no backend do ClassSync AI com persistência em repositório em memória e APIs FastAPI. |
| `_reversa_sdd/sdd/academic-space-manager.md` | `#6. Requisitos Funcionais` | `componente-novo` | Implementados os requisitos funcionais RF-01 (CRUD de salas), RF-02 (indisponibilidades horárias), RF-03 (carga transacional via CSV), RF-04 (reset semestral) e RF-05 (GET de insumos consolidados). |

---

## Regras sob vigilância

Os watch items de regressão criados nesta feature estão registrados no seguinte arquivo:
*   [regression-watch.md](file:///c:/csalas/_reversa_forward/002-implementar-space-manager/regression-watch.md) (Watch IDs: `W001`, `W002`, `W003`, `W004`, `W005`)

---

## Fontes

- `_reversa_forward/002-implementar-space-manager/requirements.md`
- `_reversa_forward/002-implementar-space-manager/roadmap.md`
- `_reversa_forward/002-implementar-space-manager/legacy-impact.md`
- `_reversa_forward/002-implementar-space-manager/regression-watch.md`
