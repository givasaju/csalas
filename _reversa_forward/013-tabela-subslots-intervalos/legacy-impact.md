# Relatório de Impacto no Legado (Legacy Impact)

> Identificador: `013-tabela-subslots-intervalos`
> Data: `2026-08-11`
> Contexto: Legado (`_reversa_sdd/architecture.md`, `_reversa_sdd/domain.md`)

---

## 1. Mapeamento de Arquivos e Impacto

| Arquivo afetado | Componente | Tipo de impacto | Severidade | Justificativa |
|-----------------|------------|-----------------|------------|---------------|
| `src/api/schemas.py` | `academic-space-manager` | `regra-nova` | LOW | Adição de schemas Pydantic (`SubslotCreate`, `SubslotUpdate`, `SubslotResponse`) |
| `db/migrations.sql` | Modelo Relacional | `delta-de-dados` | MEDIUM | Adição de DDL da tabela `subslot_time_intervals` e seed de 18 horários oficiais |
| `src/models.py` | `academic-space-manager` | `regra-nova` | LOW | Modelo SQLAlchemy ORM `SubslotTimeInterval` |
| `src/database.py` | `academic-space-manager` | `delta-de-dados` | LOW | Execução automática de `seed_subslots()` na inicialização do SQLite |
| `src/api/routes.py` | `academic-space-manager` | `delta-de-contrato-externo` | MEDIUM | Endpoints REST `/api/v1/subslots` (CRUD) e validação dinâmica de indisponibilidade docente |
| `tests/test_subslot_time_intervals.py` | Suíte de Testes | `regra-nova` | LOW | Testes automatizados cobrindo carga inicial, filtros por turno, CRUD e autenticação |

---

## 2. Diff Conceitual por Componente

### Academic Space Manager
- O componente agora suporta formalmente o cadastro e a consulta relacional de subslots de 50 minutos e intervalos de 15 minutos entre a 3ª e 4ª aula dos turnos Matutino, Vespertino e Noturno.
- A validação de indisponibilidade docente (`create_restriction`) passou a consultar dinamicamente a tabela `subslot_time_intervals`, mantendo suporte aos códigos legados `M1`..`N5`.

---

## 3. Regras de Negócio Preservadas

- `_reversa_sdd/domain.md#210`: Cadastro de restrições docentes preservado e expandido para validar códigos vigentes na tabela de subslots.
- `_reversa_sdd/domain.md#27`: Importação transacional de salas intacta.
- `_reversa_sdd/domain.md#3.0`: Autenticação via token JWT Bearer intacta.

---

## 4. Regras de Negócio Modificadas

*Nenhuma regra de negócio existente no legado foi alterada ou removida. A feature apenas adiciona novos comportamentos e tabelas relacionais sem quebra de retrocompatibilidade.*
