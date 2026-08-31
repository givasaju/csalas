# Roadmap: Cadastro de Disciplinas Lecionáveis por Docente

> Identificador: `009-disciplinas-docentes`
> Data: `2026-08-09`
> Requirements: `_reversa_forward/009-disciplinas-docentes/requirements.md`
> Confidência: 🟢 CONFIRMADO, 🟡 INFERIDO, 🔴 LACUNA

## 1. Resumo da abordagem

Esta evolução estende o módulo de docentes do ClassSync AI para registrar e gerenciar as disciplinas que cada professor está qualificado a ministrar. A solução altera a estrutura da entidade `Teacher` (adicionando o atributo `subjects` como lista de strings), atualiza os schemas Pydantic em `src/api/schemas.py` com validação de pelo menos 1 disciplina (`min_items=1`), ajusta o parser de CSV em `src/api/routes.py` para desmembrar a coluna multi-valor usando `;` como delimitador, e atualiza a interface SPA em `src/api/static/index.html` para permitir a inclusão de disciplinas e sua visualização como badges estilizadas.

## 2. Princípios aplicados

Nenhum princípio configurado em `.reversa/principles.md`.

## 3. Decisões técnicas

| ID | Decisão | Justificativa | Alternativas descartadas | Confidência |
|----|---------|----------------|--------------------------|-------------|
| D-01 | Armazenar `subjects` como tipo `JSON` (lista de strings) no modelo `Teacher` | Mantém o padrão já utilizado em `Room.features` em `src/models.py` e facilita serialização REST | Tabela N:N dedicada `TeacherSubject` (complexidade desnecessária para o escopo atual em memória) | 🟢 |
| D-02 | Utilizar ponto e vírgula (`;`) como separador multi-valor na coluna de disciplinas do CSV | Evita ambiguidades com a vírgula usada como delimitador padrão de colunas CSV | Vírgula com aspas escapadas, barra vertical (`|`) | 🟢 |
| D-03 | Validar obrigatoriedade de ao menos 1 disciplina no Pydantic `TeacherCreate` (`min_items=1`) | Garante a regra de negócio RN-03 confirmada na etapa de esclarecimentos | Permitir cadastro com lista vazia `[]` | 🟢 |
| D-04 | Renderizar disciplinas como tags/badges coloridas na SPA web (`index.html`) | Mantém a consistência visual com o layout existente de atributos de salas | Lista de texto simples, menu dropdown | 🟢 |

## 4. Premissas

Nenhuma premissa pendente. Todas as dúvidas foram esclarecidas no `requirements.md`.

## 5. Delta arquitetural

| Componente | Arquivo de origem no legado | Tipo de mudança | Resumo |
|------------|------------------------------|-----------------|--------|
| `academic-space-manager` | `_reversa_sdd/architecture.md#1-visao-geral-do-sistema` | contrato-alterado | Atualização dos schemas REST de docentes e lógica de importação CSV para suportar disciplinas |
| `occupancy-dashboard` | `_reversa_sdd/architecture.md#1-visao-geral-do-sistema` | regra-alterada | Inclusão de campo de entrada e exibição de tags de disciplinas na tabela de docentes da SPA |

## 6. Delta no modelo de dados

- Adição do atributo `subjects` (lista de strings) no modelo `Teacher` (`src/models.py`) e nos schemas Pydantic `TeacherCreate` / `TeacherResponse` (`src/api/schemas.py`).
- Detalhe completo em: `_reversa_forward/009-disciplinas-docentes/data-delta.md`

## 7. Delta de contratos externos

| Contrato | Tipo | Arquivo de detalhe |
|----------|------|--------------------|
| Gestão de Docentes API | HTTP | `_reversa_forward/009-disciplinas-docentes/interfaces/teachers-api.md` |

## 8. Plano de migração

n/a (mudança retrocompatível no ambiente em memória; registros legados sem campo `subjects` recebem lista vazia com fallback na leitura caso necessário).

## 9. Riscos e mitigações

| Risco | Impacto | Probabilidade | Mitigação |
|-------|---------|---------------|-----------|
| Arquivo CSV enviado utilizar vírgula em vez de `;` para separar disciplinas | Médio | Média | Validar o formato durante o parsing e retornar mensagem explicativa de erro 400 Bad Request indicando o uso de `;` |
| Docente cadastrado sem disciplinas via API externa | Baixo | Baixa | Validação estrita via Pydantic `Field(..., min_items=1)` |

## 10. Critério de pronto

- [ ] Todas as ações do `actions.md` marcadas `[X]`
- [ ] Testes automatizados cobrindo cadastro unitário e importação CSV de docentes com disciplinas
- [ ] `regression-watch.md` gerado
- [ ] Interface SPA permitindo cadastrar e listar disciplinas de docentes

## 11. Histórico de alterações

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-08-09 | Versão inicial gerada por `/reversa-plan` | reversa |
