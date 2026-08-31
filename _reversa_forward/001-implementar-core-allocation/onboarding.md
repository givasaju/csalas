# Onboarding: core-allocation-engine

Este guia descreve os passos práticos para implantar, simular e validar o funcionamento da funcionalidade do motor de alocação de IA do ClassSync AI.

---

## 1. Configuração do Ambiente

1. Garanta que o Python 3.12+ esteja instalado no sistema.
2. Crie e ative um ambiente virtual:
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # Linux/macOS:
   source .venv/bin/activate
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

---

## 2. Preparação de Dados para Teste

Execute o script de semente (seed) para popular o banco de dados com dados iniciais consistentes:
```bash
python scripts/seed_mock_data.py
```
Esse script criará:
*   3 Blocos prediais (Bloco A, Bloco B, Bloco C).
*   15 salas de aula com diferentes capacidades, recursos e flags de acessibilidade.
*   5 Coordenações acadêmicas, cada uma inicializada com `1000` créditos.
*   45 disciplinas com grades de indisponibilidade de professores pré-definidas.

---

## 3. Fluxo de Execução do Teste

1.  **Iniciar a Fila Assíncrona:**
    Em um terminal separado, inicie o worker da fila:
    ```bash
    python scripts/run_worker.py
    ```

2.  **Disparar Alocação:**
    Envie um POST HTTP para iniciar o processamento:
    ```bash
    curl -X POST http://localhost:8000/api/v1/allocation/run
    ```
    Você deve receber uma resposta HTTP `202 Accepted` contendo o `task_id` da tarefa assíncrona.

3.  **Consultar o Status:**
    Consulte a API repetidamente até que o processamento seja concluído:
    ```bash
    curl http://localhost:8000/api/v1/allocation/status/<task_id>
    ```

4.  **Validar Resultados:**
    *   Verifique os logs do motor para conferir as disputas de salas resolvidas por leilão de créditos.
    *   Verifique se as disciplinas de Engenharia (que disputavam a sala acessível do Bloco A) venceram devido a maiores créditos ou se houve arbitragem.
    *   Confirme que o Bloco C (com baixa ocupação simulada) foi desativado e as turmas foram consolidadas nos Blocos A e B.
