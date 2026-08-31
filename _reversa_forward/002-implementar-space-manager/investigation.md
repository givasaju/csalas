# Investigation: academic-space-manager

## 1. Pesquisa de fundo

O processamento e persistência de dados prediais e restrições horárias exigem rapidez de carregamento e integridade nas relações de dados. Investigamos bibliotecas eficientes para manipulação e validação de requisições HTTP:

*   **Pydantic V2:** Fornece um mecanismo de validação de dados extremamente rápido em Rust nativo, permitindo impor restrições (ex: `conint(gt=0)` para capacidades maiores do que zero) de forma declarativa e com geração automática de mensagens de erro claras de validação no corpo da resposta HTTP.
*   **Modulo Python `csv`:** Permite processar streams de texto com suporte nativo a delimitadores configuráveis.

---

## 2. Alternativas avaliadas

### Alternativa A: Integração direta em lote incremental
*   *Descrição:* Ler cada linha do CSV de salas e ir inserindo no banco uma a uma. Se houver erro no meio, as linhas anteriores continuam salvas.
*   *Prós:* Mais simples de codificar.
*   *Contras:* Gera estados parciais e corrompidos de dados (por exemplo, 20 salas importadas, e as últimas 10 falham). O usuário precisa rodar novamente o arquivo, o que gera duplicidades ou exige scripts de limpeza complexos no banco de dados.

### Alternativa B: Importação Transacional sob Política "Tudo ou Nada" (Adotada)
*   *Descrição:* O backend FastAPI valida a estrutura de todas as linhas e cabeçalhos em memória antes de efetuar qualquer alteração real nos dados.
*   *Prós:* Evita dados corrompidos parciais e garante integridade referencial absoluta das salas cadastradas.
*   *Contras:* Consome ligeiramente mais memória para arquivos CSV gigantescos (não aplicável ao cenário de campi universitários comuns com poucas centenas de salas).

---

## 3. Padrões aplicáveis

*   **Repository Pattern (Repositório em Memória):** Mapeamento direto de coleções de dados simuladas para garantir flexibilidade técnica e facilitar a migração futura para banco de dados relacional (PostgreSQL) real.
*   **Schema-based Request Validation:** Uso de esquemas formais Pydantic para validação na camada de transporte da API.
