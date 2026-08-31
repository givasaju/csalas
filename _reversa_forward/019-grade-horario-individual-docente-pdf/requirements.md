# Requirements: Grade de Horário Individual do Docente com Exportação PDF

> Identificador: `019-grade-horario-individual-docente-pdf`
> Data: `2026-08-14`
> Extração de referência: `_reversa_sdd/`
> Confidência: 🟢 CONFIRMADO, 🟡 INFERIDO, 🔴 LACUNA

## 1. Resumo executivo

Permitir que na seção **Relatório de Grade & Carga Horária Docente (Individual)** da aba Relatórios, ao clicar na linha de qualquer professor, seja exibido um modal ou painel expansível com a **Grade Semanal de Horários do Docente** em formato de matriz (Segunda a Sábado x Turnos/Slots). A visão contará com um botão **📄 Gerar PDF do Horário** para baixar o relatório PDF individual formatado daquele professor.

## 2. Contexto a partir do legado

| Fonte | Trecho relevante | Confidência |
|-------|------------------|-------------|
| `_reversa_sdd/addenda/018-gestao-relatorios-ocupacao-docentes.md` | Aba Relatórios com a seção de Carga Horária Docente. | 🟢 |
| `_reversa_sdd/inventory.md#src/api/routes.py` | Endpoint de geração de PDF em `/api/v1/reports/occupancy/pdf`. | 🟢 |

## 3. Regras de negócio novas ou alteradas

1. **RN-01:** Clique interativo na linha da tabela de docentes para abrir o modal `#teacherScheduleModal` ou visão expandida da matriz semanal de horários do professor. 🟢
2. **RN-02:** A matriz semanal exibirá os dias da semana (Segunda a Sábado) nas colunas e os slots/intervalos de horários (M1..M6, T1..T6, N1..N6) nas linhas, destacando disciplinas e salas alocadas. 🟢
3. **RN-03:** Botão **📄 Gerar PDF do Horário** no cabeçalho do modal/painel individual acionando a rota de exportação PDF individual do docente (`GET /api/v1/reports/teacher/{teacher_id}/pdf`). 🟢

## 4. Requisitos Funcionais

| ID | Requisito | Prioridade | Critério de aceite | Confidência |
|----|-----------|------------|--------------------|-------------|
| RF-01 | Tornar as linhas da tabela de docentes clicáveis com cursor pointer e estilo hover destacado. | Must | Clicar na linha abre a grade individual do docente. | 🟢 |
| RF-02 | Exibir a matriz semanal de horários com disciplinas, salas e horários nos slots correspondentes. | Must | A matriz é preenchida corretamente com as aulas do professor. | 🟢 |
| RF-03 | Implementar o endpoint `GET /api/v1/reports/teacher/{teacher_id}/pdf` no backend para gerar o PDF da grade do professor. | Must | Clicar no botão baixa o PDF formatado do docente. | 🟢 |

## 5. Requisitos Não Funcionais

| Tipo | Requisito | Evidência ou justificativa | Confidência |
|------|-----------|----------------------------|-------------|
| Usabilidade | Manter estética Glassmorphism com modal responsivo e badges de horário. | Padrão do ClassSync AI | 🟢 |
| Desempenho | Renderização do modal em menos de 100ms. | Execução client-side | 🟢 |

## 6. Histórico de alterações

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-08-14 | Criado por `/reversa-requirements` | reversa |
