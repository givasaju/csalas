# Pre-Spec, realocacao-docente-emergencial

> Selo 🟡 PLANEJADO. Insumo de entrada para o próximo pipeline, não é uma spec.

## Problema
🟡 Afastamento repentino de docentes por motivos de saúde/licença durante o período letivo, deixando turmas sem cobertura e gerando risco de cancelamento de disciplinas e sobrecarga de coordenações.

## Caminho escolhido
🟡 Solução Híbrida: O motor de IA calcula opções de realocação emergencial e o coordenador escolhe no painel se resolve de forma assistida (selecionando alternativas) ou se delega a aprovação/execução ao agente de IA.

## Escopo mínimo da primeira entrega
🟡 Módulo de realocação emergencial restrito a uma única coordenação, permitindo notificar a licença do docente, acionar o cálculo de opções pelo motor de IA e prover a alternância dinâmica entre modo assistido e modo delegado.

## Não-objetivos
🟡 Realocação inter-departamental (entre coordenações distintas); envio de notificações externas via WhatsApp/SMS; e alteração de preferências gerais de salas de aula.

## Restrições ativas
🟡 Reutilizar a stack e arquitetura existente do ClassSync AI (FastAPI + SPA estática HTML/CSS + `core-allocation-engine`).

## Critério de pronto
🟡 No painel de ocupação, o coordenador seleciona um docente em licença e consegue alternar dinamicamente entre escolher manualmente uma das 3 alternativas sugeridas pela IA ou clicar em 'Delegar ao Agente de IA', com a nova grade de disciplinas e salas sendo atualizada no sistema em menos de 2 minutos.

## Premissa a validar primeiro
🟡 Apresentar o fluxo dinâmico (modo assistido vs. modo delegado) a um coordenador de curso para verificar a confiabilidade percebida na delegação ao agente de IA.

## Riscos herdados
🟡 Risco de efeito dominó no recálculo da grade afetando professores não envolvidos no afastamento; risco de restrições (`Restriction`) desatualizadas; e potenciais questionamentos trabalhistas sobre alteração de atribuição sem aceite assinado.

## Âncoras no legado
🟡 `src/engine/core.py` (`CoreAllocationEngine`), `src/engine/agents.py` (`ACC`/`AMR`), `src/api/routes.py` (`academic-space-manager`), e `src/api/static/index.html` (`occupancy-dashboard`).

## Dúvidas abertas
- [DÚVIDA] 🟡 O sistema deve exigir a confirmação/aceite explícito do professor substituto antes de efetivar a realocação no banco acadêmico quando o modo delegado for acionado?
- [DÚVIDA] 🟡 Caso a IA não encontre nenhuma combinação livre dentro da coordenação, a plataforma deve sugerir aulas assíncronas/EAD como fallback ou deixar a turma pendente para intervenção manual da coordenação?

---
Gerado por reversa-pre-spec em 2026-08-13T13:20:00-03:00
Sessão: 001-realocacao-docente-emergencial
Destino sugerido: /reversa-requirements
