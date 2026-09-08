# Regression Watch: Gestão e Controle Privativo de Informações entre Instituições (Deploy Isolado Multi-Tenant)

> Identificador: `021-gestao-privativa-instituicoes`
> Data: `2026-09-07`

## 1. Itens de Vigilância de Regressão

| ID | Origem (arquivo, seção) | Regra esperada após mudança | Tipo de verificação | Sinal de violação |
|----|-------------------------|-----------------------------|---------------------|-------------------|
| W001 | `_reversa_sdd/architecture.md#database` | Conexão em `src/database.py` deve respeitar `DATABASE_URL` do ambiente, mantendo fallback seguro para SQLite local. | `presença` | Erro ao iniciar a aplicação com caminhos customizados de banco ou falha no fallback padrão. |
| W002 | `_reversa_sdd/c4-context.md#personas` | Obtenção da `SECRET_KEY` em `src/api/auth.py` deve carregar chaves dinâmicas do ambiente sem perder compatibilidade com `test-valid-token`. | `presença` | Falha ao assinar/validar tokens com chaves de tenant ou quebra nos testes de auth existentes. |
| W003 | `_reversa_sdd/architecture.md#web-app-api` | Endpoint `GET /api/v1/health` deve responder status 200 OK, metadados de conectividade do banco e o nome do tenant. | `presença` | Erro 404, 500 ou ausência da rota de health check nos containers e proxies. |
| W004 | `tests/test_multi_tenant_isolation.py` | Testes automatizados de segregação física de tabelas e rejeição de JWT cruzado devem manter 100% de aprovação. | `presença` | Qualquer contaminação de registros entre bases isoladas ou aceitação indevida de token cruzado. |

## 2. Histórico de re-extrações

*(Vazio - será preenchido nas próximas re-extrações `/reversa`)*

## 3. Arquivadas

*(Vazio)*

## 4. Observações

- Suíte de testes automatizados `pytest` executada com 100% de aprovação (70/70 testes passando com zero regressões no sistema legado).
