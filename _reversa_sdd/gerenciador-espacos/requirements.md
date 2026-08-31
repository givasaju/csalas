# Unit: gerenciador-espacos (Gerenciador de Espaços Acadêmicos)

> Especificação de requisitos para a unidade de persistência e exposição da API REST das entidades acadêmicas e de espaços físicos.

## Visão Geral
Este componente fornece a interface de comunicação HTTP REST e gerencia o inventário de salas físicas do campus, professores, turmas e o cadastro de restrições/indisponibilidades de horários de docentes. Ele serve como a camada de dados que alimenta o motor inteligente de alocação de IA.

## Responsabilidades
- Cadastrar e remover salas de aula físicas de forma isolada.
- Processar a importação em lote de salas por arquivos CSV de forma transacional (Tudo ou Nada).
- Cadastrar e resetar semestralmente as indisponibilidades docentes (dias/horários restritos).
- Expor os dados agregados do campus para a leitura do motor de IA.
- Garantir a integridade da alocação de IA, bloqueando a remoção de salas físicas durante a execução do motor.

## Regras de Negócio

*   **RN-01: Autenticação JWT Mockada**: Requisições para endpoints protegidos devem conter o cabeçalho `Authorization` do tipo `Bearer`. O token é rejeitado como `401 Unauthorized` se estiver ausente, se não possuir o prefixo `"Bearer "`, ou se for exatamente igual a `"invalid-token"`. Qualquer outro token é validado com sucesso. 🟢 (Evidência: `src/api/routes.py:16-26`)
*   **RN-02: Restrição de Sala Duplicada**: Não é permitido criar mais de uma sala física com o mesmo nome (`name`) dentro do mesmo bloco predial (`block_id`). Violações retornam `409 Conflict`. 🟢 (Evidência: `src/api/routes.py:37-40`)
*   **RN-03: Capacidade Mínima de Sala**: A capacidade física de alunos cadastrada para qualquer sala deve ser um inteiro estritamente maior que zero (`capacity > 0`). 🟢 (Evidência: `src/api/schemas.py:7`)
*   **RN-04: Transação Tudo ou Nada de CSV**: O endpoint de importação de CSV de salas de aula físicas deve validar a integridade de todas as linhas do arquivo. Se qualquer linha violar tipos, possuir cabeçalho incorreto, valores vazios ou capacidades inválidas, toda a operação deve ser revertida de forma transacional e nenhum registro do CSV deve ser adicionado ao inventário. 🟢 (Evidência: `src/api/routes.py:85-125`)
*   **RN-05: Validação de Restrição Docente**: O cadastro de indisponibilidade exige que o professor informado exista no banco de dados. O dia da semana deve ser de 1 (Segunda) a 7 (Domingo). O slot de tempo deve pertencer à lista de períodos acadêmicos (`M1`, `M2`, `T1`, `T2`, `N1`, `N2`). Indisponibilidades idênticas duplicadas para o mesmo docente são rejeitadas com `409 Conflict`. 🟢 (Evidência: `src/api/routes.py:147-164`)
*   **RN-06: Bloqueio RNF-02 de Exclusão de Sala**: É proibido remover qualquer sala física do inventário se houver alguma rodada de alocação de IA ativa (com status `"queued"` ou `"running"`) em execução em background pelo worker. Violações retornam `409 Conflict`. 🟢 (Evidência: `src/api/routes.py:224-231`)
*   **RN-07: Limite de Concorrência de Tarefas**: O worker de tarefas em background de alocação de IA é limitado a rodar no máximo 2 threads concorrentes simultaneamente. 🟢 (Evidência: `src/api/worker.py:36`)

---

## Requisitos Funcionais

| ID | Requisito | Prioridade | Critério de Aceite |
|----|-----------|-----------|-------------------|
| RF-01 | Cadastro individual de sala física. | Must | Validar que novas salas são inseridas sob validação de capacidade e unicidade por bloco predial. |
| RF-02 | Importação em lote transacional de salas via CSV. | Must | Validar que um arquivo CSV correto é importado e que qualquer arquivo com linhas inválidas é sumariamente rejeitado sem persistência. |
| RF-03 | Cadastro de indisponibilidade docente. | Must | Validar que professores existentes recebem restrições horárias respeitando dias (1-7) e slots permitidos (M1-N2). |
| RF-04 | Reset semestral de indisponibilidades docentes. | Should | Validar que todas as indisponibilidades ativas de docentes são limpas em lote no inventário. |
| RF-05 | Exclusão de sala física com trava de segurança. | Must | Validar que salas físicas são removidas com sucesso se não houver tarefas assíncronas ativas, e bloqueadas em caso de motor rodando. |

---

## Requisitos Não Funcionais

| Tipo | Requisito inferido | Evidência no código | Confiança |
|------|--------------------|---------------------|-----------|
| Segurança | Autenticação obrigatória por Header JWT em rotas de alteração de dados do campus. | `src/api/routes.py:16` | 🟢 |
| Integridade | Consistência e não-interrupção do motor de IA durante modificações de infraestrutura (RNF-02). | `src/api/routes.py:224-227` | 🟢 |
| Escalabilidade | Execução assíncrona desacoplada em pool de threads limitado para processar o motor de IA pesado. | `src/api/worker.py:36` | 🟢 |

---

## Critérios de Aceitação

```gherkin
Dado que o usuário está autenticado com token JWT válido
Quando tenta cadastrar uma sala chamada "Sala A1" no bloco "Bloco A" que já possui uma sala cadastrada com esse mesmo nome
Então o sistema deve rejeitar o cadastro com o status 409 Conflict.

Dado que o usuário envia um arquivo CSV contendo 10 salas válidas e 1 sala com capacidade igual a "-5" (linha 8)
Quando o sistema processa o endpoint de importação em lote CSV
Então o sistema deve rejeitar a requisição inteira com 422 Unprocessable Entity e nenhuma das 11 salas deve ser cadastrada no inventário.

Dado que há uma tarefa de alocação de IA executando em background com status "running"
Quando o usuário tenta excluir a sala física "sala-a1" pelo endpoint DELETE /rooms/sala-a1
Então o sistema deve bloquear a operação e responder com status 409 Conflict informando que há rodadas de alocação em andamento.
```

---

## Prioridade (MoSCoW)

| Requisito | MoSCoW | Justificativa |
|-----------|--------|---------------|
| Cadastro de Salas e API REST | Must | Necessário para popular o inventário do campus sem o qual o motor de IA não pode ler os dados. |
| Trava de Exclusão (RNF-02) | Must | Evita erros de referência nula ou travamentos internos catastróficos no motor de alocação de IA em execução. |
| Importação CSV Transacional | Must | Facilita a carga em massa de salas de aula no início de períodos letivos de forma segura. |
| Reset de Indisponibilidades | Should | Prático para transição de semestres letivos, embora possa ser realizado por remoções unitárias manuais. |

---

## Rastreabilidade de Código

| Arquivo | Função / Classe | Cobertura |
|---------|-----------------|-----------|
| [`src/api/routes.py`](file:///c:/csalas/src/api/routes.py) | `create_room`, `import_rooms_csv`, `create_restriction`, `delete_room`, `get_input_data` | 🟢 |
| [`src/api/schemas.py`](file:///c:/csalas/src/api/schemas.py) | `RoomCreate`, `RestrictionCreate` | 🟢 |
| [`src/api/worker.py`](file:///c:/csalas/src/api/worker.py) | `db_rooms`, `db_teachers`, `db_restrictions`, `db_coordinations` (banco simulado) | 🟢 |
