# Addendum: Gestão de Relatórios de Ocupação e Carga Docente

> Identificador: `018-gestao-relatorios-ocupacao-docentes`
> Data: `2026-08-14`
> Cenário: Legado (`_reversa_sdd/architecture.md` e `domain.md`)

## Vigência

Vigente desde 2026-08-14.

## Resumo da entrega

Implementar a nova aba de navegação **📊 Relatórios** no sistema ClassSync AI para prover visões analíticas consolidadas e individuais sobre a taxa de ocupação de ambientes acadêmicos por turno/bloco, além de relatórios detalhados das disciplinas e horários lecionados por cada docente. A interface conta com filtros interativos em tempo real e integração direta com os geradores de arquivos PDF e Excel em `/api/v1/reports/summary`.
Total de ações executadas: 4 de 4 (100% concluído).

## Impacto por artefato da extração

| Artefato | Seção | Tipo de impacto | Delta |
|----------|-------|-----------------|-------|
| `_reversa_sdd/architecture.md` | `#academic-space-manager` | `contrato-novo` | Adição do endpoint REST `GET /api/v1/reports/summary` em `src/api/routes.py`. |
| `_reversa_sdd/architecture.md` | `#occupancy-dashboard` | `componente-novo` | Adição do container `#reports-tab` e filtros de Bloco/Turno/Docente em `src/api/static/index.html`. |

## Regras sob vigilância

- `W001`: Vigilância de funcionamento do endpoint `GET /api/v1/reports/summary` em `_reversa_forward/018-gestao-relatorios-ocupacao-docentes/regression-watch.md`
- `W002`: Vigilância de presença do botão `📊 Relatórios` e ativação da aba `#reports-tab` em `_reversa_forward/018-gestao-relatorios-ocupacao-docentes/regression-watch.md`

## Fontes

- `_reversa_forward/018-gestao-relatorios-ocupacao-docentes/requirements.md`
- `_reversa_forward/018-gestao-relatorios-ocupacao-docentes/roadmap.md`
- `_reversa_forward/018-gestao-relatorios-ocupacao-docentes/actions.md`
- `_reversa_forward/018-gestao-relatorios-ocupacao-docentes/legacy-impact.md`
- `_reversa_forward/018-gestao-relatorios-ocupacao-docentes/regression-watch.md`
