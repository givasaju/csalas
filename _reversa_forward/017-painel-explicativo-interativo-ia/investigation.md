# Investigation: Painel Explicativo Interativo e Flutuante na Gestão com IA

> Identificador: `017-painel-explicativo-interativo-ia`
> Data: `2026-08-14`

## 1. Pesquisa de fundo

A aba **Gestão com IA** (`#ai-management-tab`) foi criada recentemente para centralizar a alocação predial. No entanto, coordenadores que acessam essa tela nem sempre sabem quando é realmente vantajoso disparar a inteligência artificial versus realizar pequenos ajustes manuais.

A adição de um widget interativo flutuante orientará os usuários de forma dinâmica, oferecendo recursos de acessibilidade e customização visual (arraste, redimensionamento de texto e ocultação).

## 2. Alternativas avaliadas

1. **Opção A: Widget Flutuante Draggable & Resizable (Escolhida)**
   - Não bloqueia a visão dos extratos de leilão.
   - Permite ajuste fino de tamanho de fonte e posição na tela.

2. **Opção B: Texto Fixo no Topo da Tela**
   - Descartada por ocupar espaço vertical permanente da aba.

## 3. Padrões aplicáveis

- Manipulação de eventos DOM Vanilla JS (`mousedown`, `mousemove`, `mouseup`).
- Glassmorphism CSS (`backdrop-filter: blur(12px)`).
