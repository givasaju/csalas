# Interface HTTP: Reports API

> Identificador da feature: `007-export-relatorios-pdf-excel`  
> Data: `2026-08-08`  

---

## 1. Visão Geral

Contrato REST HTTP para geração e download de relatórios de ocupação de salas físicas em formatos PDF e Excel.

---

## 2. Endpoints

### 2.1 GET /api/v1/reports/occupancy/pdf

Gera e envia o relatório impresso limpo em formato PDF.

- **Método**: `GET`
- **Headers de Requisição**:
  - `Authorization: Bearer <token>` (Obrigatório)
- **Query Parameters**:
  - `block_id` (opcional, string): Filtrar por ID do bloco predial (ex: `BLOCO_A`).
  - `shift` (opcional, string): Filtrar por turno (`M` = Manhã, `T` = Tarde, `N` = Noite).
- **Respostas**:
  - `200 OK`:
    - `Content-Type: application/pdf`
    - `Content-Disposition: attachment; filename="relatorio-ocupacao-YYYYMMDD.pdf"`
    - Corpo: Stream binário PDF.
  - `401 Unauthorized`: Token ausente ou inválido.
  - `400 Bad Request`: Parâmetro `shift` ou `block_id` inválido.

---

### 2.2 GET /api/v1/reports/occupancy/excel

Gera e envia a planilha de ocupação detalhada em formato Excel (.xlsx).

- **Método**: `GET`
- **Headers de Requisição**:
  - `Authorization: Bearer <token>` (Obrigatório)
- **Query Parameters**:
  - `block_id` (opcional, string): Filtrar por ID do bloco predial.
  - `shift` (opcional, string): Filtrar por turno (`M`, `T`, `N`).
- **Respostas**:
  - `200 OK`:
    - `Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`
    - `Content-Disposition: attachment; filename="relatorio-ocupacao-YYYYMMDD.xlsx"`
    - Corpo: Stream binário XLSX.
  - `401 Unauthorized`: Token ausente ou inválido.
  - `400 Bad Request`: Parâmetro inválido.
