# Onboarding: Cadastro de Disciplinas Lecionáveis por Docente

> Identificador: `009-disciplinas-docentes`
> Data: `2026-08-09`

---

## Passo a Passo Executável para Testar a Feature

### Pré-requisitos

1. Python 3.10+ e ambiente configurado.
2. Servidor backend rodando ou suíte de testes com `pytest`.

---

### 1. Testar Cadastro Unitário com Disciplinas via HTTP REST

Execute o comando HTTP cURL para cadastrar um docente com disciplinas:

```bash
curl -X POST http://localhost:8000/api/v1/teachers \
  -H "Authorization: Bearer mock-token" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "DOC-201",
    "name": "Prof. Roberto Mendes",
    "department": "Engenharia",
    "subjects": ["Cálculo I", "Álgebra Linear"]
  }'
```

**Resultado Esperado:** HTTP 201 Created com o JSON contendo `"subjects": ["Cálculo I", "Álgebra Linear"]`.

---

### 2. Testar Rejeição de Docente sem Disciplinas

Execute o cadastro sem disciplinas:

```bash
curl -X POST http://localhost:8000/api/v1/teachers \
  -H "Authorization: Bearer mock-token" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "DOC-202",
    "name": "Prof. Sem Disciplina",
    "department": "Engenharia",
    "subjects": []
  }'
```

**Resultado Esperado:** HTTP 422 Unprocessable Entity (ou 400 Bad Request) com mensagem indicando que `subjects` deve possuir pelo menos 1 item.

---

### 3. Testar Importação em Lote via Arquivo CSV

Crie um arquivo temporário `docentes_disciplinas.csv`:

```csv
id,name,department,disciplines
DOC-301,Profa. Helena,Ciências,Física I;Física II
DOC-302,Prof. Fernando,Humanas,Filosofia;Sociologia
```

Envie o arquivo via endpoint de importação:

```bash
curl -X POST http://localhost:8000/api/v1/teachers/import-csv \
  -H "Authorization: Bearer mock-token" \
  -F "file=@docentes_disciplinas.csv"
```

**Resultado Esperado:** HTTP 200 OK informando a importação de 2 docentes com suas respectivas disciplinas.

---

### 4. Validar Interface Web SPA

1. Abra `src/api/static/index.html` no navegador.
2. Navegue até a aba **"👨‍🏫 Gestão de Docentes"**.
3. Verifique se o formulário contém o campo de inserção de disciplinas.
4. Cadastre um docente e certifique-se de que as disciplinas aparecem como tags na tabela.
