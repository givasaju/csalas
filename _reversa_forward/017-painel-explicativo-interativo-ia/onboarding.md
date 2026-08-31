# Onboarding: Painel Explicativo Interativo e Flutuante na Gestão com IA

> Identificador: `017-painel-explicativo-interativo-ia`
> Data: `2026-08-14`

## Passo a Passo para Validação Manual da Feature

### 1. Iniciar o Servidor
Verifique se o servidor uvicorn está ativo na porta 8000:
```bash
.\\.venv\\Scripts\\python.exe -m uvicorn src.main:app --host 127.0.0.1 --port 8000 --reload
```

### 2. Acessar a Aba Gestão com IA
1. Acesse `http://127.0.0.1:8000` no seu navegador.
2. Clique na aba **`🤖 Gestão com IA`**.

### 3. Testar a Caixa Explicativa Interativa
1. **Visualização Inicial**: Observe a caixa explicativa flutuante moderna com orientações de "Quando Usar" e "Quando Não Usar" a IA.
2. **Arrastar & Soltar**: Clique e segure no cabeçalho do painel e arraste-o para qualquer canto da tela.
3. **Controle de Fonte**: Clique no botão `A+` para aumentar o texto explicativo e `A-` para diminuir.
4. **Fechar & Reabrir**: Clique no botão `✖` no canto superior do painel para fechá-lo. Clique em `💡 Guia da IA` para exibi-lo novamente.
