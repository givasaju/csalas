# Regression Watch: Reduzir 50% do tamanho das fontes na seção Auditoria e Extrato

> Identificador: `015-reduzir-fonte-auditoria-extrato`
> Data: `2026-08-14`

## 1. Itens de Vigilância de Regressão

| ID | Origem (arquivo, seção) | Regra esperada após mudança | Tipo de verificação | Sinal de violação |
|----|-------------------------|-----------------------------|---------------------|-------------------|
| W001 | `_reversa_sdd/inventory.md#src/api/static/index.css` | A classe `.auctions-table tbody td` deve manter `font-size: 0.44rem`. | `redação` | Fonte retornando a tamanhos superiores a `0.5rem`. |
| W002 | `_reversa_sdd/domain.md#auditoria-leiloes` | As cores `#10b981`, `#ef4444`, `#6366f1` devem permanecer nos estilos. | `presença` | Remoção das cores de destaque dos leilões. |

## 2. Histórico de re-extrações

*(Vazio - será preenchido nas próximas re-extrações `/reversa`)*

## 3. Arquivadas

*(Vazio)*

## 4. Observações

- Todos os 61 testes automatizados da suíte `pytest` continuam passando sem falhas.
