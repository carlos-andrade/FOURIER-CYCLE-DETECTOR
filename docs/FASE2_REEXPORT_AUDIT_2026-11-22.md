# FASE 2 — Auditoria complementar da reexportação WINFUT

Data da análise: 2026-11-22  
Ficheiro recebido: `FASE 2 — WINFUT(1).xlsx`  
Folha: `Folha1`  
SHA-256: `497e28690131332e36d81893d9d28a7df5f5100b20054661919e6bd4cd957235`  
Tamanho: 4.100.934 bytes

## 1. Estrutura observada

- 13.390 linhas de dados × 65 colunas.
- 147 sessões.
- Período: 2026-04-22 09:04 até 2026-11-19 18:07.
- Seis campos-base: Data, Abertura, Máxima, Mínima, Fechamento e Contador de Candles.
- As restantes 59 colunas são saídas/campos de indicadores e estratégias, incluindo BRICKMASTER_FVG_ATLAS_V1, GIROSCOPE_V1, BM_VOL_MMS9_ATR_SIMETRICO e CAR_1CENTO_v13_versao6.
- BMFB_001 e BMFB_002 permanecem vazias.
- A folha está visível; não foram encontradas fórmulas, tabelas Excel ou folhas adicionais.
- Os campos Data não contêm timezone embutido. O timezone `America/Sao_Paulo` já tinha sido confirmado pelo utilizador na auditoria anterior; esta reexportação não acrescenta prova independente do timezone.

## 2. Integridade estrutural

- 13.390/13.390 registos têm Data, OHLC e Contador de Candles preenchidos.
- Não foram encontrados OHLC com Máxima inferior à Mínima.
- Não foram encontrados casos em que Máxima fique abaixo da Abertura/Fechamento ou Mínima acima da Abertura/Fechamento.
- O contador cobre sequencialmente 1..N em cada uma das 147 sessões, sem lacunas ou repetições.
- Registos por sessão: mínimo 42, mediana 87, máximo 158.
- A exportação está ordenada em ordem cronológica inversa (mais recente primeiro). A sequência do contador também é inversa à ordem cronológica dentro de cada sessão; invertida a ordenação, o contador fica consistente com a progressão 1..N.
- Existem 27 grupos de timestamps repetidos (54 linhas), com precisão temporal ao minuto. O contador distingue as barras dentro desses grupos, mas não permite reconstruir o instante intraminuto.

## 3. Preços

- 10.511 registos apresentam pelo menos um campo OHLC que não é múltiplo de 5.
- Os restantes 2.879 registos têm os quatro campos OHLC múltiplos de 5.
- Os valores OHLC originais foram preservados; não houve arredondamento, reescala ou correção.
- A reexportação mantém a necessidade de investigar a alteração de regime observada a partir de 14/10/2026. A grelha de 5 pontos continua a ser apenas uma grelha candidata, não uma certificação do tick oficial.

## 4. Campos de atividade/volume

Não foram encontradas colunas explicitamente identificadas como:
- número de negócios/trades por barra (`trade_count`);
- quantidade/volume de contratos negociados;
- volume financeiro.

`Contador de Candles` é um índice sequencial de barras dentro da sessão. Não representa número de negócios, contratos ou volume financeiro. As colunas de indicadores e estratégias também não substituem campos-fonte de atividade.

Consequentemente, esta folha não demonstra que cada barra contenha 60.000 negócios. A configuração 60K Trades continua declarada pelo utilizador, mas não está comprovada pelos campos desta exportação.

## 5. Comparação com a auditoria anterior

A nova reexportação tem a mesma dimensão (13.390 × 65), período e número de sessões descritos na auditoria inicial, mas possui SHA-256 diferente:
- Amostra anterior: `5e0005c96f3642aa7dbf956cee62883a042057a6eb08b16b084537b266639c7f`
- Nova reexportação: `497e28690131332e36d81893d9d28a7df5f5100b20054661919e6bd4cd957235`

Sem o ficheiro anterior disponível para comparação binária/linha a linha nesta execução, não se afirma que os conteúdos sejam idênticos. A auditoria complementar confirma as métricas estruturais acima para o ficheiro recebido agora.

## 6. Conclusão e bloqueios

A reexportação confirma a integridade estrutural básica dos campos OHLC e do contador de barras. Não fecha, porém, os gates de certificação:

1. Identidade exata do instrumento e vencimento.
2. Configuração do gráfico no Profit One e prova do critério 60K.
3. Existência/definição de trade_count e volume, ou documentação do método de construção da barra.
4. Semântica do timestamp (abertura, fecho, último negócio ou outro).
5. Proveniência dos preços e explicação da mudança observada em 14/10/2026.
6. Provedor/feed e direitos de utilização/armazenamento.

**Estado:** FASE 2 continua NÃO CERTIFICADA; FASE 2.1 continua ABERTA/BLOQUEADA por metadados e evidências externas. Não iniciar FASE 3 com esta exportação como se estivesse certificada.

O ficheiro XLSX original não foi publicado no GitHub. Apenas este relatório técnico agregado e o hash de integridade são registados no repositório.
