# Risks: Gestão de Relatórios de Ocupação e Carga Docente

> Selo 🟡 PLANEJADO em todos os itens. Documento adversarial por design.

## Premortem
🟡 **Manchete 1:** Coordenadores ignoram o novo módulo de relatórios porque os filtros da UI não atendem às perguntas específicas de última hora da diretoria (causa raiz: escopo de relatórios engessado e sem flexibilidade de consulta).
🟡 **Manchete 2:** Exportações massivas de relatórios em PDF travam o servidor web FastAPI/Uvicorn em horários de pico (causa raiz: geração de relatórios pesados de forma síncrona na thread principal).
🟡 **Manchete 3:** Relatórios gerados apresentam divergência com a alocação real por falta de integração com os logs de realocação emergencial (causa raiz: descontinuidade nos registros do banco SQLite).

**Manchete que mais assusta o usuário:** 🟡 Manchete 1 (Risco de baixa adoção devido a engessamento dos relatórios).

---

## Opção A, Hub de Relatórios Integrado no Dashboard UI
- **Premissa que mata:** 🟡 Os coordenadores necessitarem de visualizações altamente customizáveis que filtros fixos em tela não conseguem suprir.
- **Teste barato da premissa:** 🟡 Apresentar um protótipo de tabela com filtros de turno/bloco para 1 coordenador validar as perguntas-chave em 30 minutos.
- **Custo escondido:** 🟡 Custo de re-renderização e manutenção de seletores DOM adicionais em JavaScript Vanilla em `src/api/static/index.html`.
- **Ponto sem volta:** 🟡 Acoplamento de múltiplos endpoints de consulta específicos no backend `src/api/routes.py`.

## Opção B, Módulo Analítico com Heatmap e Gráficos de Ocupação
- **Premissa que mata:** 🟡 A visualização gráfica em gráficos/heatmaps (Chart.js) ser bonita, mas pouco prática para a conferência minuciosa de disciplinas e professores por sala.
- **Teste barato da premissa:** 🟡 Exibir um mockup visual de heatmap para os usuários antes de programar para verificar se realmente apoia a decisão.
- **Custo escondido:** 🟡 Inclusão de dependência JS externa via CDN e consumo excessivo de memória ao renderizar muitos canvas na mesma página.
- **Ponto sem volta:** 🟡 Adição e acoplamento de bibliotecas de terceiros de gráficos no frontend.

## Opção C, Não construir (Processo manual)
- **Premissa que mata:** 🟡 Os usuários aceitarem continuar navegando individualmente por múltiplas abas e tabelas dispersas para montar relatórios consolidados em planilhas externas.
- **Teste barato da premissa:** 🟡 Cronometrar quanto tempo um coordenador leva hoje para consolidar manualmente a ocupação de 5 blocos.
- **Custo escondido:** 🟡 Custo de horas humanas desperdiçadas repetidamente a cada início de período letivo.
- **Ponto sem volta:** 🟡 Inexistente (nenhum impacto de código).

## Opção D, Usar algo pronto (Exportação CSV / Power BI / Excel)
- **Premissa que mata:** 🟡 Todos os usuários finais possuírem domínio de Power BI ou tabelas dinâmicas no Excel para montar os relatórios sozinhos a partir dos dados brutos.
- **Teste barato da premissa:** 🟡 Enviar um arquivo CSV compilado para 2 coordenadores e pedir que montem o relatório de ocupação por turno no Excel sem ajuda.
- **Custo escondido:** 🟡 Demanda contínua de suporte de TI para treinar e tirar dúvidas de usuários sobre cruzamento de dados no Excel/BI.
- **Ponto sem volta:** 🟡 Dependência de software e treinamento externo.

---

## Riscos transversais
🟡 **Performance de geração de arquivos:** Geração síncrona de relatórios PDF/Excel contendo muitos registros pode temporariamente elevar o uso de CPU e bloquear a API FastAPI se não for paginado/assíncrono.
🟡 **Qualidade e consistência de dados:** Se registros de professores ou salas possuírem campos nulos ou incompletos, a consolidação dos relatórios exibirá totais divergentes.

## O que precisa ser respondido antes de decidir
1. 🟡 Os coordenadores precisam de exportação em PDF/Excel formatado ou a visualização direta em tabelas na tela é suficiente?
2. 🟡 Qual o volume máximo esperado de dados por relatório (ex.: 50 salas vs 500 salas)?
3. 🟡 É aceitável uma solução com filtros estáticos rápidos (Opção A) em vez de uma ferramenta externa flexível (Opção D)?

---
Gerado por reversa-challenger em 2026-08-14T14:16:00Z
Sessão: 002-gestao-relatorios-ocupacao-docentes
