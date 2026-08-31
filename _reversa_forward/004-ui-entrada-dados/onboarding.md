# Onboarding: Testando a UI de Entrada de Dados

Passo a passo para validar a interface visual de entrada de dados:

1. **Certifique-se de que o servidor FastAPI está ativo:**
   ```bash
   .venv\Scripts\python.exe -m uvicorn src.main:app --reload --port 8000
   ```

2. **Acesse a aplicação no navegador:**
   - Navegue até `http://127.0.0.1:8000/`

3. **Validação do Cadastro de Sala:**
   - Clique na aba **Cadastrar Sala**.
   - Preencha os campos (Bloco, Nome, Capacidade, Tipo).
   - Clique em **Salvar Sala** e verifique o toast de confirmação e a inclusão da sala na tabela de inventário.

4. **Validação do Cadastro de Restrições:**
   - Clique na aba **Restrições Docentes**.
   - Selecione um professor no dropdown.
   - Clique nos slots desejados da matriz de horários para cadastrar a indisponibilidade.

5. **Validação da Importação CSV:**
   - Na aba **Importar CSV**, selecione ou arraste um arquivo `.csv` válido.
   - Verifique a mensagem de sucesso e a atualização das salas.
