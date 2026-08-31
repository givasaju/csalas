# Investigation: Reduzir 50% do tamanho das fontes na seção Auditoria e Extrato

> Identificador: `015-reduzir-fonte-auditoria-extrato`
> Data: `2026-08-14`

## 1. Pesquisa de fundo

A seção "Auditoria e Extrato de Leilões de Créditos" renderiza os resultados do leilão cooperativo através da função `renderAuctionsTable` em `src/api/static/index.html`. O estilo da tabela é regido pelas regras em `src/api/static/index.css`.

A necessidade do usuário é exibir os dados de auditoria em um formato compacto (50% do tamanho base da fonte), mantendo as cores e o layout intactos.

## 2. Alternativas avaliadas

1. **Opção A: Estilo CSS escopado via `.auctions-table tbody td` (Escolhida)**
   - Definição limpa no arquivo CSS estático `index.css`.
   - Baixo acoplamento e manutenção simples.

2. **Opção B: Inline styles via JavaScript (`renderAuctionsTable`)**
   - Descartada por sujar a lógica de renderização e dificultar a manutenção visual.

## 3. Padrões aplicáveis

- Princípio BEM / CSS Escopado no projeto ClassSync AI.
- Regra de herança de CSS (`font-size: inherit`) para tags em negrito (`strong`) e destaques (`span`).
