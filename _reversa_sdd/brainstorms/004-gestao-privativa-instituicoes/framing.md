# Framing: gestao-privativa-instituicoes

> Selo 🟡 PLANEJADO em todos os itens, sujeito a validação.

## Classificação da entrada
🟡 Solução disfarçada de problema: A requisição inicial questiona "qual será a melhor forma de gerenciar e controlar as informações de forma privativa", focando na arquitetura técnica de segregação/multi-tenancy para resolver a dor de exposição indevida e falta de fronteiras de privacidade entre organizações clientes na plataforma.

## Problema
🟡 Ausência de isolamento estrito e controle privativo de informações entre diferentes instituições na plataforma, gerando risco de visualização não autorizada, vazamento de dados estratégicos/pessoais (professores, horários, salas, turmas) e quebra de confidencialidade entre organizações distintas.

## Quem sente
🟡 Usuários operacionais de cada instituição (coordenadores de curso, diretores de infraestrutura, docentes e equipes administrativas) que manipulam informações institucionais no dia a dia, e responsáveis por conformidade/segurança que exigem proteção contra acesso cruzado.

## Quando dói
🟡 Imediatamente a partir da autenticação/login e durante toda a navegação e consumo de dados (painéis, listagens, cadastros, alocações e relatórios gerenciais).

## Custo de não fazer
🟡 Inviabilidade de ofertar a plataforma com segurança para mais de uma instituição (bloqueio de modelo SaaS/multi-tenant), risco grave de violação de termos de confidencialidade e LGPD por contaminação cruzada de dados institucionais.

## Job to be done
🟡 Quando o usuário logar na plataforma, eu quero que ele acesse somente as informações referentes a sua instituição, para manter a privacidade das informações e dados.

## Fora de escopo declarado
🟡 Alterações nos algoritmos heurísticos fundamentais de alocação de salas (ACC/AMR) para uma única instituição; o foco é o isolamento, governança e privacidade de dados entre organizações distintas.

## Âncoras no legado
🟡
- `_reversa_sdd/architecture.md`: O ClassSync AI foi concebido originalmente como single-tenant, sem as entidades `Institution` ou `Tenant` nas tabelas relacionais e modelos de domínio.
- `_reversa_sdd/domain.md`: Mapeia entidades acadêmicas (Coordination, Teacher, Room, Class) em escopo global único.
- `_reversa_sdd/addenda/020-landing-page-login-rbac.md`: Define autenticação e papéis de usuário (RBAC), mas ainda sem chave de particionamento ou escopo institucional.

---
Gerado por reversa-framer em 2026-09-07T12:30:45-03:00
Sessão: 004-gestao-privativa-instituicoes
