# Actions for feature `cadastro-docentes`

## Resumo
- Total de ações: 11
- Ações paralelizáveis: 5
- Maior cadeia de dependência: T001 → T003 → T006 → T009

### Tabela de Ações

| ID   | Descrição                                                               | Dependências          | Paralelismo | Arquivo alvo                               | Confidência | Status |
|------|--------------------------------------------------------------------------|-----------------------|-------------|--------------------------------------------|------------|--------|
| T001 | Criar enum `DepartmentEnum` em `src/models.py`                          |                       | [//]        | src/models.py                               | 🟢        | [ ] |
| T002 | Atualizar modelo `Teacher` para usar `DepartmentEnum`                     | T001                  |             | src/models.py                               | 🟢        | [ ] |
| T003 | Gerar migração SQLite para adicionar coluna `department` na tabela Teacher | T002                  |             | migrations_sqlite.sql                       | 🟢        | [ ] |
| T004 | Implementar `AuthMiddleware` e função `get_current_admin_user` em `src/api/auth.py` |                       | [//]        | src/api/auth.py                            | 🟢        | [ ] |
| T005 | Atualizar rotas de docentes (`src/api/routes.py`) para exigir dependência `Depends(get_current_admin_user)` e tratar 401/403 | T004, T002            |             | src/api/routes.py                          | 🟢        | [ ] |
| T006 | Implementar validação de `department` usando enum nas rotas de criação de docente | T005                  |             | src/api/routes.py                          | 🟢        | [ ] |
| T007 | Implementar importação CSV com pandas e transação SQLAlchemy atomica      | T003, T005            | [//]        | src/api/routes.py                          | 🟢        | [ ] |
| T008 | Atualizar UI (`src/api/static/endpoints.html`) – nova aba “Gestão de Docentes”, toast de sucesso |                       | [//]        | src/api/static/endpoints.html              | 🟢        | [ ] |
| T009 | Criar testes unitários e de integração para rotas de docentes (CRUD, CSV, auth) | T005, T007, T008      |             | tests/test_teachers.py                     | 🟢        | [ ] |
| T010 | Atualizar documentação OpenAPI (tags, schemas) para refletir novo modelo e auth | T005                  | [//]        | src/api/routes.py (docs)                   | 🟢        | [ ] |
| T011 | Executar migração, rodar testes, validar end-to-end e gerar relatório final | T009, T010            |             | (nenhum)                                   | 🟢        | [ ] |

> Digite **CONTINUAR** para prosseguir conforme a sugestão acima.
