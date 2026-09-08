# Decision: gestao-privativa-instituicoes

> Selo 🟡 PLANEJADO. Decisão humana registrada, sujeita a revisão.

## Problema de referência
🟡 Quando o usuário logar na plataforma, eu quero que ele acesse somente as informações referentes a sua instituição, para manter a privacidade das informações e dados.

## Placar
| Opção | Job to be done | Esforço | Risco residual | Custo no legado | Total |
|---|---|---|---|---|---|
| **Opção B, Instâncias dedicadas por instituição (Deploy isolado)** | 5 | 3 | 3 | 5 | **16** |
| **Opção A, Multi-tenancy lógico com discriminador no banco e RLS** | 5 | 3 | 4 | 2 | **14** |
| **Opção Usar algo pronto (SaaS IAM B2B: Clerk/Auth0/Zitadel)** | 4 | 3 | 3 | 3 | **13** |
| **Opção Não construir (Manter plataforma mono-cliente)** | 1 | 5 | 1 | 5 | **12** |
| **Opção C, Multi-tenancy por schemas separados no PostgreSQL** | 5 | 1 | 2 | 3 | **11** |

🟡 A Opção B liderou a pontuação principalmente devido ao impacto nulo no código legado (Custo no legado = 5), eliminando o risco de quebrar os algoritmos matemáticos e heurísticas do motor de alocação de salas (`core-allocation-engine`), isolando a privacidade na camada de infraestrutura/rede.

## Recomendação do Arbiter
🟡 Opção B (Instâncias dedicadas por instituição / Deploy isolado). Garante isolamento físico total e inviolável de dados para atender à privacidade e LGPD, sem exigir refatoração invasiva no backend ou risco de vazamento acidental de dados por falha de query.

## O que se perde ao escolher ela
🟡 Perde-se a economia de escala e o custo marginal zero de infraestrutura compartilhada: cada nova instituição demanda provisionamento de containers e banco dedicado, elevando os custos de nuvem e exigindo automação robusta de CI/CD e monitoramento.

## Em que condição a recomendação muda
🟡 Se a plataforma precisar escalar para mais de 20 instituições com ticket médio baixo em modelo SaaS *self-service*, a Opção B se torna financeiramente e operacionalmente proibitiva; nessa condição, a **Opção A (Multi-tenancy Lógico com RLS no PostgreSQL)** passa a ser mandatória.

## Decisão do usuário
🟡 Opção B (Instâncias dedicadas por instituição / Deploy isolado), decidido por givas em 2026-09-07T12:39:49-03:00.

## A validar antes de comprometer
🟡 Simular os custos mensais em nuvem (AWS/GCP/DigitalOcean) para hospedar de 5 a 20 instâncias completas (API FastAPI + PostgreSQL + Dashboard) e confrontar com o modelo de precificação/mensalidade das instituições clientes (1 dia de planilha/orçamento).

## Riscos aceitos conscientemente
🟡
- Custo financeiro de infraestrutura multiplicado pelo número de clientes.
- Sobrecarga de manutenção de pipelines de deploy automatizados e orquestração de rotinas de backup isoladas para cada cliente (`_reversa_sdd/architecture.md`).
- Risco de drift de versões caso atualizações de ambiente não sejam estritamente centralizadas via CI/CD.

---
Gerado por reversa-arbiter em 2026-09-07T12:40:00-03:00
Sessão: 004-gestao-privativa-instituicoes
