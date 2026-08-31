# Adendo: Realocação Docente Emergencial

> Identificador: `014-realocacao-docente-emergencial`
> Data: `2026-08-13`
> Cenário: `legado`

## Vigência
Vigente desde 2026-08-13.

## Resumo da entrega
Permite à coordenação acadêmica gerenciar afastamentos não planejados de docentes (licenças de saúde, cursos, aposentadorias) durante o período letivo. A solução calcula alternativas emergenciais de substituição via motor de IA (`core-allocation-engine`), oferecendo ao coordenador um modo duplo de operação (Modo Assistido com seleção manual vs. Modo Delegado com homologação automática).
Total de 8 ações técnicas concluídas com 100% de cobertura de testes automatizados.

## Impacto por artefato da extração

| Artefato | Seção | Tipo de impacto | Delta |
|----------|-------|-----------------|-------|
| `_reversa_sdd/architecture.md` | `#1.1-módulos-principais` | `regra-nova` | Adiciona o método `calculate_emergency_reallocation` em `src/engine/core.py` no motor `core-allocation-engine` |
| `_reversa_sdd/architecture.md` | `#1.1-módulos-principais` | `delta-de-contrato-externo` | Adiciona os endpoints HTTP REST API `/api/v1/emergency-reallocations/calculate` e `/commit` no `academic-space-manager` (`src/api/routes.py`) |
| `_reversa_sdd/architecture.md` | `#1.1-módulos-principais` | `componente-novo` | Adiciona a aba de Realocação Emergencial e modal de escolha no `occupancy-dashboard` (`src/api/static/index.html`) |
| `_reversa_sdd/domain.md` | `#entidades-e-regras` | `delta-de-dados` | Adiciona o registro DDL das tabelas `emergency_reallocation_logs` e `emergency_reallocation_details` em `db/migrations.sql` |
| `_reversa_sdd/domain.md` | `#regras-de-negócio` | `regra-nova` | Introduz a busca de substitutos com expansão para coordenações correlatas e modo delegado autônomo sem bloqueio de aceite |

## Regras sob vigilância
- `W001`: Busca prioritária na mesma coordenação antes da busca expandida
- `W002`: Respeito estrito às restrições horárias dos docentes (`is_teacher_restricted`)
- `W003`: Suporte ao modo duplo (Assistido vs. Delegado) no painel e API
- `W004`: Gravação de log de auditoria estruturado ao efetivar realocação

Ver detalhes em `_reversa_forward/014-realocacao-docente-emergencial/regression-watch.md`.

## Fontes
- `_reversa_forward/014-realocacao-docente-emergencial/requirements.md`
- `_reversa_forward/014-realocacao-docente-emergencial/roadmap.md`
- `_reversa_forward/014-realocacao-docente-emergencial/legacy-impact.md`
- `_reversa_forward/014-realocacao-docente-emergencial/regression-watch.md`
