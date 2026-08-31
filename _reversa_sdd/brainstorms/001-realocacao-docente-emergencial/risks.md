# Risks, realocacao-docente-emergencial

> Selo 🟡 PLANEJADO em todos os itens. Documento adversarial por design.

## Premortem
🟡 Manchete 1: "Professores recusam em massa as realocações propostas porque restrições informais de horário não estavam cadastradas no sistema, forçando a coordenação a voltar para o papel e WhatsApp." (causa raiz: dados de restrições desatualizados)
🟡 Manchete 2: "A realocação emergencial resolveu a turma do professor ausente, mas gerou um efeito dominó de insatisfação e sobrecarga em 5 outros docentes que não foram consultados." (causa raiz: otimização técnica focada na grade ignorando o impacto humano)
🟡 Manchete 3: "Coordenadores ignoram as sugestões do sistema por receio de questionamentos trabalhistas/sindicais e continuam fazendo acertos informais fora da plataforma." (causa raiz: falta de governança, aprovação formal e segurança jurídica)
🟡 Manchete 4: "A reorganização emergencial da grade travou por falta de salas com acessibilidade/recursos nos mesmos slots, deixando turmas pendentes sem solução." (causa raiz: acoplamento e rigidez de restrições físicas no legado)

**Manchete que mais assusta o usuário:** 🟡 Manchete 3: "Coordenadores ignoram as sugestões do sistema por receio de questionamentos trabalhistas/sindicais e continuam fazendo acertos informais fora da plataforma."

---

## Opção A, Remanejamento Manual Assistido
- **Premissa que mata:** 🟡 O coordenador dispõe de informações confiáveis de disponibilidade dos docentes e consegue negociar a substituição manualmente sem gerar atritos políticos/pessoais.
- **Teste barato da premissa:** 🟡 Simular uma licença recente em reunião de 30 minutos com o coordenador, fornecendo a lista de docentes com janelas livres e avaliando se ele conclui a escolha sem precisar ligar/mandar mensagem para cada um.
- **Custo escondido:** 🟡 `src/api/schemas.py` e `src/api/routes.py` — Custo de implementar trilha de auditoria e controle de permissões de aprovação formal para evitar questionamentos jurídicos.
- **Ponto sem volta:** 🟡 Quando as alterações de grade manuais começarem a ser efetivadas no banco acadêmico sem um fluxo de confirmação assinado pelo docente.

## Opção B, Motor de Otimização Emergencial via IA
- **Premissa que mata:** 🟡 Os docentes aceitam de forma passiva substituições e trocas de horários atribuídas por um algoritmo de IA sem negociação direta prévia.
- **Teste barato da premissa:** 🟡 Apresentar a 3 docentes uma grade "reotimizada automaticamente por IA" para cobrir uma licença fictícia e medir o nível de rejeição ou exigência de ajuste.
- **Custo escondido:** 🟡 `src/engine/core.py` (método `run_allocation`) e `src/engine/agents.py` (`ACC`/`AMR`) — Risco de efeito dominó: a re-alocação via leilão pode deslocar professores e turmas terceiras não envolvidas no afastamento inicial para satisfazer a consolidação predial do `BuildingOptimizer`.
- **Ponto sem volta:** 🟡 Quando o motor de IA disparar notificações automáticas de mudança de grade para os docentes sem uma etapa de validação humana prévia.

---

## Opção sempre presente, não construir
- **Premissa que mata:** 🟡 Os docentes da coordenação possuem margem em seus contratos/cargas horárias para absorver turmas de um afastamento de 60 dias via acordos informais.
- **Teste barato da premissa:** 🟡 Analisar os registros das últimas 3 licenças docentes e verificar o tempo médio em que turmas ficaram sem aulas efetivas até a resolução informal.
- **Custo escondido:** 🟡 `_reversa_sdd/domain.md` — Passivo trabalhista por acúmulo não registrado de carga horária e risco regulatório por descumprimento do plano de ensino das turmas.
- **Ponto sem volta:** 🟡 Abertura de processo administrativo ou denúncia de descumprimento de carga horária por parte de alunos/órgão regulador.

## Opção sempre presente, usar algo pronto
- **Premissa que mata:** 🟡 Os softwares de prateleira (SaaS) conseguem se integrar perfeitamente com os cadastros de `Teacher`, `Restriction` e regras de créditos do ClassSync AI.
- **Teste barato da premissa:** 🟡 Exportar a lista de professores/turmas do banco atual para um arquivo CSV e tentar importar em um trial gratuito de 7 dias de ferramenta comercial (ex: ASC TimeTables).
- **Custo escondido:** 🟡 `src/database.py` e `_reversa_sdd/dependencies.md` — Custo recorrente de licença comercial e desenvolvimento/manutenção de conectores de sincronização entre o SaaS e a base legado.
- **Ponto sem volta:** 🟡 Assinatura do contrato de licenciamento do software externo e migração da base operacional.

---

## Riscos transversais
🟡 **Segurança jurídica e trabalhista:** Alterações na atribuição de disciplinas sem aceite expresso do docente podem gerar passivos sindicais ou trabalhistas.
🟡 **Efeito dominó no motor de alocação legado:** O re-cálculo de grade pode propagar desalocações não intencionais em turmas que não tinham relação com a licença original (`src/engine/core.py`).
🟡 **Integridade e sincronização dos cadastros:** Se os dados de indisponibilidade docente (`Restriction`) não estiverem 100% em dia, qualquer recomendação (manual ou por IA) gerará conflitos na prática.

## O que precisa ser respondido antes de decidir
🟡 1. A instituição exige o aceite formal do docente substituto antes de efetivar a realocação no sistema?
🟡 2. A substituição deve ser restrita estritamente aos docentes da mesma coordenação/departamento ou pode envolver docentes de outras áreas?
🟡 3. É aceitável que a realocação modifique os horários de turmas/professores que NÃO estavam originalmente em licença (efeito dominó)?
🟡 4. O coordenador deve ter a palavra final para aprovar/rejeitar a proposta da plataforma antes da publicação?

---
Gerado por reversa-challenger em 2026-08-13T13:13:00-03:00
Sessão: 001-realocacao-docente-emergencial
