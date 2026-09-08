# Investigation: Gestão e Controle Privativo de Informações entre Instituições (Deploy Isolado Multi-Tenant)

> Identificador: `021-gestao-privativa-instituicoes`
> Data: `2026-09-07`

## 1. Contexto e Motivação

O ClassSync AI foi projetado como um sistema mono-institucional. Com o amadurecimento da plataforma e a demanda de expansão para redes de ensino e múltiplos clientes universitários, tornou-se crítico garantir a privacidade irrefutável e o isolamento total dos dados de cada instituição cliente, respeitando as exigências da LGPD e as políticas de sigilo de malha horária, docentes e turmas.

Esta investigação analisou as estratégias de multi-tenancy e consolidou a fundamentação para a abordagem de instâncias dedicadas (Single-Tenant por Container).

## 2. Análise Comparativa de Padrões de Multi-Tenancy

| Padrão | Vantagens | Desvantagens | Decisão |
|---|---|---|---|
| **Multi-Tenancy Lógico (Mesmo Banco / Mesmas Tabelas com `institution_id`)** | Custo mínimo de infraestrutura e economia de escala. | Risco de vazamento de dados caso qualquer query esqueça a cláusula de filtro; exige refatoração profunda em todas as entidades legadas e no motor de alocação. | Descartado para a fase atual. |
| **Multi-Tenancy por Schemas (PostgreSQL Schemas no mesmo cluster)** | Segregação lógica forte de tabelas sem duplicar instâncias de banco. | Complexidade de gerenciamento dinâmico de conexões assíncronas no pool do FastAPI e dificuldade de manter migrações sincronizadas em N schemas. | Descartado devido à complexidade. |
| **Instâncias Dedicadas / Deploy Isolado (Container e Banco Desacoplados)** | **Isolamento de segurança absoluto por barreira física/processo**; zero risco de contaminação cruzada; preserva 100% o código legado sem qualquer refatoração no motor de alocação; migração e backup trivial por volume. | Maior consumo de recursos em escala elevada (acima de 20 instâncias); exige scripts de automação de infraestrutura. | **Escolhido e aprovado.** |

## 3. Arquitetura de Containerização e Execução Híbrida

1. **Dockerfile Otimizado Multi-Stage**:
   - Base com `python:3.11-slim` para imagem compacta e com superfície mínima de ataque.
   - Instalação de dependências sem cache de build desnecessário.
   - Execução sob usuário não-root para atender às melhores práticas de segurança em containers.
2. **Abstração de Banco de Dados (`DATABASE_URL`)**:
   - O ClassSync AI utiliza SQLAlchemy. Ao parametrizar `DATABASE_URL`, o sistema pode rodar com SQLite local montado em `./data/{TENANT_NAME}/classsync.db` (zero custo e zero configuração adicional) ou apontar para um PostgreSQL em nuvem corporativa (`postgresql://user:pass@host:5432/tenant_db`).
3. **Isolamento Criptográfico de Tokens**:
   - Cada instância carrega uma `SECRET_KEY` pseudoaleatória única injetada via `.env`. Mesmo que um invasor intercepte um token JWT de uma instituição, ele é matematicamente inválido em qualquer outra instituição.

## 4. Estratégia de Roteamento e Entrada

1. **Ambiente Local e Homologação**:
   - Mapeamento direto de portas de host para container (ex.: `8001:8000`, `8002:8000`), permitindo validar múltiplas instâncias em paralelo na mesma máquina de desenvolvimento sem alterar arquivos de sistema (`/etc/hosts`).
2. **Ambiente de Produção (Nginx / Caddy)**:
   - Configuração de proxy reverso upstream mapeando subdomínios corporativos (`{tenant}.classsync.ai`) para o container correspondente na rede interna do Docker, injetando cabeçalhos `X-Forwarded-For` e garantindo isolamento de certificados SSL/TLS.

## 5. Rotinas de Backup e Resiliência

- A abordagem de volumes desacoplados (`./data/{TENANT_NAME}`) permite backups atômicos sem travar a aplicação:
  - Para SQLite, scripts utilizam cópias consistentes ou comando `.backup`.
  - O script consolidado do host compacta cada pasta de tenant em arquivos `.tar.gz` organizados cronologicamente, permitindo restauração independente de uma instituição sem afetar as demais.
