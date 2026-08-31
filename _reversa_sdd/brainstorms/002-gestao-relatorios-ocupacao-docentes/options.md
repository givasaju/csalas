# Options: Gestão de Relatórios de Ocupação e Carga Docente

> Selo 🟡 PLANEJADO em todos os itens. Nenhuma opção foi escolhida ainda.

## Problema de referência
🟡 Quando estiver analisando o uso da infraestrutura e a distribuição de aulas, eu quero visualizar e exportar relatórios detalhados e consolidados por ambiente e docente por turno, para conseguir otimizar a ocupação predial e garantir transparência na alocação docente.

## Restrições ativas
🟡 Nenhuma declarada pelo usuário.

---

## Opção A: Hub de Relatórios Integrado no Dashboard UI
- **Em uma frase:** 🟡 Adicionar uma aba/seção dedicada "📊 Relatórios Acadêmicos" no frontend HTML/JS existente com filtros por turno, bloco e docente, permitindo visualização direta e exportação em PDF e Excel.
- **Como resolve o problema:** 🟡 Oferece aos coordenadores visão integrada de tabelas analíticas individuais (por professor) e coletivas (por prédio/turno) na própria interface web.
- **Esforço:** 🟡 Médio , exige criação de novos seletores de filtro no frontend e novos endpoints de agregação no FastAPI backend.
- **Impacto no legado:** 🟡 Estende a barra de abas em `src/api/static/index.html` e adiciona endpoints de relatórios em `src/api/routes.py`.
- **Reversibilidade:** 🟡 Fácil , alterações restritas à UI e novos endpoints sem alteração do banco SQLite.
- **O que precisa ser verdade para funcionar:** 🟡 Os dados de salas, docentes, disciplinas e slots horários no SQLite precisam estar atualizados.

## Opção B: Módulo Analítico com Heatmap e Gráficos de Ocupação
- **Em uma frase:** 🟡 Construir um painel analítico avançado contendo gráficos de distribuição (Chart.js) com heatmap visual de ocupação de salas por turno e linha do tempo de carga horária docente.
- **Como resolve o problema:** 🟡 Proporciona análise visual imediata da ocupação predial por horário e identifica visualmente professores subutilizados ou sobrecarregados.
- **Esforço:** 🟡 Alto , requer integração de biblioteca de gráficos no frontend e cálculos analíticos complexos no backend.
- **Impacto no legado:** 🟡 Inclusão de scripts CDN no HTML e adição de algoritmos de distribuição temporal no backend.
- **Reversibilidade:** 🟡 Médio , adição de dependência de visualização JS.
- **O que precisa ser verdade para funcionar:** 🟡 A infraestrutura de frontend precisa suportar renderização de canvas de gráficos responsivos.

---

## Opção sempre presente, não construir
- **Em uma frase:** 🟡 Manter o sistema atual e instruir a equipe a utilizar os relatórios simples existentes e navegar diretamente pelas abas "Gestão de Ambientes" e "Gestão de Docentes".
- **Como resolve o problema:** 🟡 Os dados brutos continuam acessíveis nas tabelas existentes de cada aba, porém exigindo compilação manual pela coordenação.
- **Esforço:** 🟡 Baixo , zero desenvolvimento de software.
- **Impacto no legado:** 🟡 Nenhum.
- **Reversibilidade:** 🟡 Fácil , sem nenhuma alteração de código.
- **O que precisa ser verdade para funcionar:** 🟡 Os usuários aceitarem navegar individualmente em cada aba para consultar as informações sem visão unificada.

## Opção sempre presente, usar algo pronto
- **Em uma frase:** 🟡 Expor uma API de dados unificados em formato CSV/JSON e conectar a ferramentas externas prontas de BI (ex.: Power BI, Metabase ou Microsoft Excel).
- **Como resolve o problema:** 🟡 Transfere a geração e personalização de relatórios/dashboards para uma ferramenta de relatórios consolidada do mercado.
- **Esforço:** 🟡 Baixo , necessita apenas de um endpoint simples de exportação de dados brutos relacionais.
- **Impacto no legado:** 🟡 Criação de 1 endpoint de exportação unificada em `src/api/routes.py`.
- **Reversibilidade:** 🟡 Fácil , endpoint isolado de leitura.
- **O que precisa ser verdade para funcionar:** 🟡 Os usuários terem acesso e conhecimento básico na ferramenta externa de BI (Power BI/Excel).

---
Gerado por reversa-explorer em 2026-08-14T14:15:25Z
Sessão: 002-gestao-relatorios-ocupacao-docentes
Nenhuma recomendação emitida por design. Convergência é papel de /reversa-arbiter.
