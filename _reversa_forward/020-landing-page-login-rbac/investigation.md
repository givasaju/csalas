# Investigation: Landing Page Institucional, Auto-Cadastro e Login com RBAC

> Identificador: `020-landing-page-login-rbac`
> Data: `2026-08-26`

## 1. Contexto e Motivação

O ClassSync AI possui um motor de alocação multiagente cooperativo e relatórios analíticos, mas carecia de uma presença pública institucional e de um mecanismo seguro de entrada para os usuários do campus universitário. Esta investigação analisa as melhores práticas para a interface da Landing Page, segurança no ciclo de autenticação e desenho da arquitetura de RBAC.

## 2. Melhores Práticas de UI/UX para Landing Page Acadêmica / SaaS

1. **Estrutura Visual de Alta Conversão**:
   - **Hero Section**: Título de alto impacto explicando a proposta de valor ("Otimização Inteligente de Salas de Aula com IA"), subtítulo conciso, botões primários ("Acessar Plataforma" / "Cadastre-se") e prévia visual do dashboard.
   - **Seção de Recursos e IA**: Cards explicativos detalhando os Agentes Coordenadores (ACC), Agente Mediador (AMR) e a Consolidação Predial para economia de energia.
   - **Métricas e Impacto**: Indicadores numéricos (ex.: "+45% de otimização de espaço", "Economia de até 30% em energia predial", "Resolução de conflitos em segundos").
   - **Rodapé Institucional**: Informações institucionais, links rápidos e identificação de direitos autorais.
2. **Design Responsivo e Estilo**:
   - Utilização de Tailwind CSS com paleta escura tecnológica (`#0B0F19`, `#1E293B`, acentos em `#3B82F6` e `#10B981`).
   - Efeitos de profundidade e *Glassmorphism* suaves para manter consistência com o restante do sistema.

## 3. Segurança de Autenticação e RBAC

1. **Armazenamento Seguro de Senhas**:
   - Hashing com algoritmo `bcrypt` via biblioteca Python padrão ou `hashlib` com salt seguro, garantindo proteção contra ataques de dicionário e rainbow tables.
2. **Tokens JWT Stateless**:
   - Tokens assinados com `HS256`, contendo payload com `sub` (e-mail), `name`, `role` e `exp`.
   - Renovação e expiração configurada para balancear segurança e usabilidade.
3. **Ciclo de Governança e Aprovação**:
   - Para evitar cadastros maliciosos ou acesso imediato a dados acadêmicos sensíveis, o auto-cadastro define `is_active: false`.
   - O Gestor/Admin dispõe de endpoint e interface para aprovação e atribuição do papel correto (`gestor`, `coordenador`, `docente`).

## 4. Padrões de Código e Integração

- **FastAPI Dependency Injection**: Utilizar `Depends(get_current_user)` e `require_roles(["gestor", "coordenador"])` para validação declarativa e limpa nas rotas da API.
- **Transição Fluida na SPA**: O frontend verifica a existência do token no `localStorage`. Se não autenticado, renderiza a Landing Page; se autenticado, exibe o painel operacional adaptando os menus ao perfil do usuário.
