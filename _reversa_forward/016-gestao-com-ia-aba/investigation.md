# Investigation: Nova aba Gestão com IA no Navbar Principal

> Identificador: `016-gestao-com-ia-aba`
> Data: `2026-08-14`

## 1. Pesquisa de fundo

A barra de navegação principal em `src/api/static/index.html` possui os botões de navegação:
- `📊 Dashboard & KPIs` (`dashboard-tab`)
- `🏛️ Gestão de Ambientes` (`rooms-tab`)
- `👨‍🏫 Gestão de Docentes` (`teachers-tab`)

A adição da aba `🤖 Gestão com IA` (`ai-management-tab`) permitirá reunir a ação de cálculo do solver de IA (`#btnRunAllocation`), o monitor de progresso assíncrono e o extrato de auditoria de leilões em uma única interface especializada.

## 2. Alternativas avaliadas

1. **Opção A: Nova Aba Principal `#ai-management-tab` (Escolhida)**
   - Reorganização intuitiva da UI alinhada ao feedback do usuário.
   - Preservação total de funções JS de roteamento (`switchTab`).

2. **Opção B: Modal Popup para IA**
   - Descartada por poluir a tela e impedir o acompanhamento contínuo dos extratos de leilão.

## 3. Padrões aplicáveis

- Função de roteamento por visibilidade `.tab-content.active` nativa em `index.html`.
