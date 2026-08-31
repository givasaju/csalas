# Impacto no Legado: Cadastro e Importação CSV de Docentes

> Identificador: `005-cadastro-docentes`  
> Data: `2026-08-07`  

---

## Mapeamento de Impacto por Arquivo

| Arquivo afetado | Componente | Tipo | Severidade | Justificativa |
|-----------------|------------|------|------------|---------------|
| `src/api/schemas.py` | API Schemas | `regra-nova` | LOW | Adição do modelo `TeacherCreate` |
| `src/api/routes.py` | API Routes | `regra-nova` | LOW | Implementação dos endpoints `POST /api/v1/teachers`, `POST /api/v1/teachers/import-csv` e `DELETE /api/v1/teachers/{id}` |
| `src/api/static/index.html` | Frontend SPA | `regra-nova` | LOW | Adição da aba de Gestão de Docentes, formulários e integração CSV |
| `tests/test_api_teachers.py` | Testes | `regra-nova` | LOW | Cobertura de testes unitários para a API de professores |

---

## Regras Preservadas (Intactas)

- 🟢 **RN-001 (Alocação Inteligente):** O motor de alocação consome a lista atualizada de professores e restrições.
- 🟢 **RN-003 (Política Tudo ou Nada no CSV):** A importação de docentes valida e rejeita dados incorretos com status 422.
