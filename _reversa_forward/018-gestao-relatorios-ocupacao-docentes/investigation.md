# Investigation: Gestão de Relatórios de Ocupação e Carga Docente

> Identificador: `018-gestao-relatorios-ocupacao-docentes`
> Data: `2026-08-14`

## 1. Pesquisa de fundo

Atualmente, o ClassSync AI dispõe de geradores de relatórios em PDF e Excel acessíveis por botões na barra superior, mas faltava uma aba dedicada no sistema para consulta interativa e analítica com filtros dinâmicos por Bloco, Turno e Docente.

A criação da aba **📊 Relatórios** unifica a consulta e a exportação, proporcionando aos coordenadores uma visão imediata da alocação de salas e da carga horária docente.

## 2. Alternativas avaliadas

1. **Aba Dedicada "📊 Relatórios" (Escolhida)**:
   - Apresenta visões organizadas e filtros em tempo real sem poluir as demais abas.

2. **Inserir relatórios como modais no Dashboard**:
   - Descartada por limitar a usabilidade e a comparação visual simultânea.

## 3. Padrões aplicáveis

- Rotas FastAPI baseadas em `APIRouter` e injetor `Session = Depends(get_db)`.
- Renderização dinâmica de tabelas em JavaScript Vanilla sem bibliotecas pesadas.
