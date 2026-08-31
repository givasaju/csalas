# Decision: Gestão de Relatórios de Ocupação e Carga Docente

> Selo 🟡 PLANEJADO. Decisão humana registrada, sujeita a revisão.

## Problema de referência
🟡 Quando estiver analisando o uso da infraestrutura e a distribuição de aulas, eu quero visualizar e exportar relatórios detalhados e consolidados por ambiente e docente por turno, para conseguir otimizar a ocupação predial e garantir transparência na alocação docente.

## Placar
| Opção | Job to be done | Esforço | Risco residual | Custo no legado | Total |
|---|---|---|---|---|---|
| **Opção A: Hub de Relatórios Integrado no Dashboard UI** | 5 | 3 | 4 | 4 | **16** |
| **Opção B: Módulo Analítico com Heatmap (Chart.js)** | 4 | 2 | 2 | 3 | **11** |
| **Opção C: Não construir (Processo manual)** | 2 | 5 | 2 | 5 | **14** |
| **Opção D: Usar algo pronto (Exportação CSV / Power BI)** | 4 | 4 | 3 | 4 | **15** |

🟡 Placar sem empates. A Opção A venceu com 16/20 pontos.

## Recomendação do Arbiter
🟡 **Opção A: Hub de Relatórios Integrado no Dashboard UI**. Oferece visualização unificada na própria interface web do sistema com filtros dinâmicos por turno, bloco e docente, integrando com as APIs nativas de exportação PDF e Excel sem adicionar dependências externas pesadas.

## O que se perde ao escolher ela
🟡 Perde-se a flexibilidade de montar relatórios analíticos ad-hoc altamente customizáveis que uma ferramenta dedicada de BI externa (Opção D) ofereceria.

## Em que condição a recomendação muda
🟡 Se a demanda da diretoria exigir dashboards executivos altamente customizáveis com gráficos dinâmicos sem prazo de desenvolvimento, a Opção D (Power BI/Excel) passa à frente.

## Decisão do usuário
🟡 **Opção A: Hub de Relatórios Integrado no Dashboard UI**, decidido por **givas** em 2026-08-14T14:18:42-03:00.

## A validar antes de comprometer
🟡 Apresentar um protótipo de tela com tabelas e filtros de turno/bloco para 1 coordenador validar as perguntas-chave em 30 minutos antes de implementar a totalidade dos filtros.

## Riscos aceitos conscientemente
🟡 Risco de coordenadores solicitarem filtros ad-hoc não previstos na UI inicial; necessidade de garantir que rotas de exportação PDF/Excel rodem de maneira otimizada no servidor FastAPI.

---
Gerado por reversa-arbiter em 2026-08-14T14:18:45-03:00
Sessão: 002-gestao-relatorios-ocupacao-docentes
