# Framing: Gestão de Relatórios de Ocupação e Carga Docente

> Selo 🟡 PLANEJADO em todos os itens, sujeito a validação.

## Classificação da entrada
🟡 Solução disfarçada de problema, a demanda solicita a criação de uma UI/módulo de relatórios ("gestão de relatórios"), escondendo a dor de falta de visibilidade analítica e prestação de contas sobre uso de salas e alocação docente.

## Problema
🟡 Dificuldade da coordenação acadêmica e de infraestrutura em obter relatórios analíticos claros (individuais e consolidados) sobre a taxa de ocupação dos ambientes por horários/turnos e sobre a grade horária e disciplinas sob responsabilidade de cada docente.

## Quem sente
🟡 Coordenadores de curso, gerentes de infraestrutura predial e auditores acadêmicos que precisam analisar a distribuição de espaço e carga horária docente.

## Quando dói
🟡 No planejamento semestral de turmas, na consolidação do uso de prédios por turno (manhã, tarde, noite) e nas auditorias de alocação de professores e salas.

## Custo de não fazer
🟡 Risco de ociosidade não detectada em blocos inteiros de salas, sobrecarga ou subutilização de docentes e incapacidade de exportar relatórios gerenciais consolidados para a direção.

## Job to be done
🟡 Quando estiver analisando o uso da infraestrutura e a distribuição de aulas, eu quero visualizar e exportar relatórios detalhados e consolidados por ambiente e docente por turno, para conseguir otimizar a ocupação predial e garantir transparência na alocação docente.

## Fora de escopo declarado
🟡 Alteração manual direta de cadastros de professores ou salas (foco exclusivo em visualização, consolidação e exportação de relatórios).

## Âncoras no legado
🟡
- `_reversa_sdd/architecture.md#occupancy-dashboard`: Mapeia o dashboard e relatórios de exportação em PDF/Excel.
- `_reversa_sdd/domain.md#teachers-rooms`: Descreve a estrutura de turmas, docentes e restrições de horários.
- `_reversa_sdd/inventory.md#src/api/routes.py`: Mapeia os serviços existentes de geração de relatórios em `/api/v1/reports/pdf` e `/api/v1/reports/excel`.

---
Gerado por reversa-framer em 2026-08-14T14:11:30Z
Sessão: 002-gestao-relatorios-ocupacao-docentes
