# Contrato de dados

## Campos essenciais

- timestamp: data/hora com timezone ou regra explícita de timezone.
- open, high, low, close: preços numéricos.
- volume: quantidade negociada, unidade documentada.
- brick_index: índice sequencial, único e crescente.
- direction: direção derivada e validada contra a regra de construção.
- instrument: identificador do contrato WINFUT e vencimento.
- source: origem do dado/exportação.
- renko_spec: parâmetros e método efetivo de construção do Renko.

## Campos opcionais

- financial_volume.
- cumulative_delta.
- bid/ask ou agressão, se a fonte disponibilizar com semântica documentada.

## Integridade

Validar ordenação, duplicidade, lacunas, valores não finitos, OHLC coerente, índice monotônico e timestamps. Não preencher silenciosamente campos ausentes.

## Renko

Não presumir que “30R” determina universalmente tamanho de tijolo, reversão, pavio ou regra de fechamento. Registrar a configuração efetiva do Profit e validar com amostras exportadas. O índice de tijolos é o eixo de eventos; timestamps permitem análises temporais separadas.

## Custódia

Não versionar dados proprietários ou sujeitos a restrições de redistribuição. Usar fixtures sintéticas e amostras autorizadas/anonimizadas.
