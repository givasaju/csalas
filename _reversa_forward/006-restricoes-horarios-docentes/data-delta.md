# Delta do Modelo de Dados: Restrições Horárias Docentes

> Identificador: `006-restricoes-horarios-docentes`  
> Data: `2026-08-08`  

---

## 1. Resumo do Delta

Nenhum campo novo ou tabela adicional precisa ser criada na base de dados relacional. A entidade `Restriction` já se encontra totalmente estruturada em `src/models.py`.

---

## 2. Entidade Afetada: `Restriction`

- **Tabela:** `restrictions`
- **Campos existentes:**
  - `id`: `String(36)` (Chave primária, UUID)
  - `teacher_id`: `String(50)` (Chave estrangeira para `teachers.id`)
  - `day_of_week`: `Integer` (1 a 7)
  - `time_slot_id`: `String(10)` (`M1`, `M2`, `T1`, `T2`, `N1`, `N2`)

---

## 3. Alterações de Schema

Nenhuma alteração de schema DDL é necessária.

---

## 4. Estrutura de Dicionário em Memória (Engine Runtime)

No `core.py`, o modelo em memória para rápida validação utilizará a estrutura:

```python
teacher_restrictions = {
    ("prof-claudio", 1, "M1"): True,
    ("prof-isabela", 2, "T2"): True
}
```
