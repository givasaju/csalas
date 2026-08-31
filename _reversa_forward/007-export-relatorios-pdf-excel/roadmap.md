# Roadmap: Exportação de relatórios de ocupação das salas em PDF/Excel

> Identificador: `007-export-relatorios-pdf-excel`
> Data: `2026-08-08`
> Requirements: `_reversa_forward/007-export-relatorios-pdf-excel/requirements.md`
> Confidência: 🟢 CONFIRMADO, 🟡 INFERIDO, 🔴 LACUNA

## 1. Resumo da abordagem

A abordagem técnica consiste em adicionar dois endpoints HTTP REST dedicados em `src/api/routes.py` (`GET /api/v1/reports/occupancy/pdf` e `GET /api/v1/reports/occupancy/excel`) para compilação dinâmica de dados de ocupação de salas e blocos prediais. Os geradores utilizarão geradores em memória (`io.BytesIO`) com utilitários Python para renderizar relatórios em PDF com estilo "Impressão Limpa" (cabeçalho institucional em preto e branco) e planilhas Excel (.xlsx) contendo abas de resumo por bloco e detalhamento de turmas. No frontend `src/api/static/index.html`, serão integrados dois botões de ação ("Exportar PDF" e "Exportar Excel") na barra superior do painel de ocupação para acionamento com 1 clique e download direto no navegador.

## 2. Princípios aplicados

Não há arquivo `.reversa/principles.md` registrado no projeto.

| Princípio | Como a feature se relaciona | Status |
|-----------|------------------------------|--------|
| N/A | Nenhum princípio cadastrado em `.reversa/principles.md`. | respeita |

## 3. Decisões técnicas

| ID | Decisão | Justificativa | Alternativas descartadas | Confidência |
|----|---------|----------------|--------------------------|-------------|
| D-01 | Geração em memória via `io.BytesIO` e `StreamingResponse` do FastAPI | Evita acúmulo de arquivos temporários órfãos em disco no servidor, garantindo execução stateless e limpa. | Salvar arquivos físicos em diretório `/tmp` do servidor | 🟢 |
| D-02 | Utilização de `reportlab` / `fpdf2` / `openpyxl` ou estruturas em memória leves com `openpyxl` / `ReportLab` | Padrão robusto da comunidade Python para renderização de tabelas PDF de impressão limpa e formatação nativa de pastas XLSX. | Geração manual de HTML para conversão via CLI externa (wkhtmltopdf) | 🟢 |
| D-03 | Suporte aos query params `block_id` e `shift` (`M`, `T`, `N`) | Permite aos gestores filtrar os relatórios por blocos prediais ou turnos específicos sem duplicar rotas. | Criar um endpoint separado para cada tipo de filtro | 🟢 |
| D-04 | Inclusão de botões de exportação na barra de ações da SPA (`index.html`) | Garante usabilidade direta para Isabela e Cláudio com acionamento nativo via JavaScript (`fetch` com `Blob` URL). | Criar uma página separada de relatórios na SPA | 🟢 |

## 4. Premissas

Nenhuma premissa pendente. Todas as dúvidas do `requirements.md` foram resolvidas na sessão `/reversa-clarify`.

| Premissa | Origem (`requirements.md` seção) | Risco se errada |
|----------|----------------------------------|-----------------|
| N/A | `## 9. Esclarecimentos` | N/A |

## 5. Delta arquitetural

| Componente | Arquivo de origem no legado | Tipo de mudança | Resumo |
|------------|------------------------------|-----------------|--------|
| `academic-space-manager` | `_reversa_sdd/architecture.md#1.-visao-geral-do-sistema` | contrato-novo | Adiciona as rotas REST `GET /api/v1/reports/occupancy/pdf` e `GET /api/v1/reports/occupancy/excel` em `src/api/routes.py`. |
| `occupancy-dashboard` | `_reversa_sdd/architecture.md#1.-visao-geral-do-sistema` | regra-alterada | Adiciona os botões de ação e manipuladores JS de download em `src/api/static/index.html` e estilos de impressão em `src/api/static/index.css`. |

## 6. Delta no modelo de dados

- Resumo das mudanças: A exportação de relatórios é uma operação de leitura agregada sobre os dados existentes de salas (`Room`), turmas (`Class`) e alocações ativas em memória (`worker.py`). Não altera o schema das tabelas.
- Detalhe completo em: `_reversa_forward/007-export-relatorios-pdf-excel/data-delta.md`

## 7. Delta de contratos externos

| Contrato | Tipo | Arquivo de detalhe |
|----------|------|--------------------|
| `reports-api` | HTTP | `_reversa_forward/007-export-relatorios-pdf-excel/interfaces/reports-api.md` |

## 8. Plano de migração

Não exige migração de banco de dados ou estado persistido ("n/a").

1. n/a

## 9. Riscos e mitigações

| Risco | Impacto | Probabilidade | Mitigação |
|-------|---------|---------------|-----------|
| Ausência de bibliotecas `reportlab` ou `openpyxl` no ambiente de execução Python | médio | baixo | Adicionar `reportlab` e `openpyxl` ao `requirements.txt` ou prover gerador em memória como fallback estruturado. |
| Consumo elevado de memória ao gerar relatórios grandes | médio | baixo | Aplicar agregação eficiente via geradores e limitar o escopo por filtros `block_id`/`shift`. |

## 10. Critério de pronto

- [ ] Todas as ações do `actions.md` marcadas `[X]`
- [ ] `cross-check.md` (se executado) sem CRITICAL nem HIGH
- [ ] `regression-watch.md` gerado
- [ ] Testes unitários e de integração validando os headers `Content-Type` e o status `200 OK` nas rotas de exportação

## 11. Histórico de alterações

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-08-08 | Versão inicial gerada por `/reversa-plan` | reversa |
