# Onboarding & Guia de Teste: Landing Page, Cadastro e Login com RBAC

> Identificador: `020-landing-page-login-rbac`
> Data: `2026-08-26`

Este documento apresenta o passo a passo para testar a experiência completa da Landing Page, fluxo de auto-cadastro com aprovação e login segmentado por perfil.

---

## 1. Inicialização do Servidor

Execute o servidor localmente:
```bash
python -m src.main
```
Acesse no navegador: `http://localhost:8001/`

---

## 2. Passo a Passo de Validação

### Passo 1: Experiência da Landing Page Pública
1. Acesse `http://localhost:8001/`.
2. Verifique a apresentação institucional:
   - Navbar com logo ClassSync AI e botões de **Entrar** e **Cadastre-se**.
   - Hero Section com proposta de valor da IA e visual moderno.
   - Seções de apresentação dos Agentes (ACC, AMR, Otimização Predial) e Métricas de Impacto.
   - Rodapé institucional.
3. Teste a responsividade alternando a largura da janela do navegador ou usando a visualização de dispositivos móveis.

### Passo 2: Auto-Cadastro de Novo Usuário (Pendente de Aprovação)
1. Na Landing Page, clique em **"Cadastre-se"**.
2. Preencha o formulário:
   - **Nome:** `Prof. Carlos Santos`
   - **E-mail:** `carlos.santos@universidade.edu.br`
   - **Departamento:** `Engenharia`
   - **Senha:** `senha123`
3. Submeta o formulário e verifique a mensagem informativa de que o cadastro foi realizado com sucesso e está aguardando liberação do Gestor.

### Passo 3: Tentativa de Login com Conta Pendente
1. Clique em **"Entrar"** e informe as credenciais de `carlos.santos@universidade.edu.br` com a senha `senha123`.
2. Verifique que o sistema impede o acesso exibindo o aviso amigável: *"Sua conta aguarda aprovação pelo gestor da plataforma"*.

### Passo 4: Login como Gestor e Aprovação de Usuário
1. No modal de Login, entre com a conta do administrador:
   - **E-mail:** `admin@classsync.ai`
   - **Senha:** `admin123`
2. Observe que o usuário gestor é redirecionado para o painel completo do ClassSync AI.
3. Clique na nova opção **"👥 Gestão de Usuários"** no cabeçalho/menu.
4. Localize o cadastro de `Prof. Carlos Santos` na listagem de pendentes.
5. Clique em **"Aprovar"**, selecione o perfil desejado (`Docente` ou `Coordenador`) e confirme.

### Passo 5: Login com Conta Aprovada e Validação de RBAC
1. Clique no botão de **"Sair (Logout)"** no topo direito.
2. Na Landing Page, clique em **"Entrar"** e logue com `carlos.santos@universidade.edu.br`.
3. Verifique que o login é efetuado com sucesso e o painel operacional é exibido com a visão filtrada para o papel atribuído (Docente visualiza suas turmas/salas; Coordenador visualiza seu departamento; abas restritas de configuração ficam protegidas).
