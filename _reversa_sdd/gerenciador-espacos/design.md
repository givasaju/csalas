# Unit: gerenciador-espacos, Design Técnico

> Especificação de design técnico detalhando endpoints, schemas de validação e fluxo de dados da API REST de gerenciamento.

## Interface

Esta unit é exposta através da API REST utilizando FastAPI. O acesso a todos os endpoints descritos abaixo exige cabeçalho de autorização `Authorization: Bearer <token>` (com exceção de token igual a `"invalid-token"` que resulta em `401 Unauthorized`).

### Endpoints HTTP expostos

| Método | Caminho | Entrada | Saída | Status codes |
|--------|---------|---------|-------|--------------|
| `POST` | `/api/v1/rooms` | `RoomCreate` (JSON) | Objeto Sala Criado | 201, 401, 409 |
| `POST` | `/api/v1/rooms/import-csv` | `file` (Multipart CSV Form) | Resumo de Importação | 200, 400, 401, 422 |
| `DELETE` | `/api/v1/rooms/{room_id}` | `room_id: string` (Path) | Mensagem de Exclusão | 200, 401, 404, 409 |
| `POST` | `/api/v1/allocation/restrictions` | `RestrictionCreate` (JSON) | Objeto Restrição Criado | 201, 401, 404, 409, 422 |
| `DELETE` | `/api/v1/allocation/restrictions` | Nenhuma | Resumo de Limpeza | 200, 401 |
| `GET` | `/api/v1/allocation/input-data` | Nenhuma | Dados Consolidados para a IA | 200, 401 |

---

## Fluxo Principal

### 1. Cadastro de Sala Física (`POST /rooms`)
1. Intercepta requisição e chama `check_jwt_auth` para validar token JWT no Header (`src/api/routes.py:35`).
2. Valida o payload recebido baseado no schema `RoomCreate` (capacidade > 0, campos obrigatórios) (`src/api/routes.py:30`).
3. Busca se já existe sala com o mesmo `name` no mesmo `block_id` na lista `db_rooms`. Se duplicada, retorna `409 Conflict` (`src/api/routes.py:37-40`).
4. Atribui um UUID aleatório, adiciona a sala física à lista `db_rooms` e retorna a sala criada com status `201 Created` (`src/api/routes.py:42-53`).

### 2. Importação Transacional CSV de Salas (`POST /rooms/import-csv`)
1. Valida token JWT (`src/api/routes.py:63`).
2. Lê o arquivo enviado e decodifica seu binário em UTF-8 (`src/api/routes.py:66-67`).
3. Analisa e valida se o cabeçalho é idêntico a: `bloco, sala, capacidade, tipo, acessivel, recursos` (`src/api/routes.py:77-83`).
4. **Validação total na memória**: Itera sobre cada linha, validando campos não vazios, capacidade (`int > 0`) e tipo de sala permitido (`common`, `lab`, `auditorium`) (`src/api/routes.py:85-122`).
5. Se nenhuma linha falhar, adiciona todas as salas importadas em massa a `db_rooms` através de `extend()` (`src/api/routes.py:125`).

---

## Fluxos Alternativos

*   **Validação do CSV Falha em qualquer Linha**: A rota aborta o processamento imediatamente disparando `400 Bad Request` ou `422 Unprocessable Entity`. Nenhuma alteração é gravada em `db_rooms`, mantendo a transacionalidade "Tudo ou Nada" (`src/api/routes.py:85-125`).
*   **Tentativa de exclusão de sala sob execução da IA**: Ao chamar `DELETE /rooms/{room_id}`, a rota varre `db_tasks` para verificar se existe alguma rodada de alocação de IA ativa (com status `queued` ou `running`). Se existir, bloqueia a operação imediatamente e retorna status `409 Conflict` (`src/api/routes.py:224-231`).

---

## Dependências

*   **Pydantic**: Utilizado para modelagem de schemas declarativos e validação automática de dados de entrada (`src/api/schemas.py:1-17`).
*   **FastAPI APIRouter**: Motor HTTP REST do backend (`src/api/routes.py:5-14`).
*   **worker.py**: Camada simuladora de banco de dados e controle de background threads, importando as listas de coleções na memória local (`src/api/routes.py:8-10`).

---

## Decisões de Design Identificadas

| Decisão | Evidência no código | Confiança |
|---------|---------------------|-----------|
| **Validação Transacional em Memória**: Processamento total do CSV em memória e aplicação tardia via `extend` para garantir transacionalidade nativa sem banco. | `src/api/routes.py:85-125` | 🟢 |
| **Proteção de Integridade de IA (RNF-02)**: Trava de API impedindo alterações físicas de infraestrutura acadêmica se o worker estiver computando. | `src/api/routes.py:224-231` | 🟢 |
| **JWT Mockado**: Autenticação simplificada baseada em String estática no cabeçalho sem criptografia ou chaves reais de validação. | `src/api/routes.py:16-26` | 🟢 |

---

## Estado Interno

*   **Banco em Memória Volátil**: Dados armazenados em listas locais Python de dicionários importadas de `src/api/worker.py`:
    *   `db_rooms`: Lista de salas físicas do campus.
    *   `db_restrictions`: Lista de indisponibilidades cadastradas para professores.
    *   `db_teachers`: Lista padrão de professores do campus.
    *   `db_tasks`: Fila e status de execução de tarefas assíncronas do motor.

---

## Observabilidade

*   **Logs do FastAPI**: Logs gerados por `logger.info` e `logger.warning` detalhando cada cadastramento, importação massiva, e resets semestrais executados na API.

---

## Riscos e Lacunas

*   🔴 **DESACOPLAMENTO DO BANCO DE DADOS**: Toda a API REST de gerenciamento está acoplada a variáveis locais de listas em memória volátil Python. O script de banco de dados físico PostgreSQL (`db/migrations.sql`) está 100% desconectado da aplicação backend. Qualquer reinicialização do servidor de backend esvazia e apaga todas as salas, restrições cadastrados e históricos de execução do campus.
