# Guia de Onboarding e Validação: Alocações e Limite de 4 Aulas Consecutivas

> Identificador da feature: `008-alocacao-docente-max-4-aulas`  
> Data: `2026-08-08`  

---

## 1. Objetivo

Validação manual das regras de agendamento de aulas de 50 minutos e da trava rígida que rejeita a 5ª aula consecutiva para o mesmo docente no mesmo turno.

---

## 2. Passos para Validação via cURL / HTTPie

### Passo 1: Agendar 4 aulas consecutivas (Sucesso)
Cadastrar sub-slots 1, 2, 3 e 4 para o professor `"prof-alan"` no turno `M` na segunda-feira (`day_of_week=1`):

```bash
for slot in 1 2 3 4; do
  curl -X POST "http://127.0.0.1:8000/api/v1/allocations" \
    -H "Authorization: Bearer mock-token" \
    -H "Content-Type: application/json" \
    -d "{\"teacher_id\": \"prof-alan\", \"room_id\": \"sala-101\", \"day_of_week\": 1, \"shift\": \"M\", \"sub_slot\": $slot}"
done
```
- **Resultado Esperado**: Retorna HTTP `201 Created` para os 4 agendamentos.

### Passo 2: Tentar agendar a 5ª aula consecutiva (Rejeição)
Tentar agendar o sub-slot 5 no mesmo turno `M`:

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/allocations" \
  -H "Authorization: Bearer mock-token" \
  -H "Content-Type: application/json" \
  -d "{\"teacher_id\": \"prof-alan\", \"room_id\": \"sala-102\", \"day_of_week\": 1, \"shift\": \"M\", \"sub_slot\": 5}"
```
- **Resultado Esperado**: Retorna HTTP `409 Conflict` com a mensagem `"Limite máximo de 4 aulas seguidas no mesmo turno atingido para o docente."`.

---

## 3. Validação via Interface Web (SPA)

1. Acesse o dashboard no endereço `http://127.0.0.1:8000/`.
2. Clique na aba **"📅 Alocação de Aulas"**.
3. Selecione um professor e uma sala.
4. Tente marcar 5 checkboxes consecutivas de aulas no turno da Manhã.
5. Verifique que a 5ª checkbox exibe um aviso de bloqueio e desabilita o envio do formulário.
