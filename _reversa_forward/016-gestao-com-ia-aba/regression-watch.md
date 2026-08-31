# Regression Watch: Nova aba Gestão com IA no Navbar Principal

> Identificador: `016-gestao-com-ia-aba`
> Data: `2026-08-14`

## 1. Itens de Vigilância de Regressão

| ID | Origem (arquivo, seção) | Regra esperada após mudança | Tipo de verificação | Sinal de violação |
|----|-------------------------|-----------------------------|---------------------|-------------------|
| W001 | `_reversa_sdd/inventory.md#src/api/static/index.html` | A opção `🤖 Gestão com IA` deve estar visível no `.tab-navigation`. | `presença` | Ausência da aba de Gestão com IA no navbar principal. |
| W002 | `_reversa_sdd/architecture.md#occupancy-dashboard` | O botão `#btnRunAllocation` e cards `#auctionsTableBody`, `#taskStatusBadge` devem existir dentro de `#ai-management-tab`. | `presença` | Seletores DOM ausentes ou soltos fora da aba. |

## 2. Histórico de re-extrações

*(Vazio - será preenchido nas próximas re-extrações `/reversa`)*

## 3. Arquivadas

*(Vazio)*

## 4. Observações

- Suíte de testes automatizados `pytest` executada e 100% aprovada (61/61 testes passando).
