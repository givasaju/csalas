# PRD: ClassSync AI

> Selo 🟡 PLANEJADO. Documento gerado a partir de ideation + personas.

**Versão:** 1.0  
**Data:** 2026-08-07T13:48:00-03:00  
**Autor:** reversa-drafter  
**Status:** rascunho  

---

## 1. Problema

A alocação e distribuição de salas de aula em instituições de ensino (escolas/universidades) é um problema clássico de otimização altamente complexo (NP-difícil), comumente resolvido manualmente por planilhas ou de forma estática por ERPs rígidos. Isso gera conflitos constantes de horários entre coordenações, desperdício predial com salas ociosas ou superlotadas, altos custos operacionais com energia e limpeza em blocos subutilizados e extrema dificuldade de adaptação em tempo real a imprevistos (ex: salas danificadas).

### Quem sente

- **Cláudio (Coordenador de Curso):** Sente a dor no início de cada semestre acadêmico ao tentar conciliar as grades dos professores com a disponibilidade de salas e laboratórios específicos, participando de discussões de espaço inter-departamentais desgastantes.
- **Isabela (Diretora de Infraestrutura):** Sente a dor no dia a dia operacional devido à falta de visibilidade da real ocupação física do campus e à pressão orçamentária da Reitoria para reduzir o consumo de energia predial.

---

## 2. Personas-alvo

Referência completa em [`personas.md`](./personas.md). Resumo:

- **Cláudio (Coordenador de Curso)**: 🟡 Coordenador acadêmico sobrecarregado pela montagem semestral de grades e busca por salas adequadas. Dor principal: desperdício de tempo e desgaste na negociação manual de salas e laboratórios com outras coordenações acadêmicas.
- **Isabela (Diretora de Infraestrutura)**: 🟡 Gestora de logística acadêmica e infraestrutura física focada em redução de custos operacionais do campus. Dor principal: falta de visibilidade em tempo real sobre o uso efetivo de salas e altos custos prediais por salas subutilizadas em blocos abertos.

---

## 3. Métricas de sucesso

As métricas focam na otimização de espaço físico e na economia de recursos operacionais da instituição:

| Métrica | Unidade | Alvo | Prazo |
|---|---|---|---|
| 🟡 Redução na ociosidade física | Porcentagem (%) | Redução de 30% na ociosidade de assentos e laboratórios | 3 meses de uso |
| 🟡 Eliminação de conflitos de reserva | Quantidade (conflitos) | 0 conflitos de reservas no início do semestre letivo | Início do semestre letivo |
| 🟡 Redução de custos prediais | Porcentagem (%) | Redução de custos com energia (ar-condicionado e luz) nos blocos | 3 meses de uso |

---

## 4. Escopo (in)

- 🟡 Cadastro de restrições de professores (grade, horários) e demandas de turmas.
- 🟡 Especificação declarativa de requisitos de infraestrutura física obrigatórios por disciplina (computadores, acessibilidade, projetor, química, etc.).
- 🟡 Motor de inteligência artificial de alocação central (AAC) baseado em critérios de restrições rígidas (hard constraints) e preferências suaves (soft constraints).
- 🟡 Protocolo de negociação multiagente e mediação de conflitos automática (ACC + AMR) por meio de um sistema de créditos de prioridade acadêmica.
- 🟡 Painel (Dashboard) interativo para visualização da ocupação das salas de aula em tempo real.
- 🟡 Sugestão de agrupamento predial inteligente de turmas para economia energética do campus.

---

## 5. Não-objetivos (out)

- 🟡 Gerenciamento de folha de pagamento ou cálculo de carga horária financeira de professores.
- 🟡 Integração física com sensores IoT de presença/temperatura nas salas de aula (otimização predial declarativa baseada na ocupação planejada).
- 🟡 🟡 [INDEFINIDO, validar com usuário] Controle de presença/frequência de alunos nas salas.

---

## 6. Restrições

As restrições de arquitetura e conformidade técnica identificadas até o momento:

| Tipo | Descrição |
|---|---|
| 🟡 Técnica | Os agentes de IA devem ser implementados em Python, e a interface do usuário (painel/dashboard web) em React/Next.js. |
| 🟡 Prazo | 🟡 [INDEFINIDO, validar com usuário] |
| 🟡 Compliance | 🟡 [INDEFINIDO, validar com usuário] (Adequação à LGPD para manuseio de dados de alunos/professores) |
| 🟡 Orçamento | 🟡 [INDEFINIDO, validar com usuário] |

---

## 7. Dependências externas

- 🟡 Integração via API ou importação com o ERP Acadêmico existente na instituição de ensino para obter grades de turmas, docentes e turmas matriculadas.

---

## 8. Riscos

| Risco | Impacto | Probabilidade | Mitigação proposta |
|---|---|---|---|
| 🟡 Resistência das coordenações a perdas de "salas proprietárias" | Alto | Média | Permitir configuração de travas e prioridades absolutas na IA para salas muito específicas de coordenações. |
| 🟡 Lentidão de processamento e convergência do algoritmo multiagente | Médio | Baixa | Realizar o cálculo pesado de alocação assincronamente e aplicar caching para reallocações locais rápidas. |
| 🟡 Confusão logística de alunos e docentes com mudanças dinâmicas | Médio | Média | Envio automático de alertas e atualizações visuais em tempo real no painel do campus. |

---

## 9. Critérios de aceite (alto nível)

- 🟡 **Dado** que o Coordenador Cláudio cadastrou as restrições e submeteu as demandas do curso, **Quando** o processamento de alocação de salas é concluído, **Então** o sistema deve retornar uma grade de salas 100% compatível com a capacidade de alunos e as restrições técnicas (como laboratórios) sem conflitos com outros cursos.
- 🟡 **Dado** que a Diretora Isabela definiu as metas de consolidação de blocos prediais, **Quando** a IA calcular as alocações, **Então** as turmas devem ser agrupadas preferencialmente no menor número possível de blocos físicos, maximizando a eficiência de custos do campus.

---

## Pendências de cobertura

- 🟡 Definição de compliance e segurança de dados (LGPD).
- 🟡 Definição de cronograma/prazo e restrições de orçamento para desenvolvimento.
- 🟡 Decisão sobre o escopo de controle de presença/frequência de alunos.

---

Gerado por reversa-drafter em 2026-08-07T13:48:00-03:00  
Fontes: ideation.md, personas.md
