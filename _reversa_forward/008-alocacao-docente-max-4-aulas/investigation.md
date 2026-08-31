# Pesquisa Técnica e Investigação: Entrada de Alocações e Limite de 4 Aulas Consecutivas

> Identificador da feature: `008-alocacao-docente-max-4-aulas`  
> Data: `2026-08-08`  

---

## 1. Contexto e Motivação

A legislação de trabalho acadêmico e as normas pedagógicas impõem limites à quantidade continuada de exposições de professores em sala de aula sem intervalo de descanso. A feature 008 insere a funcionalidade de agendamento de aulas de 50 minutos e formaliza a trava rígida (*Hard Constraint*) que impede o agendamento de mais de 4 aulas de 50 minutos consecutivas para um mesmo professor dentro do mesmo turno (`M`, `T`, `N`).

---

## 2. Algoritmo de Validação de Aulas Consecutivas

### Estrutura dos Dados
Para cada professor, dia e turno (`teacher_id`, `day_of_week`, `shift`), o sistema recupera a lista de sub-slots alocados (ex: `sub_slots = [1, 2, 3]`).

### Lógica da Janela Deslizante
Ao tentar inserir um novo sub-slot `S`:
1. Une-se o conjunto atual com `{S}` e ordena-se a lista resultante.
2. Percorre-se a lista contando a maior sequência de inteiros consecutivos ($x_{i+1} = x_i + 1$).
3. Se a maior sequência consecutiva for $> 4$, a operação é abortada com exceção `HTTP 409 Conflict`.

```python
def check_consecutive_limit(existing_sub_slots: list[int], new_sub_slot: int) -> bool:
    all_slots = sorted(set(existing_sub_slots + [new_sub_slot]))
    max_consecutive = 1
    current = 1
    for i in range(1, len(all_slots)):
        if all_slots[i] == all_slots[i - 1] + 1:
            current += 1
            if current > max_consecutive:
                max_consecutive = current
        else:
            current = 1
    return max_consecutive <= 4
```

---

## 3. Padrões de Interface no Dashboard SPA

No frontend (`index.html`), o formulário de cadastro de aulas apresentará seletores para:
- Professor (`teacher_id`)
- Sala física (`room_id`)
- Dia da semana (1 - Segunda a 7 - Domingo)
- Turno (`Manhã`, `Tarde`, `Noite`)
- Sub-slots (checkboxes para aulas 1, 2, 3, 4, 5 de 50 minutos)

Caso o usuário marque 5 checkboxes seguidas, o próprio JavaScript exibirá um alerta instantâneo e desabilitará o botão de confirmação.
