# Estimativa de Preco

**Feature:** `_reversa_forward/011-disciplina-alocacao-aula`
**Gerado em:** 2026-08-09 16:45 UTC
**Versao dos calculos:** Esforco v2.0, Valor v2.0, Mercado v2.0

**Pre-requisitos consumidos:**
- Profile: `_reversa_sdd/_pricing/profile.json`
- Size: `_reversa_sdd/_pricing/011-disciplina-alocacao-aula/size.json` (classe `M`, score auxiliar `35`)

## Visao geral

| Cenario | Faixa | Comentario |
|---|---|---|
| **Esforco** | R$ 4.950,00 a R$ 13.200,00 BRL | 12 a 32h, custo + imposto + markup |
| **Valor** | Nao disponivel | Cliente nao declarou retorno mensuravel |
| **Faixa de Mercado** | R$ 1.200,00 a R$ 6.400,00 BRL | Taxa hora fonteada por pais e senioridade |

## Cenario Esforco

**O que e:** preco calculado a partir de horas provaveis, taxa hora, reserva tributaria aproximada e markup de projeto. E o piso defensavel para nao subsidiar o cliente.

**Quando usar:** sempre como sanity check. Cobrar abaixo do Esforco significa assumir prejuizo ou reduzir demais o lucro do projeto.

| Item | Valor |
|---|---|
| Classe de complexidade | M |
| Senioridade | senior |
| Fator de senioridade | 1.00 |
| Horas estimadas | 12 a 32 h |
| Ponto medio | 22 h |
| Taxa hora | 250,00 BRL/h |
| Custo direto | R$ 3.000,00 a R$ 8.000,00 BRL |
| Reserva tributaria aproximada (15%) | R$ 450,00 a R$ 1.200,00 BRL |
| Markup de projeto (50%) | R$ 1.500,00 a R$ 4.000,00 BRL |
| **Faixa Esforco** | **R$ 4.950,00 a R$ 13.200,00 BRL** |
| Ponto medio | R$ 9.075,00 BRL |
| Em USD | $ 825.00 a $ 2,200.00 USD (cambio: 1 USD = 6.00 BRL) |

> Aviso: Parte do fator tributario pode ser imposto destacado e repassado ao cliente. Valide com contador.

## Cenario Valor

**O que e:** preco baseado em parte do valor economico anual que a feature gera ou protege para o cliente. O Reversa usa captura de 10% a 30% do valor anual declarado.

**Quando usar:** quando o cliente consegue declarar retorno, economia ou custo de nao fazer.

> **Cenario Valor nao disponivel:** Cenario Valor nao pode ser calculado: cliente nao declarou retorno mensuravel.

## Cenario Faixa de Mercado

**O que e:** faixa derivada de benchmark horario por pais e senioridade, multiplicado pela mesma faixa de horas do cenario Esforco.

**Quando usar:** como referencia externa. A v2 nao multiplica por perfil de cliente porque nao ha dataset publico confiavel para isso.

| Item | Valor |
|---|---|
| Pais / Senioridade | Brasil (BR) / senior |
| Modelo / Perfil cliente | valor_fixo_por_entrega / todos |
| Complexidade | M |
| Taxa hora de mercado | R$ 100,00 a R$ 200,00 BRL/h |
| Tipo de fonte | salary_derived_freelance_estimate |
| Ano de referencia | 2025-2026 |
| Fontes | Portal Salario CAGED, Glassdoor Brasil |
| **Faixa Mercado** | **R$ 1.200,00 a R$ 6.400,00 BRL** |
| Em USD | $ 200.00 a $ 1,066.67 USD (cambio: 1 USD = 6.00 BRL) |

## Como escolher entre os tres

Como o cliente nao declarou retorno mensuravel, o Cenario Valor nao esta disponivel. Utilize o Cenario Esforco (R$ 4.950,00 a R$ 13.200,00 BRL) como piso minimo defensavel para garantir a rentabilidade pretendida (com markup de 50% e reserva fiscal).

Heuristica geral:

1. Cliente sem retorno claro: use Esforco como piso e Mercado como referencia externa
2. Cliente com retorno alto e claro: prefira Valor, com Esforco apenas como piso minimo
3. Esforco acima do Mercado: revise profile, size ou adequacao do cliente
4. Mercado acima do Esforco: ha espaco para subir markup ou melhorar proposta

## Disclaimer

Disclaimer: os numeros nesta estimativa sao aproximacoes para orientacao de orcamento, nao garantia de fechamento. O fator de imposto e uma reserva aproximada, nao uma aliquota legal exata. Validacao tributaria real e responsabilidade do contador do usuario. A faixa de mercado e estatica e baseada nas fontes documentadas em `market-benchmarks.md`. O retorno declarado pelo cliente no cenario Valor e input bruto, nao validado. Recomenda-se adicionar `_reversa_sdd/_pricing/<feature>/estimate.{md,json}` ao `.gitignore` antes de commitar.
