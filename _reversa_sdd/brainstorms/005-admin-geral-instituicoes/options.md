# Options, admin-geral-instituicoes

> Selo 🟡 PLANEJADO em todos os itens. Nenhuma opção foi escolhida ainda.

## Problema de referência
🟡 Quando o usuário 'doctor-chef' logar na plataforma, ele quer acessar uma UI de gestão de instituições para cadastrar uma nova instituição e definir o login do usuário 'master-chef', para conseguir delegar a governança e gestão da respectiva instância institucional de forma amigável, autônoma e segura.

## Restrições ativas
🟡 Preservação integral do modelo de isolamento físico multi-tenant (cada instituição em seu container/banco independente); nenhum impacto ou alteração no motor de alocação de salas legado.

---

## Opção A, SuperAdmin Integrado com Orquestrador Local
- **Em uma frase:** 🟡 Construção de uma rota restrita /admin/super servida pela própria aplicação com papel 'doctor-chef' e interface SPA interna, acionando o provisionamento diretamente via chamadas de subprocesso/Docker no servidor.
- **Como resolve o problema:** 🟡 Oferece uma UI única no frontend existente para o 'doctor-chef' preencher o nome da instituição e dados do 'master-chef', disparando a criação do container e inserção das credenciais na base do novo tenant.
- **Esforço:** 🟡 Médio: requer criação de novas telas no frontend estático, endpoints protegidos no FastAPI e execução segura de comandos de sistema/Docker em background.
- **Impacto no legado:** 🟡 Adiciona rotas de controle e nova role no modelo de autenticação (src/api/auth.py), exigindo permissões de execução no host pelo processo da aplicação.
- **Reversibilidade:** 🟡 Fácil: as rotas administrativas podem ser isoladas ou removidas sem afetar o comportamento das instâncias individuais.
- **O que precisa ser verdade para funcionar:** 🟡 O processo da aplicação precisa ter privilégios e acesso confiável ao daemon Docker do servidor para instanciar novos containers dinamicamente.

## Opção B, Control Plane SaaS Independente (Microsserviço de Gestão)
- **Em uma frase:** 🟡 Criação de um serviço dedicado e desacoplado (Control Plane) com banco global de instituições e UI própria, responsável unicamente pela orquestração do ciclo de vida dos tenants e criação do 'master-chef'.
- **Como resolve o problema:** 🟡 Separa completamente o plano de controle (gestão global do 'doctor-chef') do plano de dados (instâncias acadêmicas dos clientes), entregando um portal exclusivo de administração SaaS.
- **Esforço:** 🟡 Alto: envolve a arquitetura de uma aplicação secundária autônoma, banco de dados global de controle, API de orquestração e gerenciamento de ciclo de vida de instâncias.
- **Impacto no legado:** 🟡 Nenhum: as instâncias clientes do ClassSync AI permanecem 100% inalteradas, recebendo apenas os parâmetros de inicialização gerados pelo Control Plane.
- **Reversibilidade:** 🟡 Cara: o investimento de desenvolvimento e manutenção de um serviço secundário independente é substancial.
- **O que precisa ser verdade para funcionar:** 🟡 O volume de clientes e a complexidade de governança da plataforma justificarem a sustentação de um serviço secundário de infraestrutura.

## Opção C, Painel Web Leve Acoplado a Webhook de Automação
- **Em uma frase:** 🟡 Disponibilização de um formulário administrativo autenticado que despacha uma carga útil (payload JSON) para um orquestrador de automação (como n8n, webhook runner ou script daemon) encarregado do deploy e envio de convite.
- **Como resolve o problema:** 🟡 O 'doctor-chef' interage com uma interface visual amigável, enquanto a complexidade de execução de comandos pesados de infraestrutura e disparo de e-mails fica delegada para um fluxo assíncrono.
- **Esforço:** 🟡 Médio: desenvolvimento da tela e da rota de envio no FastAPI, aliado à configuração do fluxo de automação receptor.
- **Impacto no legado:** 🟡 Baixo: acrescenta apenas um endpoint de despacho na API, sem acoplar chamadas de terminal diretamente no ciclo de vida síncrono do servidor web.
- **Reversibilidade:** 🟡 Fácil: caso o orquestrador seja trocado, apenas o destino do webhook precisa ser reconfigurado.
- **O que precisa ser verdade para funcionar:** 🟡 Disponibilidade de uma ferramenta ou serviço intermediário de automação (n8n ou daemon de filas) para processar o webhook com segurança.

---

## Opção sempre presente, não construir
- **Em uma frase:** 🟡 Manter o provisionamento através dos scripts CLI existentes (scripts/deploy-institution.ps1 e .sh), adicionando parâmetros para criação automática do usuário 'master-chef' e documentando um Procedimento Operacional Padrão (POP).
- **Como resolve o problema:** 🟡 Atende à necessidade de cadastrar a instituição e o respectivo 'master-chef' na inicialização do banco, mas de forma procedimental via terminal de comando, sem interface gráfica.
- **Esforço:** 🟡 Baixo: extensão pontual dos scripts existentes para aceitar --master-chef-email e --master-chef-password no momento do seed inicial.
- **Impacto no legado:** 🟡 Baixo: alteração restrita aos scripts de automação em scripts/, mantendo a aplicação inalterada.
- **Reversibilidade:** 🟡 Fácil: reversível a qualquer momento com zero dependências residuais.
- **O que precisa ser verdade para funcionar:** 🟡 O operador 'doctor-chef' ter conforto operacional com execução de comandos no terminal e a cadência de novas instituições ser compatível com processos manuais.

## Opção sempre presente, usar algo pronto
- **Em uma frase:** 🟡 Adotar uma plataforma de gerenciamento de containers e deploys open-source com RBAC (como Portainer, Coolify ou Dokku) para que o 'doctor-chef' utilize templates visuais de provisionamento.
- **Como resolve o problema:** 🟡 Oferece uma interface web pronta de administração de containers, onde o 'doctor-chef' preenche as variáveis de ambiente (TENANT_NAME, PORT, credenciais do 'master-chef') em um template pré-configurado com um clique.
- **Esforço:** 🟡 Baixo/Médio: instalação e configuração da ferramenta de terceiros no host, sem desenvolvimento de código proprietário de UI.
- **Impacto no legado:** 🟡 Nenhum: utiliza as imagens Docker e arquivos Compose já existentes na raiz do projeto.
- **Reversibilidade:** 🟡 Fácil: as instâncias continuam sendo containers Docker convencionais executados no host.
- **O que precisa ser verdade para funcionar:** 🟡 A plataforma de terceiros atender aos requisitos de usabilidade do 'doctor-chef' e a equipe concordar em manter uma dependência de ferramenta externa no ambiente de produção.

---
Gerado por reversa-explorer em 2026-09-07T16:22:00-03:00
Sessão: 005-admin-geral-instituicoes
Nenhuma recomendação emitida por design. Convergência é papel de /reversa-arbiter.
