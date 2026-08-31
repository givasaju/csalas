# Spec: occupancy-dashboard

**Versão:** 1.0  
**Status:** Rascunho  
**Autor:** reversa-spec-sdd  
**Data:** 2026-08-07  
**Reviewers:** N/A  

---

## 1. Resumo

O `occupancy-dashboard` é a interface de usuário (UI) baseada na web do ClassSync AI. Desenvolvido em React/Next.js, ele fornece painéis interativos em tempo real para visualização do mapa físico do campus, acompanhamento de taxas de ocupação, acompanhamento visual dos leilões automáticos de salas, gerenciamento de regras prediais e controle de reallocações de emergência.

---

## 2. Contexto e Motivação

**Problema:**  
Diretores de infraestrutura e coordenadores acadêmicos não dispõem de uma interface amigável para visualizar em tempo real quais salas estão ocupadas, quais estão ociosas e o andamento das negociações automáticas promovidas pelo motor de IA. Isso impede tomadas de decisões rápidas ou monitoramento da eficiência operacional.

**Evidências:**  
A reitoria necessita de relatórios consolidados de uso predial e os coordenadores reclamam que não conseguem saber com facilidade onde seus professores estão alocados em tempo útil no início do período letivo.

**Por que agora:**  
Para entregar uma camada visual premium e interativa que torne inteligíveis e acionáveis as informações brutas geradas pelo motor de IA e pelas regras acadêmicas do backend.

---

## 3. Goals (Objetivos)

- [ ] G-01: 🟡 Apresentar visualmente a taxa de ocupação de salas de aula e blocos prediais em tempo real.
- [ ] G-02: 🟡 Disponibilizar painel interativo de submissão de restrições para os coordenadores de curso.
- [ ] G-03: 🟡 Exibir alertas prediais imediatos de eficiência (indicações de blocos subocupados a fechar).

**Métricas de sucesso:**  
| Métrica | Baseline atual | Target | Prazo |
|---------|---------------|--------|-------|
| 🟡 Tempo de resposta de interação de UI | Vários segundos de processamento | < 100ms na transição de abas | 3 meses |
| 🟡 Taxa de adoção do portal | Uso zero de ferramentas web | > 95% de uso por coordenadores activos | 3 meses |

---

## 4. Non-Goals (Fora do Escopo)

- NG-01: 🟡 Criação ou customização de materiais didáticos das aulas.
- NG-02: 🟡 Visualização de dados privados e notas individuais dos estudantes do campus.
- NG-03: 🟡 Controle físico real de chaves ou trancas eletrônicas das portas de salas.

---

## 5. Usuários e Personas

**Usuário primário:** 🟡 Cláudio (Coordenador de Curso), que usa a interface para inserir as restrições da sua grade e ver suas salas finais.  
**Usuário secundário:** 🟡 Isabela (Diretora de Infraestrutura), que gerencia as metas prediais e acompanha o dashboard de consumo.  

**Jornada atual (sem a feature):**  
1. 🟡 O coordenador telefona para a secretaria predial para conferir qual sala foi reservada para sua disciplina.  
2. 🟡 A diretora predial imprime mapas físicos em papel para planejar onde alocar as monitorias do mês.  

**Jornada futura (com a feature):**  
1. 🟡 O coordenador acessa a aplicação web e visualiza de forma instatânea a grade completa em um grid interativo.  
2. 🟡 A diretora monitora as taxas de ocupação globais através de gráficos em tempo real no dashboard.  

---

## 6. Requisitos Funcionais

### 6.1 Requisitos Principais

| ID | Requisito | Prioridade | Critério de Aceite |
|----|-----------|-----------|-------------------|
| RF-01 | 🟡 O sistema deve exibir um grid de calendário interativo mostrando a ocupação de salas por bloco, andar e faixa horária. | Must | 🟡 Visualizar o grid do Bloco A e confirmar que os blocos de horário ocupados exibem o nome do curso correspondente. |
| RF-02 | 🟡 O sistema deve fornecer uma tela de cadastro de restrições de horários e infraestrutura para coordenadores. | Must | 🟡 Submeter um formulário de restrição de professor e validar que a requisição de API correspondente é despachada corretamente. |
| RF-03 | 🟡 O sistema deve exibir notificações em tempo real na tela quando um leilão de salas entre coordenações for iniciado ou resolvido pelo motor de IA. | Must | 🟡 Simular recebimento de mensagem WebSockets e verificar se o toast de notificação surge na tela em menos de 500ms. |
| RF-04 | 🟡 O sistema deve destacar visualmente em um mapa esquemático 2D os blocos que estão com ocupação crítica (abaixo de 20%) para tomada de ação. | Should | 🟡 Simular Bloco C com 10% de ocupação e validar se o bloco é renderizado na cor vermelha com alerta de eficiência predial. |
| RF-05 | 🟡 O sistema deve permitir exportar relatórios de ocupação e eficiência predial em formato PDF. | Could | 🟡 Clicar no botão "Exportar PDF" e confirmar a geração do arquivo de relatório visual estruturado. |

### 6.2 Fluxo Principal (Happy Path)

1. 🟡 A diretora Isabela efetua o login no sistema.  
2. 🟡 O dashboard lê as taxas de ocupação do backend e renderiza os gráficos de eficiência predial na tela inicial.  
3. 🟡 Isabela clica em um bloco no mapa 2D e visualiza a listagem de salas ativas e ociosas.  
4. 🟡 O sistema atualiza os dados em background de forma transparente.  

### 6.3 Fluxos Alternativos

**Fluxo Alternativo A — Edição offline de restrição:**  
1. 🟡 O coordenador Cláudio edita as restrições prediais todavia perde a conexão de internet temporariamente.  
2. 🟡 O sistema armazena a alteração no `localStorage`, altera o indicador de status para "Modo Offline" e sincroniza as edições pendentes assim que a conexão é restaurada.  

---

## 7. Requisitos Não-Funcionais

| ID | Requisito | Valor alvo | Observação |
|----|-----------|-----------|------------|
| RNF-01 | Performance | 🟡 Tempo de carregamento inicial (FCP) < 1.5s | Crucial para boa experiência em dispositivos móveis no campus. |
| RNF-02 | Acessibilidade | 🟡 Compatibilidade com WCAG 2.1 AA | Interface acessível para leitores de tela e navegação por teclado. |
| RNF-03 | Responsividade | 🟡 Suporte a telas de celulares e desktops | Flexibilidade para coordenadores acessarem em deslocamentos no campus. |

---

## 8. Design e Interface

**Componentes afetados:**  
- Grid de Calendário de Ocupação  
- Formulário de cadastro de restrições  
- Toast Notification Manager  

**Comportamento esperado:**  
- 🟡 Elementos interativos mudam de cor suavemente ao passar o mouse (hover).  
- 🟡 Transições de telas e abertura de modais com animações sutis de fade-in.  

**Estados da UI:**  
- *Estado vazio:* Quando não há turmas cadastradas para o bloco selecionado, o painel exibe uma ilustração neutra e o texto "Nenhuma turma agendada para este bloco".  
- *Estado de carregamento:* Um esqueleto (skeleton component) cinza pulsante no lugar dos gráficos e tabelas de dados.  
- *Estado de erro:* Banner vermelho no topo com texto claro do problema ("Falha de conexão com o servidor") e um botão "Tentar novamente".  
- *Estado de sucesso:* Toast verde no canto inferior direito ("Configurações de restrição salvas com sucesso!").  

---

## 9. Modelo de Dados

**Entidades novas ou modificadas:**  
```
DashboardState {
  active_tab: string
  selected_block_id: string
  connection_status: string // online, offline, reconnecting
  notifications: list       // toasts ativos em tela
}
```

---

## 10. Integrações e Dependências

| Dependência | Tipo | Impacto se indisponível |
|-------------|------|------------------------|
| API do Academic Space Manager | Obrigatória | O portal carrega a estrutura estática todavia não exibe dados acadêmicos ou salas. |
| Gateway WebSockets do Engine | Should | Alertas e negociações de salas em tempo real param de funcionar, exigindo refresh manual. |

---

## 11. Edge Cases e Tratamento de Erros

| Cenário | Trigger | Comportamento esperado |
|---------|---------|----------------------|
| EC-01: 🟡 Backend Fora do Ar (Falha de Rede) | O dashboard tenta buscar dados de salas contudo a API do backend retorna erro de timeout ou falha HTTP 5xx | 🟡 A UI bloqueia edições, ativa o estado de erro, exibe banner informando instabilidade temporária e tenta reconexão automática de 30 em 30 segundos. |
| EC-02: 🟡 Formato de payload inválido de resposta | A API do backend retorna dados estruturados de forma corrompida ou incompleta | 🟡 O dashboard executa um fallback seguro (tratando campos nulos), limpa o console de erros para o usuário, e exibe banner sugerindo recarregar o navegador. |
| EC-03: 🟡 Perda de Conexão WebSockets em lote | Queda de rede wifi durante o andamento de um leilão de salas crítico | 🟡 O sistema reverte a exibição dinâmica do leilão para status "Aguardando sincronização", e notifica o coordenador para não desligar o painel. |
| EC-04: 🟡 Envio de formulário com dados em branco | Usuário clica em salvar restrição sem preencher o nome do docente ou horários | 🟡 A UI bloqueia o clique de envio, destaca os campos obrigatórios vazios em borda vermelha e exibe mensagem de erro na base do input. |

---

## 12. Segurança e Privacidade

- **Autenticação:** 🟡 Verificação de sessão ativa via cookies seguros (HttpOnly) em cada requisição de rota interna do Next.js.  
- **Autorização:** 🟡 Coordenações não possuem acesso à aba de Configurações Globais de Blocos (restrito a Isabela).  

---

## 13. Plano de Rollout

- **Estratégia:** 🟡 Rollout gradual (canary deploy) iniciando com acesso liberado a apenas 3 coordenações de cursos de teste para detecção precoce de inconsistências de interface.  

---

## 14. Open Questions

| # | Pergunta | Impacto | Dono | Prazo |
|---|---------|---------|------|-------|
| OQ-01 | 🟡 Será desenvolvido um aplicativo nativo móvel ou a versão web responsiva será suficiente para cobrir os professores em sala? | Baixo | Design Lead | Fase de prototipagem visual |

---

## 15. Decisões Tomadas (Decision Log)

| Decisão | Alternativas consideradas | Racional |
|---------|--------------------------|---------|
| 🟡 Uso de Next.js Server Components para dados estáticos | Single Page Application (SPA) pura com React convencional | Acelera consideravelmente o carregamento inicial (FCP) de dados fixos prediais do campus, melhorando a UX. |

---

## Avaliação de Qualidade

```
============================================================
  SPEC QUALITY REPORT
  Arquivo: _reversa_sdd/sdd/occupancy-dashboard.md
============================================================

  SCORE TOTAL: 100.0/100  —  ⭐ Excelente — Pronta para implementação

  BREAKDOWN POR DIMENSÃO:
  Dimensão             Score      Peso     Contribuição
  --------------------------------------------------
  Completude           100%       30%     30.0/pt
  Testabilidade        100%       25%     25.0/pt
  Clareza              100%       20%     20.0/pt
  Escopo               100%       15%     15.0/pt
  Edge Cases           100%       10%     10.0/pt

  ✅ PONTOS FORTES:
     ✅ Seção 1 (Resumo) presente e preenchida
     ✅ Seção 2 (Contexto) presente e preenchida
     ✅ Seção 3 (Goals) presente e preenchida
     ✅ Seção 4 (Non-Goals) presente e preenchida
     ✅ Seção 5 (Usuários) presente e preenchida
     ✅ Cobertura adequada de edge cases
============================================================
```
