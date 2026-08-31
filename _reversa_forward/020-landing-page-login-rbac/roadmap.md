# Roadmap: Landing Page de Apresentação Institucional, Auto-Cadastro e Login com RBAC

> Identificador: `020-landing-page-login-rbac`
> Data: `2026-08-26`
> Requirements: `_reversa_forward/020-landing-page-login-rbac/requirements.md`
> Confidência: 🟢 CONFIRMADO, 🟡 INFERIDO, 🔴 LACUNA

## 1. Resumo da abordagem

A implementação introduz a camada pública de apresentação institucional e a infraestrutura completa de autenticação com controle de acesso baseado em papéis (RBAC):
1. **Landing Page Institucional na Rota Raiz**: Criar na interface web (`src/api/static/index.html`) uma landing page moderna, elegante e responsiva com Tailwind CSS e Glassmorphism, contendo Hero Section com proposta de valor, apresentação dos recursos da IA de alocação de salas, estatísticas prediais, depoimentos e chamadas para ação (CTA).
2. **Componentes Modais de Autenticação**: Implementar modais de Login e Auto-Cadastro (Sign-up) integrados com validação de campos em tempo real e tratamento de erros.
3. **Persistência de Usuários (`User`)**: Adicionar a entidade `User` no SQLAlchemy (`src/models.py`) armazenando hash seguro de senha (`bcrypt`), perfil (`gestor`, `coordenador`, `docente`), departamento e status de ativação (`is_active`).
4. **API de Autenticação e RBAC no Backend**: Implementar em `src/api/auth.py` e `src/api/routes.py` os endpoints `POST /api/v1/auth/register`, `POST /api/v1/auth/login`, `GET /api/v1/auth/me`, `GET /api/v1/users` e `PATCH /api/v1/users/{user_id}/status`, protegidos por verificação de token JWT e autorização estrita por perfil.
5. **Governança e Interface de Gestão de Usuários**: Incluir no painel do Gestor/Admin um modal/seção de gerenciamento para visualizar cadastros pendentes, aprovar contas e atualizar permissões com 1 clique.
6. **Controle de Acesso no Frontend SPA**: Exibir ou ocultar abas e ações com base nas claims do token JWT decodificado, com botão de Logout e exibição do usuário logado no topo.

## 2. Princípios aplicados

| Princípio | Como a feature se relaciona | Status |
|-----------|------------------------------|--------|
| Design Moderno e Responsivo | Adota Tailwind CSS, Glassmorphism, gradientes modernos e componentes adaptáveis a qualquer tela. | respeita |
| Segurança em Profundidade | Validação estrita de RBAC em cada rota FastAPI backend e hashing seguro de senhas com bcrypt. | respeita |
| Não-Destrutivo ao Legado | Preserva o motor de IA e as rotas operacionais existentes, apenas adicionando controle de acesso e portal de entrada. | respeita |

## 3. Decisões técnicas

| ID | Decisão | Justificativa | Alternativas descartadas | Confidência |
|----|---------|----------------|--------------------------|-------------|
| D-01 | Servir Landing Page na rota pública `/` com transição suave para o Dashboard operacional | Garante apresentação pública moderna sem quebrar a estrutura de SPA servida pelo FastAPI | Criar duas aplicações web separadas em portas distintas | 🟢 |
| D-02 | Hashing de senhas com `bcrypt` e JWT assinado com chave secreta | Padrão da indústria para segurança de senhas e autenticação stateless | Armazenamento de senha em texto plano ou tokens opacos com sessão em banco | 🟢 |
| D-03 | Auto-cadastro em estado `pendente` com aprovação pelo Gestor | Atende ao requisito de governança institucional evitando acessos indevidos | Auto-ativação imediata sem supervisão | 🟢 |
| D-04 | Dependência FastAPI `require_roles([...])` para proteção de endpoints | Impede que usuários não autorizados chamem rotas sensíveis via API/curl | Autorização apenas na interface gráfica | 🟢 |

## 4. Premissas

Nenhuma premissa adotada a partir de dúvidas abertas. O documento de requisitos possui 0 dúvidas pendentes após a sessão de esclarecimentos `/reversa-clarify`.

## 5. Delta arquitetural

| Componente | Arquivo de origem no legado | Tipo de mudança | Resumo |
|------------|------------------------------|-----------------|--------|
| `web-app-api` | `_reversa_sdd/architecture.md#web-app-api` | componente-alterado | Inclusão de rotas de autenticação e gestão de usuários em `src/api/routes.py` e `src/api/auth.py`. |
| `frontend-spa` | `_reversa_sdd/inventory.md#src/api/static/index.html` | componente-alterado | Adição da Landing Page pública, modais de login/cadastro e painel de gestão de usuários. |
| `database-schema` | `_reversa_sdd/architecture.md#database` | componente-alterado | Adição da tabela `users` no modelo SQLAlchemy (`src/models.py`). |

## 6. Delta no modelo de dados

- Resumo das mudanças: Adição da tabela `User` para controle de autenticação, perfil e status de aprovação.
- Detalhe completo em: `_reversa_forward/020-landing-page-login-rbac/data-delta.md`

## 7. Delta de contratos externos

| Contrato | Tipo | Arquivo de detalhe |
|----------|------|--------------------|
| `auth-api` | HTTP (REST) | `_reversa_forward/020-landing-page-login-rbac/interfaces/auth-api.md` |

## 8. Plano de migração

1. Criar a tabela `User` no banco SQLite via `Base.metadata.create_all(bind=engine)`.
2. Provisionar automaticamente um usuário administrador padrão (`admin@classsync.ai` / role `gestor` / `is_active: True`) na inicialização do sistema se a tabela de usuários estiver vazia.

## 9. Riscos e mitigações

| Risco | Impacto | Probabilidade | Mitigação |
|-------|---------|---------------|-----------|
| Bloqueio acidental de rotas operacionais para testes | médio | baixa | Manter compatibilidade com header de autorização e usuário mock nos testes automatizados. |
| Responsividade quebrar em resoluções mobile intermediárias | baixo | média | Utilizar classes responsivas do Tailwind (`md:`, `lg:`, `max-w-7xl`) e testar em múltiplos viewports. |

## 10. Critério de pronto

- [ ] Todas as ações do `actions.md` marcadas `[X]`
- [ ] Landing page institucional acessível na rota raiz `/` com Hero, recursos de IA, depoimentos e rodapé
- [ ] Modal de login e cadastro funcionando com validação e feedback
- [ ] Usuário gestor capaz de aprovar cadastros pendentes e alterar perfis
- [ ] Proteção de rotas backend validada por suíte de testes `pytest`

## 11. Histórico de alterações

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-08-26 | Versão inicial gerada por `/reversa-plan` | reversa |
