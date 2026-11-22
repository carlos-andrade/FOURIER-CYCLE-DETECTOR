# Modelo matemático

## Série de entrada
Para fechamento P_t, retorno em pontos r_t=P_t-P_(t-1). Frequências sobre sequência Renko são ciclos por tijolo, não ciclos por segundo/minuto.

## DFT
X_k = sum(x_n * exp(-i*2*pi*k*n/N)). A potência implementada é |X_k|². A amplitude unilateral é corrigida pelo ganho coerente da janela Hann; DC e Nyquist não são duplicados. A seleção do ciclo dominante exclui DC e respeita os limites de frequência configurados.

## Regressão harmônica
x_t = offset + a*cos(omega*t) + b*sin(omega*t) + erro.
A=sqrt(a²+b²); fase=atan2(b,a), usando a convenção ajustada(t)=offset+A*cos(omega*t-fase).

## Energia e entropia
p_k=power_k/sum(power). H=-sum(p_k*ln(p_k))/ln(M), para M bins selecionados. Estados degenerados retornam valid=false, sem NaN silencioso. A implementação permite restringir métricas a uma banda de frequência; bins fora da banda não participam do denominador.

## Convenções implementadas em Python 0.2.0
- FFT real via numpy.fft.rfft.
- Frequência em ciclos por amostra; para Renko, ciclos por tijolo.
- Amplitude de pico corrigida pelo ganho coerente da janela.
- Power é magnitude ao quadrado dos coeficientes DFT da série janelada; é uma medida relativa sob mesmo tamanho/janela, não uma PSD calibrada.
- Regressão harmônica por mínimos quadrados com intercepto.
- Entropia normalizada e concentração máxima da energia relativa, calculadas na banda selecionada.

## Limitações
Séries financeiras são não estacionárias. Estimativas dependem da janela, detrending e faixa de frequência. Pico espectral não prova ciclo persistente nem prevê reversão. Entropia e concentração descrevem a distribuição de energia; não são, isoladamente, critérios de confiabilidade. É obrigatório validar fora da amostra.
