# Legacy Impact: Exportação de relatórios de ocupação das salas em PDF/Excel

> Identificador da feature: `007-export-relatorios-pdf-excel`  
> Data: `2026-08-08`  
> Âncora de contexto: Legado (`_reversa_sdd/architecture.md` + `_reversa_sdd/domain.md`)  

---

## 1. Arquivos Afetados e Impacto no Legado

| Arquivo afetado | Componente | Tipo | Severidade | Justificativa |
|-----------------|------------|------|------------|---------------|
| `requirements.txt` | `academic-space-manager` | `regra-nova` | LOW | Adição das dependências `reportlab` e `openpyxl` para suporte a relatórios. |
| `src/api/reports.py` | `academic-space-manager` | `componente-novo` | LOW | Novo módulo responsável pela compilação de relatórios PDF e Excel em memória. |
| `src/api/routes.py` | `academic-space-manager` | `contrato-novo` | MEDIUM | Adição dos endpoints REST `GET /api/v1/reports/occupancy/pdf` e `excel`. |
| `src/api/static/index.html` | `occupancy-dashboard` | `componente-novo` | LOW | Adição dos botões de exportação "Exportar PDF" e "Exportar Excel" com manipuladores JS. |
| `src/api/static/index.css` | `occupancy-dashboard` | `componente-novo` | LOW | Adição de estilo `.btn-secondary` e regras de impressão `@media print`. |

---

## 2. Diff Conceitual por Componente

### 2.1 academic-space-manager (`src/api/routes.py` e `src/api/reports.py`)
- **Resumo**: Foi introduzida a capacidade de relatórios gerenciais e operacionais. Os dados de ocupação de salas e blocos são lidos da base e formatados em tempo de execução sem afetar a lógica transacional das tabelas de salas ou docentes.

### 2.2 occupancy-dashboard (`src/api/static/index.html` e `index.css`)
- **Resumo**: A barra de ações da interface gráfica foi expandida com dois botões estilizados para download direto de arquivos binários sem recarregamento da página SPA.

---

## 3. Regras de Negócio Preservadas

As seguintes regras confirmadas em `_reversa_sdd/domain.md` permanecem 100% intactas:
- **RN-01 (Autenticação de Requisições de UI)**: Mantida a exigência de cabeçalho `Authorization: Bearer <token>` em todas as novas rotas HTTP de relatório. 🟢
- **RN-2.6 (Otimização e Consolidação Predial)**: Os cálculos de ocupação e blocos ativos continuam sendo lidos de forma não intrusiva. 🟢
- **RN-3 (Segurança e Autenticação JWT)**: Todas as rotas `/api/v1/reports/*` validam o token JWT através da dependência `check_jwt_auth`. 🟢

---

## 4. Regras de Negócio Modificadas

Nenhuma regra de negócio existente foi descontinuada ou alterada negativamente nesta entrega ("N/A").
