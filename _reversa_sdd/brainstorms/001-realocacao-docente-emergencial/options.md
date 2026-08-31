# Options, realocacao-docente-emergencial

> Selo 🟡 PLANEJADO em todos os itens. Nenhuma opção foi escolhida ainda.

## Problema de referência
🟡 Quando ocorrer um afastamento não planejado de um docente, eu quero mitigar este problema, para conseguir uma realocação de horários e disciplinas de forma emergencial.

## Restrições ativas
🟡 Nenhuma declarada até o momento pelo usuário.

---

## Opção A, Remanejamento Manual Assistido
- **Em uma frase:** 🟡 Interface administrativa no painel existente que calcula janelas de compatibilidade docente e apoia o coordenador no remanejamento pontual de turmas.
- **Como resolve o problema:** 🟡 Permite ao coordenador visualizar rapidamente professores da mesma coordenação com horários livres e alocar a turma afetada sem gerar novos conflitos.
- **Esforço:** 🟡 baixo , estende os endpoints REST do `academic-space-manager` e adiciona um modal de substituição no `occupancy-dashboard`.
- **Impacto no legado:** 🟡 Adiciona endpoint `/allocations/reassign` no FastAPI, reutilizando os cadastros de `Teacher` e `Restriction` sem alterar o algoritmo central de IA.
- **Reversibilidade:** 🟡 fácil , as alterações são limitadas a novas rotas de API e componentes de UI sem modificar o motor de leilão existente.
- **O que precisa ser verdade para funcionar:** 🟡 O coordenador aceita tomar a decisão final manualmente a partir de uma lista de sugestões de substitutos compatíveis.

## Opção B, Motor de Otimização Emergencial via IA
- **Em uma frase:** 🟡 Extensão do motor de IA (`core-allocation-engine`) para recalcular automaticamente a malha horária e predial no evento de afastamento.
- **Como resolve o problema:** 🟡 Executa uma rodada de re-alocação otimizada por leilão multiagente visando minimizar o número total de docentes e turmas impactados pela mudança.
- **Esforço:** 🟡 alto , exige modelar a função objetivo de impacto mínimo no `BuildingOptimizer` e gerenciar tarefas de realocação no `AllocationTask`.
- **Impacto no legado:** 🟡 Modifica a lógica de arbitragem do `core-allocation-engine` e cria estados adicionais de realocação emergencial nas máquinas de estado existentes.
- **Reversibilidade:** 🟡 cara , altera regras profundas da engine de otimização e tabelas de histórico de alocação.
- **O que precisa ser verdade para funcionar:** 🟡 Os dados de restrições de todos os professores da coordenação estarem rigorosamente atualizados e o algoritmo ser capaz de rodar em poucos segundos.

---

## Opção sempre presente, não construir
- **Em uma frase:** 🟡 Resolver o afastamento por meio de protocolo de contingência operacional e pedagógica, sem desenvolvimento de software.
- **Como resolve o problema:** 🟡 Estabelece diretrizes organizacionais onde a coordenação aciona professores substitutos previamente acordados por portaria interna ou migra temporariamente a carga para módulos assíncronos/EAD.
- **Esforço:** 🟡 baixo , exige apenas pactuação de processos, minutas de portaria e reuniões de alinhamento com os docentes.
- **Impacto no legado:** 🟡 Nenhum no código; altera apenas a rotina operacional da coordenação acadêmica.
- **Reversibilidade:** 🟡 fácil , pode ser ajustado ou revogado a qualquer momento por decisão administrativa da coordenação.
- **O que precisa ser verdade para funcionar:** 🟡 Que a regulamentação institucional permita aulas assíncronas/EAD temporárias ou haja disponibilidade prévia na carga horária dos docentes remanescentes.

## Opção sempre presente, usar algo pronto
- **Em uma frase:** 🟡 Adotar um software comercial de gestão e otimização de grade horária acadêmica de prateleira (ex: ASC TimeTables ou Celcat Timetabling).
- **Como resolve o problema:** 🟡 Utiliza os recursos nativos de substituição emergencial e gestão de ausências já desenvolvidos e testados nesses softwares comerciais.
- **Esforço:** 🟡 médio , envolve processo de licitação/contratação de SaaS e integração/importação dos dados de turmas e salas atuais.
- **Impacto no legado:** 🟡 Baixo a médio; requer exportar dados do ClassSync AI para a ferramenta externa ou integrá-la via API/Webhooks.
- **Reversibilidade:** 🟡 cara , dependência de fornecedor externo (lock-in) e custo de subscrição recorrente.
- **O que precisa ser verdade para funcionar:** 🟡 Haver orçamento disponível para licenciamento do software e viabilidade técnica de importação de turmas/docentes.

---
Gerado por reversa-explorer em 2026-08-13T12:53:00-03:00
Sessão: 001-realocacao-docente-emergencial
Nenhuma recomendação emitida por design. Convergência é papel de /reversa-arbiter.
