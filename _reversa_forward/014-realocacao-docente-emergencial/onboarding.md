# Onboarding: Realocação Docente Emergencial

> Identificador: `014-realocacao-docente-emergencial`
> Data: `2026-08-13`
> Roadmap: `_reversa_forward/014-realocacao-docente-emergencial/roadmap.md`

---

## Passo a passo de teste manual da feature

Este guia descreve como um desenvolvedor ou testador pode executar e validar a funcionalidade de realocação docente emergencial pela primeira vez.

---

### Passo 1: Iniciar o Servidor FastAPI
Execute no terminal da raiz do projeto:

```bash
python -m uvicorn src.main:app --reload
```

---

### Passo 2: Verificar a API de Realocação Emergencial

#### 2.1 Calcular Opções de Realocação (`POST /api/v1/emergency-reallocations/calculate`)
Envie um payload HTTP `POST` para `/api/v1/emergency-reallocations/calculate`:

```json
{
  "absent_teacher_id": "T001",
  "start_date": "2026-09-01",
  "end_date": "2026-10-31",
  "mode": "assisted"
}
```

**Resultado esperado (HTTP 200):**
O sistema retorna até 3 opções de substituição com a lista de docentes da coordenação sugeridos e o `impact_score`.

---

#### 2.2 Efetivar Realocação em Modo Assistido (`POST /api/v1/emergency-reallocations/commit`)
Envie um payload HTTP `POST` confirmando a opção escolhida:

```json
{
  "absent_teacher_id": "T001",
  "selected_option_index": 1,
  "mode": "assisted",
  "substitutions": [
    {
      "class_id": "C001",
      "substitute_teacher_id": "T005",
      "substitute_teacher_name": "Prof. Carlos",
      "time_slot": "M1"
    }
  ]
}
```

**Resultado esperado (HTTP 200):**
Retorna `log_id` gerado, status `"success"` e atualiza a atribuição da turma na grade.

---

#### 2.3 Efetivar Realocação em Modo Delegado (`POST /api/v1/emergency-reallocations/commit`)
Envie um payload com `mode: "delegated"` para testar a aprovação automática pelo agente de IA.

---

### Passo 3: Testar na Interface SPA (`occupancy-dashboard`)
1. Abra o navegador em `http://localhost:8000/`.
2. Acesse o painel de ocupação e selecione a aba **Realocação Emergencial**.
3. Escolha o professor em licença no seletor.
4. Alterne o toggle entre **Modo Assistido** e **Modo Delegado**.
5. Clique em **Gerar Opções de Realocação** e confirme a efetivação na plataforma.
