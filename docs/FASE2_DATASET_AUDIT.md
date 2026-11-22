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
- 6.908 registos apresentam pelo menos um campo OHLC que não é múltiplo de 5.

## Interpretação e bloqueios

Esta auditoria confirma integridade estrutural básica do conjunto OHLC e continuidade do contador por sessão. Não certifica a construção 60K Trades.

Não é possível verificar a quantidade de negócios por barra porque a folha não contém campo explícito de trade_count nem eventos individuais. A ausência de volume explícito também impede reconciliar número de negócios, quantidade de contratos e volume financeiro.

Os timestamps repetidos podem resultar de precisão de exportação limitada a minutos; a amostra não permite reconstruir a ordem intraminuto. A frequência de preços não múltiplos de 5 requer reconciliação com a origem e a transformação dos preços antes de aceitar os OHLC como cotações nativas do WINFUT.

As colunas de indicadores não devem ser tratadas como fonte primária de mercado. Os campos completamente vazios devem permanecer ausentes, não ser preenchidos artificialmente.

## Estado

- Auditoria estrutural inicial: CONCLUÍDA COM RESSALVAS.
- Certificação da configuração 60K Trades: PENDENTE.
- Certificação da semântica dos preços OHLC: PENDENTE.
- Certificação de volume/trade_count: PENDENTE.
- Adaptador de produção: NÃO CERTIFICADO.

## Próximas verificações necessárias

1. Confirmar no Profit One o instrumento, vencimento e configuração exata usada para gerar a exportação.
2. Exportar amostra com volume e, se disponível, número de negócios por barra.
3. Confirmar se os timestamps representam abertura, fecho ou outro marco temporal da barra.
4. Explicar a ocorrência de OHLC não múltiplo de 5 e reconciliar com os dados originais.
5. Definir o tratamento das barras iniciais/finais de sessão e das barras incompletas.
6. Só depois converter a amostra autorizada em fixtures de teste e certificar o adaptador.

