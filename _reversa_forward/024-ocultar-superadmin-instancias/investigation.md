# Investigation: Ocultação e Proteção do Super Administrador nas Instâncias

> Identificador: `024-ocultar-superadmin-instancias`
> Data: `2026-09-08`

## 1. Contexto e Motivação

O ClassSync AI adota uma arquitetura multi-tenant com instâncias dedicadas por instituição cliente. Em cada base SQLite, o método `seed_users()` cria uma conta administrativa de inicialização (`admin@classsync.ai`) e a conta de governança global da plataforma (`doctor@classsync.ai`, role `doctor-chef`, nome "Super Administrador Geral").

Ao abrir o modal de Gestão de Usuários (`#usersModal`) em uma instituição cliente, o gestor institucional visualizava a conta `doctor@classsync.ai` na lista de usuários a aprovar/gerenciar. Isso gerava três problemas:
1. **Quebra de expectativa visual / UX:** O seletor de papéis do modal contém apenas as opções `Gestor / Admin`, `Coordenador` e `Docente`, gerando inconsistência visual com a role `doctor-chef`.
2. **Risco de integridade operacional:** O gestor local podia acidentalmente clicar em "Desativar" ou reatribuir o papel do Super Administrador Geral no SQLite da instituição.
3. **Vazamento de dados administrativos:** Exposição desnecessária do e-mail institucional e identificador do operador da plataforma em ambientes de clientes.

## 2. Alternativas Avaliadas

### Alternativa A: Filtragem exclusiva na interface SPA (JavaScript)
- **Vantagem:** Muito rápida de implementar, apenas um `.filter()` no array retornado.
- **Desvantagem:** Dados confidenciais continuam trafegando na rede em chamadas Ajax, visíveis no DevTools / Network tab, e o endpoint `PATCH` continuaria aceitando mutação direta.
- **Decisão:** Rejeitada como solução única; mantida apenas como camada de apoio.

### Alternativa B: Remoção física do seed de `doctor-chef` nas bases dos tenants
- **Vantagem:** A conta não existiria no banco do cliente.
- **Desvantagem:** Quebra a capacidade do superadministrador de autenticar diretamente na instância do cliente em cenários de suporte ou auditoria técnica direta.
- **Decisão:** Rejeitada para preservar a compatibilidade de suporte operacional.

### Alternativa C: Filtragem no backend (`GET /api/v1/users`) + Trava de mutação (`PATCH`) + Defesa na UI (Recomendada)
- **Vantagem:** Princípio de defesa em profundidade: a API não expõe dados no payload JSON, o endpoint de alteração protege a integridade do superadministrador com HTTP 403, e a UI filtra redundantemente.
- **Decisão:** Adotada integralmente.

## 3. Padrões de Segurança Aplicados

- **Princípio do Menor Privilégio (PoLP):** Usuários locais só devem enxergar dados e contas pertencentes ao seu próprio domínio acadêmico.
- **Defesa em Profundidade (Defense-in-Depth):** Validação e filtragem em camadas redundantes (ORM/Query, Handler de Rota e View Controller do Frontend).
