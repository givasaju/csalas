# Requirements: CRUD de Gestão de Instituições e Master-Chef

> Identificador: `023-crud-instituicoes-master-chef`
> Data: `2026-09-07`
> Pasta da extração reversa: `_reversa_sdd/`
> Confidência: 🟢 CONFIRMADO, 🟡 INFERIDO

## 1. Resumo executivo

Disponibiliza capacidades completas de ciclo de vida (CRUD - Criação, Leitura, Atualização e Exclusão) na interface de Administração Geral para a gestão de instituições clientes e seus respectivos gestores gerais ('master-chef'). O recurso permite ao superadministrador da plataforma ('doctor-chef') inspecionar detalhes completos de cada instituição, editar metadados cadastrais, arquivar ou remover instituições de forma segura com preservação de auditoria e reemitir ou atualizar credenciais do master-chef responsável com troca obrigatória de senha, eliminando lacunas de manutenção e suporte pós-onboarding.

## 2. Contexto a partir do legado

| Fonte | Trecho relevante | Confidência |
|-------|------------------|-------------|
| `_reversa_sdd/addenda/022-admin-geral-instituicoes.md#resumo-da-entrega` | Interface visual de Administração Geral e endpoints iniciais de listagem e provisionamento de instâncias pelo superadministrador (`doctor-chef`). | 🟢 |
| `_reversa_sdd/addenda/021-gestao-privativa-instituicoes.md#resumo-da-entrega` | Arquitetura multi-tenant com isolamento físico de dados em `./data/{slug}/`, portas TCP dedicadas e ciclo de vida de containers. | 🟢 |
| `_reversa_sdd/architecture.md#web-app-api` | Módulo de rotas FastAPI e entrega de arquivos estáticos da SPA (`src/api/static/index.html` e `index.css`). | 🟢 |
| `_reversa_sdd/architecture.md#jwt-auth-service` | Mecanismo de autenticação JWT, controle de perfis (`doctor-chef` vs papéis locais) e política de redefinição de senha (`must_change_password`). | 🟢 |
| `_reversa_sdd/domain.md#governanca-e-privacidade` | Diretrizes de privacidade e LGPD para segregação de credenciais e proteção contra acesso indevido a bases institucionais. | 🟢 |

## 3. Personas e cenários de uso

| Persona | Objetivo | Cenário-chave |
|---------|----------|---------------|
| Administrador Geral da Plataforma (`doctor-chef`) | Gerenciar o ciclo de vida operacional das instituições clientes e prestar suporte administrativo aos gestores locais | Acessa a aba de Administração Geral, inspeciona a lista detalhada de instituições clientes, altera o nome de exibição da instituição, redefine as credenciais do master-chef com nova senha provisória ou arquiva instâncias desativadas com confirmação explícita de slug. |
| Gestor Geral da Instituição (`master-chef`) | Manter acesso legítimo e contínuo à sua instituição independente de perda acidental de senha ou transição de equipe | Solicita ao suporte central a redefinição de sua credencial de acesso institucional e, ao receber a senha provisória reemitida, acessa a sua instância privativa e realiza a troca obrigatória de senha. |

## 4. Regras de negócio novas ou alteradas

1. **RN-01: Consulta e Detalhamento Completo da Instituição e Master-Chef:** 🟢
   - Origem no legado: `_reversa_sdd/addenda/022-admin-geral-instituicoes.md#resumo-da-entrega`
   - Tipo: nova
   - A interface de governança global expõe o registro detalhado de cada instituição, englobando o nome de exibição, identificador único (`slug`), porta TCP alocada, status de execução do container, data de provisionamento e o e-mail do master-chef vinculado.
2. **RN-02: Redefinição de Credenciais com Geração Automática e Override Manual:** 🟢
   - Origem no legado: `_reversa_sdd/domain.md#governanca-e-privacidade` e Sessão de Esclarecimentos de 2026-09-07
   - Tipo: nova
   - O superadministrador pode redefinir a credencial do master-chef; o sistema gera por padrão uma senha provisória segura aleatória, oferecendo campo editável caso o operador prefira digitar uma credencial específica. Ao aplicar no banco SQLite isolado do tenant, o hash é atualizado e o status `must_change_password=True` é obrigatoriamente acionado.
3. **RN-03: Atualização Segura de Metadados e Imutabilidade de Infraestrutura:** 🟢
   - Origem no legado: `_reversa_sdd/addenda/022-admin-geral-instituicoes.md#impacto-por-artefato-da-extracao` e Sessão de Esclarecimentos de 2026-09-07
   - Tipo: nova
   - A edição da instituição em produção é estritamente delimitada a dados cadastrais (nome de exibição e e-mail de contato do master-chef). O identificador (`slug`) e a porta TCP alocada permanecem fixos e imutáveis para garantir estabilidade operacional e evitar conflitos de mapeamento de rede.
4. **RN-04: Exclusão Assistida com Arquivamento (Soft Delete) e Confirmação de Slug:** 🟢
   - Origem no legado: `_reversa_sdd/addenda/021-gestao-privativa-instituicoes.md#resumo-da-entrega` e Sessão de Esclarecimentos de 2026-09-07
   - Tipo: nova
   - A operação de exclusão exige que o operador digite exatamente o `slug` da instituição para habilitar a confirmação. Ao confirmar, o sistema encerra o container Docker, libera a porta TCP para futuros cadastros e move o diretório de dados para `./data/.archived/{slug}/`, preservando os dados para fins de auditoria e conformidade legal.
5. **RN-05: Inviolabilidade de Senhas e Segregação de Privilégios:** 🟢
   - Origem no legado: `_reversa_sdd/domain.md#3-seguranca-e-autenticacao`
   - Tipo: nova
   - As senhas definitivas armazenadas nos bancos dos clientes nunca são expostas em texto puro ou retornadas por endpoints da API. Apenas a credencial provisória recém-gerada pelo procedimento de redefinição pode ser informada ao superadministrador em modal protegido de cópia.

## 5. Requisitos Funcionais

| ID | Requisito | Prioridade | Critério de aceite | Confidência |
|----|-----------|------------|--------------------|-------------|
| RF-01 | Criar endpoints REST autenticados e restritos à role `doctor-chef` para consulta detalhada (`GET /api/v1/platform/tenants/{slug}`), atualização de dados cadastrais (`PUT /api/v1/platform/tenants/{slug}`) e exclusão/arquivamento (`DELETE /api/v1/platform/tenants/{slug}`). | Must | Apenas tokens JWT assinados com a role `doctor-chef` têm autorização de acesso; outras roles recebem HTTP 403 Forbidden. Na deleção, a pasta é movida para `./data/.archived/{slug}/` e a porta TCP é desocupada. | 🟢 |
| RF-02 | Implementar endpoint seguro de redefinição do master-chef (`POST /api/v1/platform/tenants/{slug}/master-chef/reset`) que aceita senha manual opcional ou gera automaticamente, atualizando o banco SQLite da instituição e ativando `must_change_password=True`. | Must | A resposta retorna a credencial provisória atribuída e o status de sucesso. O usuário master-chef é obrigado a trocar a credencial no primeiro login seguinte. | 🟢 |
| RF-03 | Desenvolver na SPA existente (`src/api/static/`) modal visual de edição para atualização do nome da instituição e e-mail do master-chef, mantendo slug e porta como campos somente leitura desabilitados. | Must | O modal exibe os valores correntes, bloqueia alteração de porta/slug e despacha atualização cadastral com feedback imediato. | 🟢 |
| RF-04 | Implementar na SPA modal de exclusão assistida com verificação estrita de texto, exigindo a digitação exata do slug antes de disparar a requisição de arquivamento. | Must | O botão de confirmação permanece desabilitado enquanto o texto digitado for divergente do slug da instituição. | 🟢 |
| RF-05 | Desenvolver modal de redefinição de credenciais do master-chef oferecendo opção de geração de senha aleatória ou inserção manual, com exibição protegida e botão de cópia da senha final. | Must | Permite copiar a credencial com um clique e alerta o operador sobre a necessidade de envio seguro ao gestor da instituição. | 🟢 |
| RF-06 | Atualizar dinamicamente os cartões de KPIs e a tabela de instituições na interface gráfica após a conclusão de qualquer operação do CRUD sem exigir recarregamento completo da página. | Should | A listagem reflete imediatamente arquivamentos, edições e alterações de status mantendo a fluidez de navegação do usuário. | 🟢 |

## 6. Requisitos Não Funcionais

| Tipo | Requisito | Evidência ou justificativa | Confidência |
|------|-----------|----------------------------|-------------|
| Segurança | O acesso aos endpoints do CRUD de governança deve ser restrito estritamente a usuários autenticados portando a role `doctor-chef`. | Arquitetura RBAC estabelecida na entrega `022-admin-geral-instituicoes`. | 🟢 |
| Privacidade / LGPD | Nenhuma senha definitiva de clientes deve ser armazenada em texto claro ou trafegada em logs da aplicação. | Diretrizes de segurança do projeto (`_reversa_sdd/domain.md#governanca-e-privacidade`). | 🟢 |
| Usabilidade | Manter todos os elementos visuais integrados à SPA existente em Vanilla JavaScript e CSS puro, sem introduzir dependências externas de terceiros. | Princípio de preservação do bundle frontend nativo. | 🟢 |
| Desempenho | As operações de consulta e atualização de metadados devem responder em tempo inferior a 300 milissegundos. | Arquitetura assíncrona FastAPI do backend (`src/main.py`). | 🟢 |

## 7. Critérios de Aceitação

```gherkin
Cenário: Consulta e atualização bem-sucedida de dados de uma instituição cliente
  Dado que o usuário 'doctor-chef' está autenticado na plataforma
  Quando ele acessa a tela de Administração Geral e clica em 'Editar' na instituição com slug 'faculdade-inovacao'
  E altera o nome para 'Centro Universitário Inovação' e confirma
  Então o sistema atualiza o registro cadastral com código HTTP 200 OK
  E a tabela da interface exibe imediatamente o novo nome sem alterar a porta TCP original

Cenário: Redefinição de credencial do master-chef com geração automática ou manual
  Dado que o usuário 'doctor-chef' está autenticado
  Quando ele aciona a ação de 'Redefinir Credencial do Master-Chef' da instituição 'faculdade-inovacao'
  E opta por gerar senha provisória e confirma a operação
  Então o sistema atualiza a senha na base isolada da instituição com a flag 'must_change_password' igual a verdadeiro
  E exibe a nova credencial provisória para cópia
  E o master-chef é obrigado a cadastrar nova senha privativa ao fazer login na sua instância

Cenário: Exclusão e arquivamento de instituição com confirmação correta do slug
  Dado que o usuário 'doctor-chef' está autenticado
  Quando ele aciona a exclusão da instituição com slug 'faculdade-teste'
  E digita exatamente 'faculdade-teste' no campo de verificação e clica em 'Confirmar Exclusão'
  Então o sistema interrompe os containers associados e move a pasta para './data/.archived/faculdade-teste'
  E a porta TCP correspondente é desocupada no inventário da plataforma
  E a instituição deixa de constar na lista de clientes ativos

Cenário: Tentativa de exclusão com slug divergente no modal de confirmação
  Dado que o usuário 'doctor-chef' abriu o modal de exclusão da instituição 'faculdade-teste'
  Quando ele digita 'outro-nome' no campo de verificação
  Então o botão de confirmação permanece desabilitado e a requisição de deleção não é enviada

Cenário: Tentativa de acesso aos endpoints de CRUD por perfil acadêmico local
  Dado que um usuário autenticado possui o papel 'gestor' ou 'docente'
  Quando ele efetua uma requisição para 'DELETE /api/v1/platform/tenants/faculdade-inovacao'
  Então a requisição é rejeitada com código HTTP 403 Forbidden
```

## 8. Prioridade MoSCoW

| Item | MoSCoW | Justificativa |
|------|--------|---------------|
| RF-01 (Endpoints REST do CRUD) | Must | Sustentação básica no backend para todas as operações de governança. |
| RF-02 (Reset de Credencial do Master-Chef) | Must | Essencial para suporte e resolução de problemas de acesso de clientes. |
| RF-03 (Modal de Edição de Dados na SPA) | Must | Viabiliza a atualização de metadados cadastrais via interface gráfica amigável. |
| RF-04 (Modal de Exclusão Assistida com Slug) | Must | Mecanismo crítico de proteção contra perda acidental de instâncias de clientes. |
| RF-05 (Modal de Credenciais Provisórias) | Must | Garante a passagem segura da nova senha reemitida para o operador. |
| RF-06 (Atualização Dinâmica sem Reload) | Should | Melhora a fluidez e usabilidade da SPA para os administradores. |

## 9. Esclarecimentos

### Sessão 2026-09-07

- **Q:** Como o sistema deve tratar o armazenamento de dados (`./data/{slug}/`) ao excluir uma instituição cliente?  
  **R:** Soft delete / Arquivamento: o sistema interrompe e remove o container Docker, libera a porta TCP no inventário de rede e move o diretório de dados para `./data/.archived/{slug}/`, preservando os dados para auditoria ou eventual restauração (incorporado em RN-04 e RF-01).
- **Q:** Como deve ser definida a nova senha provisória do Master-Chef na ação de redefinição?  
  **R:** Geração automática com override manual: o sistema gera uma senha provisória aleatória segura por padrão, mas permite que o SuperAdmin digite uma senha manualmente se preferir, exibindo a credencial final confirmada em modal de cópia (incorporado em RN-02, RF-02 e RF-05).
- **Q:** Na edição de uma instituição cliente já ativa, quais parâmetros devem ser passíveis de alteração?  
  **R:** Apenas metadados cadastrais e contato: a edição permite alterar o nome de exibição e o e-mail do gestor; a porta TCP alocada e o slug da instituição permanecem fixos e imutáveis para evitar indisponibilidade do container e conflitos de infraestrutura (incorporado em RN-03 e RF-03).

## 10. Lacunas

> Nenhuma lacuna ou dúvida pendente. Todas as 3 dúvidas originais foram esclarecidas e incorporadas ao documento.

## 11. Histórico de alterações

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-09-07 | Versão inicial gerada por `/reversa-requirements` a partir da solicitação do usuário | reversa |
| 2026-09-07 | Esclarecimento de 3 dúvidas sobre arquivamento, política de senhas e imutabilidade de infraestrutura via `/reversa-clarify` | reversa |
