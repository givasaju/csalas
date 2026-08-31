# Requirements: Implementar a interface visual occupancy-dashboard

> Identificador: `003-implementar-dashboard`  
> Data: `2026-08-07`  
> Pasta da extração reversa: `_reversa_sdd/`  
> Confidência: 🟢 CONFIRMADO, 🟡 INFERIDO, 🔴 LACUNA / DÚVIDA  

---

## 1. Resumo executivo

Esta feature entrega a interface visual interativa `occupancy-dashboard` do ClassSync AI. Ela será construída em React/Next.js e fornecerá aos administradores de infraestrutura e coordenadores de curso dashboards em tempo real das métricas prediais (taxa de ocupação de blocos, economia de energia em blocos desativados) e histórico/auditoria dos leilões de créditos resolvidos pelo motor de alocação de salas.

---

## 2. Contexto a partir do legado

As definições do dashboard de ocupação baseiam-se nos artefatos gerados no refinamento greenfield:

| Fonte | Trecho relevante | Confidência |
|-------|------------------|-------------|
| `_reversa_sdd/prd.md#4. Escopo (in)` | Visualização de métricas prediais e relatórios de auditoria predial. | 🟡 |
| `_reversa_sdd/sdd/occupancy-dashboard.md#1. Resumo` | O dashboard é uma interface SPA interativa em React/Next.js. | 🟡 |
| `_reversa_sdd/sdd/occupancy-dashboard.md#6. Requisitos Funcionais` | Exigências de cards de KPI, tabelas de auditoria de leilões e controle de status de execuções. | 🟡 |

---

## 3. Personas e cenários de uso

| Persona | Objetivo | Cenário-chave |
|---------|----------|---------------|
| **Isabela (Diretora de Infraestrutura)** | Acompanhar a economia de energia do campus e visualizar quais blocos foram desligados de forma segura. | Visualizar o painel com o KPI de 25% de economia de energia e a lista contendo Bloco C desativado. |
| **Cláudio (Coordenador de Curso)** | Auditar a integridade das alocações do seu curso e acompanhar as transações de créditos do leilão. | Visualizar o extrato do leilão detalhando que a disciplina X venceu a disputa pagando Y créditos e Direito foi compensado. |

---

## 4. Regras de negócio novas ou alteradas

1. **RN-01:** Bloqueio de renderização de painéis de ocupação caso nenhuma execução de alocação de salas tenha sido concluída no semestre corrente (estado vazio). 🟡
   - Origem no legado: `_reversa_sdd/sdd/occupancy-dashboard.md#11. Edge Cases (EC-01)`
   - Tipo: nova
2. **RN-02:** Sinalização visual com cores de alerta em vermelho para salas que excedam a taxa de ocupação de segurança permitida. 🟡
   - Origem no legado: `_reversa_sdd/sdd/occupancy-dashboard.md#11. Edge Cases (EC-02)`
   - Tipo: nova

---

## 5. Requisitos Funcionais

| ID | Requisito | Prioridade | Critério de aceite | Confidência |
|----|-----------|------------|--------------------|-------------|
| RF-01 | O dashboard deve exibir 4 cards de KPIs principais: Taxa de Ocupação Geral, Economia de Energia, Blocos Desativados e Conflitos Resolvidos. | Must | Validar a renderização correta dos 4 cards de KPI com os dados consolidados da última tarefa. | 🟡 |
| RF-02 | O sistema deve exibir o extrato de auditoria detalhando as transações de leilões de créditos ocorridas (vencedor, perdedor, valor). | Must | Acessar a tabela de leilões e conferir as colunas de transações de crédito com os dados reais de lances. | 🟡 |
| RF-03 | O painel deve permitir disparar manualmente uma nova execução de alocação de salas por meio de um botão interativo. | Should | Clicar no botão e verificar se o status muda para "queued", "running" e exibe barra de progresso. | 🟡 |
| RF-04 | A interface deve apresentar estados adequados de carregamento (Skeleton screen) e estado de erro predial. | Should | Forçar falha de rede e verificar se a interface renderiza a tela de erro amigável ao usuário. | 🟡 |

---

## 6. Requisitos Não Funcionais

| Tipo | Requisito | Evidência ou justificativa | Confidência |
|------|-----------|----------------------------|-------------|
| Responsividade | Layout adaptável para dispositivos móveis, tablets e desktop (Mobile-first). | Isabela precisa consultar o dashboard em trânsito no campus via smartphone. | 🟡 |
| Latência | Tempo de renderização inicial da página sob conexão 3G móvel < 2.0 segundos. | RNF de acessibilidade em redes móveis de telefonia. | 🟡 |
| Acessibilidade | Conformidade mínima com as diretrizes WCAG 2.1 nível AA para contraste e navegação de teclado. | Garantir a inclusão e uso por todos os docentes. | 🟡 |

---

## 7. Critérios de Aceitação

```gherkin
Cenário: Visualização de estado de carregamento
  Dado que a requisição de busca de dados da API está lenta ou pendente
  Quando o usuário abre o dashboard
  Então o sistema deve exibir telas de esqueleto (Skeleton cards) em vez de tela branca.

Cenário: Disparar alocação em lote
  Dado que o administrador está logado na interface
  Quando ele clica no botão "Executar Otimização de Salas"
  Então o sistema deve enviar a requisição HTTP POST, exibir feedback de sucesso e atualizar o progresso na tela em tempo real.
```

---

## 8. Prioridade MoSCoW

| Item | MoSCoW | Justificativa |
|------|--------|---------------|
| RF-01 | Must | KPIs são as métricas chaves para tomada de decisão da diretora de infraestrutura. |
| RF-02 | Must | Necessário para dar transparência e auditoria de créditos para os coordenadores. |
| RF-03 | Should | Facilita a operação diária sem necessidade de usar clientes HTTP externos. |
| RF-04 | Should | Melhora a percepção de performance e robustez pelo usuário final. |

---

## 9. Esclarecimentos

### Sessão 2026-08-07
- **Q:** Qual biblioteca de visualização de gráficos deve ser adotada para renderização das métricas prediais?
- **R:** Recharts (baseado em SVG, extremamente responsivo e com excelente ecossistema no React).
- **Q:** O dashboard de ocupação predial deve permitir exportação física dos relatórios da grade?
- **R:** Apenas visualização rica em tela no momento (fora do escopo gerar arquivos PDF nativamente).

---

## 10. Lacunas

Nenhuma pendência ou lacuna não resolvida.

---

## 11. Histórico de alterações

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-08-07 | Versão inicial gerada por `/reversa-requirements` | reversa |
| 2026-08-07 | Ambas as dúvidas resolvidas na sessão de clarify | reversa |
