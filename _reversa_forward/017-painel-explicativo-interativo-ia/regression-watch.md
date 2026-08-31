# Regression Watch: Painel Explicativo Interativo e Flutuante na Gestão com IA

> Identificador: `017-painel-explicativo-interativo-ia`
> Data: `2026-08-14`

## 1. Itens de Vigilância de Regressão

| ID | Origem (arquivo, seção) | Regra esperada após mudança | Tipo de verificação | Sinal de violação |
|----|-------------------------|-----------------------------|---------------------|-------------------|
| W001 | `_reversa_sdd/inventory.md#src/api/static/index.html` | O componente `#aiGuideWidget` deve existir e estar visível na aba `#ai-management-tab`. | `presença` | Ausência do widget guia na aba de Gestão com IA. |
| W002 | `_reversa_sdd/inventory.md#src/api/static/index.html` | As funções JS `initAiGuideDrag`, `changeGuideFontSize` e `toggleAiGuideWidget` devem funcionar sem erros no console. | `presença` | Erros de script ao tentar arrastar, mudar a fonte ou fechar o painel. |

## 2. Histórico de re-extrações

*(Vazio - será preenchido nas próximas re-extrações `/reversa`)*

## 3. Arquivadas

*(Vazio)*

## 4. Observações

- Suíte de testes automatizados `pytest` executada e 100% aprovada (61/61 testes passando).
