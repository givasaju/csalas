# Requirements: Reduzir 50% do tamanho das fontes que apresentam os dados da seção Auditoria e Extrato

> Identificador: `015-reduzir-fonte-auditoria-extrato`
> Data: `2026-08-14`
> Pasta da extração reversa: `_reversa_sdd/`
> Confidência: 🟢 CONFIRMADO, 🟡 INFERIDO, 🔴 LACUNA / DÚVIDA

## 1. Resumo executivo

Ajustar a tipografia da tabela da seção "Auditoria e Extrato de Leilões de Créditos" no Dashboard (`occupancy-dashboard`), aplicando uma redução de 50% no tamanho da fonte utilizada exclusivamente nas linhas de dados (`tbody td`), enquanto preserva os cabeçalhos (`th`), o título da seção, as demais seções da UI e 100% da paleta de cores original.

## 2. Contexto a partir do legado

| Fonte | Trecho relevante | Confidência |
|-------|------------------|-------------|
| `_reversa_sdd/architecture.md#occupancy-dashboard` | Componente de interface visual responsável pela apresentação de KPIs e extratos de leilões. | 🟢 |
| `_reversa_sdd/domain.md#auditoria-leiloes` | Regras de exibição de lances, vencedores e perdedores na auditoria de leilões de créditos. | 🟢 |
| `_reversa_sdd/inventory.md#src/api/static/index.css` | Estilos CSS para cartões, tabelas e tipografia da aplicação. | 🟢 |

## 3. Personas e cenários de uso

| Persona | Objetivo | Cenário-chave |
|---------|----------|---------------|
| Coordenador de Infraestrutura | Visualizar extrato compacto de leilões | Analisar o histórico de leilões de créditos com dados em tipografia compacta e legível no Dashboard. |

## 4. Regras de negócio novas ou alteradas

1. **RN-01:** Redução de 50% no tamanho da fonte dos dados das células da tabela de auditoria (`.auctions-table tbody td` com `font-size: 0.44rem`). 🟢
   - Origem no legado: `_reversa_sdd/inventory.md#src/api/static/index.css`
   - Tipo: alterada
2. **RN-02:** Preservação estrita da paleta de cores originais (Vencedor `#10b981`, Perdedor `#ef4444`, Lances `#6366f1`, Slot Badge `#818cf8`). 🟢
   - Origem no legado: `_reversa_sdd/domain.md#auditoria-leiloes`
   - Tipo: mantida
3. **RN-03:** Manutenção do tamanho da fonte dos cabeçalhos (`th`), do título do card (`section-title`) e das demais seções e abas do sistema. 🟢
   - Origem no legado: `_reversa_sdd/architecture.md#occupancy-dashboard`
   - Tipo: mantida

## 5. Requisitos Funcionais

| ID | Requisito | Prioridade | Critério de aceite | Confidência |
|----|-----------|------------|--------------------|-------------|
| RF-01 | A classe `.auctions-table tbody td` e seus elementos filhos (`strong`, `span`) devem utilizar `font-size: 0.44rem`. | Must | Inspecionado no navegador e verificado em `index.css`. | 🟢 |
| RF-02 | As cores originais dos textos de vencedores, perdedores, lances e slots devem permanecer inalteradas. | Must | Cores `#10b981`, `#ef4444`, `#6366f1` e `#818cf8` verificadas. | 🟢 |
| RF-03 | Os cabeçalhos da tabela (`th`) e o título do card não devem sofrer alteração no tamanho da fonte. | Must | `th` mantido em `0.8rem` e `section-title` mantido em `1.15rem`. | 🟢 |

## 6. Requisitos Não Funcionais

| Tipo | Requisito | Evidência ou justificativa | Confidência |
|------|-----------|----------------------------|-------------|
| Usabilidade | Ajustar a altura da linha e padding (`padding: 0.25rem 0.4rem`) para manter legibilidade com a fonte reduzida em 50%. | Rationale visual | 🟢 |
| Isolamento | Garantir que a alteração de estilo afete estritamente a tabela `.auctions-table tbody td` sem propagar para outras tabelas. | Rationale de engenharia de CSS | 🟢 |

## 7. Critérios de Aceitação

```gherkin
Cenário: Visualização de dados compactos na tabela de leilões
  Dado que o usuário acessa a aba "Dashboard & KPIs"
  Quando inspeciona a tabela da seção "Auditoria e Extrato de Leilões de Créditos"
  Então as linhas de dados exibem fonte reduzida em 50% (0.44rem)
  E as cores verde (vencedor), vermelho (perdedor) e roxo (lances) permanecem inalteradas

Cenário: Preservação de cabeçalho e outras seções
  Dado que a fonte das células de dados foi reduzida em 50%
  Quando o usuário analisa os cabeçalhos "Sala", "Slot", "Vencedor", "Perdedor", "Lances Pago"
  Então eles permanecem em tamanho padrão de cabeçalho (0.8rem)
  E as demais tabelas e cards das abas Ambientes e Docentes permanecem intocados
```

## 8. Prioridade MoSCoW

| Item | MoSCoW | Justificativa |
|------|--------|---------------|
| RF-01 | Must | Requisito principal solicitado para exibição compacta de dados. |
| RF-02 | Must | Preservação essencial de identidade visual e acessibilidade das cores. |
| RF-03 | Must | Restrição estrita de escopo para evitar afetar cabeçalhos ou outras telas. |

## 9. Esclarecimentos

> Nenhuma sessão de dúvidas registrada ainda. Rode `/reversa-clarify` quando houver `[DÚVIDA]` pendente.

## 10. Lacunas

Nenhuma lacuna ou `[DÚVIDA]` pendente.

## 11. Histórico de alterações

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-08-14 | Versão inicial gerada por `/reversa-requirements` | reversa |
