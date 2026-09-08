# Regression Watch: CRUD de Gestão de Instituições e Master-Chef

> Identificador: `023-crud-instituicoes-master-chef`
> Data: `2026-09-07`

## 1. Itens de Vigilância de Regressão

| ID | Origem (arquivo, seção) | Regra esperada após mudança | Tipo de verificação | Sinal de violação |
|----|-------------------------|-----------------------------|---------------------|-------------------|
| W001 | `_reversa_forward/023-crud-instituicoes-master-chef/legacy-impact.md#web-app-api` | Endpoint `GET /api/v1/platform/tenants/{slug}` retorna metadados e master-chef exclusivamente para a role `doctor-chef` | presença | Retorno de erro 404 em tenant existente ou permissão concedida a perfis acadêmicos (`gestor`, `docente`). |
| W002 | `_reversa_forward/023-crud-instituicoes-master-chef/legacy-impact.md#web-app-api` | Endpoint `PUT /api/v1/platform/tenants/{slug}` atualiza nome e e-mail cadastrais sem alterar o slug ou a porta TCP alocada | redação | Alteração indevida de porta ou indisponibilidade de container após edição de metadados cadastrais. |
| W003 | `_reversa_forward/023-crud-instituicoes-master-chef/legacy-impact.md#web-app-api` | Endpoint `POST /api/v1/platform/tenants/{slug}/master-chef/reset` define hash de senha provisória e ativa mandatoriamente `must_change_password=True` | presença | Master-chef conseguir acessar a instância sem passar pela redefinição obrigatória de senha. |
| W004 | `_reversa_forward/023-crud-instituicoes-master-chef/legacy-impact.md#web-app-api` | Endpoint `DELETE /api/v1/platform/tenants/{slug}` exige confirmação com slug exato, desocupa porta e move volume para `./data/.archived/` | presença | Deleção destrutiva imediata (hard delete sem arquivamento) ou exclusão acionada com slug divergente. |
| W005 | `tests/test_platform_tenants_api.py` | Suíte de testes de governança e isolamento de instâncias mantendo 100% de aprovação (zero falhas) | presença | Falha em qualquer assert de RBAC, ciclo de vida de tenants ou rotação de credenciais. |

## 2. Histórico de re-extrações

> Nenhuma re-extração registrada para esta feature ainda.

## 3. Arquivadas

> Nenhuma regra arquivada.
