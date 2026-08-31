# Requirements: Seleção de Disciplina na Alocação de Aulas por Subslot

> Identificador: `011-disciplina-alocacao-aula`  
> Data: `2026-08-09`  
> Pasta da extração reversa: `_reversa_sdd/`  
> Confidência: 🟢 CONFIRMADO, 🟡 INFERIDO, 🔴 LACUNA / DÚVIDA  

---

## 1. Resumo executivo

Esta melhoria estende a funcionalidade de alocação de aulas no ClassSync AI permitindo que o usuário selecione qual disciplina cadastrada do docente será lecionada em cada sub-slot específico (50 min). A interface de alocação passa a atualizar dinamicamente o seletor de disciplinas conforme o professor escolhido e a tabela de alocações ativas exibirá a disciplina vinculada.

---

## 2. Contexto a partir do legado

| Fonte | Trecho relevante | Confidência |
|-------|------------------|-------------|
| `_reversa_sdd/addenda/009-disciplinas-docentes.md` | Entidade `Teacher` com lista de 1 a 6 disciplinas lecionáveis (`subjects`) | 🟢 |
| `_reversa_sdd/addenda/008-alocacao-docente-max-4-aulas.md` | Entidade `Allocation` e formulário/tabela de alocações na SPA `index.html` | 🟢 |

---

## 3. Personas e cenários de uso

| Persona | Objetivo | Cenário-chave |
|---------|----------|---------------|
| Carlos (Coordenador Acadêmico) | Atribuir uma disciplina específica da lista do docente ao agendar uma aula no subslot M1 | Selecionar o Prof. Givaldo, escolher "Manutenção Elétrica" do dropdown de disciplinas e salvar a alocação |

---

## 4. Regras de negócio novas ou alteradas

1. **RN-01:** Vínculo de Disciplina na Alocação 🟢
   - Tipo: alterada
   - Cada registro de alocação de aula (`Allocation`) passa a armazenar o nome da disciplina (`subject`) lecionada naquele subslot.

2. **RN-02:** Validação contra o Rol de Disciplinas do Docente 🟢
   - Tipo: nova
   - A disciplina selecionada para o subslot deve obrigatoriamente pertencer à lista de disciplinas cadastrada para aquele docente (`Teacher.subjects`). Se não informada explicitamente, assume a primeira disciplina do rol do docente.

3. **RN-03:** Seleção Dinâmica na Interface UI 🟢
   - Tipo: nova
   - Na tela de alocação de aulas (`index.html`), a alteração do professor no `<select id="allocTeacherSelect">` atualiza dinamicamente as opções do `<select id="allocSubject">` apenas com as disciplinas lecionáveis daquele professor.

---

## 5. Requisitos Funcionais

| ID | Requisito | Prioridade | Critério de aceite | Confidência |
|----|-----------|------------|--------------------|-------------|
| RF-01 | Adicionar campo `subject` ao modelo `Allocation` em `src/models.py` | Must | O banco de dados SQLite armazena a coluna `subject` na tabela `Allocation` | 🟢 |
| RF-02 | Atualizar schemas e rotas de alocação em `src/api/schemas.py` e `src/api/routes.py` | Must | `POST /api/v1/allocations` aceita e valida `subject` e `GET /api/v1/allocations` retorna `subject` | 🟢 |
| RF-03 | Atualizar interface SPA `src/api/static/index.html` com dropdown dinâmico e coluna na tabela | Must | O formulário de alocação exibe o select de disciplinas do professor e a tabela exibe a badge da disciplina alocada | 🟢 |

---

## 6. Critérios de Aceitação

```gherkin
Cenário: Seleção e alocação de disciplina para subslot
  Dado que o docente "Givaldo" possui as disciplinas ["Manutenção Elétrica", "Comandos Elétricos"]
  Quando o coordenador seleciona "Givaldo" no formulário de alocação
  Então o select de disciplinas lista apenas "Manutenção Elétrica" e "Comandos Elétricos"
  E ao salvar a alocação para "Manutenção Elétrica" na Sala 101 (M1), a tabela reflete a disciplina informada.
```

---

## 7. Prioridade MoSCoW

| Item | MoSCoW | Justificativa |
|------|--------|---------------|
| RF-01 | Must | Necessário para persistência da disciplina alocada |
| RF-02 | Must | Requisito da API REST para recebimento e validação |
| RF-03 | Must | Requisito direto solicitado na interface visual |
