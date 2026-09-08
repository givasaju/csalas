# Risks, admin-geral-instituicoes

> Selo 🟡 PLANEJADO em todos os itens. Documento adversarial por design.

## Premortem
🟡 Manchete 1: 'Brecha de segurança: backend com acesso root ao Docker vira vetor de ataque e expõe instâncias das faculdades' (Causa raiz: Risco crítico ao conceder permissões do Docker socket diretamente ao processo web da aplicação).
🟡 Manchete 2: 'Colapso do servidor: orquestração instável gera colisão de portas, vazamento de memória e containers zumbis' (Causa raiz: Falta de robustez no ciclo de vida, alocação concorrente de portas e limpeza de containers).
🟡 Manchete 3: 'Delegação frustrada: doctor-chef cria a instituição, mas master-chef fica travado por atrito no primeiro acesso e governança local' (Causa raiz: Falhas na experiência de ativação, entrega de credenciais e autonomia institucional).

**Manchete que mais assusta o usuário:** 🟡 Manchete 1: 'Brecha de segurança: backend com acesso root ao Docker vira vetor de ataque e expõe instâncias das faculdades' (Causa raiz: Risco de segurança ao dar permissão de Docker socket para o app web).

---

## Opção A, SuperAdmin Integrado com Orquestrador Local
- **Premissa que mata:** 🟡 É seguro e operacionalmente viável conceder acesso ao socket Docker (/var/run/docker.sock) para o processo web FastAPI no mesmo container/servidor sem abrir brecha para que uma vulnerabilidade na API permita escape para o host e comprometimento de todas as instâncias.
- **Teste barato da premissa:** 🟡 Criar um script mínimo FastAPI em ambiente de laboratório (2 a 4 horas) que invoque a API do Docker sob usuário restrito e tentar executar comandos arbitrários no host a partir de payload injetado.
- **Custo escondido:** 🟡 Hardening rigoroso de infraestrutura em Dockerfile e host; necessidade de sanitizar inputs contra injeção de parâmetros nos scripts de provisionamento; manutenção de concorrência síncrona na subida de containers.
- **Ponto sem volta:** 🟡 Quando a interface web estiver em produção com código acoplado diretamente ao daemon Docker local do servidor.

## Opção B, Control Plane SaaS Independente (Microsserviço de Gestão)
- **Premissa que mata:** 🟡 O volume de novas instituições e o modelo de negócio justificam os custos de desenvolvimento, deploy e monitoramento de uma segunda aplicação autônoma completa (banco próprio, infraestrutura e API separadas).
- **Teste barato da premissa:** 🟡 Simulação de custos e esforço de manutenção em 1 dia: se a previsão de novos clientes for menor que 5 por mês, sustentar dois sistemas independentes gera desperdício financeiro e técnico.
- **Custo escondido:** 🟡 Duplicação de esteiras CI/CD, manutenção de dois repositórios ou arquitetura monorepo complexa, e necessidade de gerenciar consistência distribuída entre o Control Plane e os hosts de execução.
- **Ponto sem volta:** 🟡 Após a estruturação do banco de dados relacional próprio do Control Plane e publicação dos contratos de API de controle.

## Opção C, Painel Web Leve Acoplado a Webhook de Automação
- **Premissa que mata:** 🟡 O ambiente dispõe de um executor de automação confiável e seguro (como n8n, webhook runner ou fila redis/celery) que consiga rodar os scripts de infraestrutura sem travar silenciosamente e consiga reportar o status de volta à UI.
- **Teste barato da premissa:** 🟡 Configurar em 2 horas um webhook listener em container de teste disparando uma execução mock de deploy-institution.ps1 / .sh e retornando status 200 OK.
- **Custo escondido:** 🟡 Observabilidade assíncrona: a UI precisa lidar com estados pendentes ('Provisionando...', 'Falha no deploy', 'Pronto') e mecanismos de polling ou WebSocket para atualizar o doctor-chef.
- **Ponto sem volta:** 🟡 Quando fluxos críticos de provisionamento e credenciais forem delegados a nós de automação externos sem versionamento formal de código no Git.

---

## Opção sempre presente, não construir
- **Premissa que mata:** 🟡 O doctor-chef aceitará operar o cadastramento e passagem de bastão das novas instituições via terminal de comando de forma contínua, sem demandar interface gráfica.
- **Teste barato da premissa:** 🟡 Executar uma simulação de onboarding de duas instituições teste utilizando apenas o terminal com os parâmetros de master-chef e cronometrar o atrito humano.
- **Custo escondido:** 🟡 Dependência humana exclusiva de quem tem acesso SSH/RDP ao servidor; impossibilidade de ter uma equipe de atendimento/suporte não técnica realizando ativações.
- **Ponto sem volta:** 🟡 Nenhum: reversível a qualquer momento com impacto zero.

## Opção sempre presente, usar algo pronto
- **Premissa que mata:** 🟡 Uma ferramenta open-source de gestão de containers (Portainer / Coolify) permite automatizar os passos específicos do ClassSync (gerar SECRET_KEY aleatória, injetar .env e criar o master-chef no banco) sem exigir intervenções manuais em arquivos.
- **Teste barato da premissa:** 🟡 Subir um Portainer CE localmente em 30 minutos e testar a criação de um template Docker App parametrizável com variáveis dinâmicas.
- **Custo escondido:** 🟡 Curva de aprendizado de uma ferramenta de DevOps para o doctor-chef, interface sobrecarregada com dezenas de opções desnecessárias e risco de alterações acidentais em outros containers do host.
- **Ponto sem volta:** 🟡 Quando as rotinas operacionais da empresa ficarem amarradas aos formatos proprietários de templates da ferramenta escolhida.

---

## Riscos transversais
🟡 Dados sensíveis e LGPD: Ao definir as credenciais do master-chef na criação da instituição, o doctor-chef não deve reter senhas em texto plano nem manter acesso eterno aos dados acadêmicos privativos da faculdade contratante (exige obrigatoriedade de troca de senha no primeiro login do master-chef).
🟡 Governança de Perfis (RBAC): A introdução da role 'doctor-chef' em src/api/auth.py não pode quebrar os escopos locais dos tenants ('gestor', 'coordenador', 'docente') definidos no adendo 020 e 021, garantindo que o isolamento de dados permaneça inviolável.

## O que precisa ser respondido antes de decidir
🟡 1. A interface do doctor-chef deve ficar dentro da aplicação atual (com perfil especial) ou deve ser um painel isolado para proteger a segurança do host?
🟡 2. Como o master-chef será notificado da criação da sua instância (e-mail automático com link de ativação ou credencial provisória entregue pelo doctor-chef)?
🟡 3. A alocação de portas TCP e subdomínios no proxy reverso (Nginx) deve ser automatizada ou selecionada pelo doctor-chef?
🟡 4. O que acontece se a subida do container falhar durante o provisionamento: como a UI sinaliza o erro e como os dados parciais são limpos?

---
Gerado por reversa-challenger em 2026-09-07T16:24:34-03:00
Sessão: 005-admin-geral-instituicoes
