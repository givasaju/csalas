# Legacy Impact: Implementar o motor de alocação core-allocation-engine

> Data: `2026-08-07`  
> Identificador: `001-implementar-core-allocation`  
> Tipo: Feature greenfield, sem legado pré-existente. Âncora: prd.md + specs SDD.  

---

## 1. Arquivos Criados e Mapeamento de Componentes

| Arquivo Criado | Componente Spec | Tipo de Impacto | Severidade | Justificativa |
|----------------|-----------------|-----------------|------------|---------------|
| `requirements.txt` | `core-allocation-engine` | `componente-novo` | LOW | Arquivo de gerenciamento de dependências Python. |
| `db/migrations.sql` | `academic-space-manager` | `componente-novo` | LOW | Definições das tabelas para persistência dos dados de leilões e tarefas. |
| `src/engine/agents.py` | `core-allocation-engine` | `componente-novo` | HIGH | Implementação das classes dos agentes ACC, AAC e AMR de leilão. |
| `src/engine/optimization.py` | `core-allocation-engine` | `componente-novo` | MEDIUM | Implementação da heurística de consolidação predial de blocos. |
| `src/engine/core.py` | `core-allocation-engine` | `componente-novo` | HIGH | Orquestrador principal do processamento do leilão e otimização. |
| `src/api/routes.py` | `core-allocation-engine` | `componente-novo` | MEDIUM | Endpoints HTTP de controle e status da alocação de salas. |
| `src/api/worker.py` | `core-allocation-engine` | `componente-novo` | MEDIUM | Fila e worker assíncrono em segundo plano para o processamento. |
| `src/main.py` | `core-allocation-engine` | `componente-novo` | LOW | Ponto de entrada executável da API do ClassSync AI. |
| `src/README.md` | `core-allocation-engine` | `componente-novo` | LOW | Documentação técnica rápida das lógicas implementadas. |

---

## 2. Diff Conceitual por Componente

*   **core-allocation-engine:** Implementação completa da inteligência multiagente baseada no Contract Net Protocol e leilão de créditos de compensação cooperativos, incluindo fechamento e remanejamento predial sustentável.
*   **academic-space-manager:** Integração conceitual de banco de dados e APIs via rotas FastAPI para fornecimento e persistência local de dados acadêmicos e do campus.

---

## 3. Preservadas

*   N/A (Nenhuma regra ou código existente alterado; feature greenfield).

---

## 4. Modificadas

*   N/A (Nenhuma regra ou código existente alterado; feature greenfield).
