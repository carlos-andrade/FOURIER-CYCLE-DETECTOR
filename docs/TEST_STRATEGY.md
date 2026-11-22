# Estratégia de testes

## Implementado em Python 0.2.0
- Recuperação de frequência/período em senoide sintética.
- Correção de amplitude com janela Hann.
- Rejeição de série constante e entradas inválidas.
- Recuperação por mínimos quadrados de amplitude, fase e offset.
- Limites de entropia/concentração e tratamento de energia nula.
- Teste básico de invariância do prefixo observado.

## Próximos testes
- Duas frequências próximas e resolução espectral.
- Ruído e modulação de amplitude.
- Frequência variável e mudança abrupta de regime.
- Propriedades matemáticas com Hypothesis.
- Replay cronológico, ausência de look-ahead e imutabilidade dos sinais emitidos.
- Robustez a janelas, sessões, liquidez e volatilidade.

## Validação financeira
Separar desenvolvimento, validação e teste final cronologicamente. Walk-forward sem contaminar o conjunto final. Incluir corretagem, emolumentos, spread e slippage quando disponíveis. Reportar expectancy, profit factor, drawdown, falsos positivos e atraso de detecção.

Os testes atuais não certificam desempenho de mercado.
