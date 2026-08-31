# Contrato de Interface: Gestão de Docentes com Disciplinas

> Identificador: `009-disciplinas-docentes`
> Contrato: HTTP REST (`/api/v1/teachers`)

---

## 1. `POST /api/v1/teachers` (Cadastro Unitário)

Adiciona um novo docente com sua lista obrigatoria de disciplinas lecionáveis.

### Cabeçalhos
- `Authorization: Bearer <token>`
- `Content-Type: application/json`

### Body (Request)
```json
{
  "id": "DOC-101",
  "name": "Prof. Carlos Eduardo",
  "department": "Engenharia",
  "subjects": ["Cálculo I", "Álgebra Linear"]
}
```

### Resposta de Sucesso (201 Created)
```json
{
  "id": "DOC-101",
  "name": "Prof. Carlos Eduardo",
  "department": "Engenharia",
  "subjects": ["Cálculo I", "Álgebra Linear"]
}
```

### Erros Possíveis
- `400 Bad Request` / `422 Unprocessable Entity`: Lista `subjects` ausente ou vazia (`[]`).
- `409 Conflict`: Matrícula/ID de docente já cadastrado.

---

## 2. `POST /api/v1/teachers/import-csv` (Importação em Lote)

Importa docentes via arquivo CSV com validação atômica tudo-ou-nada.

### Cabeçalhos
- `Authorization: Bearer <token>`
- `Content-Type: multipart/form-data`

### Form-Data
- `file`: Arquivo `.csv` com o cabeçalho `id,name,department,disciplines` (ou `disciplinas` / `subjects`).

### Formato do Conteúdo CSV
```csv
id,name,department,disciplines
DOC-102,Profa. Ana Paula,Ciências,Física I;Física II
DOC-103,Prof. Bruno,Administração,Gestão Financeira;Marketing
```

### Resposta de Sucesso (200 OK)
```json
{
  "status": "success",
  "imported_count": 2,
  "message": "2 docentes importados com sucesso."
}
```

### Erros Possíveis
- `400 Bad Request`: Falha de validação em qualquer linha (ex.: docente sem disciplina, cabeçalho incorreto). Operação completamente revertida.

---

## 3. `GET /api/v1/teachers` (Listagem de Docentes)

Retorna a lista completa de docentes incluindo o atributo `subjects`.

### Resposta (200 OK)
```json
[
  {
    "id": "DOC-101",
    "name": "Prof. Carlos Eduardo",
    "department": "Engenharia",
    "subjects": ["Cálculo I", "Álgebra Linear"]
  }
]
```
