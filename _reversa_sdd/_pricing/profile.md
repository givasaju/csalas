# Perfil de Cobranca

**Criado em:** 2026-08-09 16:41 UTC
**Versao do schema:** 1.1

## Identificacao

| Campo | Valor |
|---|---|
| Pais | Brasil (BR) |
| Moeda local | Real Brasileiro (BRL) |
| Senioridade | senior |

## Custo direto

| Campo | Valor |
|---|---|
| Modo de taxa hora | Direto |
| Renda mensal liquida desejada | N/A |
| Horas faturaveis por mes | N/A |
| Taxa hora informada | 250,00 BRL/h |

## Markup e impostos

| Campo | Valor |
|---|---|
| Markup de projeto | 50% |
| Regime tributario | Simples Nacional, servicos de TI |
| Fator aproximado | 15% |
| Tipo do fator | effective_reserve_estimate |
| Fonte do fator | Receita Federal, Simples Nacional, anexos e fator R |
| Inclui imposto destacado | Sim |
| Aviso de repasse | Sim |
| Confianca no regime | Alta, escolha explicita |

## Modelo comercial

| Campo | Valor |
|---|---|
| Modelos de cobranca | valor_fixo_por_entrega |
| Perfil de cliente | microempresa, pequena_empresa, media_empresa, enterprise, governo, cliente_internacional |
| Cobranca em moeda estrangeira | Sim, USD (1 USD = 6.00 BRL) |

## Disclaimer

Disclaimer: o fator de imposto registrado e uma reserva aproximada para orcamento, nao uma aliquota legal exata. Validacao tributaria real e responsabilidade do contador do usuario. Este arquivo contem dados financeiros sensiveis. Recomenda-se adicionar `_reversa_sdd/_pricing/profile.json` e `_reversa_sdd/_pricing/profile.md` ao `.gitignore` antes de commitar.
