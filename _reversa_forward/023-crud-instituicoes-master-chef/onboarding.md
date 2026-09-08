# Onboarding: CRUD de Gestão de Instituições e Master-Chef

> Identificador: `023-crud-instituicoes-master-chef`
> Data: `2026-09-07`

Este documento é o guia prático passo a passo para homologação e validação das funcionalidades de CRUD e gestão de master-chefs pelo SuperAdmin.

---

## 1. Pré-requisitos

1. Servidor principal do ClassSync AI em execução:
   ```bash
   uvicorn src.main:app --reload --port 8000
   ```
2. Docker ativo e funcional no ambiente para testes com containers.
3. Credencial padrão do SuperAdmin (`doctor-chef`):
   - **E-mail:** `doctor@classsync.ai`
   - **Senha:** `doctor123` (ou a credencial configurada no ambiente)

---

## 2. Roteiro de Homologação Visual (SPA)

### Passo 1: Acesso ao Painel de Administração Geral
1. Acesse `http://localhost:8000` no navegador.
2. Efetue login com as credenciais do `doctor-chef`.
3. Verifique que a aba **🌐 Administração Geral** está visível no topo da página.
4. Clique na aba: observe a tabela de instituições clientes ativas com os cards de métricas (KPIs).

### Passo 2: Teste de Edição Cadastral (Update)
1. Na linha de qualquer instituição (ex.: `faculdade_beta`), localize a coluna **Ações** e clique no botão **✏️ Editar**.
2. No modal que se abre:
   - Observe que os campos **Identificador (Slug)** e **Porta TCP** estão travados como *somente leitura* para proteger a infraestrutura.
   - Altere o campo **Nome da Instituição** para um novo valor (ex.: `Faculdade Beta Universitária`).
   - Clique em **Salvar Alterações**.
3. **Resultado Esperado:** O modal fecha com notificação de sucesso e o novo nome aparece instantaneamente na tabela sem reload de página.

### Passo 3: Teste de Redefinição de Credencial do Master-Chef (Reset)
1. Na linha da instituição, clique no botão **🔑 Master-Chef**.
2. O modal exibe o e-mail do gestor atual e as opções de credencial:
   - Clique em **Gerar Senha Automática** (uma senha segura de alta entropia será gerada no campo).
   - Ou, opcionalmente, digite uma senha provisória de sua preferência.
   - Clique no botão **Copiar Senha** e depois em **Aplicar Redefinição**.
3. **Resultado Esperado:** O sistema atualiza o hash no banco SQLite do cliente, marca `must_change_password=True` e emite alerta de confirmação.

### Passo 4: Validação do Login do Master-Chef e Troca Forçada de Senha
1. Abra uma aba anônima do navegador e conecte-se na URL da instituição (ex.: `http://localhost:8002`).
2. Tente autenticar com a nova senha provisória gerada no Passo 3.
3. **Resultado Esperado:** O login tem sucesso e o sistema abre imediatamente o modal obrigatório de redefinição de senha com a mensagem de cumprimento da LGPD, impedindo acesso às telas acadêmicas até que a nova senha privativa seja salva.

### Passo 5: Teste de Exclusão Assistida e Arquivamento (Delete)
1. De volta à aba de Administração Geral como SuperAdmin, clique no botão **🗑️ Excluir** da instituição desejada.
2. No modal de exclusão assistida:
   - Tente clicar em **Confirmar Exclusão**: o botão deve estar **desabilitado**.
   - Digite um texto incorreto (ex.: `teste`): o botão permanece desabilitado.
   - Digite exatamente o slug da instituição (ex.: `faculdade_beta`): o botão torna-se habilitado e avermelhado.
   - Clique em **Confirmar Exclusão**.
3. **Resultado Esperado:**
   - O container da instituição é encerrado e removido.
   - A pasta de dados em `./data/faculdade_beta/` é movida para `./data/.archived/`.
   - A porta TCP volta a ficar livre para novas alocações no formulário de provisionamento.
   - A linha da instituição é removida da tabela visual da SPA.

---

## 3. Roteiro de Homologação via API e Testes de Segurança (RBAC)

### Passo 6: Bloqueio de Perfil Não Autorizado
Execute uma requisição de exclusão utilizando um token de usuário comum (`role='gestor'` acadêmico):
```bash
curl -X DELETE http://localhost:8000/api/v1/platform/tenants/faculdade_beta \
  -H "Authorization: Bearer <TOKEN_GESTOR_LOCAL>"
```
**Resultado Esperado:** HTTP `403 Forbidden` com mensagem de privilégios insuficientes.

### Passo 7: Execução da Suíte Automatizada
Rode a suíte de testes de plataforma no terminal:
```bash
pytest tests/test_platform_tenants_api.py -v
```
**Resultado Esperado:** Todos os testes aprovados com 100% de sucesso.
