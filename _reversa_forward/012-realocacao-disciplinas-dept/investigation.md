# Pesquisa de Investigação Técnica: Realocação Departamental de Disciplinas

> Feature: `012-realocacao-disciplinas-dept`
> Data: `2026-08-10`

---

## 1. Contexto e Problema Tecnológico

O ClassSync AI gerencia o cadastro de docentes e suas disciplinas lecionáveis (`subjects`), bem como a alocação de salas por subslot. Ao contratar um novo docente ou reestruturar o departamento, as disciplinas precisam ser remanejadas entre professores da mesma área sem quebrar a consistência das restrições de horários ou a integridade dos dados.

## 2. Alternativas Avaliadas

### Alternativa 1: Endpoint de Transferência Dedicado Atômico (Escolhida) 🟢
- **Descrição:** Criar `POST /api/v1/teachers/reallocate-subjects` recebendo `source_teacher_id`, `target_teacher_id`, `subjects` e `replacement_subject` opcional.
- **Vantagens:** Atômico, transacional (uma única requisição HTTP), valida permissões e departamento em um só ponto, migra alocações ativas e retorna o log completo de alterações.
- **Desvantagens:** Requer adição de novos schemas Pydantic e nova rota.

### Alternativa 2: Múltiplas Chamadas Individuais na API 🔴
- **Descrição:** O cliente SPA faz chamadas `PUT /api/v1/teachers/{id}` para atualizar o professor doador e o professor receptor separadamente.
- **Vantagens:** Não exige novo endpoint na API.
- **Desvantagens:** Risco alto de inconsistência (se a segunda chamada falhar, o estado fica corrompido), não valida a obrigatoriedade da disciplina substituta de forma atômica, exige código complexo no frontend.

## 3. Padrões de Código e Arquitetura Aplicáveis

- **Padrão Iso-Department Guard:** Função utilitária no FastAPI que verifica se `teacher_a.department == teacher_b.department`.
- **Atomic Rollback Pattern:** Garantia de que a atualização dos docentes e a migração das alocações são executadas dentro do mesmo contexto de sessão do banco de dados (SQLAlchemy transaction ou mutação atômica em listas do worker).
