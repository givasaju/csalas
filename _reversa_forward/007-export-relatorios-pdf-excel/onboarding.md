# Guia de Onboarding e Validação: Exportação de Relatórios

> Identificador da feature: `007-export-relatorios-pdf-excel`  
> Data: `2026-08-08`  

---

## 1. Objetivo

Este guia fornece um passo a passo prático para testar e validar manualmente a exportação de relatórios em PDF e Excel no ClassSync AI.

---

## 2. Pré-requisitos

1. Servidor ClassSync AI em execução na porta 8000:
   ```bash
   python -m uvicorn src.main:app --reload
   ```
2. Token JWT mock de autorização: `Bearer mock-token`.

---

## 3. Passos para Validação Manual via API (cURL / HTTPie)

### Passo 1: Validar download de relatório em PDF
Execute o comando cURL para baixar o relatório PDF:
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/reports/occupancy/pdf" \
  -H "Authorization: Bearer mock-token" \
  --output relatorio_ocupacao.pdf
```
- **Resultado Esperado**: O arquivo `relatorio_ocupacao.pdf` é criado no diretório atual. O comando `file relatorio_ocupacao.pdf` ou abertura no leitor PDF confirma um documento em estilo de impressão limpa com tabela de blocos e estatísticas de ocupação.

### Passo 2: Validar download de planilha em Excel
Execute o comando cURL para baixar a planilha Excel:
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/reports/occupancy/excel" \
  -H "Authorization: Bearer mock-token" \
  --output relatorio_ocupacao.xlsx
```
- **Resultado Esperado**: O arquivo `relatorio_ocupacao.xlsx` é salvo e pode ser aberto no Excel/LibreOffice Calc com as abas "Resumo por Bloco" e "Matriz Detalhada".

### Passo 3: Validar filtros por Bloco e Turno
Execute a busca filtrada:
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/reports/occupancy/pdf?block_id=BLOCO_A&shift=M" \
  -H "Authorization: Bearer mock-token" \
  --output relatorio_bloco_a_manha.pdf
```
- **Resultado Esperado**: Retorna 200 OK com PDF contendo apenas dados do Bloco A no turno matutino.

---

## 4. Passos para Validação via Interface Web (SPA)

1. Abra o navegador no endereço `http://127.0.0.1:8000/`.
2. Observe a barra superior de ações do dashboard `occupancy-dashboard`.
3. Clique no botão **"Exportar PDF"**: O navegador iniciará o download automático do arquivo `.pdf`.
4. Clique no botão **"Exportar Excel"**: O navegador iniciará o download automático do arquivo `.xlsx`.
