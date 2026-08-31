# Investigation: Padrões de Design e UI de Entrada de Dados

## Pesquisa de Fundo

A interface de entrada de dados do ClassSync AI exige alto padrão estético (Glassmorphism, dark mode, paleta coerente HSL) e excelente usabilidade para lidar com duas tarefas principais:
1. Gestão e cadastro de salas físicas (formulário unitário + drag-and-drop CSV).
2. Gestão de restrições docentes por horário e dia da semana.

## Alternativas Avaliadas

1. **Abordagem A: Framework SPA completo (React / Vue)**
   - *Desvantagem*: Requer build pipeline extra, node_modules volumosos e altera a entrega estática do FastAPI.
2. **Abordagem B: Vanilla JS + CSS Vanilla com Fetch API (Escolhida)**
   - *Vantagem*: Totalmente autocontido, tempo de carregamento de 0ms, alta facilidade de manutenção e sincronia direta com os arquivos servidos pelo Uvicorn no FastAPI (`src/api/static/`).

## Padrões de UX/UI Adotados

- **Tabs/Abas de Navegação**: Separação clara entre "Cadastro de Salas", "Importação CSV", "Restrições de Professores" e "Inventário de Salas".
- **Matriz Selecionável**: Grade de botões interativos para os 6 slots de tempo x 7 dias da semana com alteração dinâmica de cor ao marcar/desmarcar.
- **Drag-and-Drop Dropzone**: Área visual com efeito hover pontilhado para recepção de arquivos `.csv`.
