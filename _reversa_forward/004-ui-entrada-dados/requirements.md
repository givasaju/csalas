# Requirements: UI Moderna de Entrada de Dados do ClassSync AI

> Identificador: `004-ui-entrada-dados`
> Data: `2026-08-07`
> Pasta da extração reversa: `_reversa_sdd/`
> Confidência: 🟢 CONFIRMADO, 🟡 INFERIDO, 🔴 LACUNA / DÚVIDA

## 1. Resumo executivo

Esta feature entrega uma interface visual web (UI) moderna, elegante e responsiva para cadastro e gestão dos dados de entrada do sistema ClassSync AI. A UI permitirá que gestores e coordenadores acadêmicos realizem o cadastro individual de salas físicas, a importação em lote via arquivo CSV com validação transacional "Tudo ou Nada", o cadastro de restrições/indisponibilidades de professores por dia e horário, o reset semestral de restrições e a visualização dinâmica do inventário completo do campus.

## 2. Contexto a partir do legado

| Fonte | Trecho relevante | Confidência |
|-------|------------------|-------------|
| `_reversa_sdd/architecture.md#gerenciador-espacos` | Módulo `gerenciador-espacos` responsável por expor endpoints REST de salas e restrições horárias | 🟢 |
| `_reversa_sdd/domain.md#RN-02` | Unicidade de sala por bloco e validação de capacidade mínima `capacity > 0` | 🟢 |
| `_reversa_sdd/domain.md#RN-04` | Importação em lote CSV transacional (Política Tudo ou Nada) | 🟢 |
| `_reversa_sdd/domain.md#RN-05` | Cadastro de indisponibilidade docente por slot de tempo (`M1` a `N2`) e dia da semana (1-7) | 🟢 |
| `_reversa_sdd/gerenciador-espacos/requirements.md#RF-05` | Trava de segurança no `DELETE /rooms/{room_id}` bloqueando exclusão se houver alocação de IA em andamento | 🟢 |

## 3. Personas e cenários de uso

| Persona | Objetivo | Cenário-chave |
|---------|----------|---------------|
| Coordenador Acadêmico | Cadastrar salas de aula físicas e importar dados do campus em lote via CSV | Acessar o formulário intuitivo ou a área de drag-and-drop CSV para popular o inventário do campus antes do início do semestre |
| Gestor de Infraestrutura | Configurar restrições e indisponibilidades de professores | Selecionar o docente, dia da semana e o slot (M1-N2) para registrar horários em que o professor não pode lecionar |
| Administrador do Sistema | Executar o reset semestral de restrições ou remover salas obsoletas | Disparar o acionamento do reset semestral ou tentar excluir uma sala com confirmação modal e verificação de trava de IA |

## 4. Regras de negócio novas ou alteradas

1. **RN-01:** **Autenticação Transparente via Interface:** A UI deve armazenar o token JWT de autorização (padrão `Bearer`) e incluí-lo automaticamente em todos os cabeçalhos de requisição aos endpoints `/api/v1/*`. 🟢
   - Origem no legado: `_reversa_sdd/domain.md#RN-01`
   - Tipo: nova
2. **RN-02:** **Validação Client-side Pré-envio de Salas:** O formulário de cadastro individual de salas deve aplicar feedback imediato na UI (capacidade > 0, nome obrigatorio, bloco predial selecionado e tipo entre `common`, `lab`, `auditorium`). 🟢
   - Origem no legado: `_reversa_sdd/domain.md#RN-03`
   - Tipo: nova
3. **RN-03:** **Preview e Validação Drag-and-Drop de CSV:** A área de upload CSV deve aceitar arrastar-e-soltar arquivos, exibir um preview dos registros e indicar erros de validação antes do disparo final da transação Tudo ou Nada ao backend. 🟢
   - Origem no legado: `_reversa_sdd/domain.md#RN-04`
   - Tipo: nova
4. **RN-04:** **Matriz Visual Interativa de Indisponibilidade Docente:** A seleção de horários de professores deve ser apresentada em formato de grade/matriz (Dias da semana x Slots M1..N2), permitindo marcar/desmarcar indisponibilidades com cliques visuais. 🟢
   - Origem no legado: `_reversa_sdd/domain.md#RN-05`
   - Tipo: nova
5. **RN-05:** **Tratamento de Conflito RNF-02 na Exclusão de Salas:** Caso o backend retorne status `409 Conflict` na tentativa de exclusão de sala (devido ao motor de IA rodando), a UI deve exibir um Toast de Alerta claro ao usuário impedindo a ação desastrosa. 🟢
   - Origem no legado: `_reversa_sdd/gerenciador-espacos/requirements.md#RN-06`
   - Tipo: nova

## 5. Requisitos Funcionais

| ID | Requisito | Prioridade | Critério de aceite | Confidência |
|----|-----------|------------|--------------------|-------------|
| RF-01 | Modal/Painel de Formulário para Cadastro Individual de Sala Física | Must | Formulário interativo com validações em tempo real enviando POST para `/api/v1/rooms`. | 🟢 |
| RF-02 | Área de Importação de Salas via CSV com Drag & Drop | Must | Componente visual de upload de arquivo `.csv`, com suporte a drag-and-drop, preview de linhas e feedback claro da resposta da transação. | 🟢 |
| RF-03 | Matriz Visual de Cadastro de Restrições Horárias Docentes | Must | Interface em grade permitindo selecionar um professor e clicar nos slots (M1, M2, T1, T2, N1, N2) por dia (1-7) enviando POST para `/api/v1/allocation/restrictions`. | 🟢 |
| RF-04 | Botão de Reset Semestral de Restrições com Confirmação em Modal | Should | Acionador com modal de confirmação de segurança executando DELETE em `/api/v1/allocation/restrictions` e atualizando a lista na tela. | 🟢 |
| RF-05 | Tabela Responsiva de Inventário de Salas com Ação de Exclusão | Must | Tabela com busca/filtro exibindo nome, bloco, capacidade, tipo, recursos e botão de exclusão que chama `DELETE /api/v1/rooms/{id}`. | 🟢 |
| RF-06 | Seletor de Tema Dark Glassmorphism e Design System Consistente | Should | Layout estilizado com CSS Vanilla, suporte a tema escuro moderno, efeitos de glassmorphism, gradientes e micro-animações. | 🟢 |

## 6. Requisitos Não Funcionais

| Tipo | Requisito | Evidência ou justificativa | Confidência |
|------|-----------|----------------------------|-------------|
| Usabilidade | Interface fluida e responsiva (Mobile e Desktop) utilizando CSS Vanilla sem bibliotecas externas pesadas | Alinhado aos padrões estéticos de UI moderna do ClassSync AI | 🟢 |
| Desempenho | Carregamento assíncrono instantâneo via `fetch` API com estados de carregamento (Skeleton loaders e spinners) | Melhora a experiência do usuário durante requisições de rede | 🟢 |
| Segurança | Manipulação de tokens JWT no cabeçalho `Authorization` sem expor credenciais na URL | `src/api/routes.py:27-37` | 🟢 |

## 7. Critérios de Aceitação

```gherkin
Cenário: Cadastro com sucesso de uma nova sala física pela UI
  Dado que o usuário está no painel de Entrada de Dados
  Quando preenche o bloco "Bloco B", nome "Sala B102", capacidade "40", tipo "lab", seleciona "Acessível" e clica em "Salvar Sala"
  Então a UI dispara uma requisição POST para /api/v1/rooms com os dados formatados
  E ao receber resposta 201 Created, exibe um Toast de sucesso e atualiza a tabela de salas na tela sem recarregar a página.

Cenário: Tentativa de importação de CSV com erro de validação (Tudo ou Nada)
  Dado que o usuário seleciona ou arrasta um arquivo CSV contendo uma linha com capacidade negativa
  Quando confirma o envio para a importação em lote
  Então a UI recebe o status 422 da API
  E exibe uma mensagem de erro em destaque informando que a operação foi revertida e nenhuma sala foi cadastrada.

Cenário: Exclusão de sala física bloqueada por alocação de IA ativa
  Dado que há uma execução do motor de IA em andamento no backend
  Quando o usuário clica no ícone de lixeira para excluir a "Sala B102"
  Então a UI recebe o status 409 Conflict da API e apresenta um modal/alert vermelho informando que salas não podem ser excluídas durante a alocação de IA.
```

## 8. Prioridade MoSCoW

| Item | MoSCoW | Justificativa |
|------|--------|---------------|
| RF-01 (Cadastro Individual de Sala) | Must | Funcionalidade básica essencial para gerenciamento do espaço acadêmico. |
| RF-02 (Importação CSV Transacional) | Must | Carga em massa necessária para operações de início de semestre. |
| RF-03 (Matriz de Restrição Docente) | Must | Permite configurar as indisponibilidades indispensáveis para o algoritmo da IA. |
| RF-05 (Tabela de Inventário com Exclusão) | Must | Exibição visual e manutenção das salas cadastradas. |
| RF-04 (Reset Semestral) | Should | Limpeza facilitada de restrições ao mudar de período letivo. |
| RF-06 (Design System Glassmorphism) | Should | Eleva a qualidade estética e percepção de produto do sistema. |

## 9. Esclarecimentos

> Nenhuma sessão de dúvidas registrada ainda. Rode `/reversa-clarify` quando houver `[DÚVIDA]` pendente.

## 10. Lacunas

Nenhuma lacuna crítica pendente. Todos os requisitos foram derivados das rotas existentes na API backend e nas regras de negócio mapeadas no `_reversa_sdd/`.

## 11. Histórico de alterações

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-08-07 | Versão inicial gerada por `/reversa-requirements` | reversa |
