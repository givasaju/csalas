# Investigation: Cadastro de Disciplinas Lecionáveis por Docente

> Identificador: `009-disciplinas-docentes`
> Data: `2026-08-09`

---

## 1. Contexto e Motivação

O ClassSync AI gerencia professores no módulo de restrições de horários e alocação. Contudo, até o momento, a entidade `Teacher` armazenava apenas informações administrativas genéricas (`id`, `name`, `department`). Para permitir a futura recomendação de salas e validação de turmas por área de especialidade, faz-se necessário vincular a lista de disciplinas lecionáveis diretamente ao perfil do docente.

---

## 2. Alternativas Avaliadas para Representação do Modelo

### Opção A: Array JSON no Modelo `Teacher` (Escolhida 🟢)
- **Descrição:** Adicionar o campo `subjects` como tipo `JSON` diretamente na tabela/classe `Teacher`, armazenando uma lista de strings (ex.: `["Cálculo I", "Física I"]`).
- **Vantagens:** Segue exatamente o padrão arquitetural já estabelecido na entidade `Room` (`features = Column(JSON, default=list)` em `src/models.py`), sem overhead de relacioamentos ou joins complexos no armazenamento em memória.
- **Desvantagens:** Sem chave estrangeira estrita para uma tabela de disciplinas cadastradas no sistema.
- **Veredito:** Mantém a consistência com o restante da base legado.

### Opção B: Tabela Relacional N:N `TeacherSubject` (Descartada 🔴)
- **Descrição:** Criar tabela de junção com colunas `teacher_id` e `subject_code`.
- **Desvantagens:** Aumenta a complexidade de persistência para o backend em memória sem ganho real no escopo atual.

---

## 3. Estratégia de Parsing para Importação CSV

Na importação em lote (`POST /api/v1/teachers/import-csv`), a coluna `disciplines` (ou `disciplinas` / `subjects`) no cabeçalho CSV conterá múltiplos valores.
Para separar os valores sem colidir com vírgulas de delimitador de colunas padrão CSV:
1. O delimitador interno para disciplinas é definido como `;`.
2. Exemplo de célula CSV: `Cálculo I;Álgebra Linear;Geometria Analítica`.
3. A função de parsing realiza `[s.strip() for s in raw_subjects.split(';') if s.strip()]`.
4. Se o resultado for uma lista vazia, a linha é considerada inválida e o processo dispara HTTP 400 (política atômica tudo-ou-nada).

---

## 4. Padrões de Interface SPA Web

Na SPA (`index.html`), o formulário de cadastro de docentes utilizará um campo `<input type="text" id="teacher-subjects" placeholder="Ex: Cálculo I; Física I">` ou input com tags, convertendo a string separada por vírgula ou ponto e vírgula num array JSON ao enviar para a API. A tabela renderizará cada disciplina dentro de um elemento `<span class="badge badge-subject">...</span>`.
