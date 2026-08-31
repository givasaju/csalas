# Roadmap: Reduzir 50% do tamanho das fontes que apresentam os dados da seção Auditoria e Extrato

> Identificador: `015-reduzir-fonte-auditoria-extrato`
> Data: `2026-08-14`
> Requirements: `_reversa_forward/015-reduzir-fonte-auditoria-extrato/requirements.md`
> Confidência: 🟢 CONFIRMADO, 🟡 INFERIDO, 🔴 LACUNA

## 1. Resumo da abordagem

A abordagem técnica consiste em ajustar a tipografia da classe CSS `.auctions-table tbody td` em `src/api/static/index.css` para aplicar `font-size: 0.44rem` (~50% do valor base). As tags internas (`strong`, `span`) receberão `font-size: inherit` para garantir redução uniforme sem sobreposição. As cores de destaque (`#10b981` para vencedores, `#ef4444` para perdedores, `#6366f1` para lances e `#818cf8` para slots) serão mantidas intactas, assim como os cabeçalhos (`th`) e demais seções da interface.

## 2. Princípios aplicados

| Princípio | Como a feature se relaciona | Status |
|-----------|------------------------------|--------|
| Isolamento de Escopo CSS | A alteração estilística é estritamente scoped para a classe `.auctions-table tbody td`. | respeita |
| Preservação de Identidade Visual | As cores e estruturas de destaque visual permanecem inalteradas. | respeita |

## 3. Decisões técnicas

| ID | Decisão | Justificativa | Alternativas descartadas | Confidência |
|----|---------|----------------|--------------------------|-------------|
| D-01 | Definir `font-size: 0.44rem` na regra `.auctions-table tbody td` | Atende à redução exata de 50% solicitada pelo usuário | Alterar via JavaScript inline; modificar fontes globais de `table` | 🟢 |
| D-02 | Adicionar `font-size: inherit` para `strong` e `span` dentro de `.auctions-table tbody td` | Evita que elementos em negrito ou coloridos mantenham o tamanho de fonte anterior | Criar classes específicas para cada sub-elemento | 🟢 |
| D-03 | Reduzir `padding` para `0.25rem 0.4rem` e `line-height` para `1.2` | Mantém o espaçamento proporcional ao novo tamanho da fonte | Manter padding de 0.9rem (geraria espaço em branco excessivo) | 🟢 |

## 4. Premissas

Nenhuma premissa adotada. O documento de requisitos não contém pendências de dúvidas.

## 5. Delta arquitetural

| Componente | Arquivo de origem no legado | Tipo de mudança | Resumo |
|------------|------------------------------|-----------------|--------|
| `occupancy-dashboard` | `_reversa_sdd/architecture.md#occupancy-dashboard` | regra-alterada | Tipografia compactada em 50% nas linhas da tabela de auditoria em `src/api/static/index.css`. |

## 6. Delta no modelo de dados

- Resumo das mudanças: Sem alterações em tabelas, schemas ou banco de dados.
- Detalhe completo em: `_reversa_forward/015-reduzir-fonte-auditoria-extrato/data-delta.md`

## 7. Delta de contratos externos

Não se aplica. Esta alteração é puramente de apresentação na camada visual do frontend.

## 8. Plano de migração

Não se aplica.

## 9. Riscos e mitigações

| Risco | Impacto | Probabilidade | Mitigação |
|-------|---------|---------------|-----------|
| Afetar tabelas de outras abas (`rooms-tab`, `teachers-tab`) | médio | baixa | Escopar a regra CSS exclusivamente com o seletor `.auctions-table tbody td`. |
| Fonte ilegível em telas de alta resolução | baixo | baixa | Ajustar a altura de linha e padding proporcionalmente (`line-height: 1.2`). |

## 10. Critério de pronto

- [ ] Todas as ações do `actions.md` marcadas `[X]`
- [ ] Suíte de testes automatizados `pytest` executada sem regressões (61/61 testes)
- [ ] Confirmação de renderização correta das cores e tipografia no navegador

## 11. Histórico de alterações

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-08-14 | Versão inicial gerada por `/reversa-plan` | reversa |
