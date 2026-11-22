# Estratégia de testes

## Matemática

1. Senoide pura: frequência e amplitude conhecidas.
2. Soma de senoides: identificar componentes resolvíveis.
3. Ruído: quantificar degradação.
4. Modulação de amplitude: detectar expansão/contração.
5. Frequência variável: identificar instabilidade.
6. Sinal constante/zero: tratar degenerescência.
7. Sinal não periódico: não forçar ciclo dominante.

## Causalidade

- Nenhuma observação futura pode afetar estimativa passada.
- Reprocessamento cronológico deve reproduzir sinais emitidos.
- Sinais registrados são imutáveis.
- Atualização apenas com tijolos fechados no modo operacional.

## Robustez

Avaliar janelas, regimes, sessões, liquidez, volatilidade, gaps temporais e mudanças na frequência de formação dos tijolos.

## Validação financeira

Separar desenvolvimento, validação e teste final cronologicamente. Usar walk-forward sem contaminar o conjunto final. Incluir custos, corretagem, emolumentos, spread e slippage quando disponíveis. Reportar expectancy, profit factor, drawdown, taxa de falsos positivos e atraso de detecção.

## Critério

Nenhum resultado visual isolado certifica o modelo. Resultados devem ser reproduzíveis por commit, configuração e período de dados.
