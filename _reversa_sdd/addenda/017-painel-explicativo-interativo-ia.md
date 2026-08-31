# Addendum: Painel Explicativo Interativo e Flutuante na Gestão com IA

> Identificador: `017-painel-explicativo-interativo-ia`
> Data: `2026-08-14`
> Cenário: Legado (`_reversa_sdd/architecture.md` e `domain.md`)

## Vigência

Vigente desde 2026-08-14.

## Resumo da entrega

Implementar um painel explicativo interativo com estética moderna, elegante e flutuante na aba **Gestão com IA** (`#ai-management-tab`). O painel orienta o coordenador sobre quando utilizar ou não a inteligência artificial para otimização de salas, além de explicar as opções da tela. O usuário possui controle total para arrastar (drag & drop), reposicionar, ajustar o tamanho da fonte (`A-`/`A+`) e fechar/reabrir o painel a qualquer momento.
Total de ações executadas: 4 de 4 (100% concluído).

## Impacto por artefato da extração

| Artefato | Seção | Tipo de impacto | Delta |
|----------|-------|-----------------|-------|
| `_reversa_sdd/architecture.md` | `#occupancy-dashboard` | `componente-novo` | Widget flutuante `#aiGuideWidget` adicionado à aba `#ai-management-tab` em `src/api/static/index.html`. |
| `_reversa_sdd/inventory.md` | `#src/api/static/index.css` | `componente-novo` | Adicionadas regras de estilo `.ai-guide-widget`, `.ai-guide-header`, `.btn-font-scale` e animações de drag em `index.css`. |

## Regras sob vigilância

- `W001`: Vigilância de presença do componente `#aiGuideWidget` na aba `#ai-management-tab` em `_reversa_forward/017-painel-explicativo-interativo-ia/regression-watch.md`
- `W002`: Vigilância de presença das funções JS `initAiGuideDrag`, `changeGuideFontSize` e `toggleAiGuideWidget` em `_reversa_forward/017-painel-explicativo-interativo-ia/regression-watch.md`

## Fontes

- `_reversa_forward/017-painel-explicativo-interativo-ia/requirements.md`
- `_reversa_forward/017-painel-explicativo-interativo-ia/roadmap.md`
- `_reversa_forward/017-painel-explicativo-interativo-ia/actions.md`
- `_reversa_forward/017-painel-explicativo-interativo-ia/legacy-impact.md`
- `_reversa_forward/017-painel-explicativo-interativo-ia/regression-watch.md`
