# Roadmap: UI Moderna de Entrada de Dados do ClassSync AI

> Identificador: `004-ui-entrada-dados`
> Data: `2026-08-07`
> Requirements: `_reversa_forward/004-ui-entrada-dados/requirements.md`
> Confidência: 🟢 CONFIRMADO, 🟡 INFERIDO, 🔴 LACUNA

## 1. Resumo da abordagem

A abordagem técnica consiste na criação de uma interface de usuário rica, esteticamente impecável e reativa construída com HTML5 semântico, JavaScript moderno (Fetch API, DOM manipulation) e CSS Vanilla com tokens visuais glassmorphic e modo escuro nativo. A UI interage diretamente com os endpoints já existentes da API REST do FastAPI expostos no módulo `src/api/routes.py`: `GET /api/v1/allocation/input-data`, `POST /api/v1/rooms`, `POST /api/v1/rooms/import-csv`, `POST /api/v1/allocation/restrictions`, `DELETE /api/v1/allocation/restrictions` e `DELETE /api/v1/rooms/{room_id}`.

## 2. Princípios aplicados

Nenhum arquivo `.reversa/principles.md` configurado. A implementação segue os padrões de código limpo e arquitetura desacoplada do projeto.

## 3. Decisões técnicas

| ID | Decisão | Justificativa | Alternativas descartadas | Confidência |
|----|---------|----------------|--------------------------|-------------|
| D-01 | Utilizar Vanilla CSS e Vanilla JS | Zero dependências externas no frontend, máxima velocidade de carregamento e alinhamento à arquitetura do projeto. | TailwindCSS via CDN, React/Vue | 🟢 |
| D-02 | Integrar formulários em tabs/cards interativos com Glassmorphism | Experiência de usuário premium, limpa e responsiva sem recarregamentos de página. | Páginas HTML separadas por formulário | 🟢 |
| D-03 | Matriz de restrições horárias em grade clicável (7 Dias x 6 Slots) | Interface visual intuitiva para seleção rápida dos horários M1..N2. | Seletor dropdown duplo tradicional | 🟢 |
| D-04 | Feedback visual transacional com Toast de notificações | Informa claramente resultados HTTP de sucesso (201/200) e erros detalhados (400, 409, 422). | Alerts nativos do navegador (`alert()`) | 🟢 |

## 4. Premissas

Nenhuma premissa sob dúvida. Todos os requisitos foram ancorados 100% no backend REST existente.

## 5. Delta arquitetural

| Componente | Arquivo de origem no legado | Tipo de mudança | Resumo |
|------------|------------------------------|-----------------|--------|
| `gerenciador-espacos` | `_reversa_sdd/architecture.md#gerenciador-espacos` | componente-estendido | Inclusão dos componentes estáticos de interface de entrada de dados e binding com a API |

## 6. Delta no modelo de dados

- Resumo das mudanças: Nenhuma alteração nos esquemas de banco simulados (`db_rooms`, `db_restrictions`, etc.), apenas consumo e manipulação dos dados via API REST.
- Detalhe completo em: `_reversa_forward/004-ui-entrada-dados/data-delta.md`

## 7. Delta de contratos externos

| Contrato | Tipo | Arquivo de detalhe |
|----------|------|--------------------|
| `entrada-dados-api` | HTTP REST | `_reversa_forward/004-ui-entrada-dados/interfaces/entrada-dados-api.md` |

## 8. Plano de migração

1. Criar os estilos visuais modernos e tokens de CSS em `src/api/static/index.css`.
2. Atualizar o layout base e adicionar as seções/painéis de formulários em `src/api/static/index.html`.
3. Adicionar as funções JavaScript de fetch, renderização da matriz de restrição e preview de CSV.
4. Validar chamadas de API nos endpoints backend usando `pytest`.

## 9. Riscos e mitigações

| Risco | Impacto | Probabilidade | Mitigação |
|-------|---------|---------------|-----------|
| Tentativa de exclusão de sala bloqueada por motor de IA rodando (`409 Conflict`) | Médio | Baixo | Interceptador no `fetch` da UI exibindo Toast explicativo de alerta. |
| Arquivo CSV com formatação incorreta enviado pelo usuário | Baixo | Médio | Validação Client-side do cabeçalho CSV e apresentação amigável das mensagens do backend. |

## 10. Critério de pronto

- [ ] Todas as ações do `actions.md` marcadas `[X]`
- [ ] Testes de integração de UI passando sem falhas no `pytest`
- [ ] Interface validada em execução ao vivo no navegador com Uvicorn

## 11. Histórico de alterações

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-08-07 | Versão inicial gerada por `/reversa-plan` | reversa |
