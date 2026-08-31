# Regression Watch: Exportação de relatórios de ocupação das salas em PDF/Excel

> Identificador da feature: `007-export-relatorios-pdf-excel`  
> Data de criação: `2026-08-08`  

---

## 1. Watch Items de Regressão

| ID | Origem (arquivo, seção) | Regra esperada após mudança | Tipo de verificação | Sinal de violação |
|----|-------------------------|-----------------------------|---------------------|-------------------|
| W001 | `_reversa_forward/007-export-relatorios-pdf-excel/requirements.md#RF-01` | Rota `GET /api/v1/reports/occupancy/pdf` deve retornar 200 OK com cabeçalho `application/pdf` para tokens JWT válidos | presença | Retorno 404, 500 ou Content-Type diferente de application/pdf |
| W002 | `_reversa_forward/007-export-relatorios-pdf-excel/requirements.md#RF-02` | Rota `GET /api/v1/reports/occupancy/excel` deve retornar 200 OK com planilha Excel (.xlsx) | presença | Retorno 404, 500 ou falha na geração do arquivo |
| W003 | `_reversa_forward/007-export-relatorios-pdf-excel/requirements.md#RN-04` | As rotas de exportação devem rejeitar requisições sem o cabeçalho Authorization válido retornando HTTP 401 | presença | Retorno HTTP 200 para requisições não autenticadas |

---

## 2. Histórico de re-extrações

*Nenhuma re-extração registrada ainda.*

---

## 3. Arquivadas

*Nenhum item arquivado.*

---

## 4. Observações

- Os relatórios suportam filtragem opcional via query parameters `block_id` e `shift` (`M`, `T`, `N`).
