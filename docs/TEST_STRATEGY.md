# Estratégia de testes

## Implementado em Python 0.2.x

### Testes de referência matemática
- Recuperação de frequência/período em senoide sintética.
- Correção de amplitude com janela Hann.
- Rejeição de série constante e entradas inválidas.
- Recuperação por mínimos quadrados de amplitude, fase e offset.
- Limites de entropia/concentração e tratamento de energia nula.
- Teste básico de invariância do prefixo observado.

### Robustez sintética adicionada
- Presença de dois componentes espectrais resolvíveis.
- Persistência da frequência dominante sob ruído determinístico moderado.
- Detecção de contração de amplitude por regressão em segmentos.
- Alteração da frequência dominante entre segmentos.
- Mudança de pico espectral entre dois regimes sintéticos.
- Sensibilidade à janela Hann versus retangular para tons centrados em bins.

Esses testes verificam propriedades controladas do algoritmo. Não demonstram que ciclos persistem ou antecipam movimentos no WINFUT.

## Próximos testes
- Resolução de frequências próximas e leakage para frequências fora dos bins.
- Chirp e modulação simultânea de amplitude/frequência.
- Propriedades matemáticas com Hypothesis.
- Replay cronológico, ausência de look-ahead e imutabilidade dos sinais emitidos.
- Robustez a janelas, sessões, liquidez e volatilidade.

## Validação financeira
Separar desenvolvimento, validação e teste final cronologicamente. Walk-forward sem contaminar o conjunto final. Incluir corretagem, emolumentos, spread e slippage quando disponíveis. Reportar expectancy, profit factor, drawdown, falsos positivos e atraso de detecção.

Os testes atuais não certificam desempenho de mercado.
