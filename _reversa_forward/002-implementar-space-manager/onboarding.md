# Onboarding: academic-space-manager

Este guia descreve os passos práticos para testar, validar e carregar dados no gerenciador acadêmico do ClassSync AI.

---

## 1. Submeter Dados de Salas de Aula (CRUD)

1.  **Cadastrar uma sala:**
    Envie um POST com o cabeçalho de autenticação JWT simulado:
    ```bash
    curl -X POST http://localhost:8000/api/v1/rooms \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer mock-jwt-token" \
      -d '{
        "block_id": "Bloco A",
        "name": "Sala 101",
        "capacity": 45,
        "room_type": "common",
        "is_accessible": true,
        "features": ["projector"]
      }'
    ```

2.  **Testar validação de erro de capacidade:**
    Tente cadastrar uma sala com capacidade negativa:
    ```bash
    curl -X POST http://localhost:8000/api/v1/rooms \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer mock-jwt-token" \
      -d '{
        "block_id": "Bloco A",
        "name": "Sala Inválida",
        "capacity": -5,
        "room_type": "common",
        "is_accessible": true,
        "features": []
      }'
    ```
    Você deve receber a resposta HTTP `422 Unprocessable Entity` detalhando o erro.

---

## 2. Importação em Lote via CSV

1.  Prepare um arquivo CSV (`salas.csv`) com a seguinte estrutura de cabeçalho obrigatória:
    ```csv
    bloco,sala,capacidade,tipo,acessivel,recursos
    Bloco A,Sala A1,50,common,True,projector
    Bloco B,Laboratório B1,35,lab,False,computers;projector
    ```
2.  Envie o arquivo para a API:
    ```bash
    curl -X POST http://localhost:8000/api/v1/rooms/import-csv \
      -H "Authorization: Bearer mock-jwt-token" \
      -F "file=@salas.csv"
    ```

---

## 3. Consultar Payload Consolidado de Insumos da IA

Chame o endpoint do Space Manager para verificar se todas as salas, professores, disciplinas e indisponibilidades estão agregados corretamente:
```bash
curl http://localhost:8000/api/v1/allocation/input-data \
  -H "Authorization: Bearer mock-jwt-token"
```
Você deverá obter um payload JSON unificado estruturado para alimentar diretamente o motor de alocação de salas.
