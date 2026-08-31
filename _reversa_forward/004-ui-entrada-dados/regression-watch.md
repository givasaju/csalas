# Regression Watch: UI Moderna de Entrada de Dados do ClassSync AI

> Identificador: `004-ui-entrada-dados`  
> Data: `2026-08-07`  

---

## Watch List Principal

| ID | Origem | Regra esperada após mudança | Tipo de verificação | Sinal de violação |
|----|--------|-----------------------------|----------------------|-------------------|
| W001 | `src/api/static/index.html` | Interface deve manter as 5 abas ativas (Dashboard, Cadastrar Sala, Importação CSV, Restrições, Inventário) | presença | Desaparecimento de abas ou quebra de navegação client-side |
| W002 | `src/api/static/index.html` | As chamadas de API do frontend devem manter envio do cabeçalho `Authorization: Bearer <token>` | presença | Falha de autenticação 401/403 ao acionar ações na UI |
| W003 | `src/api/static/index.html` | Exclusão de sala com agendamentos ativos deve exibir modal/toast de erro status 409 Conflict | comportamento | Remoção silenciosa ou erro 500 sem feedback visual |

---

## Histórico de Re-extrações

*(Esta seção será preenchida automaticamente quando o `/reversa` for executado para re-extração do projeto)*

---

## Arquivadas

*(Nenhum item arquivado)*

---

## Observações

- RF-001: Validação de upload de CSV tudo-ou-nada coberta em `tests/test_api_csv.py` e `tests/test_ui_input_routes.py`.
