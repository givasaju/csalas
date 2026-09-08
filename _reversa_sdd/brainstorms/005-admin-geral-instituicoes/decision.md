# Decision, admin-geral-instituicoes

> Selo 🟡 PLANEJADO. Decisão humana registrada, sujeita a revisão.

## Problema de referência
🟡 Quando o usuário 'doctor-chef' logar na plataforma, ele quer acessar uma UI de gestão de instituições para cadastrar uma nova instituição e definir o login do usuário 'master-chef', para conseguir delegar a governança e gestão da respectiva instância institucional de forma amigável, autônoma e segura.

## Placar
| Opção | Job to be done | Esforço | Risco residual | Custo no legado | Total |
|---|---|---|---|---|---|
| Opção A: SuperAdmin Integrado no Processo Local | 5 | 3 | 2 | 3 | 13 |
| Opção B: Control Plane SaaS Independente | 5 | 1 | 4 | 5 | 15 |
| Opção C: Painel Web Leve com Webhook de Automação | 5 | 3 | 4 | 4 | 16 |
| Não construir: POP via CLI Estendida | 2 | 5 | 5 | 4 | 16 |
| Usar algo pronto: Portainer / Coolify | 3 | 4 | 3 | 5 | 15 |

🟡 Nota sobre o empate numérico (16 pontos) entre a Opção C e 'Não construir': a opção 'Não construir' atinge pontuação alta apenas pelo esforço zero, mas falha no critério essencial de aderência ao Job to be Done (nota 2), pois não atende ao requisito indispensável de interface gráfica amigável para o 'doctor-chef'. A Opção C entrega nota máxima no JTBD e nota alta em risco residual por neutralizar a maior vulnerabilidade apontada no premortem (não expõe o socket root do Docker ao backend web).

## Recomendação do Arbiter
🟡 Opção C (Painel Web Leve Acoplado a Webhook de Automação): entrega a experiência visual amigável demandada pelo 'doctor-chef' e a delegação de credenciais ao 'master-chef', desacoplando o processo web dos privilégios de execução de containers no host através de um orquestrador/runner assíncrono seguro.

## O que se perde ao escolher ela
🟡 Perde-se a simplicidade arquitetural de um monólito síncrono único: a UI precisa lidar com ciclo de vida assíncrono (estados 'Provisionando...', 'Ativa', 'Falha') e a infraestrutura requer a presença de um listener/runner de automação (como n8n, webhook runner ou daemon local) para executar os scripts de deploy.

## Em que condição a recomendação muda
🟡 Se a plataforma optar por terceirizar integralmente a gestão de containers para um painel DevOps já pronto e a equipe aceitar treinar o 'doctor-chef' nessa interface de terceiros, a opção 'Usar algo pronto' (Portainer/Coolify) passa à frente por reduzir esforço de desenvolvimento front-end.

## Decisão do usuário
🟡 Opção C (Painel Web Leve Acoplado a Webhook de Automação) , decidido por givas em 2026-09-07T16:27:41-03:00

## Divergência registrada
🟡 [Ausente: a decisão humana coincidiu integralmente com a recomendação técnica do Arbiter.]

## A validar antes de comprometer
🟡 Configurar um protótipo de webhook listener em ambiente de testes (em ~2 horas) que receba um payload mock contendo tenant_name, port, master_chef_email, master_chef_password, execute uma simulação dos scripts de provisionamento existentes em scripts/ e retorne status 200 OK com os metadados da instância criada.

## Riscos aceitos conscientemente
🟡 Necessidade de implementar observabilidade assíncrona na interface do 'doctor-chef' para exibição do progresso da criação da instituição; e necessidade de obrigar a redefinição de senha no primeiro login do 'master-chef' para resguardar a privacidade e conformidade com a LGPD.

---
Gerado por reversa-arbiter em 2026-09-07T16:27:41-03:00
Sessão: 005-admin-geral-instituicoes
