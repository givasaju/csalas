# Onboarding: Gestão de Relatórios de Ocupação e Carga Docente

> Identificador: `018-gestao-relatorios-ocupacao-docentes`
> Data: `2026-08-14`

## Passo a Passo para Validação Manual da Feature

### 1. Iniciar o Servidor
Verifique se o servidor uvicorn está ativo na porta 8000:
```bash
.\\.venv\\Scripts\\python.exe -m uvicorn src.main:app --host 127.0.0.1 --port 8000 --reload
```

### 2. Acessar a Nova Aba de Relatórios
1. Acesse `http://127.0.0.1:8000` no seu navegador.
2. Na barra de navegação principal no topo, clique no novo botão **`📊 Relatórios`**.

### 3. Testar a Ocupação de Ambientes (Coletivo)
1. Escolha um Bloco no seletor (ex: **Bloco A**).
2. Escolha o Turno (ex: **Manhã**).
3. Verifique se a tabela de ocupação atualiza exibindo as salas do Bloco A com as taxas de ocupação do turno matutino.

### 4. Testar a Carga Horária Docente (Individual)
1. No seletor de professores, escolha um docente da lista (ex: **Prof. Givaldo**).
2. Verifique se a tabela exibe as disciplinas, turmas, salas alocadas e horários lecionados pelo professor selecionado.

### 5. Testar as Exportações
1. Clique no botão **`📄 Exportar PDF`** ou **`📊 Exportar Excel`** e confirme o download do relatório.
