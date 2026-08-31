# Addendum: Nova aba Gestão com IA no Navbar Principal

> Identificador: `016-gestao-com-ia-aba`
> Data: `2026-08-14`
> Cenário: Legado (`_reversa_sdd/architecture.md` e `domain.md`)

## Vigência

Vigente desde 2026-08-14.

## Resumo da entrega

Adicionar uma nova aba de navegação principal intitulada **🤖 Gestão com IA** disposta após a opção **Gestão de Docentes** no cabeçalho do sistema. Relocar para esta nova interface as seções de **Auditoria e Extrato de Leilões de Créditos**, **Status da Tarefa de IA** e o botão de ação **Disparar Alocação de IA** (anteriormente localizado no topo do header).
Total de ações executadas: 4 de 4 (100% concluído).

## Impacto por artefato da extração

| Artefato | Seção | Tipo de impacto | Delta |
|----------|-------|-----------------|-------|
| `_reversa_sdd/architecture.md` | `#occupancy-dashboard` | `contrato-alterado` | Estrutura de abas estendida em `src/api/static/index.html` com a adição da opção `🤖 Gestão com IA` (`#ai-management-tab`). |
| `_reversa_sdd/inventory.md` | `#src/api/static/index.html` | `regra-alterada` | Relocação dos componentes `#btnRunAllocation`, `.auctions-card` e `Status da Tarefa de IA` para a aba `#ai-management-tab`. |

## Regras sob vigilância

- `W001`: Vigilância de presença do botão `🤖 Gestão com IA` no navbar principal em `_reversa_forward/016-gestao-com-ia-aba/regression-watch.md`
- `W002`: Vigilância de presença dos seletores `#btnRunAllocation`, `#auctionsTableBody` e `#taskStatusBadge` em `_reversa_forward/016-gestao-com-ia-aba/regression-watch.md`

## Fontes

- `_reversa_forward/016-gestao-com-ia-aba/requirements.md`
- `_reversa_forward/016-gestao-com-ia-aba/roadmap.md`
- `_reversa_forward/016-gestao-com-ia-aba/actions.md`
- `_reversa_forward/016-gestao-com-ia-aba/legacy-impact.md`
- `_reversa_forward/016-gestao-com-ia-aba/regression-watch.md`
