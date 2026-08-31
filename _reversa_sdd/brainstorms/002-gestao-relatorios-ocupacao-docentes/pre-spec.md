# Pre-Spec: Gestão de Relatórios de Ocupação e Carga Docente

> Selo 🟡 PLANEJADO. Insumo de entrada para o próximo pipeline, não é uma spec.

## Problema
🟡 Dificuldade da coordenação acadêmica e de infraestrutura em obter relatórios analíticos claros (individuais e consolidados) sobre a taxa de ocupação dos ambientes por horários/turnos e sobre a grade horária e disciplinas sob responsabilidade de cada docente.

## Caminho escolhido
🟡 **Opção A: Hub de Relatórios Integrado no Dashboard UI**, adicionando uma aba/seção dedicada no frontend web com tabelas analíticas, filtros por bloco/turno/docente e botões de exportação PDF e Excel.

## Escopo mínimo da primeira entrega
🟡 Adição da aba "📊 Relatórios" com duas visões fundamentais:
1. **Ocupação de Ambientes**: Tabela consolidada com filtro por Bloco Predial e Turno (Manhã, Tarde, Noite).
2. **Ocupação e Carga Docente**: Tabela individualizada com filtro por Docente apresentando disciplinas lecionadas, slots e horários.
3. **Exportação**: Botões de download em PDF e Excel acionando os geradores do backend.

## Não-objetivos
🟡
- Gráficos visuais interativos ou heatmaps de salas (escopo futuro).
- Integração ou exportação para ferramentas externas de BI (Power BI / Metabase).
- Edição ou alteração manual de cadastros dentro da tela de relatórios.

## Restrições ativas
🟡 Manter total alinhamento com a stack existente (FastAPI no backend, HTML/CSS/JS Vanilla no frontend e SQLite como banco relacional).

## Critério de pronto
🟡 O coordenador consegue visualizar a ocupação de qualquer bloco por turno e a grade completa de qualquer docente selecionado na tela, efetuando os downloads dos relatórios em PDF e Excel sem erros.

## Premissa a validar primeiro
🟡 Apresentar um protótipo de tela com as duas tabelas e seletores para 1 coordenador validar os filtros em 30 minutos antes da codificação completa.

## Riscos herdados
🟡 Risco de pedidos por relatórios ad-hoc não previstos; risco de latência em exportações de tabelas muito grandes sem paginação.

## Âncoras no legado
🟡
- `_reversa_sdd/architecture.md#occupancy-dashboard`
- `_reversa_sdd/domain.md#teachers-rooms`
- `_reversa_sdd/inventory.md#src/api/routes.py`

## Dúvidas abertas
- Nenhum marcador `[DÚVIDA]` pendente.

---
Gerado por reversa-pre-spec em 2026-08-14T14:19:45Z
Sessão: 002-gestao-relatorios-ocupacao-docentes
Destino sugerido: /reversa-requirements
