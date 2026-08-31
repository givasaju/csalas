# Unit: gerenciador-espacos, Tarefas de Implementação

> Roteiro de tarefas sequenciais para a reconstrução/implementação da unidade da API REST e gerenciamento do campus.

## Pré-requisitos
- Servidor HTTP FastAPI e Uvicorn instalados no ambiente de desenvolvimento.
- Coleções em memória declaradas ou banco de dados estruturado para persistir o inventário.
- Logger configurado e interceptadores de autenticação JWT mockados definidos.

## Tarefas

- [ ] **T-01: Definição dos Schemas de Entrada Pydantic**
  - **Origem no legado**: [`src/api/schemas.py:4-17`](file:///c:/csalas/src/api/schemas.py#L4-L17)
  - **Critério de pronto**: Criar as classes `RoomCreate` (validando capacity > 0) e `RestrictionCreate` (dia da semana entre 1 e 7, slots específicos) usando Pydantic.
  - **Confiança**: 🟢
- [ ] **T-02: Implementação das rotas REST de Salas (Rooms)**
  - **Origem no legado**: [`src/api/routes.py:29-137`](file:///c:/csalas/src/api/routes.py#L29-L137) e [`src/api/routes.py:211-238`](file:///c:/csalas/src/api/routes.py#L211-L238)
  - **Critério de pronto**: Criar os endpoints `POST /rooms` (validação de unicidade bloco/sala), `POST /rooms/import-csv` (importação em lote transacional baseada em validação total prévia em memória) e `DELETE /rooms/{room_id}` (com trava RNF-02 baseada em tarefas ativas).
  - **Confiança**: 🟢
- [ ] **T-03: Implementação das rotas REST de Indisponibilidades e Agregação de Dados**
  - **Origem no legado**: [`src/api/routes.py:139-209`](file:///c:/csalas/src/api/routes.py#L139-L209)
  - **Critério de pronto**: Criar os endpoints `POST /allocation/restrictions` (validando professor existente, dias 1-7, slots e duplicidades), `DELETE /allocation/restrictions` (reset semestral) e `GET /allocation/input-data` (agregação consolidadora das entidades para a IA).
  - **Confiança**: 🟢

---

## Tarefas de Teste

- [ ] **TT-01: Teste de cadastramento de salas e unicidades**
  - **Origem no legado**: [`tests/test_api_rooms.py`](file:///c:/csalas/tests/test_api_rooms.py)
  - **Critério de pronto**: Validar que salas físicas válidas são adicionadas e que duplicidades no mesmo bloco retornam status 409 Conflict.
- [ ] **TT-02: Teste de importação de CSV transacional**
  - **Origem no legado**: [`tests/test_api_csv.py`](file:///c:/csalas/tests/test_api_csv.py)
  - **Critério de pronto**: Submeter arquivos CSV e validar que cargas válidas são salvas e cargas inválidas abortam e revertem totalmente o lote.
- [ ] **TT-03: Teste de indisponibilidades docentes e trava de exclusão (RNF-02)**
  - **Origem no legado**: [`tests/test_api_restrictions.py`](file:///c:/csalas/tests/test_api_restrictions.py) e [`tests/test_api_rooms.py`](file:///c:/csalas/tests/test_api_rooms.py)
  - **Critério de pronto**: Validar se indisponibilidades seguem as restrições e se a exclusão de sala é bloqueada com 409 se houver rodadas de IA ativas.

---

## Ordem Sugerida
1. **T-01** (Schemas Pydantic) por ser dependência direta das rotas.
2. **T-02** (Rotas de Salas) e **T-03** (Rotas Acadêmicas).
3. Testes integrados HTTP com Pytest (**TT-01**, **TT-02**, **TT-03**).

---

## Lacunas Pendentes (🔴)
- **Persistência de Dados Relacional**: Mapear os endpoints para gravar e consultar dados reais nas tabelas do banco de dados físico SQL PostgreSQL (de acordo com `db/migrations.sql`), eliminando as coleções simuladas em memória local.
