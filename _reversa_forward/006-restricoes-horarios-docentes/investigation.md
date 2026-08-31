# Investigação Técnica: Restrições Horárias Docentes

> Identificador: `006-restricoes-horarios-docentes`  
> Data: `2026-08-08`  

---

## 1. Visão geral da pesquisa

Esta investigação analisa a estrutura atual de armazenamento de restrições em `models.Restriction` e o funcionamento do motor de alocação `src/engine/core.py`.

---

## 2. Diagnóstico da arquitetura legada

1. **Modelo de Dados:**
   `models.Restriction` contém `id`, `teacher_id`, `day_of_week` (1 a 7) e `time_slot_id` (`M1`, `M2`, `T1`, `T2`, `N1`, `N2`).
2. **Rotas existentes:**
   - `POST /api/v1/allocation/restrictions`: realiza o cadastro com checagem de existência do professor e unicidade.
   - `DELETE /api/v1/allocation/restrictions`: realiza o reset semestral total.
3. **Lacunas de Contrato:**
   - Faltava rota para buscar restrições de um professor específico (`GET /api/v1/teachers/{teacher_id}/restrictions`).
   - Faltava rota para excluir uma restrição isolada (`DELETE /api/v1/allocation/restrictions/{restriction_id}`).
4. **Algoritmo do Motor de IA:**
   No loop de alocação de `core.py`, o filtro de validação de salas checa capacidade, tipo, acessibilidade e recursos, mas não consultava a matriz de indisponibilidade docente da turma em processamento.

---

## 3. Alternativas avaliadas

| Alternativa | Prós | Contras | Decisão |
|-------------|------|---------|---------|
| Checagem em O(1) com Dicionário de Restrições | Desempenho extremamente rápido sem degradação do leilão | Exige indexar restrições antes do loop | **Escolhida** |
| Consulta SQL a cada iteração do leilão | Simples de codificar | Alto overhead de I/O em loops de arbitragem | Descartada |

---

## 4. Padrões aplicáveis

- **Pre-loading Indexing Pattern**: indexar restrições na estrutura `{(teacher_id, day, slot): True}` no início do ciclo de alocação para busca instantânea.
- **RESTful Resource Deletion**: suporte a deleção granular por ID do recurso `/allocation/restrictions/{id}`.
