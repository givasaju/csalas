# Onboarding: Verificação da Ocultação do Super Administrador Geral

> Identificador: `024-ocultar-superadmin-instancias`
> Data: `2026-09-08`

Este guia fornece o passo a passo para validar a ocultação do Super Administrador Geral na interface e na API de qualquer instância de instituição cliente.

## Pré-requisitos

1. Servidor ClassSync AI em execução (ex.: `python -m src.main` na porta 8000 e instâncias locais nas portas 8001 e 8002).
2. Credenciais de um Gestor institucional local (ex.: `admin@classsync.ai` / `admin123`).

## Roteiro de Validação Visual (Frontend SPA)

1. Abra o navegador em uma das instâncias locais de ensino:
   - Faculdade Beta: `http://localhost:8001/`
   - Universidade Pepilegal: `http://localhost:8002/`
2. Clique no botão de **Login** no canto superior direito.
3. Insira as credenciais do gestor local:
   - **E-mail:** `admin@classsync.ai`
   - **Senha:** `admin123`
4. Na barra de navegação superior, clique no botão **Gestão de Usuários**.
5. Observe a listagem de contas exibidas na tabela:
   - ✅ **Resultado Esperado:** Apenas contas acadêmicas de gestores, coordenadores e docentes da faculdade são exibidas. A conta com nome "Super Administrador Geral" (`doctor@classsync.ai`) **NÃO** aparece na listagem nem no contador de usuários.

## Roteiro de Validação via API (cURL / PowerShell)

### Teste 1: Consulta direta à API de Usuários
1. Obtenha o token de autenticação:
   ```bash
   curl -X POST http://localhost:8001/api/v1/auth/login \
     -H "Content-Type: application/json" \
     -d '{"email": "admin@classsync.ai", "password": "admin123"}'
   ```
2. Realize a chamada ao endpoint `/users`:
   ```bash
   curl -X GET http://localhost:8001/api/v1/users \
     -H "Authorization: Bearer <TOKEN_OBTIDO>"
   ```
3. ✅ **Resultado Esperado:** O array JSON retornado contém os usuários da faculdade, e nenhum elemento possui `"role": "doctor-chef"` ou `"email": "doctor@classsync.ai"`.

### Teste 2: Tentativa de desativação forçada do SuperAdmin
1. Tente enviar um `PATCH` diretamente para o ID do superadministrador (`u-doctor-001`):
   ```bash
   curl -X PATCH http://localhost:8001/api/v1/users/u-doctor-001/status \
     -H "Authorization: Bearer <TOKEN_OBTIDO>" \
     -H "Content-Type: application/json" \
     -d '{"is_active": false}'
   ```
2. ✅ **Resultado Esperado:** Código HTTP `403 Forbidden` com mensagem informativa:
   `{"detail": "Não é permitido alterar o status ou o papel de contas de administração global (doctor-chef)."}`
