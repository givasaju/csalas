# Requirements: Ocultação do Super Administrador Geral na Gestão de Usuários das Instâncias

> Identificador: `024-ocultar-superadmin-instancias`
> Data: `2026-09-08`
> Pasta da extração reversa: `_reversa_sdd/`
> Confidência: 🟢 CONFIRMADO, 🟡 INFERIDO, 🔴 LACUNA / DÚVIDA

## 1. Resumo executivo

Garante o isolamento institucional e a segurança de credenciais ao impedir que os dados cadastrais da conta do Super Administrador Geral da plataforma sejam exibidos ou modificados na interface gráfica de gestão de usuários das instâncias locais de ensino. O recurso protege os privilégios da governança global contra visualização indevida, desativação acidental ou alteração não autorizada de papéis por gestores acadêmicos locais.

## 2. Contexto a partir do legado

| Fonte | Trecho relevante | Confidência |
|-------|------------------|-------------|
| `_reversa_sdd/addenda/020-landing-page-login-rbac.md#resumo-da-entrega` | Implementação do modal de gestão de usuários (`#usersModal`) e endpoints de listagem (`GET /api/v1/users`) e atualização de status (`PATCH /api/v1/users/{id}/status`). | 🟢 |
| `_reversa_sdd/addenda/022-admin-geral-instituicoes.md#resumo-da-entrega` | Criação da role global `doctor-chef` e seed do usuário `doctor@classsync.ai` com o nome 'Super Administrador Geral' no banco de dados. | 🟢 |
| `_reversa_sdd/addenda/021-gestao-privativa-instituicoes.md#resumo-da-entrega` | Arquitetura de instâncias isoladas com bancos de dados SQLite privativos por instituição cliente. | 🟢 |
| `_reversa_sdd/domain.md#3-seguranca-e-autenticacao` | Diretrizes de controle de privilégios de acesso e validação de tokens JWT baseados em papéis. | 🟢 |

## 3. Personas e cenários de uso

| Persona | Objetivo | Cenário-chave |
|---------|----------|---------------|
| Gestor da Instituição Local (`gestor` / `master-chef`) | Gerenciar e aprovar contas de usuários locais (coordenadores e docentes) da sua unidade | Abre o modal de Gestão de Usuários na sua instituição e visualiza exclusivamente as contas acadêmicas locais, sem visualização ou acesso aos dados do Super Administrador Geral da plataforma. |
| Super Administrador Geral (`doctor-chef`) | Manter controle global da plataforma SaaS sem exposição indevida nas instâncias de clientes | Acessa instâncias dedicadas de clientes sem que sua conta de infraestrutura seja listada ou desativada pelos operadores locais da instituição. |

## 4. Regras de negócio novas ou alteradas

1. **RN-01: Ocultação Obrigatória do Super Administrador Geral na Gestão Local:** 🟢
   - Origem no legado: `_reversa_sdd/addenda/020-landing-page-login-rbac.md#resumo-da-entrega` e Sessão de Esclarecimentos de 2026-09-08
   - Tipo: alterada
   - A listagem de contas de usuários apresentada no modal de gestão de usuários das instâncias institucionais e no endpoint `GET /api/v1/users` deve omitir sistematicamente a conta com papel `doctor-chef` (`doctor@classsync.ai`), garantindo que apenas usuários acadêmicos locais sejam visualizados e gerenciados.
2. **RN-02: Blindagem contra Modificação de Privilégios Globais com HTTP 403:** 🟢
   - Origem no legado: `_reversa_sdd/addenda/022-admin-geral-instituicoes.md#resumo-da-entrega` e Sessão de Esclarecimentos de 2026-09-08
   - Tipo: nova
   - O sistema rejeita categoricamente qualquer tentativa de alteração de papel (`role`) ou status de ativação (`is_active`) direcionada à conta do Super Administrador Geral no endpoint `PATCH /api/v1/users/{user_id}/status`, retornando código `HTTP 403 Forbidden` com mensagem explícita de violação de privilégio.
3. **RN-03: Filtragem em Camada de Dados e Defesa em Profundidade:** 🟢
   - Origem no legado: `_reversa_sdd/domain.md#3-seguranca-e-autenticacao`
   - Tipo: nova
   - A supressão dos dados ocorre tanto na API backend (`GET /api/v1/users`) quanto na camada frontend da SPA (`usersModal`), eliminando qualquer risco de vazamento de dados através de inspeção via ferramentas de desenvolvedor (DevTools).

## 5. Requisitos Funcionais

| ID | Requisito | Prioridade | Critério de aceite | Confidência |
|----|-----------|------------|--------------------|-------------|
| RF-01 | Filtrar os registros retornados na listagem de usuários (`GET /api/v1/users`) para omitir contas que possuam o papel `doctor-chef` quando a listagem for consultada na gestão institucional. | Must | Usuários com perfil `doctor-chef` não são retornados no array JSON de usuários retornado pela API. | 🟢 |
| RF-02 | Assegurar que a interface visual de gestão de usuários (`#usersModal`) não renderize o registro do Super Administrador Geral na tabela de contas. | Must | A tabela de usuários na interface gráfica exibe somente contas acadêmicas locais (gestores, coordenadores e docentes). | 🟢 |
| RF-03 | Bloquear qualquer requisição de alteração de status ou papel (`PATCH /api/v1/users/{user_id}/status`) cujo alvo seja a conta `doctor-chef`, retornando código HTTP 403 Forbidden. | Must | Tentativas de desativar ou alterar o papel da conta do superadministrador resultam em HTTP 403 Forbidden com mensagem de bloqueio explicativa. | 🟢 |
| RF-04 | Atualizar a suíte de testes automatizados para verificar a exclusão do Super Administrador Geral na listagem de usuários e a proteção do endpoint de status contra requisições não autorizadas. | Must | Novos testes adicionados à suíte passam com 100% de sucesso sem regressões nas suítes legadas. | 🟢 |

## 6. Requisitos Não Funcionais

| Tipo | Requisito | Evidência ou justificativa | Confidência |
|------|-----------|----------------------------|-------------|
| Segurança | Impedir vazamento de dados de contas administrativas centrais da plataforma SaaS para usuários locais das instituições clientes. | Princípio de privilégio mínimo e isolamento institucional (`_reversa_sdd/domain.md#3-seguranca-e-autenticacao`). | 🟢 |
| Usabilidade | A remoção do registro na tabela da interface gráfica não deve gerar quebra de layout, erro de renderização ou inconsistência na contagem de usuários. | Qualidade da interface do usuário em HTML e CSS puros (`_reversa_sdd/architecture.md#frontend-spa`). | 🟢 |
| Desempenho | A aplicação do filtro de registros não deve introduzir sobrecarga computacional superior a 10 milissegundos na resposta da listagem. | Padrão assíncrono de alto desempenho da API REST (`_reversa_sdd/architecture.md#web-app-api`). | 🟢 |

## 7. Critérios de Aceitação

```gherkin
Cenário: Gestor local consulta a lista de usuários no modal administrativo da instituição
  Dado que o usuário 'gestor' da faculdade está autenticado na sua instância dedicada
  Quando ele abre o modal de 'Gestão de Usuários'
  Então a tabela exibe apenas contas acadêmicas de coordenadores, docentes e gestores locais
  E nenhum registro com o nome 'Super Administrador Geral' ou papel 'doctor-chef' é apresentado

Cenário: Requisição direta à API de listagem de usuários por gestor local
  Dado que um token de acesso de perfil 'gestor' é enviado no cabeçalho Authorization
  Quando uma requisição 'GET /api/v1/users' é processada
  Então a resposta HTTP retorna código 200 OK
  E a lista JSON não contém nenhum usuário com o papel 'doctor-chef' ou e-mail 'doctor@classsync.ai'

Cenário: Tentativa de desativação da conta do Super Administrador Geral por gestor local
  Dado que um gestor acadêmico local tenta enviar 'PATCH /api/v1/users/{id-do-doctor}/status' com 'is_active: false'
  Quando a requisição é recebida pela API
  Então a operação é sumariamente rejeitada com código HTTP 403 Forbidden
  E o status da conta do Super Administrador Geral permanece ativo e inalterado
```

## 8. Prioridade MoSCoW

| Item | MoSCoW | Justificativa |
|------|--------|---------------|
| RF-01 (Filtro na API de Usuários) | Must | Garante a segurança na camada de dados, impedindo inspeção via DevTools no navegador. |
| RF-02 (Ocultação Visual na UI) | Must | Atende diretamente ao requisito solicitado pelo usuário na interface gráfica. |
| RF-03 (Bloqueio com HTTP 403 via API) | Must | Impede desativação ou corrupção do perfil do superadministrador por chamadas externas. |
| RF-04 (Cobertura com Testes Automatizados) | Must | Garante a integridade contínua da regra e ausência de regressões futuras. |
| RNF de Segurança | Must | Essencial para conformidade com segregação de privilégios de governança. |

## 9. Esclarecimentos

### Sessão 2026-09-08

- **Q:** Como a conta do 'Super Administrador Geral' deve ser tratada na API e na interface de gestão de usuários?  
  **R:** Omitir sempre da listagem de usuários de instâncias locais, tanto na API (`GET /api/v1/users`) quanto na interface visual para qualquer gestor institucional (incorporado em RN-01, RF-01 e RF-02).
- **Q:** Caso uma requisição direta tente desativar ou alterar o papel do Super Administrador Geral via API (`PATCH /api/v1/users/{id}/status`), qual deve ser a resposta?  
  **R:** Retornar `HTTP 403 Forbidden` informando expressamente que contas de governança global não podem ser alteradas ou desativadas por gestores locais (incorporado em RN-02 e RF-03).

## 10. Lacunas

> Nenhuma lacuna ou dúvida pendente. Todas as dúvidas identificadas foram esclarecidas e incorporadas ao documento.

## 11. Histórico de alterações

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-09-08 | Versão inicial gerada por `/reversa-requirements` a partir da solicitação do usuário | reversa |
| 2026-09-08 | Esclarecimento de dúvidas sobre omissão em API/UI e código HTTP 403 de bloqueio via /reversa-clarify | reversa |
