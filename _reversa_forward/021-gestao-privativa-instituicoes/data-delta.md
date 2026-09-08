# Data Delta: Gestão e Controle Privativo de Informações entre Instituições (Deploy Isolado Multi-Tenant)

> Identificador: `021-gestao-privativa-instituicoes`
> Data: `2026-09-07`

## 1. Resumo do Delta

Diferentemente de abordagens lógicas que exigem alterações invasivas em todas as tabelas (adicionando colunas `institution_id` e chaves estrangeiras compostas), a arquitetura de **Instâncias Dedicadas** preserva integralmente o schema relacional das tabelas de negócio do ClassSync AI documentadas em `_reversa_sdd/architecture.md#erd`:
- `Coordination`
- `Teacher`
- `Room`
- `Class`
- `Restriction`
- `AllocationTask`
- `AuctionBid`
- `User`

O delta de dados reside na **camada de persistência e parametrização de armazenamento**:
1. Cada instituição cliente opera com um banco de dados relacional físico 100% isolado.
2. O caminho e tipo do banco de dados passam a ser configurados dinamicamente via variável de ambiente `DATABASE_URL`.

## 2. Estrutura de Diretórios e Persistência Física

No host, os dados de cada instituição são segregados em volumes independentes montados em `/app/data` dentro do container:

```
csalas/
├── data/
│   ├── .gitignore
│   ├── faculdade_alfa/
│   │   ├── classsync.db        # Banco de dados SQLite da Faculdade Alfa
│   │   └── exports/            # Relatórios e grades exportadas da Alfa
│   └── faculdade_beta/
│       ├── classsync.db        # Banco de dados SQLite da Faculdade Beta
│       └── exports/            # Relatórios e grades exportadas da Beta
```

## 3. Parametrização em `src/database.py`

Para suportar execução híbrida (SQLite em volume desacoplado ou PostgreSQL corporativo), o mecanismo de conexão de banco em `src/database.py` é atualizado para ler `DATABASE_URL` do ambiente com fallback seguro:

```python
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./classsync.db")

# Ajuste automático de argumentos de conexão para SQLite vs PostgreSQL
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

## 4. Garantia de Inviolabilidade de Dados

- **Zero compartilhamento de disco:** O container da `faculdade_alfa` monta estritamente `./data/faculdade_alfa:/app/data`, não tendo visibilidade nem permissão de leitura sobre `./data/faculdade_beta`.
- **Seed inicial independente:** Cada banco novo provisionado gera sua própria conta inicial de gestor padrão isolada, sem qualquer vínculo com contas de outras faculdades.
- **Restauração atômica:** Caso uma faculdade precise restaurar um backup de 3 dias atrás, apenas o arquivo `./data/{TENANT_NAME}/classsync.db` é substituído, sem qualquer impacto nas demais instituições ativas.
