# Investigation: CRUD de Gestão de Instituições e Master-Chef

> Identificador: `023-crud-instituicoes-master-chef`
> Data: `2026-09-07`

## 1. Contexto e Pesquisa de Fundo

Com a entrega da feature `022-admin-geral-instituicoes`, a plataforma ClassSync AI ganhou a capacidade de provisionar novas instituições clientes de forma automatizada e visual, criando containers Docker isolados, alocando portas TCP incrementais e semeando o gestor institucional ('master-chef') com flag de troca obrigatória de senha no primeiro login.
No entanto, no dia a dia operacional de uma infraestrutura SaaS educacional surgem demandas contínuas de governança após a entrega inicial da instância:
1. **Perda de acesso pelo Master-Chef:** Se o gestor institucional esquecer sua senha privativa ou houver transição de diretoria na faculdade cliente, o superadministrador necessita de uma forma segura de reemitir uma credencial provisória sem precisar abrir manualmente o banco SQLite no terminal ou violar a privacidade dos dados acadêmicos.
2. **Atualização Cadastral:** Ajustar o nome da instituição (por exemplo, quando uma faculdade se transforma em Centro Universitário) sem desmanchar o container ou alterar a URL/porta em produção.
3. **Desativação e Desprovisionamento:** Clientes que encerram contrato ou instâncias de teste/demonstração que precisam ser desativadas, liberando a porta TCP alocada para novos clientes, sem perder permanentemente os dados acadêmicos históricos (exigência de guarda e auditoria prevista em contratos educacionais e pela LGPD).

## 2. Padrões de Exclusão e Retenção: Soft Delete / Arquivamento

### 2.1. Desvantagens do Hard Delete em Sistemas Multi-Tenant
A exclusão definitiva e destrutiva (`docker rm -f` acompanhado de deleção recursiva de pasta via `shutil.rmtree`) traz riscos inaceitáveis em ambiente de produção:
- Um erro de digitação do operador ou clique não intencional pode destruir sem volta centenas de grades horárias, cadastros de salas e restrições docentes.
- Compromete exigências regulatórias do MEC e da LGPD, que exigem a retenção de dados acadêmicos e registros por prazos de guarda definidos.

### 2.2. Solução Adotada: Soft Delete com Arquivamento Físico
- O container Docker é interrompido e removido da execução (`docker stop` e `docker rm`), desocupando a memória RAM e liberando a porta TCP do host.
- O arquivo `.env.{slug}` é renomeado para `.env.{slug}.archived` (ou movido para a pasta de arquivos arquivados).
- O diretório de dados `./data/{slug}/` é movido atomicamente para `./data/.archived/{slug}_{timestamp}/`.
- Desta forma, a instituição deixa de aparecer na listagem de tenants ativos e a porta fica imediatamente livre para novo reuso, mas os dados permanecem preservados em estado frio para restauração ou auditoria.

## 3. Acesso Seguro Cross-Tenant ao SQLite do Cliente para Reset do Master-Chef

### 3.1. Abordagens Avaliadas
- **Abordagem A (Endpoint Interno na Instância):** Criar uma rota interna HTTP na instância do cliente (ex.: `POST /internal/admin/reset`) protegida por chave de serviço compartilhada.
  - *Desvantagem:* Exige que o container da instituição esteja necessariamente ligado e saudável para resetar o acesso; se a instância estiver parada ou com erro de inicialização de rede, o reset falha.
- **Abordagem B (Manipulação Direta Segura no Arquivo SQLite):** Como os dados de cada tenant residem em volume mapeado no host (`./data/{slug}/classsync.db`), o serviço central da plataforma pode conectar-se diretamente ao SQLite do tenant, validar a tabela `User`, atualizar o hash da senha (gerado com PBKDF2/SHA-256 e o salt padrão do sistema) e marcar `must_change_password = 1`.
  - *Vantagem:* Funciona independentemente do status do container (online ou offline), é atômico, rápido e não expõe endpoints de privilégio elevado na rede da instância cliente.

## 4. UX e Salvaguardas contra Ações Destrutivas

Seguindo o padrão de plataformas modernas de nuvem e repositórios (GitHub, AWS, Vercel), ações com impacto significativo de interrupção ou desativação de serviço utilizam:
1. **Confirmação Estrita com Slug Exato:** O modal de exclusão exibe uma caixa de texto onde o operador deve digitar o slug exato da instituição. O botão de exclusão só é habilitado pelo JavaScript quando o valor digitado coincidir exatamente com a string do identificador da instituição.
2. **Cópia Segura de Senha Provisória:** Ao redefinir a credencial do master-chef, a nova senha provisória é exibida em campo protegido com botão de cópia direta para a área de transferência, emitindo alerta visual de que a credencial só será mostrada uma única vez e que sua substituição será mandatória no primeiro login.

## 5. Referências e Normas Aplicáveis

- **NIST SP 800-63B:** *Digital Identity Guidelines - Authentication and Lifecycle Management*.
- **OWASP Secure Design Principles:** *Fail-safe defaults and Defense in Depth*.
- **LGPD (Lei 13.709/2018):** Princípios de segurança, prevenção, não-discriminação e responsabilização no tratamento de dados cadastrais e credenciais.
