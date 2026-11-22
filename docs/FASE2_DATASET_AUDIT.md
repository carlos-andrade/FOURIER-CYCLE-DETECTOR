# FASE 2 — Auditoria inicial da amostra WINFUT

## Identificação da amostra

- Ficheiro recebido: `FASE 2 — WINFUT.xlsx`
- SHA-256: `5e0005c96f3642aa7dbf956cee62883a042057a6eb08b16b084537b266639c7f`
- Folha: `Folha1`
- Dimensão: 13.390 linhas de dados × 65 colunas.
- Período observado: 2026-04-22 09:04 até 2026-11-19 18:07.
- Sessões distintas: 147.
- A amostra foi inspecionada localmente. O ficheiro original não foi copiado para o repositório.

## Estrutura identificada

- Colunas iniciais: Data, Abertura, Máxima, Mínima, Fechamento e Contador de Candles.
- Colunas de indicadores incluem BRICKMASTER_FVG_ATLAS_V1, GIROSCOPE_V1, BM_VOL_MMS9_ATR_SIMETRICO e CAR_1CENTO_v13_versao6.
- BMFB_001 e BMFB_002 estão integralmente vazias.
- Não foi encontrada coluna explícita de trade_count ou volume negociado na estrutura da folha.

## Verificações executadas

- 13.390/13.390 registos têm data, OHLC e contador preenchidos.
- Não foram encontrados casos de máxima inferior à mínima.
- Não foram encontrados casos em que a máxima fique abaixo da abertura/fecho ou a mínima acima da abertura/fecho.
- O contador reinicia em 1 em cada sessão e progride sem lacunas até ao total de registos daquela sessão, em todas as 147 sessões.
- Registos por sessão: mínimo 42, mediana 87, máximo 158.
- Existem 27 timestamps repetidos. A precisão temporal exportada é de minuto; não há segundos registados.
- Os intervalos intrassessão são variáveis: mediana 4 minutos, média aproximada 6,06 minutos.
- 10.511 registos apresentam pelo menos um campo OHLC que não é múltiplo de 5 (recontagem por Decimal, sem tolerância de ponto flutuante).

## Adaptador offline implementado

- `MarketBar` representa barras OHLC com índice global, contador de origem, timestamp, semântica temporal explícita/UNKNOWN e campos opcionais de trade_count e volume.
- `iter_profit_one_xlsx` lê somente Data, Abertura, Máxima, Mínima, Fechamento e Contador de Candles.
- Colunas de indicadores são deliberadamente ignoradas.
- A ordenação é cronológica; o contador original é usado para desempatar timestamps iguais.
- O timezone IANA é obrigatório na chamada do adaptador. Não há inferência automática de timezone.
- A semântica do timestamp começa como UNKNOWN e não é presumida como abertura ou fecho da barra.
- trade_count, volume e volume financeiro permanecem ausentes quando não estão na exportação.
- O SHA-256 do ficheiro de origem é preservado em cada MarketBar.
- Dependência XLSX isolada no extra opcional `excel`.

## Execução de leitura com timezone confirmado

- Timezone confirmado pelo utilizador para a coluna Data: `America/Sao_Paulo`.
- Leitura da folha `Folha1` com a mesma seleção de seis colunas e regras de parsing documentadas no adaptador.
- Registos processados: 13.390.
- Erros de parsing/OHLC/contador: 0.
- Primeiro timestamp normalizado: 2026-04-22 09:04:00 -03:00.
- Último timestamp normalizado: 2026-11-19 18:07:00 -03:00.
- Timestamps repetidos: 27 grupos, todos preservados e ordenados pelo contador de origem.
- Contador: sequência de 1 até ao número de registos da sessão, sem lacunas, nas 147 sessões.
- Semântica temporal mantida como UNKNOWN; a confirmação do timezone não determina se Data é abertura ou fecho da barra.
- trade_count, volume e volume financeiro continuam NULL, pois não existem colunas-fonte correspondentes.
- SHA-256 confirmado: `5e0005c96f3642aa7dbf956cee62883a042057a6eb08b16b084537b266639c7f`.

A recontagem corrigiu o valor anterior de 6.908 para 10.511 registos com pelo menos um OHLC não múltiplo de 5. Esta diferença é uma correção da auditoria, não uma alteração dos dados originais.

## Análise temporal da conformidade dos preços

A distribuição da ocorrência não é uniforme ao longo do período:

- De 2026-04-22 a 2026-10-13: 121 sessões; todas as 10.511 barras desse intervalo apresentam pelo menos um campo OHLC não múltiplo de 5.
- De 2026-10-14 a 2026-11-19: 26 sessões; 2.879 barras sem qualquer campo OHLC não múltiplo de 5.
- Nas 10.511 barras afetadas, 10.443 têm os quatro campos OHLC não múltiplos de 5; 68 têm entre dois e três campos afetados.
- Nas 2.879 barras restantes, os quatro campos OHLC são múltiplos de 5.

O corte observado entre 2026-10-13 e 2026-10-14 é uma mudança temporal objetiva na representação dos preços. No limite entre as sessões, o último fecho de 13/10 é 210.690,00 e a primeira abertura de 14/10 é 210.500,00. A escala nominal permanece semelhante, pelo que a observação não parece uma simples conversão de unidade de 1.000x; isso não identifica a causa nem exclui outras transformações. A amostra, isoladamente, não permite determinar se decorre de alteração na origem, no instrumento/vencimento, no ajuste histórico, na exportação ou noutra transformação. Não arredondar, reescalar ou corrigir os valores para os tornar múltiplos de 5 sem evidência da origem. A conformidade deve ser investigada por regime temporal, antes de qualquer certificação.

## Interpretação e bloqueios

Esta auditoria confirma integridade estrutural básica do conjunto OHLC e continuidade do contador por sessão. Não certifica a construção 60K Trades.

Não é possível verificar a quantidade de negócios por barra porque a folha não contém campo explícito de trade_count nem eventos individuais. A ausência de volume explícito também impede reconciliar número de negócios, quantidade de contratos e volume financeiro.

Os timestamps repetidos podem resultar de precisão de exportação limitada a minutos; a amostra não permite reconstruir a ordem intraminuto. A frequência de preços não múltiplos de 5 requer reconciliação com a origem e a transformação dos preços antes de aceitar os OHLC como cotações nativas do WINFUT.

O adaptador é um parser de ingestão offline e não uma certificação da fonte. A configuração 60K, o instrumento/vencimento, o timezone, a semântica temporal e a completude da barra continuam a exigir confirmação.

## Estado

- Auditoria estrutural inicial: CONCLUÍDA COM RESSALVAS.
- Parser XLSX offline: IMPLEMENTADO; CI APROVADA.
- Certificação da configuração 60K Trades: PENDENTE.
- Certificação da semântica dos preços OHLC: PENDENTE.
- Certificação de volume/trade_count: PENDENTE.
- Adaptador de produção: NÃO CERTIFICADO.

## Próximas verificações necessárias

1. Confirmar no Profit One o instrumento, vencimento e configuração exata usada para gerar a exportação.
2. Confirmar o timezone da coluna Data e se representa abertura, fecho ou outro marco temporal da barra.
3. Exportar amostra com volume e, se disponível, número de negócios por barra.
4. Explicar a ocorrência de OHLC não múltiplo de 5 e reconciliar com os dados originais.
5. Definir o tratamento das barras iniciais/finais de sessão e das barras incompletas.
6. Só depois converter amostra autorizada em fixtures de teste de integração e certificar o adaptador.
