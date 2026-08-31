# Regression Watch: Gestão de Relatórios de Ocupação e Carga Docente

> Identificador: `018-gestao-relatorios-ocupacao-docentes`
> Data: `2026-08-14`

## 1. Itens de Vigilância de Regressão

| ID | Origem (arquivo, seção) | Regra esperada após mudança | Tipo de verificação | Sinal de violação |
|----|-------------------------|-----------------------------|---------------------|-------------------|
| W001 | `_reversa_sdd/inventory.md#src/api/routes.py` | O endpoint `GET /api/v1/reports/summary` deve retornar código HTTP 200 com os arrays `room_occupancy` e `teacher_reports`. | `presença` | Falha ou erro 500 ao chamar `/api/v1/reports/summary`. |
| W002 | `_reversa_sdd/inventory.md#src/api/static/index.html` | A opção `📊 Relatórios` deve estar visível no navbar e a aba `#reports-tab` ser ativada ao clicar. | `presença` | Ausência do botão no navbar ou aba invisível. |

## 2. Histórico de re-extrações

*(Vazio - será preenchido nas próximas re-extrações `/reversa`)*

## 3. Arquivadas

*(Vazio)*

## 4. Observações

- Suíte de testes automatizados `pytest` executada e 100% aprovada (61/61 testes passando).
