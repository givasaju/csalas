# Monitor de Regressão Semântica (Regression Watch)

> Identificador: `013-tabela-subslots-intervalos`
> Data: `2026-08-11`

---

## 1. Watch Items

| ID | Origem (arquivo, seção) | Regra esperada após mudança | Tipo de verificação | Sinal de violação |
|----|-------------------------|-----------------------------|---------------------|-------------------|
| W001 | `_reversa_sdd/domain.md#210` | Restrições docentes de indisponibilidade continuam aceitando códigos `M1`..`N5` com validação de subslot existente | `presença` | Tentativa de cadastrar restrição com subslot válido falha com erro de código |
| W002 | `_reversa_forward/013-tabela-subslots-intervalos/requirements.md#RN-04` | Cada turno (matutino, vespertino, noturno) deve possuir 5 aulas de 50 min e 1 intervalo de 15 min entre aula 3 e 4 | `presença` | O seed ou consulta de subslots não retorna o intervalo de 15 min entre a 3ª e 4ª aula |

---

## 2. Histórico de Re-extrações

*Nenhuma re-extração executada após esta entrega.*

---

## 3. Arquivadas

*Nenhum item arquivado.*

---

## 4. Observações

- A verificação de regressão semântica será executada automaticamente quando o `/reversa` for acionado em futuras rodadas de re-extração.
