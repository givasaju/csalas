# Pre-Spec, admin-geral-instituicoes

> Selo 🟡 PLANEJADO. Insumo de entrada para o próximo pipeline, não é uma spec.

## Problema
🟡 Ausência de uma interface visual administrativa e centralizada (SaaS SuperAdmin) para criação e delegação de instâncias institucionais pelo usuário 'doctor-chef', dependendo atualmente de scripts manuais no terminal do host.

## Caminho escolhido
🟡 Opção C (Painel Web Leve Acoplado a Webhook de Automação): tela administrativa restrita no frontend SPA servida com perfil 'doctor-chef', disparando o provisionamento seguro do container e seed do 'master-chef' via webhook/runner desacoplado do processo web principal.

## Escopo mínimo da primeira entrega
🟡 Formulário administrativo na SPA para o 'doctor-chef' autenticado cadastrar uma nova instituição (nome e identificador slug) e definir o login e senha provisória do respectivo 'master-chef', disparando a automação que cria o diretório de dados, sobe o container isolado na porta alocada e inicializa a conta do 'master-chef' como gestor institucional com acesso imediato à URL dedicada.

## Não-objetivos
🟡 Módulos de faturamento e billing recorrente; painéis de monitoramento avançado de consumo de CPU/memória do servidor; edição e destruição de containers existentes via UI; e integração de provedores externos de pagamento ou SSO corporativo (nesta primeira fatia).

## Restrições ativas
🟡 Preservar a stack visual existente em HTML, CSS e Vanilla JavaScript nativo em src/api/static/ sem introdução de frameworks pesados de frontend; manter a segregação física estrita com banco desacoplado em ./data/{tenant} e porta TCP exclusiva; e nenhuma alteração nos motores de alocação de salas legados.

## Critério de pronto
🟡 O usuário 'doctor-chef' autentica-se na plataforma, acessa a tela de gestão de instituições, preenche o formulário com o nome da instituição e dados do 'master-chef', confirma a criação e, após o provisionamento, o 'master-chef' realiza login com sucesso na URL da sua instância dedicada assumindo o papel de gestor geral institucional.

## Premissa a validar primeiro
🟡 O listener de webhook/automação consegue receber o payload {tenant_name, port, master_chef_email, master_chef_password} e acionar os scripts de provisionamento de forma não-bloqueante, retornando status de sucesso em ambiente de testes em menos de 2 horas.

## Riscos herdados
🟡 Necessidade de gerenciar a observabilidade assíncrona na UI para exibir o status de criação (progresso / sucesso / falha); e necessidade de impor a troca de credencial no primeiro login do 'master-chef' para mitigar riscos de privacidade sob a LGPD.

## Âncoras no legado
🟡
- _reversa_sdd/addenda/021-gestao-privativa-instituicoes.md: Arquitetura de deploy isolado multi-tenant, variáveis .env e scripts de automação (scripts/deploy-institution.ps1 e .sh).
- _reversa_sdd/addenda/020-landing-page-login-rbac.md e src/api/auth.py: Fluxo de login JWT e definição de roles (gestor, coordenador, docente), agora recepcionando a role 'doctor-chef' na hierarquia superior.
- src/api/static/index.html e index.css: Estrutura da SPA e componentes visuais do ClassSync AI.

## Dúvidas abertas
- [DÚVIDA] 🟡 A alocação da porta TCP para o novo container deve ser calculada de forma incremental automática pelo sistema ou sugerida pelo 'doctor-chef' na interface?
- [DÚVIDA] 🟡 O runner de automação do deploy deve ser empacotado como um endpoint em segundo plano na própria FastAPI (usando BackgroundTasks) ou via webhook listener independente (como container auxiliar ou n8n)?
- [DÚVIDA] 🟡 O sistema deve forçar a troca de senha no primeiro login do 'master-chef' através de um atributo booleano na tabela User ou permitir uso direto da senha cadastrada pelo 'doctor-chef'?

---
Gerado por reversa-pre-spec em 2026-09-07T16:32:12-03:00
Sessão: 005-admin-geral-instituicoes
Destino sugerido: /reversa-requirements
