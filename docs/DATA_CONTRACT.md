# Contrato de dados — FOURIER CYCLE DETECTOR

## Fonte e configuração do gráfico

- Plataforma declarada: Profit One.
- Gráfico de referência: 60K Trades.
- Instrumento inicial do projeto: WINFUT, sujeito à confirmação no ficheiro exportado.
- Unidade de construção da barra: contagem de negócios (trades), conforme a configuração 60K Trades.
- O valor 60K identifica a configuração declarada do gráfico; a conformidade de cada barra deve ser verificada nos dados exportados.
- Não utilizar Renko, brick size, reversal distance ou brick_index neste contrato.

## Campos essenciais da série de barras

- bar_index: índice sequencial da barra, único e crescente na série exportada.
- bar_start_at: início da barra, se fornecido pela fonte.
- bar_end_at: fecho/fim da barra, com timezone explícito.
- open, high, low, close: preços numéricos.
- trade_count: número de negócios que compõem a barra, quando fornecido ou calculável a partir dos eventos de origem; não substituir por volume de contratos.
- volume: quantidade negociada, mantendo a unidade exatamente como documentada pela exportação.
- instrument: identificador do instrumento e vencimento do contrato.
- source: origem, nome do ficheiro, plataforma e metadados da exportação.
- chart_configuration: identificação literal da configuração 60K Trades e parâmetros disponíveis na exportação.

## Campos opcionais

- financial_volume.
- cumulative_delta.
- bid/ask ou agressão, somente quando a fonte disponibilizar esses campos com semântica documentada.
- event_at, information_available_at e received_at, quando existirem eventos de negócio individuais.

## Integridade e validação

Validar:
- ordenação e unicidade de bar_index;
- timestamps com timezone e monotonicidade compatível com a série;
- OHLC coerente e valores numéricos finitos;
- trade_count observado por barra e desvios em relação ao alvo configurado;
- identificação de barras incompletas, especialmente no encerramento da sessão ou no fim da exportação;
- unidade e semântica de volume;
- instrumento, vencimento, sessão e origem.

Não preencher silenciosamente campos ausentes. Não assumir que uma barra tem exatamente 60.000 negócios sem verificar a exportação e o comportamento de barras parciais.

## Custódia e direitos

Não versionar dados proprietários ou sujeitos a restrições de redistribuição. Usar fixtures sintéticas e amostras autorizadas/anonimizadas.
