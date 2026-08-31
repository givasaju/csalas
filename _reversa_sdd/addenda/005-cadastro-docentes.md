# Adendo: Cadastro e Importação CSV de Docentes

> Identificador: `005-cadastro-docentes`  
> Data: `2026-08-07`  
> Cenário: Legado  

---

## Vigência

Vigente desde 2026-08-07.
Superado pela re-extração de 2026-08-09.

---

## Resumo da entrega

Esta feature entregou a funcionalidade completa de Gestão de Docentes no ClassSync AI. Foram implementadas as rotas `POST /api/v1/teachers` (cadastro unitário por matrícula, nome e departamento), `POST /api/v1/teachers/import-csv` (importação em lote via CSV com validação atômica tudo-ou-nada) e `DELETE /api/v1/teachers/{id}` (exclusão tratada com status 409 Conflict se houver vínculo de restrições horárias). A SPA em HTML/CSS/JS foi enriquecida com a nova aba "👨‍🏫 Gestão de Docentes", com formulários reativos, upload por Drag & Drop e tabela de docentes sincronizada.

---

## Impacto por artefato da extração

| Artefato | Seção | Tipo de impacto | Delta |
|----------|-------|-----------------|-------|
| `_reversa_sdd/architecture.md` | `# Componentes` | `regra-nova` | A API REST foi expandida com endpoints para professores e o frontend adicionou suporte à gestão de cadastro docente. |
| `_reversa_sdd/domain.md` | `# Regras de Negócio` | `regra-nova` | Validação atômica de matrículas docentes e regra de tudo-ou-nada na importação CSV. |

---

## Regras sob vigilância

Os watch items de regressão criados nesta feature estão registrados no seguinte arquivo:
* [regression-watch.md](file:///c:/csalas/_reversa_forward/005-cadastro-docentes/regression-watch.md) (Watch IDs: `W001`, `W002`)

---

## Fontes

- `_reversa_forward/005-cadastro-docentes/requirements.md`
- `_reversa_forward/005-cadastro-docentes/actions.md`
- `_reversa_forward/005-cadastro-docentes/legacy-impact.md`
- `_reversa_forward/005-cadastro-docentes/regression-watch.md`
