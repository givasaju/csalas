# Roadmap: Painel Explicativo Interativo e Flutuante na Gestão com IA

> Identificador: `017-painel-explicativo-interativo-ia`
> Data: `2026-08-14`
> Requirements: `_reversa_forward/017-painel-explicativo-interativo-ia/requirements.md`
> Confidência: 🟢 CONFIRMADO, 🟡 INFERIDO, 🔴 LACUNA

## 1. Resumo da abordagem

A abordagem técnica consiste em integrar um widget flutuante e interativo `#aiGuideWidget` no container `#ai-management-tab` em `src/api/static/index.html` com suporte em `src/api/static/index.css`:
1. Estilizar o painel com estética moderna em `index.css` (Glassmorphism, gradiente escuro refinado `#0f172a`, borda `rgba(99, 102, 241, 0.3)` e sombra elevada).
2. Adicionar o cabeçalho manipulável `.ai-guide-header` com cursor `grab`/`grabbing` para arraste (drag and drop) via event listeners em JavaScript (`mousedown`, `mousemove`, `mouseup`).
3. Adicionar botões de controle de fonte (`A-`/`A+`) que alteram dinamicamente a variável/propriedade `font-size` do conteúdo interno `.ai-guide-body` entre `0.75rem` e `1.15rem`.
4. Adicionar botão de fechamento (✖) e botão auxiliar no cabeçalho da aba `#btnToggleAiGuide` ("💡 Guia da IA") para reabrir/restaurar o painel no local original.

## 2. Princípios aplicados

| Princípio | Como a feature se relaciona | Status |
|-----------|------------------------------|--------|
| UI Rica e Estética Moderna | Utiliza elementos visuais refinados (Glassmorphism, badges HSL e micro-animações). | respeita |
| Interatividade Nativa sem Dependências | Drag & drop e redimensionamento de fonte implementados em JavaScript Vanilla leve. | respeita |

## 3. Decisões técnicas

| ID | Decisão | Justificativa | Alternativas descartadas | Confidência |
|----|---------|----------------|--------------------------|-------------|
| D-01 | Criar widget flutuante manipulável `#aiGuideWidget` | Permite mover o painel para não cobrir a tabela de auditoria durante a leitura | Modal bloqueante (modal backdrop) | 🟢 |
| D-02 | Implementar Drag and Drop em JS Vanilla com `position: absolute` / `position: fixed` | Evita inclusão de bibliotecas externas pesadas (ex: jQuery UI) | Utilizar biblioteca de terceiros | 🟢 |
| D-03 | Armazenar o tamanho da fonte em variável local e alterar a classe `.ai-guide-body` | Proporciona ajuste visual limpo e responsivo | Alterar fonte de toda a página | 🟢 |

## 4. Premissas

Nenhuma premissa adotada. O documento de requisitos possui 0 dúvidas.

## 5. Delta arquitetural

| Componente | Arquivo de origem no legado | Tipo de mudança | Resumo |
|------------|------------------------------|-----------------|--------|
| `occupancy-dashboard` | `_reversa_sdd/architecture.md#occupancy-dashboard` | componente-novo | Widget flutuante `#aiGuideWidget` adicionado à aba `#ai-management-tab` em `src/api/static/index.html`. |

## 6. Delta no modelo de dados

- Resumo das mudanças: Sem alterações no banco SQLite ou APIs FastAPI.
- Detalhe completo em: `_reversa_forward/017-painel-explicativo-interativo-ia/data-delta.md`

## 7. Delta de contratos externos

Não se aplica. Alteração restrita à interface frontend.

## 8. Plano de migração

Não se aplica.

## 9. Riscos e mitigações

| Risco | Impacto | Probabilidade | Mitigação |
|-------|---------|---------------|-----------|
| Widget arrastado para fora dos limites visíveis da janela | baixo | baixa | Adicionar travas de contorno (`Math.max` / `Math.min`) nos eixos `X` e `Y` durante o drag. |

## 10. Critério de pronto

- [ ] Todas as ações do `actions.md` marcadas `[X]`
- [ ] Suíte de testes `pytest` executada com 100% de aprovação (61/61 testes)
- [ ] Teste de arraste, redimensionamento de fonte e fechamento/reabertura funcionando perfeitamente na UI

## 11. Histórico de alterações

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-08-14 | Versão inicial gerada por `/reversa-plan` | reversa |
