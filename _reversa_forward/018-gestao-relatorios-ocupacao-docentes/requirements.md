# Requirements: Gestão de Relatórios de Ocupação e Carga Docente

> Identificador: `018-gestao-relatorios-ocupacao-docentes`
> Data: `2026-08-14`
> Extração de referência: `_reversa_sdd/` (proveniente do Brainstorm Session 002 `pre-spec.md`)
> Confidência: 🟢 CONFIRMADO, 🟡 INFERIDO, 🔴 LACUNA / DÚVIDA

## 1. Resumo executivo

Implementar a nova aba de navegação **📊 Relatórios** no sistema ClassSync AI para prover visões analíticas consolidadas e individuais sobre a taxa de ocupação de ambientes acadêmicos por turno/bloco, além de relatórios detalhados das disciplinas e horários lecionados por cada docente. A interface contará com filtros interativos em tempo real e integração direta com os geradores de arquivos PDF e Excel.

## 2. Contexto a partir do legado

| Fonte | Trecho relevante | Confidência |
|-------|------------------|-------------|
| `_reversa_sdd/architecture.md#occupancy-dashboard` | Painel principal e estrutura de relatórios de exportação em PDF e Excel. | 🟢 |
| `_reversa_sdd/domain.md#teachers-rooms` | Mapeamento de docentes, disciplinas, restrições e salas físicas. | 🟢 |
| `_reversa_sdd/inventory.md#src/api/routes.py` | Rotas de backend para exportação em `/api/v1/reports/pdf` e `/api/v1/reports/excel`. | 🟢 |
| `_reversa_sdd/addenda/016-gestao-com-ia-aba.md` | Estrutura de abas do navbar principal. | 🟢 |

## 3. Personas e cenários de uso

| Persona | Objetivo | Cenário-chave |
|---------|----------|---------------|
| Coordenador de Curso / Infraestrutura | Consultar a ocupação de um bloco específico por turno e a carga docente | Acessa a aba "📊 Relatórios", escolhe o Bloco e Turno na visão coletiva ou o Docente na visão individual, visualiza a tabela formatada e baixa o relatório em PDF/Excel. |

## 4. Regras de negócio novas ou alteradas

1. **RN-01:** Adição do 5º botão de aba no navbar principal intitulado **📊 Relatórios** disposta após **🤖 Gestão com IA**. 🟢
   - Origem no legado: `_reversa_sdd/architecture.md#occupancy-dashboard`
   - Tipo: nova
2. **RN-02:** Sub-seção 1 - **Relatório de Ocupação de Ambientes (Coletivo)**: 🟢
   - Exibir tabela com colunas: Sala, Bloco, Capacidade, Turno (Manhã, Tarde, Noite), Status Ocupação e Taxa de Ocupação %.
   - Filtros dinâmicos: Filtro por Bloco (Todos, Bloco A, Bloco B, etc.) e Filtro por Turno (Todos, Manhã, Tarde, Noite).
3. **RN-03:** Sub-seção 2 - **Relatório de Grade & Carga Horária Docente (Individual)**: 🟢
   - Exibir tabela com colunas: Código Disciplina, Nome da Disciplina, Sala Alocada, Slot/Horário, Carga Horária (horas).
   - Filtro dinâmico por Docente (seletor drop-down atualizado com a lista do banco SQLite).
4. **RN-04:** Botões de Exportação Integrada: 🟢
   - Botões **Exportar PDF** e **Exportar Excel** na aba de relatórios com parâmetro de filtro aplicado.

## 5. Requisitos Funcionais

| ID | Requisito | Prioridade | Critério de aceite | Confidência |
|----|-----------|------------|--------------------|-------------|
| RF-01 | Criar a aba `#reports-tab` no navbar principal com o botão `📊 Relatórios`. | Must | O botão aparece no topo e alterna a visão sem recarregar a página. | 🟢 |
| RF-02 | Exibir o painel de Ocupação Coletiva com filtro de Bloco e Turno. | Must | Alterar os seletores de Bloco/Turno filtra a tabela em tempo real. | 🟢 |
| RF-03 | Exibir o painel de Carga Horária Docente com filtro drop-down de Professor. | Must | Selecionar um docente exibe suas turmas, salas e horários correspondentes. | 🟢 |
| RF-04 | Conectar os botões de exportação aos endpoints `/api/v1/reports/pdf` e `/api/v1/reports/excel`. | Must | Clicar em exportar gera o arquivo para download no navegador. | 🟢 |

## 6. Requisitos Não Funcionais

| Tipo | Requisito | Evidência ou justificativa | Confidência |
|------|-----------|----------------------------|-------------|
| Desempenho | O processamento dos filtros em tela deve ser executado em menos de 100ms. | Rationale de experiência de uso em frontend Vanilla JS | 🟢 |
| Usabilidade | Manter o padrão estético (dark mode, glassmorphism e badges coloridos HSL) igual ao restante do sistema. | Diretrizes de design system do ClassSync AI | 🟢 |

## 7. Critérios de Aceitação

```gherkin
Cenário: Filtro de ocupação coletiva de ambientes por turno
  Dado que o usuário navega para a aba "📊 Relatórios"
  Quando ele seleciona o Bloco "Bloco A" e o Turno "Manhã"
  Então a tabela exibe apenas as salas do Bloco A com a taxa de ocupação do turno matutino

Cenário: Consulta individual de carga docente
  Dado que o usuário está na aba "📊 Relatórios"
  Quando ele seleciona o docente "Prof. Givaldo" no seletor de professores
  Então a tabela exibe a listagem completa de disciplinas, salas alocadas e horários lecionados por ele
```

## 8. Prioridade MoSCoW

| Item | MoSCoW | Justificativa |
|------|--------|---------------|
| RF-01 | Must | Aba principal de navegação para a nova funcionalidade. |
| RF-02 | Must | Requisito fundamental de relatório de ocupação por turno e ambiente. |
| RF-03 | Must | Requisito fundamental de relatório individual de disciplinas do docente. |
| RF-04 | Must | Requisito funcional de exportação de dados em PDF/Excel. |

## 9. Esclarecimentos

> Nenhuma dúvida registrada. Todos os requisitos foram alinhados no brainstorm session 002.

## 10. Lacunas

Nenhuma lacuna ou `[DÚVIDA]` pendente.

## 11. Histórico de alterações

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-08-14 | Versão inicial gerada por `/reversa-requirements` | reversa |
