# Spec: academic-space-manager

**Versão:** 1.0  
**Status:** Rascunho  
**Autor:** reversa-spec-sdd  
**Data:** 2026-08-07  
**Reviewers:** N/A  

---

## 1. Resumo

O `academic-space-manager` é o componente de backend e banco de dados do ClassSync AI encarregado de gerenciar o inventário físico do campus (blocos, salas, recursos) e os dados acadêmicos (professores, turmas, disciplinas, e restrições horárias/infraestruturais declaradas). Ele fornece as APIs fundamentais que servem de entrada para o motor de IA (`core-allocation-engine`).

---

## 2. Contexto e Motivação

**Problema:**  
As informações sobre grades de horários, indisponibilidades de professores e especificidades físicas das salas (capacidade, recursos computacionais, acessibilidade) ficam espalhadas em planilhas despadronizadas e no ERP acadêmico legado de forma estática. Não há um repositório centralizado que correlacione esses dados para viabilizar algoritmos de otimização inteligentes.

**Evidências:**  
Turmas alocadas em laboratórios sem computadores funcionais, alunos cadeirantes matriculados em salas no segundo andar sem elevador e professores escalados para lecionar no mesmo horário em salas geograficamente distantes.

**Por que agora:**  
Para alimentar o motor de IA cooperativo com dados limpos, consistentes e estruturados, eliminando o lixo nas entradas de processamento que inviabilizaria qualquer otimização.

---

## 3. Goals (Objetivos)

- [ ] G-01: 🟡 Centralizar o inventário físico de salas de aula e recursos prediais do campus com controle de estado.
- [ ] G-02: 🟡 Padronizar a declaração de restrições (grades de horários de docentes e necessidades de disciplinas).
- [ ] G-03: 🟡 Expor APIs de alta performance para extração rápida de dados pelo motor de IA.

**Métricas de sucesso:**  
| Métrica | Baseline atual | Target | Prazo |
|---------|---------------|--------|-------|
| 🟡 Tempo de cadastro de restrições | Várias horas em planilhas | < 15 minutos por curso | Início do semestre |
| 🟡 Integridade de dados de salas | Dados físicos defasados | 100% das salas auditadas no sistema | 1 mês |

---

## 4. Non-Goals (Fora do Escopo)

- NG-01: 🟡 Criação ou controle de diários de classe de professores.
- NG-02: 🟡 Processamento de matrículas de estudantes ou remanejamento individual de alunos.
- NG-03: 🟡 Controle financeiro de contratos docentes ou pagamento de horas-aula.

---

## 5. Usuários e Personas

**Usuário primário:** 🟡 Cláudio (Coordenador de Curso), que gerencia as disciplinas e restrições horárias de seus professores.  
**Usuário secundário:** 🟡 Isabela (Diretora de Infraestrutura), que cadastra novos blocos prediais, salas de aula e seus respectivos recursos disponíveis.  

**Jornada atual (sem a feature):**  
1. 🟡 O coordenador anota as preferências e indisponibilidades de horário dos professores em uma planilha.  
2. 🟡 A diretora de infraestrutura mantém um documento em PDF com a capacidade e recursos de cada sala.  
3. 🟡 Não há cruzamento rápido de dados para verificar se o professor pode usar a sala X no horário Y.  

**Jornada futura (com a feature):**  
1. 🟡 O coordenador entra na interface do ClassSync AI e cadastra as restrições acadêmicas da sua grade.  
2. 🟡 A diretora de infraestrutura mantém o banco de salas atualizado pelo sistema.  
3. 🟡 O sistema valida instantaneamente se os dados estão completos e consistentes, prontos para o motor de IA ler.  

---

## 6. Requisitos Funcionais

### 6.1 Requisitos Principais

| ID | Requisito | Prioridade | Critério de Aceite |
|----|-----------|-----------|-------------------|
| RF-01 | 🟡 O sistema deve permitir o cadastro de blocos e salas de aula com capacidade física, tipo (comum, laboratório, auditório), recursos (projetor, ar-condicionado) e restrição de acessibilidade. | Must | 🟡 Cadastrar uma sala com acessibilidade obrigatória e validar que o banco persiste essa flag corretamente. |
| RF-02 | 🟡 O sistema deve permitir o cadastro de disciplinas vinculadas aos seus requisitos mandatórios de infraestrutura física. | Must | 🟡 Associar a disciplina "Química Orgânica" ao recurso obrigatório "Laboratório de Química" e validar integridade. |
| RF-03 | 🟡 O sistema deve permitir o cadastro da grade de indisponibilidade de professores (dias e horários em que o docente não pode ministrar aulas). | Must | 🟡 Bloquear o professor "Claudio" nas segundas de manhã e testar se a API retorna essa restrição no payload. |
| RF-04 | 🟡 O sistema deve expor uma API GET `/api/v1/allocation/input-data` contendo o payload consolidado e higienizado para o motor de IA. | Must | 🟡 Chamar o endpoint e verificar se o JSON retornado segue a especificação técnica em menos de 1 segundo. |
| RF-05 | 🟡 O sistema deve aceitar a importação de planilhas CSV com a listagem inicial de salas e professores para acelerar o setup acadêmico. | Should | 🟡 Importar um CSV com 50 salas e verificar se todas aparecem registradas corretamente no banco. |

### 6.2 Fluxo Principal (Happy Path)

1. 🟡 A Diretora de Infraestrutura cadastra as salas de aula no painel.  
2. 🟡 O Coordenador de Curso vincula as restrições de horários dos docentes e as turmas a serem alocadas.  
3. 🟡 O sistema valida que nenhuma turma excede a capacidade das salas cadastradas e que não há restrições cruzadas impossíveis.  
4. 🟡 Os dados ficam persistidos de forma estruturada.  
5. 🟡 O motor de IA consome o endpoint REST para processamento.  

### 6.3 Fluxos Alternativos

**Fluxo Alternativo A — Importação Parcial com Erros:**  
1. 🟡 O coordenador envia uma lista de salas em CSV contendo 3 salas com capacidade negativa ou texto no lugar de números.  
2. 🟡 O sistema interrompe a transação de importação, aponta as linhas e colunas exatas dos erros e rejeita o arquivo inteiro, instruindo a correção.  

---

## 7. Requisitos Não-Funcionais

| ID | Requisito | Valor alvo | Observação |
|----|-----------|-----------|------------|
| RNF-01 | Performance | 🟡 Tempo de resposta da API GET de inputs < 500ms | O motor de IA requer download rápido de grandes payloads de dados. |
| RNF-02 | Integridade | 🟡 Integridade referencial total | Impossibilitar deleção de salas que possuem turmas ativas alocadas. |
| RNF-03 | Concorrência | 🟡 Suportar 50 coordenadores salvando restrições simultaneamente | Garante estabilidade no período crítico de início de semestre. |

---

## 8. Design e Interface

**Componentes afetados:**  
- API RESTful (`/api/v1/rooms`, `/api/v1/teachers`, `/api/v1/restrictions`)  
- Banco de dados relacional (PostgreSQL)  

**Comportamento esperado:**  
- 🟡 As APIs de escrita devem responder com status `201 Created` ou `200 OK` contendo a entidade persistida no corpo de resposta.  
- 🟡 Validações de entrada de API mal-formatadas devem retornar HTTP `420 Unprocessable Entity` com mensagem descritiva no padrão JSON.  

---

## 9. Modelo de Dados

**Entidades novas ou modificadas:**  
```
Room {
  id: uuid
  block_id: string
  name: string
  capacity: integer
  room_type: string         // common, lab, auditorium
  is_accessible: boolean
  features: list            // projector, air_conditioner, computers
}

Teacher {
  id: uuid
  name: string
  email: string
}

TeacherRestriction {
  id: uuid
  teacher_id: uuid
  day_of_week: integer      // 1 to 7
  time_slot_id: string      // M1, M2, T1, T2, N1, N2
}
```

---

## 10. Integrações e Dependências

| Dependência | Tipo | Impacto se indisponível |
|-------------|------|------------------------|
| Banco de dados PostgreSQL | Obrigatória | O sistema fica totalmente inoperante. |
| API de Autenticação Central | Obrigatória | Coordenadores não conseguem acessar as telas de edição de dados. |

---

## 11. Edge Cases e Tratamento de Erros

| Cenário | Trigger | Comportamento esperado |
|---------|---------|----------------------|
| EC-01: 🟡 Exclusão de sala com agendamento ativo | O usuário tenta deletar uma sala física que possui aulas agendadas nela para o semestre corrente | 🟡 O sistema nega a exclusão, retorna erro HTTP `409 Conflict` e instrui o usuário a mover as turmas antes de deletar a sala física. |
| EC-02: 🟡 Entrada de dados inválidos de capacidade | Cadastro de sala com capacidade igual a 0 ou negativa | 🟡 O validador rejeita a entrada no backend e retorna erro HTTP `422 Unprocessable Entity` explicando a inconsistência. |
| EC-03: 🟡 Banco de Dados Indisponível (Timeout) | Falha de conexão ou timeout inesperado na comunicação com a instância de banco SQL | 🟡 A API retorna erro HTTP `503 Service Unavailable`, tenta um retry automático em background, aciona logs de emergência e avisa o monitor. |
| EC-04: 🟡 Restrição contraditória do próprio professor | Coordenador tenta cadastrar indisponibilidade no mesmo horário de uma aula obrigatória fixa | 🟡 O validador de restrições avisa em tempo de inserção que a restrição entra em conflito direto com o escopo da disciplina e rejeita o salvamento. |

---

## 12. Segurança e Privacidade

- **Autenticação:** 🟡 Autenticação JWT obrigatória para qualquer requisição HTTP de escrita.  
- **Autorização:** 🟡 Apenas usuários com a role `Coordination` ou `Infrastructure` podem modificar entidades.  
- **Dados sensíveis:** 🟡 Nome e e-mail dos docentes protegidos em conformidade com as regras de sigilo da instituição (LGPD).  

---

## 13. Plano de Rollout

- **Estratégia:** 🟡 Deploy inicial em ambiente de homologação para carga massiva de teste de dados prediais antes da liberação do painel para os coordenadores.  

---

## 14. Open Questions

| # | Pergunta | Impacto | Dono | Prazo |
|---|---------|---------|------|-------|
| OQ-01 | 🟡 Será integrada uma rotina de sincronização automática diária com o ERP Acadêmico legado ou a importação por CSV será o padrão? | Alto | Product Manager | Fim do refinamento técnico |

---

## 15. Decisões Tomadas (Decision Log)

| Decisão | Alternativas consideradas | Racional |
|---------|--------------------------|---------|
| 🟡 Uso de UUID para IDs das salas e professores | IDs numéricos sequenciais (BigInt) | Facilita a migração, sincronização e segurança das APIs, evitando enumeração maliciosa de recursos prediais. |

---

## Avaliação de Qualidade

```
============================================================
  SPEC QUALITY REPORT
  Arquivo: _reversa_sdd/sdd/academic-space-manager.md
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

