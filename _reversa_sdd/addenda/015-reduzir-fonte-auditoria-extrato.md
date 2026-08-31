# Addendum: Reduzir 50% do tamanho das fontes que apresentam os dados da seção Auditoria e Extrato

> Identificador: `015-reduzir-fonte-auditoria-extrato`
> Data: `2026-08-14`
> Cenário: Legado (`_reversa_sdd/architecture.md` e `domain.md`)

## Vigência

Vigente desde 2026-08-14.

## Resumo da entrega

Ajustar a tipografia da tabela da seção "Auditoria e Extrato de Leilões de Créditos" no Dashboard (`occupancy-dashboard`), aplicando uma redução de 50% no tamanho da fonte utilizada exclusivamente nas linhas de dados (`tbody td`), enquanto preserva os cabeçalhos (`th`), o título da seção, as demais seções da UI e 100% da paleta de cores original.
Total de ações executadas: 3 de 3 (100% concluído).

## Impacto por artefato da extração

| Artefato | Seção | Tipo de impacto | Delta |
|----------|-------|-----------------|-------|
| `_reversa_sdd/architecture.md` | `#occupancy-dashboard` | `regra-alterada` | Linhas de dados da tabela de auditoria agora utilizam `font-size: 0.44rem` (~50% do valor base) em `src/api/static/index.css`. |
| `_reversa_sdd/domain.md` | `#auditoria-leiloes` | `regra-preservada` | Preservação estrita das cores de destaque para vencedores (`#10b981`), perdedores (`#ef4444`) e lances (`#6366f1`). |
| `_reversa_sdd/inventory.md` | `#src/api/static/index.css` | `regra-alterada` | Adicionadas regras CSS escopadas `.auctions-table tbody td` com `font-size: 0.44rem` e `font-size: inherit` nas sub-tags. |

## Regras sob vigilância

- `W001`: Vigilância de redação do tamanho da fonte `font-size: 0.44rem` em `_reversa_forward/015-reduzir-fonte-auditoria-extrato/regression-watch.md`
- `W002`: Vigilância de presença das cores originais `#10b981`, `#ef4444`, `#6366f1` em `_reversa_forward/015-reduzir-fonte-auditoria-extrato/regression-watch.md`

## Fontes

- `_reversa_forward/015-reduzir-fonte-auditoria-extrato/requirements.md`
- `_reversa_forward/015-reduzir-fonte-auditoria-extrato/roadmap.md`
- `_reversa_forward/015-reduzir-fonte-auditoria-extrato/actions.md`
- `_reversa_forward/015-reduzir-fonte-auditoria-extrato/legacy-impact.md`
- `_reversa_forward/015-reduzir-fonte-auditoria-extrato/regression-watch.md`
