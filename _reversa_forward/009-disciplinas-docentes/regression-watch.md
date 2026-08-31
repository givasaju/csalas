# Regression Watch: Cadastro de Disciplinas Lecionáveis por Docente

> Identificador: `009-disciplinas-docentes`  
> Data: `2026-08-09`  

---

## Tabela de Vigilância

| ID | Origem (arquivo, seção) | Regra esperada após mudança | Tipo de verificação | Sinal de violação |
|----|-------------------------|-----------------------------|---------------------|-------------------|
| W001 | `_reversa_sdd/domain.md` | O cadastro de docente exige obrigatoriamente de 1 a 6 disciplinas lecionáveis | `presença` | Docente cadastrado com 0 ou mais de 6 disciplinas |
| W002 | `_reversa_sdd/domain.md` | O parser de CSV de docentes extrai disciplinas separadas por ';' de forma transacional | `presença` | Importação CSV aceita docente sem disciplinas ou ignora coluna disciplinas |
| W003 | `_reversa_sdd/domain.md` | A SPA web apresenta badges visuais para as disciplinas lecionáveis de cada professor | `presença` | Tabela de docentes na SPA deixa de renderizar as disciplinas lecionáveis |

---

## Histórico de re-extrações

---

## Arquivadas

