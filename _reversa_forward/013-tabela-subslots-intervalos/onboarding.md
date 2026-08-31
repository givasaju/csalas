# Guia de Onboarding e Teste: Tabela de Subslots com Intervalos

> Identificador: `013-tabela-subslots-intervalos`
> Data: `2026-08-11`

Este documento orienta o passo a passo para um desenvolvedor ou testador validar a nova tabela de subslots de horários de aulas e intervalos.

---

## 1. Pré-requisitos

1. Ambiente de desenvolvimento configurado com Python 3.10+.
2. Banco de dados inicializado ou migrations executadas (script SQL em `db/migrations.sql`).

---

## 2. Passo a Passo de Validação

### Passo 1: Executar a suíte de testes unitários e de API
Execute o pytest para validar que os testes automatizados da nova rota passam com 100% de sucesso:

```bash
pytest tests/test_subslot_time_intervals.py -v
```

### Passo 2: Iniciar a aplicação localmente
Inicie a aplicação FastAPI:

```bash
python src/main.py
```

### Passo 3: Consultar os Subslots via GET API
Realize uma requisição HTTP GET para verificar a listagem de subslots:

```bash
curl -X GET "http://localhost:8000/api/v1/subslots?shift=matutino" \
     -H "Authorization: Bearer mock-token"
```

**Resultado Esperado:**
- Retorno de HTTP 200 OK.
- Lista contendo 5 aulas de 50 minutos e 1 intervalo das 09:30 às 09:45.

### Passo 4: Testar Operação de Criação (POST)
Envie uma requisição para criar um subslot personalizado (exemplo de subslot extra):

```bash
curl -X POST "http://localhost:8000/api/v1/subslots" \
     -H "Authorization: Bearer mock-token" \
     -H "Content-Type: application/json" \
     -d '{
       "code": "M6",
       "shift": "matutino",
       "class_number": 6,
       "start_time": "11:25",
       "end_time": "12:15",
       "is_interval": false
     }'
```

**Resultado Esperado:**
- Retorno de HTTP 201 Created.
