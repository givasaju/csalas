# Impacto no Legado: Ocultação do Super Administrador Geral nas Instâncias

> Identificador: `024-ocultar-superadmin-instancias`
> Data: `2026-09-08`
> Política de Edição do Legado: `allowLegacyEdits: true`
> Caminhos liberados em allowedPaths: `["src/**", "data/**", "tests/**", "scripts/**", "nginx/**", "Dockerfile", "docker-compose.yml", "docker-compose-proxy.yml", ".env.example"]`

## 1. Tabela de Arquivos Afetados

| Arquivo afetado | Componente | Tipo | Severidade | Justificativa |
|---|---|---|---|---|
| `src/api/routes.py` | `academic-space-manager` | `regra-alterada` | LOW | Filtragem de contas `doctor-chef` em `GET /api/v1/users` e blindagem com HTTP 403 em `PATCH /api/v1/users/{user_id}/status`. |
| `src/api/static/index.html` | `occupancy-dashboard` | `regra-alterada` | LOW | Adição de filtro defensivo client-side no método `loadUsersList()` para omitir `doctor-chef` da tabela visual. |
| `tests/test_auth_rbac.py` | `test-suite` | `regra-nova` | LOW | Cenários de teste automatizados para validação do isolamento da listagem e proteção 403 contra mutações não autorizadas. |

## 2. Diff Conceitual por Componente

### Academic Space Manager (`src/api/routes.py`)
- O endpoint `GET /api/v1/users` agora aplica filtro explícito tanto na consulta ORM (`filter(models.User.role != "doctor-chef")`) quanto na lista retornada, garantindo que credenciais ou metadados da governança global da plataforma não sejam enviados a clientes locais.
- O endpoint `PATCH /api/v1/users/{user_id}/status` introduziu uma trava de segurança que intercepta requisições dirigidas a contas com `role == "doctor-chef"` ou `email == "doctor@classsync.ai"`, rejeitando imediatamente com `HTTP 403 Forbidden` e impedindo qualquer alteração de status ou de perfil.

### Occupancy Dashboard (`src/api/static/index.html`)
- O controlador JavaScript de visualização de usuários (`loadUsersList`) aplica filtragem no array antes de iterar e injetar os nós no DOM, assegurando integridade visual e consistência na tabela mesmo em casos extremos de inconsistência de rede.

### Test Suite (`tests/test_auth_rbac.py`)
- Inclusão dos testes `test_users_list_omits_doctor_chef` e `test_update_doctor_chef_status_forbidden`, além do reforço da fixture `setup_auth_db` para assegurar estado íntegro e limpo da conta de governança global.

## 3. Preservadas

Regras 🟢 do modelo de domínio (`_reversa_sdd/domain.md`) mantidas íntegras:
- **2.6 Otimização e Consolidação Predial**: Algoritmo `BuildingOptimizer` inalterado.
- **2.7 Importação Transacional de Salas (Tudo ou Nada)**: Validação e rollback de CSV inalterados.
- **2.8 Restrição de Cadastro de Salas Duplicadas**: Validação `409 Conflict` preservada.
- **2.9 Bloqueio de Exclusão de Salas em Execução (RNF-02)**: Trava de integridade do motor preservada.
- **2.10 Restrições de Indisponibilidade Docente**: Validação de slots e dias preservada.
- **2.11 Limite de Concorrência de Threads do Motor**: Pool de 2 threads mantido.
- **3. Segurança e Autenticação**: Validação JWT, assinatura de tokens e dependências de papéis existentes preservadas.

## 4. Modificadas

Regras 🟢 do modelo de domínio afetadas pela feature:
- **RN-01 (Ocultação de Super Administrador em GET /users)**: A listagem de contas de usuários da instância local passa a omitir sistematicamente registros com a role `doctor-chef`.
- **RN-02 (Blindagem de Privilégio Global em PATCH /users/{id}/status)**: O endpoint de mutação de usuários rejeita requisições sobre contas `doctor-chef` retornando `HTTP 403 Forbidden`.
