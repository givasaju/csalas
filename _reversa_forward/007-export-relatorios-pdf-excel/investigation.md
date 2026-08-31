# Pesquisa Técnica e Investigação: Exportação de relatórios em PDF/Excel

> Identificador da feature: `007-export-relatorios-pdf-excel`  
> Data: `2026-08-08`  

---

## 1. Contexto e Motivação

O ClassSync AI demanda relatórios executivos e operacionais de ocupação para dois perfis principais de usuários:
1. **Isabela (Diretora de Infraestrutura)**: Necessita de documentos em PDF de alta legibilidade, adequados para impressão física rápida e reuniões de gestão.
2. **Cláudio (Coordenador de Curso)**: Necessita de planilhas estruturadas em Excel (.xlsx) para tratamento e cruzamento analítico de dados de turmas e salas.

---

## 2. Alternativas Avaliadas para Geração de PDF

### Opção A: `reportlab` / `fpdf2` (Escolha recomendada)
- **Vantagens**: Biblioteca Python pura, rápida, sem dependência de binários nativos do sistema operacional (como Chromium ou wkhtmltopdf). Gera PDFs nativos diretamente em buffers `io.BytesIO`.
- **Desvantagens**: Requer adição ao `requirements.txt`.
- **Veredito**: Selecionada pela robustez e performance determinística.

### Opção B: Conversão via Headless Browser (Puppeteer / Playwright / WeasyPrint)
- **Vantagens**: Permite reaproveitar HTML/CSS da SPA.
- **Desvantagens**: Dependência pesada de instâncias de navegadores ou ferramentas de terceiros no servidor, inviável para ambientes enxutos.
- **Veredito**: Descartada.

---

## 3. Alternativas Avaliadas para Geração de Excel (XLSX)

### Opção A: `openpyxl` (Escolha recomendada)
- **Vantagens**: Padrão da comunidade Python para escrita de arquivos `.xlsx`, suporta múltiplas abas, estilos de célula, larguras automáticas de colunas e cabeçalhos formatados.
- **Desvantagens**: Pequena dependência externa.
- **Veredito**: Selecionada.

### Opção B: Exportação simples de arquivos CSV com suporte a MIME de planilha
- **Vantagens**: Sem dependências externas.
- **Desvantagens**: Não suporta múltiplas abas ("Resumo por Bloco" e "Matriz Detalhada"), estilos visuais ou formatação de colunas exigidos no `requirements.md`.
- **Veredito**: Descartada.

---

## 4. Padrões de Integração no FastAPI e Frontend

- **Backend**: Utilização de `fastapi.responses.StreamingResponse` ou `Response` retornando `bytes` gerados por `BytesIO` com cabeçalho HTTP `Content-Disposition: attachment; filename="relatorio-ocupacao-YYYYMMDD.pdf"`.
- **Frontend**: Requisição via `fetch` assíncrono com cabeçalho `Authorization: Bearer <token>`, conversão da resposta em `blob` e criação de URL temporária via `window.URL.createObjectURL(blob)` para disparo de download no navegador sem recarregar a página.
