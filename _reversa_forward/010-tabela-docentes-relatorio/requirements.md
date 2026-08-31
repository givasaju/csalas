# Requirements: Tabela de Alocações por Docente no Relatório de Ocupação

> Identificador: `010-tabela-docentes-relatorio`  
> Data: `2026-08-09`  
> Pasta da extração reversa: `_reversa_sdd/`  
> Confidência: 🟢 CONFIRMADO, 🟡 INFERIDO, 🔴 LACUNA / DÚVIDA  

---

## 1. Resumo executivo

Esta melhora expande o Relatório de Ocupação de Salas do ClassSync AI (gerado em PDF e Excel) adicionando uma nova tabela dedicada ao detalhamento de alocações por docente. A tabela listará os docentes em ordem alfabética juntamente com suas disciplinas lecionáveis, a sala física ocupada, o turno e o sub-slot de cada aula alocada.

---

## 2. Contexto a partir do legado

| Fonte | Trecho relevante | Confidência |
|-------|------------------|-------------|
| `_reversa_sdd/addenda/007-export-relatorios-pdf-excel.md#resumo-da-entrega` | Geração de relatórios PDF e Excel em `src/api/reports.py` e rotas GET `/api/v1/reports/occupancy/pdf` / `/excel` em `routes.py` | 🟢 |
| `_reversa_sdd/addenda/008-alocacao-docente-max-4-aulas.md#resumo-da-entrega` | Entidade `Allocation` (`teacher_id`, `room_id`, `day_of_week`, `shift`, `sub_slot`) | 🟢 |
| `_reversa_sdd/addenda/009-disciplinas-docentes.md#resumo-da-entrega` | Entidade `Teacher` com lista de disciplinas `subjects` | 🟢 |

---

## 3. Personas e cenários de uso

| Persona | Objetivo | Cenário-chave |
|---------|----------|---------------|
| Isabela (Diretora de Infraestrutura) | Visualizar no relatório impresso/PDF/Excel a grade de docentes e salas ocupadas | Baixar o relatório de ocupação e consultar a seção "Ocupação por Docente" em ordem alfabética |

---

## 4. Regras de negócio novas ou alteradas

1. **RN-01:** Tabela de Ocupação por Docente no Relatório 🟢
   - Tipo: nova
   - O relatório de ocupação (PDF e XLSX) deve passar a incluir uma nova tabela/seção contendo as alocações ativas de docentes.

2. **RN-02:** Ordenação Alfabética por Nome de Docente 🟢
   - Tipo: nova
   - Os registros da tabela de docentes no relatório devem ser apresentados estritamente ordenados pelo nome do docente em ordem alfabética crescente (A-Z).

3. **RN-03:** Campos Obrigatórios da Tabela 🟢
   - Tipo: nova
   - Cada linha da tabela deve exibir: Nome do Docente, Disciplinas Lecionáveis (`subjects`), Sala Ocupada (ID/Nome da sala), Turno (M/T/N) e Sub-slot (1 a 5).

---

## 5. Requisitos Funcionais

| ID | Requisito | Prioridade | Critério de aceite | Confidência |
|----|-----------|------------|--------------------|-------------|
| RF-01 | Incluir tabela de ocupação docente no PDF em `src/api/reports.py` | Must | O PDF gerado via `generate_pdf_report()` exibe a Seção 3 com docentes em ordem A-Z, suas disciplinas, sala, turno e subslot | 🟢 |
| RF-02 | Incluir aba/tabela de ocupação docente no Excel em `src/api/reports.py` | Must | A planilha XLSX criada via `generate_excel_report()` inclui a aba "Alocações por Docente" ordenada de A-Z | 🟢 |
| RF-03 | Carregar e cruzar dados de alocações, docentes e salas em `src/api/routes.py` | Must | As rotas `GET /api/v1/reports/occupancy/pdf` e `/excel` realizam os `joins` / buscas necessárias no banco SQLite para alimentar o relatório | 🟢 |

---

## 6. Requisitos Não Funcionais

| Tipo | Requisito | Evidência ou justificativa | Confidência |
|------|-----------|----------------------------|-------------|
| Estética | Manter o padrão visual "Impressão Limpa" no PDF e estilo corporativo no XLSX | `_reversa_sdd/addenda/007-export-relatorios-pdf-excel.md` | 🟢 |
| Desempenho | A geração de relatórios com até 100 alocações deve responder em menos de 1 segundo | Desempenho atual do `reports.py` | 🟢 |

---

## 7. Critérios de Aceitação

```gherkin
Cenário: Emissão de relatório PDF com tabela de docentes
  Dado que existem alocações cadastradas para o Prof. Bruno (Filosofia) na Sala 101 (M1) e Profa. Ana (Física) na Sala 102 (T2)
  Quando a diretora requisita o relatório GET /api/v1/reports/occupancy/pdf
  Então o PDF retornado contém a nova tabela "Ocupação por Docente"
  E a Profa. Ana aparece como primeiro registro da tabela (ordem A-Z) exibindo disciplinas, sala, turno e subslot
  E o Prof. Bruno aparece em seguida.

Cenário: Emissão de relatório Excel com aba de docentes
  Dado que existem docentes e alocações no sistema
  Quando o relatório GET /api/v1/reports/occupancy/excel é gerado
  Então o arquivo XLSX contém a aba "Alocações por Docente" com os dados consolidados e ordenados de A-Z.
```

---

## 8. Prioridade MoSCoW

| Item | MoSCoW | Justificativa |
|------|--------|---------------|
| RF-01 | Must | Requisito direto solicitado para o formato PDF |
| RF-02 | Must | Requisito direto solicitado para o formato Excel |
| RF-03 | Must | Necessário para alimentar o relatório com dados completos do banco |

---

## 9. Esclarecimentos

Nenhum ponto pendente.

---

## 10. Lacunas

Nenhuma lacuna.

---

## 11. Histórico de alterações

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-08-09 | Versão inicial gerada por `/reversa-requirements` | reversa |
