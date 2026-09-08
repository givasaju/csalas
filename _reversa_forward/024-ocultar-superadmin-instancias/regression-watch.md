# Regression Watch: Ocultação e Blindagem do Super Administrador Geral

> Identificador: `024-ocultar-superadmin-instancias`
> Data: `2026-09-08`
> Feature: Ocultação do Super Administrador Geral na Gestão de Usuários das Instâncias

## 1. Itens de Vigilância Ativa

| ID | Origem (arquivo, seção) | Regra esperada após mudança | Tipo de verificação | Sinal de violação |
|---|---|---|---|---|
| W001 | `src/api/routes.py` (`GET /api/v1/users`) | O endpoint `GET /api/v1/users` omite contas com a role `doctor-chef` ou e-mail `doctor@classsync.ai` da lista JSON retornada a gestores locais. | presença | Usuário com papel `doctor-chef` ou e-mail `doctor@classsync.ai` presente no payload retornado por `GET /api/v1/users`. |
| W002 | `src/api/routes.py` (`PATCH /api/v1/users/{user_id}/status`) | O endpoint `PATCH /api/v1/users/{user_id}/status` responde com `HTTP 403 Forbidden` contra tentativas de alterar `is_active` ou `role` de contas `doctor-chef`. | presença | Resposta HTTP 200 ou alteração de atributos da conta do Super Administrador Geral no banco de dados. |

## 2. Histórico de re-extrações

*Nenhuma re-extração executada até o momento. Esta seção será preenchida por futuras execuções do `/reversa`.*

## 3. Arquivadas

*Nenhum item arquivado.*
