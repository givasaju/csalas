# Requirements: Cadastro de Disciplinas Lecionáveis por Docente

> Identificador: `009-disciplinas-docentes`
> Data: `2026-08-09`
> Pasta da extração reversa: `_reversa_sdd/`
> Confidência: 🟢 CONFIRMADO, 🟡 INFERIDO, 🔴 LACUNA / DÚVIDA

## 1. Resumo executivo

Esta feature expande o cadastro de docentes do ClassSync AI permitindo incluir e gerenciar a lista de disciplinas/matérias que cada professor está apto a lecionar. Atualmente, o docente possui apenas dados cadastrais básicos (matrícula, nome, departamento). Com esta melhoria, a coordenação acadêmica poderá informar as disciplinas lecionáveis via formulário unitário, importação CSV em lote e visualizar essas aptidões no painel web, preparando a base para alocações inteligentes baseadas em competência.

## 2. Contexto a partir do legado

| Fonte | Trecho relevante | Confidência |
|-------|------------------|-------------|
| `_reversa_sdd/architecture.md#3-modelo-de-entidade-relacionamento-erd` | Entidade `Teacher` com atributos `id`, `name`, `email` | 🟢 |
| `_reversa_sdd/domain.md#210-restricoes-de-indisponibilidade-docente` | Cadastro docente e associação de restrições de horários | 🟢 |
| `_reversa_sdd/addenda/005-cadastro-docentes.md#resumo-da-entrega` | Endpoints `POST /api/v1/teachers`, `POST /api/v1/teachers/import-csv` e interface SPA | 🟢 |

## 3. Personas e cenários de uso

| Persona | Objetivo | Cenário-chave |
|---------|----------|---------------|
| Cláudio (Coordenador de Curso) | Cadastrar as disciplinas que um docente pode ministrar | Ao cadastrar um novo docente ou editar um existente, selecionar/digitar as disciplinas habilitadas para o professor |
| Cláudio (Coordenador de Curso) | Importar em lote docentes com suas respectivas disciplinas | Enviar um arquivo CSV contendo a lista de professores e suas matérias lecionáveis |

## 4. Regras de negócio novas ou alteradas

1. **RN-01:** Lista de Disciplinas por Docente 🟢
   - Origem no legado: `_reversa_sdd/addenda/005-cadastro-docentes.md`
   - Tipo: alterada
   - Cada docente cadastrado deve possuir um conjunto de disciplinas habilitadas (códigos ou nomes de disciplinas).

2. **RN-02:** Importação CSV com Coluna de Disciplinas 🟢
   - Origem no legado: `_reversa_sdd/domain.md#27-importacao-transacional-de-salas-tudo-ou-nada`
   - Tipo: alterada
   - O arquivo CSV de importação de docentes passa a aceitar a coluna `disciplines` (ou `disciplinas`), utilizando ponto e vírgula (`;`) como separador multi-valor (ex.: `Cálculo I;Álgebra Linear`). Na importação em lote, a validação permanece atômica (tudo-ou-nada).

3. **RN-03:** Obrigatoriedade de Disciplinas no Cadastro 🟢
   - Origem no legado: N/A (regra nova)
   - Tipo: nova
   - Ao menos 1 disciplina lecionável deve ser informada obrigatoriamente no momento do cadastro de um docente (seja unitário ou via CSV). Registros sem disciplinas vinculadas são rejeitados com erro de validação.

## 5. Requisitos Funcionais

| ID | Requisito | Prioridade | Critério de aceite | Confidência |
|----|-----------|------------|--------------------|-------------|
| RF-01 | Permitir incluir lista de disciplinas no cadastro unitário de docente (`POST /api/v1/teachers`) | Must | A requisição exige o campo `subjects` (lista com pelo menos 1 string) e persiste a informação vinculada ao docente | 🟢 |
| RF-02 | Suportar coluna de disciplinas na importação em lote por CSV (`POST /api/v1/teachers/import-csv`) | Must | O parser de CSV extrai as disciplinas separadas por `;` da coluna correspondente e realiza a inserção atômica | 🟢 |
| RF-03 | Exibir a lista de disciplinas lecionáveis por docente na interface SPA (`index.html`) | Must | A tabela de docentes na aba "Gestão de Docentes" exibe as disciplinas cadastradas em formato de tags ou lista separada por vírgulas | 🟢 |
| RF-04 | Permitir atualizar/editar as disciplinas lecionáveis de um docente cadastrado | Should | O sistema oferece endpoint ou mecanismo para atualizar as disciplinas associadas a um professor existente | 🟡 |

## 6. Requisitos Não Funcionais

| Tipo | Requisito | Evidência ou justificativa | Confidência |
|------|-----------|----------------------------|-------------|
| Desempenho | O parsing e validação do CSV com até 500 docentes e disciplinas deve responder em menos de 1 segundo | Compatibilidade com o padrão dos endpoints de importação existentes (`routes.py`) | 🟢 |
| Usabilidade | Na SPA web, a entrada de disciplinas deve permitir adicionar múltiplos itens de forma limpa (tags/pills) | Padrão visual do ClassSync AI para listas de atributos | 🟡 |
| Integridade | Falhas de validação sintática nas disciplinas durante importação CSV devem cancelar a transação inteira | `_reversa_sdd/domain.md#27-importacao-transacional-de-salas-tudo-ou-nada` | 🟢 |

## 7. Critérios de Aceitação

```gherkin
Cenário: Cadastro unitário de docente com disciplinas lecionáveis
  Dado que o coordenador está na página de Gestão de Docentes
  Quando preenche a matrícula "DOC-101", nome "Prof. Carlos", departamento "Engenharia" e disciplinas ["Cálculo I", "Álgebra Linear"]
  E clica em "Salvar Docente"
  Então o docente é cadastrado com sucesso
  E a tabela de docentes exibe "Prof. Carlos" com as disciplinas "Cálculo I, Álgebra Linear"

Cenário: Importação CSV de docentes com coluna de disciplinas
  Dado que o coordenador possui um arquivo CSV com o cabeçalho "id,name,department,disciplines"
  E a linha contendo "DOC-102,Profa. Ana,Ciências,Física I;Física II"
  Quando realiza o upload do arquivo em "Importar CSV"
  Então o sistema importa todos os registros com sucesso
  E a docente "Profa. Ana" é armazenada com as disciplinas ["Física I", "Física II"]

Cenário: Tentativa de cadastro de docente sem disciplinas lecionáveis
  Dado que o coordenador preenche os dados do docente sem informar nenhuma disciplina
  Quando tenta submeter o formulário ou enviar CSV sem disciplinas
  Então o sistema rejeita a requisição com erro de validação (400 Bad Request / 422 Unprocessable Entity)
  E nenhum docente é inserido
```

## 8. Prioridade MoSCoW

| Item | MoSCoW | Justificativa |
|------|--------|---------------|
| RF-01 | Must | Essencial para o registro individual de disciplinas lecionáveis por professor |
| RF-02 | Must | Fundamental para a carga em lote de dados acadêmicos |
| RF-03 | Must | Necessário para a visualização e acompanhamento pela coordenação |
| RF-04 | Should | Importante para manter o cadastro atualizado ao longo dos semestres |
| RNF de Integridade | Must | Garante que a importação CSV mantenha a consistência atômica |

## 9. Esclarecimentos

### Sessão 2026-08-09

- **Q:** Qual deve ser o separador de disciplinas na coluna do arquivo CSV para importação em lote?
  **R:** Ponto e vírgula (`;`) — ex.: `'Cálculo I;Álgebra Linear'`
- **Q:** O cadastro inicial de um docente pode ser realizado sem disciplinas vinculadas (lista vazia)?
  **R:** Não, ao menos 1 disciplina lecionável deve ser informada obrigatoriamente no momento do cadastro

## 10. Lacunas

Nenhuma lacuna pendente. Todas as dúvidas foram esclarecidas na Sessão 2026-08-09.

## 11. Histórico de alterações

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-08-09 | Versão inicial gerada por `/reversa-requirements` | reversa |
| 2026-08-09 | Esclarecimento de dúvidas via `/reversa-clarify` | reversa |
