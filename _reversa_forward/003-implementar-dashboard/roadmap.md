# Roadmap: Implementar a interface visual occupancy-dashboard

> Identificador: `003-implementar-dashboard`  
> Data: `2026-08-07`  
> Requirements: `_reversa_forward/003-implementar-dashboard/requirements.md`  
> Confidência: 🟢 CONFIRMADO, 🟡 INFERIDO, 🔴 LACUNA  

---

## 1. Resumo da abordagem

A interface visual responsiva `occupancy-dashboard` será implementada como uma Single Page Application (SPA) em React integrada ao backend de alocação. Ela consumirá a API consolidada `/api/v1/allocation/input-data` e o status do processamento assíncrono `/api/v1/allocation/status/{task_id}`.

A tela exibirá 4 cards principais de métricas (KPIs), uma tabela de auditoria contendo o histórico detalhado de lances de créditos do leilão cooperativo (AAC/AMR) e um controle interativo com botão para disparo do motor de alocação de salas, exibindo feedback de progresso em tempo real. A biblioteca Recharts será utilizada para a plotagem dos gráficos de ocupação física de blocos.

---

## 2. Princípios aplicados

Não há princípios específicos cadastrados no arquivo `.reversa/principles.md` deste projeto.

---

## 3. Decisões técnicas

| ID | Decisão | Justificativa | Alternativas descartadas | Confidência |
|----|---------|----------------|--------------------------|-------------|
| D-01 | **Uso da biblioteca Recharts** | Renderização responsiva baseada em SVG que permite total interatividade no React. | Uso de Canvas 2D imperativo puro. | 🟢 |
| D-02 | **Mecanismo de Polling com debounce para progresso** | Garante atualizações visuais de andamento da IA de alocação (a cada 2s) enquanto o status for `queued` ou `running` sem sobrecarregar a rede. | Uso de conexões bidirecionais WebSockets de alta complexidade. | 🟢 |

---

## 4. Premissas

Nenhuma premissa sob dúvida ativa. Todas as questões levantadas no `requirements.md` foram esclarecidas no clarify.

---

## 5. Delta arquitetural

A arquitetura do ClassSync AI será expandida com a interface do usuário:

| Componente | Arquivo de origem no legado | Tipo de mudança | Resumo |
|------------|------------------------------|-----------------|--------|
| **occupancy-dashboard** | `_reversa_sdd/sdd/occupancy-dashboard.md` | componente-novo | Módulo de interface visual responsiva do ClassSync AI. |

---

## 6. Delta no modelo de dados

- Resumo das mudanças: Mapeamento de estado em React para monitorar a execução assíncrona, progresso e armazenar as métricas prediais de ocupação e créditos.
- Detalhe em: `_reversa_forward/003-implementar-dashboard/data-delta.md`

---

## 7. Delta de contratos externos

| Contrato | Tipo | Arquivo de detalhe |
|----------|------|--------------------|
| **dashboard-ui-integration** | HTTP/JSON | `_reversa_forward/003-implementar-dashboard/interfaces/dashboard-ui.md` |

---

## 8. Plano de migração

Nenhuma migração aplicável (cenário greenfield).

---

## 9. Riscos e mitigações

| Risco | Impacto | Probabilidade | Mitigação |
|-------|---------|---------------|-----------|
| Inconsistência visual em dispositivos móveis devido a gráficos SVG grandes | médio | média | Configurar contêineres dinâmicos `<ResponsiveContainer>` do Recharts para redimensionamento fluido. |
| Inutilização do painel por indisponibilidade de rede temporária do backend | médio | baixa | Exibir esqueleto (Skeleton screens) com aviso e botão de recarga manual das APIs. |

---

## 10. Critério de pronto

- [ ] Todas as ações do `actions.md` marcadas `[X]`
- [ ] `regression-watch.md` gerado
- [ ] Interface validada visualmente com mocks de estados vazios, carregamento e sucesso de alocação de salas.

---

## 11. Histórico de alterações

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-08-07 | Versão inicial gerada por `/reversa-plan` | reversa |
