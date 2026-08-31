# Requirements: Exportação de relatórios de ocupação das salas em PDF/Excel

> Identificador: `007-export-relatorios-pdf-excel`
> Data: `2026-08-08`
> Pasta da extração reversa: `_reversa_sdd/`
> Confidência: 🟢 CONFIRMADO, 🟡 INFERIDO, 🔴 LACUNA / DÚVIDA

## 1. Resumo executivo

Esta feature adiciona a funcionalidade de exportação de relatórios consolidados de ocupação de salas de aula nos formatos PDF e Excel (XLSX). Ela atende diretores de infraestrutura e coordenadores acadêmicos, permitindo gerar relatórios gerenciais sobre taxas de utilização de blocos, distribuição de turmas por sala física e horários de pico para tomada de decisão e auditoria externa.

## 2. Contexto a partir do legado

| Fonte | Trecho relevante | Confidência |
|-------|------------------|-------------|
| `_reversa_sdd/architecture.md#1.-visao-geral-do-sistema` | O ClassSync AI consolida o inventário de salas físicas e alocações por bloco predial. | 🟢 |
| `_reversa_sdd/domain.md#2.6-otimizacao-e-consolidacao-predial` | Mapeamento das taxas de ocupação por bloco e slot de tempo. | 🟢 |
| `_reversa_sdd/painel-ocupacao/requirements.md#visão-geral` | O `occupancy-dashboard` exibe KPIs de ocupação e auditoria predial. | 🟢 |
| `_reversa_sdd/addenda/003-implementar-dashboard.md#resumo-da-entrega` | Interface SPA integrada em `src/api/static/` pronta para novos controles visuais. | 🟢 |

## 3. Personas e cenários de uso

| Persona | Objetivo | Cenário-chave |
|---------|----------|---------------|
| Isabela (Diretora de Infraestrutura) | Extrair relatórios consolidados de ocupação predial em PDF para apresentação executiva. | Isabela clica em "Exportar PDF" no dashboard e baixa um documento formatado com gráficos e tabelas de ocupação dos blocos. |
| Cláudio (Coordenador de Curso) | Exportar planilha detalhada em Excel com a matriz de alocação de salas por turma e slot. | Cláudio clica em "Exportar Excel" para obter os dados brutos filtráveis de turmas e salas. |

## 4. Regras de negócio novas ou alteradas

1. **RN-01: Disponibilização Transacional de Arquivos de Exportação** 🟢
   - Origem no legado: N/A (nova)
   - Tipo: nova
2. **RN-02: Formatação Padronizada de Relatório Excel (XLSX)** 🟢
   - Origem no legado: N/A (nova)
   - Tipo: nova
3. **RN-03: Formatação Visual de Relatório PDF** 🟢
   - Origem no legado: `_reversa_sdd/painel-ocupacao/requirements.md#RN-06`
   - Tipo: nova
   - O PDF deve adotar estilo de Impressão Limpa: fundo branco com cabeçalho institucional simples em preto e branco para rápida impressão física.
4. **RN-04: Autenticação em Endpoints de Download** 🟢
   - Origem no legado: `_reversa_sdd/domain.md#3.-seguranca-e-autenticacao`
   - Tipo: nova

## 5. Requisitos Funcionais

| ID | Requisito | Prioridade | Critério de aceite | Confidência |
|----|-----------|------------|--------------------|-------------|
| RF-01 | Endpoint backend `GET /api/v1/reports/occupancy/pdf` para exportação em PDF. | Must | Retornar cabeçalho `Content-Type: application/pdf` com o documento PDF compilado da ocupação atual das salas. | 🟢 |
| RF-02 | Endpoint backend `GET /api/v1/reports/occupancy/excel` para exportação em Excel. | Must | Retornar cabeçalho `Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet` com o arquivo `.xlsx`. | 🟢 |
| RF-03 | Botões de acionamento de exportação PDF e Excel no `occupancy-dashboard`. | Must | Adicionar botões com ícone de download no painel SPA executando o download direto dos relatórios. | 🟢 |
| RF-04 | Inclusão de estatísticas consolidadas de ocupação por bloco nos relatórios. | Must | Exibir total de salas, capacidade total, vagas ocupadas e percentual de ocupação por bloco nos relatórios. | 🟢 |
| RF-05 | Filtros opcionais por bloco predial e por turno na geração de relatórios. | Should | Permitir os parâmetros query params `block_id` e `shift` (`M`, `T`, `N`) para filtragem dos dados do relatório. | 🟢 |

## 6. Requisitos Não Funcionais

| Tipo | Requisito | Evidência ou justificativa | Confidência |
|------|-----------|----------------------------|-------------|
| Desempenho | O tempo de geração dos relatórios (PDF ou Excel) não deve exceder 2 segundos para o volume atual de salas do campus. | Evidência em `_reversa_sdd/architecture.md#4.4` | 🟢 |
| Segurança | Os endpoints de exportação devem validar autenticação JWT da sessão ativa. | Evidência em `_reversa_sdd/domain.md#3.-seguranca-e-autenticacao` | 🟢 |
| Usabilidade | Os arquivos baixados devem ter nomes descritivos com a data de geração (ex: `relatorio-ocupacao-2026-08-08.pdf`). | Rationale de padrão de usabilidade | 🟢 |

## 7. Critérios de Aceitação

```gherkin
Cenário: Exportação com sucesso de relatório de ocupação em formato PDF
  Dado que o usuário está autenticado com token JWT válido
  Quando ele solicita a rota GET /api/v1/reports/occupancy/pdf
  Então o backend responde com status 200 OK
  E o Content-Type da resposta é application/pdf
  E o corpo da resposta contém um documento PDF estruturado com KPIs e ocupação dos blocos.

Cenário: Exportação com sucesso de planilha em formato Excel
  Dado que o usuário está autenticado com token JWT válido
  Quando ele solicita a rota GET /api/v1/reports/occupancy/excel
  Então o backend responde com status 200 OK
  E o Content-Type da resposta é application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
  E o arquivo retornado contém as abas de resumo por bloco e detalhamento de turmas.

Cenário: Tentativa de exportação sem autenticação válida
  Dado que a requisição não inclui o cabeçalho Authorization correto
  Quando a rota GET /api/v1/reports/occupancy/pdf é acionada
  Então o sistema retorna status 401 Unauthorized
  E nenhuma exportação é efetuada.
```

## 8. Prioridade MoSCoW

| Item | MoSCoW | Justificativa |
|------|--------|---------------|
| RF-01 | Must | Requisito fundamental para relatórios executivos em PDF. |
| RF-02 | Must | Requisito fundamental para análise de dados brutos pelos coordenadores em Excel. |
| RF-03 | Must | Integração visual no dashboard para acionamento simples pelos usuários. |
| RF-04 | Must | Dados de ocupação por bloco são essenciais no conteúdo retornado. |
| RF-05 | Should | Filtros por bloco predial e turno aprimoram a usabilidade e o detalhamento analítico. |

## 9. Esclarecimentos

### Sessão 2026-08-08

- **Q:** Qual o layout visual e estilo gráfico desejado para os relatórios em PDF?  
  **R:** Estilo Impressão Limpa: Fundo branco com cabeçalho simples em preto e branco para rápida impressão física.
- **Q:** Quais opções de filtragem prévia devem ser suportadas nas rotas de exportação (PDF/Excel)?  
  **R:** Permite filtro opcional por Bloco Predial (`block_id`) e por Turno (`shift`: `M`, `T`, `N`) via query params.

## 10. Lacunas

Nenhuma lacuna pendente nesta versão.

## 11. Histórico de alterações

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-08-08 | Versão inicial gerada por `/reversa-requirements` | reversa |
| 2026-08-08 | Resolução de dúvidas via `/reversa-clarify` (estilo visual PDF e filtros query params) | reversa |
