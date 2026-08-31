# Onboarding: Reduzir 50% do tamanho das fontes na seção Auditoria e Extrato

> Identificador: `015-reduzir-fonte-auditoria-extrato`
> Data: `2026-08-14`

## Passo a Passo para Validação Manual da Feature

### 1. Iniciar o Servidor
Certifique-se de que o servidor FastAPI está ativo na porta 8000:
```bash
.\\.venv\\Scripts\\python.exe -m uvicorn src.main:app --host 127.0.0.1 --port 8000 --reload
```

### 2. Acessar a Interface do Dashboard
1. Abra o navegador em `http://127.0.0.1:8000`.
2. Certifique-se de estar na aba **📊 Dashboard & KPIs**.

### 3. Verificar a Tabela de Auditoria e Extrato
1. Observe a seção **"Auditoria e Extrato de Leilões de Créditos"**.
2. Verifique se o título e o cabeçalho (`Sala`, `Slot`, `Vencedor`, `Perdedor`, `Lances Pago`) permanecem em tamanho padrão legível.
3. Dispare uma rodada de alocação de IA se necessário ou inspecione as linhas existentes.
4. Confirme que as linhas de dados exibem tipografia compacta de `0.44rem` (~50% do tamanho base).
5. Confirme que as cores dos textos de vencedores (Verde 👑), perdedores (Vermelho 🛡️) e lances (Índigo ⚡) estão preservadas.
