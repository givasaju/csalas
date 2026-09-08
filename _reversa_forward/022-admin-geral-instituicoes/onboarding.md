# Onboarding: Interface do Administrador Geral para Gestão e Delegação de Instituições

> Identificador: `022-admin-geral-instituicoes`
> Data: `2026-09-07`

## 1. Visão Geral

Este guia descreve o procedimento operacional e o teste manual passo a passo para validar a interface administrativa do `doctor-chef`, o provisionamento automático de novas instituições e o primeiro acesso com troca de senha do `master-chef`.

## 2. Pré-requisitos

1. Ambiente de desenvolvimento ativo com Python 3.10+ e dependências instaladas (`pip install -r requirements.txt`).
2. Docker e Docker Compose instalados no host (caso vá testar a subida de containers reais).
3. Servidor backend ativo na raiz do projeto executando `python -m src.main` (ou container `classsync-platform` ativo).

## 3. Roteiro Passo a Passo de Teste e Validação

### Passo 1: Autenticar como SuperAdmin ('doctor-chef')
1. Abra o navegador em `http://localhost:8001/` (ou porta configurada para o ambiente principal).
2. Acesse a tela de Login e insira as credenciais do `doctor-chef`:
   - **Email:** `doctor@classsync.ai`
   - **Senha:** `Doctor@2026`
3. Verifique que a barra de navegação superior exibe a nova aba **"Administração Geral"** (exclusiva para essa role).

### Passo 2: Acessar a Interface de Gestão de Instituições
1. Clique na aba **"Administração Geral"**.
2. Observe a tabela com as instituições atualmente ativas (ex.: `faculdade_alpha`, `faculdade_beta`), listando nome, porta TCP exposta, status de integridade e data de criação.
3. Clique no botão **"+ Nova Instituição"**.

### Passo 3: Preencher e Submeter o Formulário de Onboarding
1. No modal/formulário exibido, informe:
   - **Nome da Instituição:** `Faculdade Gama`
   - **Identificador (Slug):** `faculdade_gama`
   - **Porta TCP Sugerida:** `8003` (o sistema calcula e preenche automaticamente; valide que permite edição)
   - **E-mail do Master-Chef:** `diretor@gama.edu.br`
   - **Senha Provisória:** `Gama@2026`
2. Clique em **"Provisionar Instituição"**.
3. Observe a resposta imediata (`202 Accepted`) com indicador de progresso ("Criando volume, gerando segredos criptográficos e inicializando container...").
4. A tabela atualiza e exibe o novo registro `faculdade_gama` com status `Ativo` e o link `http://localhost:8003/`.

### Passo 4: Validar Primeiro Acesso e Troca Obrigatória de Senha do 'master-chef'
1. Abra uma nova aba anônima no navegador e navegue até `http://localhost:8003/`.
2. Acesse a tela de login da nova instituição e informe:
   - **Email:** `diretor@gama.edu.br`
   - **Senha:** `Gama@2026`
3. Ao submeter, observe que o sistema intercepta o login e exibe a tela:
   > **"Primeiro Acesso — Redefinição Obrigatória de Senha"**  
   > *"Por motivos de conformidade com a LGPD e segurança da sua instituição, defina sua nova senha pessoal antes de continuar."*
4. Informe a nova senha definitiva (ex.: `GamaSegura#2026`) e confirme.
5. O sistema salva o novo hash PBKDF2, remove a flag `must_change_password` e redireciona o `master-chef` para o painel de gestor da instituição.

### Passo 5: Validar Autonomia de Gestão da Instituição
1. Logado como `diretor@gama.edu.br`, navegue pelas abas acadêmicas (Salas, Docentes, Alocações).
2. Cadastre um coordenador ou docente local.
3. Confirme que todos os registros são salvos privativamente no banco em `./data/faculdade_gama/classsync.db` sem qualquer interferência com outras faculdades.

