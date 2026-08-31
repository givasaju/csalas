# Regression Watch: Cadastro e Importação CSV de Docentes

> Identificador: `005-cadastro-docentes`  
> Data: `2026-08-07`  

---

## Watch List Principal

| ID | Origem | Regra esperada após mudança | Tipo de verificação | Sinal de violação |
|----|--------|-----------------------------|----------------------|-------------------|
| W001 | `src/api/routes.py` | Importação CSV de docentes deve rejeitar arquivos com matrículas duplicadas ou incompletas (status 422) | comportamento | Aceitação parcial de linhas ou erro 500 sem feedback |
| W002 | `src/api/routes.py` | Exclusão de docentes com restrições horárias ativas deve retornar 409 Conflict | presença | Exclusão em cascata acidental ou perda de vínculo de restrições |
