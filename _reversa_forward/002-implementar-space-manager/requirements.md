# Requirements: Implementar o gerenciador acadêmico academic-space-manager

> Identificador: `002-implementar-space-manager`  
> Data: `2026-08-07`  
> Pasta da extração reversa: `_reversa_sdd/`  
> Confidência: 🟢 CONFIRMADO, 🟡 INFERIDO, 🔴 LACUNA / DÚVIDA  

---

## 1. Resumo executivo

Esta feature entrega o componente de persistência de backend `academic-space-manager` do ClassSync AI. Ele será responsável por expor as APIs de cadastro e gerenciamento predial (blocos, salas de aula, capacidades e recursos) e dados acadêmicos (professores, disciplinas, indisponibilidade horária e demandas de turmas). Ele atuará como a base de dados de entrada para o processamento do motor de inteligência artificial.

---

## 2. Contexto a partir do legado

As definições do gerenciador acadêmico baseiam-se diretamente nos documentos concebidos e especificados no refinamento greenfield de design de software:

| Fonte | Trecho relevante | Confidência |
|-------|------------------|-------------|
| `_reversa_sdd/prd.md#4. Escopo (in)` | Cadastro de restrições de professores (grade, horários) e demandas de turmas. | 🟡 |
| `_reversa_sdd/sdd/academic-space-manager.md#1. Resumo` | O gerenciador é responsável por prover APIs de consulta física e acadêmica. | 🟡 |
| `_reversa_sdd/sdd/academic-space-manager.md#6. Requisitos Funcionais` | Requisitos de cadastro de blocos, salas, indisponibilidades de professores e API GET de consolidação. | 🟡 |

---

## 3. Personas e cenários de uso

| Persona | Objetivo | Cenário-chave |
|---------|----------|---------------|
| **Cláudio (Coordenador de Curso)** | Registrar as restrições horárias dos professores e as necessidades de infraestrutura do curso. | Acessar o painel para cadastrar que o professor X não pode lecionar na segunda-feira pela manhã. |
| **Isabela (Diretora de Infraestrutura)** | Manter o inventário de salas de aula e recursos físicos do campus sempre atualizado. | Atualizar a capacidade e adicionar a flag de acessibilidade em uma sala após reforma predial. |

---

## 4. Regras de negócio novas ou alteradas

1. **RN-01:** Bloqueio de deleção física de salas de aula que possuam vínculos com alocações ativas no semestre corrente. 🟡
   - Origem no legado: `_reversa_sdd/sdd/academic-space-manager.md#11. Edge Cases (EC-01)`
   - Tipo: nova
2. **RN-02:** Validação no backend impedindo capacidades físicas de salas de aula menores ou iguais a zero. 🟡
   - Origem no legado: `_reversa_sdd/sdd/academic-space-manager.md#11. Edge Cases (EC-02)`
   - Tipo: nova
3. **RN-03:** Proteção de dados de nome e e-mail dos docentes no payload público em conformidade com as diretivas de privacidade acadêmica. 🟡
   - Origem no legado: `_reversa_sdd/sdd/academic-space-manager.md#12. Segurança e Privacidade`
   - Tipo: nova

---

## 5. Requisitos Funcionais

| ID | Requisito | Prioridade | Critério de aceite | Confidência |
|----|-----------|------------|--------------------|-------------|
| RF-01 | O sistema deve expor endpoints CRUD para gerenciamento de salas (capacidade, recursos, bloco, acessibilidade). | Must | Chamar a API POST `/api/v1/rooms` e verificar se a sala é inserida no banco com sucesso. | 🟡 |
| RF-02 | O sistema deve permitir que coordenadores cadastrem a grade semanal de indisponibilidade de horários dos professores. | Must | Cadastrar indisponibilidade do professor X na terça-feira e validar se a API retorna esse registro. | 🟡 |
| RF-03 | O sistema deve expor o endpoint GET `/api/v1/allocation/input-data` contendo a consolidação higienizada para o motor de IA. | Must | Chamar o endpoint consolidado e validar se o JSON retornado segue a tipagem de dados correta em < 500ms. | 🟡 |
| RF-04 | O sistema deve impedir a alteração de dados de restrição enquanto uma rodada de alocação de IA estiver em execução. | Should | Tentar atualizar uma restrição de professor durante uma execução ativa e verificar se a API retorna erro HTTP 409. | 🟡 |

---

## 6. Requisitos Não Funcionais

| Tipo | Requisito | Evidência ou justificativa | Confidência |
|------|-----------|----------------------------|-------------|
| Desempenho | Tempo de resposta do endpoint GET `/api/v1/allocation/input-data` < 500ms para grandes conjuntos de dados. | Necessário para evitar gargalos na comunicação inicial do motor de IA. | 🟡 |
| Segurança | Autenticação JWT obrigatória com controle de permissões por roles (`Coordination` ou `Infrastructure`). | Proteção dos dados contra edições indevidas de outros cursos. | 🟡 |
| Concorrência | Suportar pelo menos 50 requisições simultâneas de edição de restrições sem deadlock no banco. | Pico esperado no período de montagem semestral de grades. | 🟡 |

---

## 7. Critérios de Aceitação

```gherkin
Cenário: Tentativa de deleção de sala com uso ativo
  Dado que a sala 101 está alocada para a turma de Engenharia M1
  Quando o administrador envia um DELETE para `/api/v1/rooms/101`
  Então o sistema deve recusar a exclusão, retornar HTTP 409 Conflict e manter a sala ativa.

Cenário: Cadastro de sala com capacidade inválida
  Dado que o usuário tenta cadastrar uma nova sala com capacidade = -5
  Quando a requisição POST é enviada
  Então o sistema deve rejeitar, retornar HTTP 422 Unprocessable Entity e exibir mensagem de validação.
```

---

## 8. Prioridade MoSCoW

| Item | MoSCoW | Justificativa |
|------|--------|---------------|
| RF-01 | Must | Essencial para termos o inventário básico do campus. |
| RF-02 | Must | Necessário para alimentar o motor de IA com restrições horárias. |
| RF-03 | Must | Canal de comunicação obrigatório de entrada para a IA. |
| RF-04 | Should | Importante para evitar inconsistência de dados durante a execução da IA. |

---

## 9. Esclarecimentos

### Sessão 2026-08-07
- **Q:** Qual o formato aceito para a importação de salas de aula via arquivo?
- **R:** Arquivo simples de texto CSV com cabeçalho: `bloco,sala,capacidade,tipo,acessivel,recursos` (recursos múltiplos separados por ponto e vírgula).
- **Q:** Qual a política de retenção para logs e dados de indisponibilidade de professores de semestres anteriores?
- **R:** Reset automático ao final de cada semestre letivo (exigindo novas restrições para a nova grade).

---

## 10. Lacunas

Nenhuma pendência ou lacuna não resolvida.

---

## 11. Histórico de alterações

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-08-07 | Versão inicial gerada por `/reversa-requirements` | reversa |
| 2026-08-07 | Ambas as dúvidas resolvidas na sessão de clarify | reversa |
