# Onboarding: Nova aba Gestão com IA no Navbar Principal

> Identificador: `016-gestao-com-ia-aba`
> Data: `2026-08-14`

## Passo a Passo para Validação Manual da Feature

### 1. Iniciar o Servidor
Verifique se o servidor uvicorn está ativo na porta 8000:
```bash
.\\.venv\\Scripts\\python.exe -m uvicorn src.main:app --host 127.0.0.1 --port 8000 --reload
```

### 2. Navegar até a aplicação
1. Acesse `http://127.0.0.1:8000` no seu navegador.
2. Na barra de navegação superior, verifique a presença da nova opção **`🤖 Gestão com IA`** disposta logo após **`👨‍🏫 Gestão de Docentes`**.

### 3. Testar a nova aba
1. Clique em **`🤖 Gestão com IA`**.
2. Verifique se o painel exibe:
   - Botão **`Disparar Alocação de IA`**.
   - Card **`Status da Tarefa de IA`**.
   - Card **`Auditoria e Extrato de Leilões de Créditos`**.
3. Clique em **Disparar Alocação de IA** e certifique-se de que a barra de progresso e a tabela de leilões funcionam e atualizam normalmente.
