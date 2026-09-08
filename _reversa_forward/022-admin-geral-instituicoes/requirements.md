# Requirements: Interface do Administrador Geral para Gestão e Delegação de Instituições

> Identificador: `022-admin-geral-instituicoes`
> Data: `2026-09-07`
> Pasta da extração reversa: `_reversa_sdd/`
> Confidência: 🟢 CONFIRMADO, 🟡 INFERIDO

## 1. Resumo executivo

Disponibiliza uma interface administrativa unificada e amigável para o superadministrador da plataforma ('doctor-chef'), permitindo o provisionamento autônomo de novas instituições de ensino e a definição direta das credenciais do seu gestor geral ('master-chef'). Essa entrega elimina a dependência operacional de intervenções manuais via terminal no servidor, garantindo a transferência segura e privativa da governança local para a instituição contratante.

## 2. Contexto a partir do legado

| Fonte | Trecho relevante | Confidência |
|-------|------------------|-------------|
| `_reversa_sdd/addenda/021-gestao-privativa-instituicoes.md#resumo-da-entrega` | Arquitetura multi-tenant isolada (containers independentes, volume desacoplado em `./data/{tenant}` e scripts de deploy). | 🟢 |
| `_reversa_sdd/addenda/020-landing-page-login-rbac.md#regras-de-negocio` | Sistema de autenticação JWT com senhas criptografadas (PBKDF2) e controle de perfis de usuário (`gestor`, `coordenador`, `docente`). | 🟢 |
| `_reversa_sdd/architecture.md#web-app-api` | Rotas FastAPI e entrega de arquivos estáticos da SPA (`src/api/static/index.html` e `index.css`). | 🟢 |
| `_reversa_sdd/brainstorms/005-admin-geral-instituicoes/decision.md` | Decisão consensual pela Opção C: painel web na SPA acoplado a runner de automação desacoplado para execução segura de deploys. | 🟢 |
| `_reversa_sdd/brainstorms/005-admin-geral-instituicoes/pre-spec.md` | Definição do escopo mínimo da entrega, não-objetivos explícitos e critérios de aceite observáveis. | 🟢 |

## 3. Personas e cenários de uso

| Persona | Objetivo | Cenário-chave |
|---------|----------|---------------|
| Administrador Geral da Plataforma (`doctor-chef`) | Provisionar novas instituições e atribuir o responsável geral da instituição sem usar terminal | Acessa a aba/visão 'Gestão Global', preenche o formulário com dados da instituição e credenciais do 'master-chef', aciona a criação e acompanha a liberação da URL dedicada. |
| Gestor Geral da Instituição (`master-chef`) | Assumir a governança administrativa exclusiva da sua instituição e definir sua equipe local | Conecta-se à URL dedicada da sua faculdade usando as credenciais definidas no onboarding, ajusta sua senha privativa e cadastra gestores e coordenadores da unidade. |
| Gestor Acadêmico / Coordenador Local | Operar salas, turmas e alocações dentro do campus institucional | Acessa o sistema sob convite/cadastro do 'master-chef' para gerenciar os dados acadêmicos privativos da sua organização. |

## 4. Regras de negócio novas ou alteradas

1. **RN-01: Perfil Hierárquico SuperAdmin ('doctor-chef'):** 🟢
   - Origem no legado: `_reversa_sdd/addenda/020-landing-page-login-rbac.md`
   - Tipo: nova
   - O sistema introduz a role global `doctor-chef`, que possui acesso exclusivo aos endpoints e telas de governança e criação de instituições na plataforma SaaS, sem acesso a dados pedagógicos privativos das instâncias clientes.
2. **RN-02: Delegação Obrigatória de 'master-chef' no Onboarding:** 🟢
   - Origem no legado: `_reversa_sdd/brainstorms/005-admin-geral-instituicoes/pre-spec.md`
   - Tipo: nova
   - Toda criação de instituição requer a indicação de um e-mail válido e senha provisória para o usuário 'master-chef'. Esse usuário nasce na base de dados da nova instituição com perfil de gestor geral institucional (`role='gestor'` com status ativo e `must_change_password=True`).
3. **RN-03: Desacoplamento Seguro da Execução de Deploy via BackgroundTasks:** 🟢
   - Origem no legado: `_reversa_sdd/brainstorms/005-admin-geral-instituicoes/decision.md`
   - Tipo: nova
   - O provisionamento da instância é orquestrado de forma assíncrona utilizando `BackgroundTasks` da API FastAPI, respondendo imediatamente com `202 Accepted`. O processo gera o arquivo `.env`, o volume `./data/{tenant}` e inicializa o container sem bloquear o event loop e sem expor o socket do Docker diretamente.
4. **RN-04: Segregação Física e URL de Acesso Dedicada:** 🟢
   - Origem no legado: `_reversa_sdd/addenda/021-gestao-privativa-instituicoes.md`
   - Tipo: confirmada
   - Cada nova instituição opera em container, volume e porta TCP próprios, sendo acessível via subdomínio exclusivo ou porta dedicada sem contaminação entre clientes.
5. **RN-05: Redefinição Obrigatória de Senha no 1º Acesso (LGPD):** 🟢
   - Origem no legado: `_reversa_sdd/brainstorms/005-admin-geral-instituicoes/risks.md`
   - Tipo: nova
   - No primeiro login do 'master-chef' utilizando a credencial provisória criada pelo 'doctor-chef', o sistema força a criação de uma nova senha pessoal definitiva, invalidando a senha inicial e assegurando a inviolabilidade dos dados locais.
6. **RN-06: Alocação Incremental de Porta com Override Manual:** 🟢
   - Origem no legado: Sessão de esclarecimentos de 2026-09-07
   - Tipo: nova
   - O sistema identifica automaticamente a próxima porta TCP livre a partir de 8001 inspecionando os tenants ativos e a sugere no formulário, permitindo que o 'doctor-chef' informe outra porta caso necessário.

## 5. Requisitos Funcionais

| ID | Requisito | Prioridade | Critério de aceite | Confidência |
|----|-----------|------------|--------------------|-------------|
| RF-01 | Criar endpoint autenticado e restrito para listagem e criação de instituições na API (`POST /api/v1/platform/tenants` e `GET /api/v1/platform/tenants`) exclusivo para usuários com perfil `doctor-chef`. | Must | Apenas tokens JWT assinados contendo a role `doctor-chef` têm permissão de acesso; outras roles recebem 403 Forbidden. | 🟢 |
| RF-02 | Desenvolver interface visual (seção/aba 'Administração Geral') na SPA existente (`src/api/static/`) visível exclusivamente para o perfil `doctor-chef`. | Must | Ao autenticar como 'doctor-chef', a SPA exibe o painel de instituições com tabela de tenants ativos e botão 'Nova Instituição'. | 🟢 |
| RF-03 | Implementar formulário de provisionamento com campo de porta automática incremental (com opção de edição manual), validação de slug e dados do 'master-chef'. | Must | O formulário sugere a próxima porta livre a partir de 8001 e valida duplicidade de slug e de porta antes do envio. | 🟢 |
| RF-04 | Integrar o backend com o executor assíncrono via `BackgroundTasks`, retornando `202 Accepted` e orquestrando a criação de volume, segredos e subida do container. | Must | A requisição responde em menos de 300ms, enquanto o container sobe em segundo plano com a base e o 'master-chef' criados. | 🟢 |
| RF-05 | Exibir na UI do 'doctor-chef' o status em tempo real do provisionamento e o link de acesso direto à nova instância dedicada. | Must | A UI exibe a URL gerada (ex: `http://localhost:PORT` ou subdomínio configurado) e o status do container. | 🟢 |
| RF-06 | Permitir que o 'master-chef' autentique na nova instância com a credencial provisória e seja direcionado para a tela de redefinição obrigatória de senha. | Must | Após a troca de senha, o 'master-chef' recebe acesso irrestrito de gestor geral para cadastrar coordenadores e docentes. | 🟢 |

## 6. Requisitos Não Funcionais

| Tipo | Requisito | Evidência ou justificativa | Confidência |
|------|-----------|----------------------------|-------------|
| Segurança | O backend web não deve acessar diretamente o socket root do Docker (`/var/run/docker.sock`), operando via runner isolado para mitigar brechas de container breakout. | Premortem da sessão de ideação 005 (`risks.md`). | 🟢 |
| Usabilidade | Manter a interface integrada à SPA existente em Vanilla JavaScript e CSS nativo, sem frameworks pesados ou dependências externas que alterem o bundle estático. | Restrição declarada pelo usuário no pre-spec. | 🟢 |
| Privacidade / LGPD | Assegurar que o 'doctor-chef' não retenha acesso aos dados acadêmicos e pedagógicos cadastrados pelos usuários locais após a entrega da instituição. | Princípio de segregação de dados do adendo 021. | 🟢 |
| Desempenho | O acionamento da criação na interface não deve bloquear o event loop da aplicação FastAPI, respondendo em menos de 500ms. | Arquitetura assíncrona FastAPI (`src/main.py`). | 🟢 |

## 7. Critérios de Aceitação

```gherkin
Cenário: Provisionamento bem-sucedido de nova instituição pelo doctor-chef
  Dado que o usuário 'doctor-chef' está autenticado na plataforma
  Quando ele preenche o formulário com a instituição 'Faculdade Inovação' (slug 'faculdade_inovacao') e o master-chef 'diretor@inovacao.edu.br'
  E confirma a criação
  Então o sistema retorna status de aceitação com a porta alocada
  E a nova instância sobe em container independente com banco isolado
  E o usuário 'diretor@inovacao.edu.br' consegue efetuar login na URL dedicada da 'Faculdade Inovação'

Cenário: Tentativa de acesso à área de gestão de instituições por usuário sem permissão
  Dado que um usuário com perfil 'gestor' ou 'docente' está autenticado
  Quando ele tenta acessar o endpoint 'POST /api/v1/platform/tenants'
  Então a requisição deve ser rejeitada com código HTTP 403 Forbidden
```

## 8. Prioridade MoSCoW

| Item | MoSCoW | Justificativa |
|------|--------|---------------|
| RF-01 (API de Tenants para doctor-chef) | Must | Base obrigatória de autorização e controle de instituições. |
| RF-02 (UI de Gestão na SPA) | Must | Entrega a interface gráfica amigável exigida pelo usuário. |
| RF-03 (Formulário de Cadastro com Master-Chef) | Must | Garante a captura dos dados essenciais para o provisionamento. |
| RF-04 (Automação Desacoplada de Deploy) | Must | Elimina tarefas manuais no terminal mantendo o isolamento físico. |
| RF-05 (Exibição de URL da Instância) | Should | Facilita a passagem de bastão operacional para o master-chef. |
| RF-06 (Login do Master-Chef na Instância) | Must | Comprova o fechamento do ciclo de onboarding. |

## 9. Esclarecimentos

### Sessão 2026-09-07

- **Q:** Como o sistema deve definir a porta TCP para a nova instância da instituição?  
  **R:** Automática incremental com override: o sistema detecta e sugere a próxima porta TCP livre a partir de 8001, permitindo edição caso o 'doctor-chef' deseje (incorporado em RN-06 e RF-03).
- **Q:** Como deve ser implementado o executor assíncrono de provisionamento da instância?  
  **R:** FastAPI `BackgroundTasks`: a requisição retorna `202 Accepted` imediatamente e uma tarefa assíncrona interna executa a rotina de provisionamento sem travar a aplicação (incorporado em RN-03 e RF-04).
- **Q:** Qual deve ser a política de segurança para a senha inicial do 'master-chef'?  
  **R:** Redefinição obrigatória no 1º login: o 'master-chef' acessa com a credencial inicial e o sistema exige a criação de uma nova senha pessoal privativa em conformidade com a LGPD (incorporado em RN-02, RN-05 e RF-06).

## 10. Lacunas

> Nenhuma lacuna ou dúvida pendente. Todas as 3 dúvidas originais foram esclarecidas e incorporadas ao documento.

## 11. Histórico de alterações

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-09-07 | Versão inicial gerada por `/reversa-requirements` a partir do pre-spec 005 | reversa |
| 2026-09-07 | Esclarecimento de 3 dúvidas de arquitetura, portas e segurança via `/reversa-clarify` | reversa |
