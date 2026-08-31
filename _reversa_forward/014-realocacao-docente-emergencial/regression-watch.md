# Regression Watch: Realocação Docente Emergencial

> Identificador: `014-realocacao-docente-emergencial`
> Data: `2026-08-13`
> Feature: `_reversa_forward/014-realocacao-docente-emergencial/requirements.md`

---

## 1. Watch Items Principais

| ID | Origem (arquivo, seção) | Regra esperada após mudança | Tipo de verificação | Sinal de violação |
|----|-------------------------|-----------------------------|---------------------|-------------------|
| W001 | `_reversa_sdd/domain.md#Coordination` | Realocação emergencial busca prioritariamente docentes da mesma coordenação | presença | Atribuição de docentes de fora quando há docentes livres no mesmo departamento |
| W002 | `_reversa_sdd/code-analysis.md#1.3-fluxo-de-controle` | Respeitar rigorosamente `is_teacher_restricted` no cálculo de substitutos | presença | Atribuição de aula emergencial em slot restrito pelo professor |
| W003 | `_reversa_forward/014-realocacao-docente-emergencial/requirements.md#RN-03` | Suporte à escolha dinâmica entre Modo Assistido e Modo Delegado no painel | presença | Ausência de toggle de modo na interface ou falta de parâmetro `mode` no endpoint |
| W004 | `_reversa_forward/014-realocacao-docente-emergencial/requirements.md#RN-05` | Gravação do log de auditoria estruturado ao efetivar realocação emergencial | presença | Ausência de registro na tabela `emergency_reallocation_logs` |

---

## 2. Histórico de re-extrações

*(Inicialmente vazio; será preenchido pelo agente reverso em re-extrações futuras)*

---

## 3. Arquivadas

*(Inicialmente vazio)*

---

## 4. Observações

- RFs implementados validados com 100% de sucesso na suíte de testes automatizados `tests/test_emergency_reallocation.py` (61 testes passando).
