# Decision, realocacao-docente-emergencial

> Selo 🟡 PLANEJADO. Decisão humana registrada, sujeita a revisão.

## Problema de referência
🟡 Quando ocorrer um afastamento não planejado de um docente, eu quero mitigar este problema, para conseguir uma realocação de horários e disciplinas de forma emergencial.

## Placar
| Opção | Job to be done | Esforço | Risco residual | Custo no legado | Total |
|---|:---:|:---:|:---:|:---:|:---:|
| **Opção A, Remanejamento Manual Assistido** | 4 | 4 | 4 | 4 | **16** |
| **Opção B, Motor de Otimização Emergencial via IA** | 5 | 2 | 2 | 2 | **11** |
| **Opção C, Não construir (Protocolo Operacional)** | 2 | 5 | 2 | 5 | **14** |
| **Opção D, Usar algo pronto (SaaS Comercial)** | 4 | 3 | 3 | 3 | **13** |

🟡 Placar calculado pelo método Arbiter considerando o cenário de código legado do ClassSync AI.

## Recomendação do Arbiter
🟡 Opção A (Remanejamento Manual Assistido) , por ter menor custo de alteração nos módulos de IA do legado e resolver a dor imediata mantendo o coordenador no controle.

## O que se perde ao escolher ela
🟡 Perde-se a capacidade do algoritmo calcular automaticamente combinações complexas em lote para grandes contingentes de professores ausentes simultaneamente.

## Em que condição a recomendação muda
🟡 Se o volume de substituições simultâneas for elevado a ponto de inviabilizar a escolha manual pelo coordenador.

## Decisão do usuário
🟡 Híbrida: Opção A + Opção B (IA calculando alternativas e Coordenador homologando na plataforma) , decidido por givas em 2026-08-13T13:18:00-03:00

## Divergência registrada
🟡 O Arbiter recomendou a Opção A puramente para economizar esforço no `core-allocation-engine`. O usuário optou por combinar o motor de IA (Opção B) como gerador de sugestões/alternativas com a interface assistida (Opção A), garantindo que a decisão final e homologação fiquem registradas no sistema pela coordenação.

## A validar antes de comprometer
🟡 Apresentar a um coordenador de curso o fluxo visual de aprovação de sugestões geradas por IA para garantir que a homologação na plataforma seja ágil e juridicamente segura.

## Riscos aceitos conscientemente
🟡 Esforço elevado de desenvolvimento no motor de alocação legado (`src/engine/core.py`), risco de efeito dominó em turmas não diretamente afetadas e necessidade de manter restrições horárias (`Restriction`) atualizadas no sistema.

---
Gerado por reversa-arbiter em 2026-08-13T13:18:00-03:00
Sessão: 001-realocacao-docente-emergencial
