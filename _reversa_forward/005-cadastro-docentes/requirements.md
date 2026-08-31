# Requirements: Cadastro e Importação CSV de Docentes

> Identificador: `005-cadastro-docentes`  
> Data: `2026-08-07`

---

## Objetivo

Implementar a gestão completa de docentes (professores) no ClassSync AI, disponibilizando cadastro unitário, importação atômica em lote via arquivo CSV (com campos de Matrícula/ID, Nome e Departamento), exclusão de cadastro com validação de vínculo e nova aba reativa na interface web.

---

## Requisitos Funcionais (RF)

- **RF-01 (Cadastro Unitário):** A API e a UI devem permitir cadastrar novos docentes informando `id` (matrícula), `name` (nome completo) e `department` (departamento ou área). *Departamento deve ser um dos valores: “Administração”, “Engenharia”, “Ciências”, “Humanas”.*

- **RF-02 (Importação CSV em Lote):** O sistema deve aceitar upload de arquivos CSV no formato `matricula, nome, departamento` com política *Tudo ou Nada* (rejeição status 422 em caso de linhas inválidas ou matrículas duplicadas já existentes no BD). *A única validação adicional requerida é impedir duplicação de matrícula existente no banco.*

- **RF-03 (Exclusão com Validação):** A API deve permitir remover docentes do cadastro (`DELETE /api/v1/teachers/{id}`) **sem restrições** (exclusão sempre permitida).

- **RF-04 (Interface de Gestão):** A SPA deve apresentar a aba **👨‍🏫 Gestão de Docentes**, com formulários de cadastro, área de Drag & Drop para CSV e tabela dinâmica de docentes sincronizada com o formulário de restrições horárias. Ao concluir operação (cadastro, exclusão ou importação) a interface deve exibir um *toast de confirmação* e manter a aba aberta.

- **RF-05 (Controle de Acesso):** Apenas usuários com perfil *admin* podem executar as rotas de criação, importação e exclusão de docentes. As rotas devem requerer autenticação JWT e validar a role `admin`.

## Esclarecimentos

### Sessão 2026-08-07

- **Q:** Qual conjunto de valores é aceito para o campo `department`?
  **R:** “Administração”, “Engenharia”, “Ciências”, “Humanas”.

- **Q:** Quais regras de validação devem ser aplicadas a cada linha do CSV?
  **R:** Impedir duplicação de `matricula` já existente no banco de dados.

- **Q:** Quais tipos de restrição horária impedem a exclusão de um docente?
  **R:** Nenhuma restrição; a exclusão é sempre permitida.

- **Q:** Como a aba “Gestão de Docentes” deve reagir a alterações?
  **R:** Exibir um toast de confirmação e manter a aba aberta.

- **Q:** Existe requisito de autenticação para as rotas de docentes?
  **R:** Sim, apenas usuários admin podem criar, importar ou excluir docentes.

## Lacunas

*Ainda não há dúvidas pendentes.*
