# Modelo matemático

## Série de entrada

Para preço de fechamento P_t, retorno em pontos: r_t = P_t - P_(t-1). A direção d_t = sign(r_t) pode ser usada como série auxiliar. A série principal e qualquer detrending devem ser explicitamente configurados e documentados.

## DFT

X_k = sum(n=0..N-1) x_n exp(-i 2 pi k n/N).

A potência pode ser definida como |X_k|². A normalização da amplitude depende da convenção adotada e deve ser testada com sinais sintéticos. Excluir o componente DC da seleção de ciclo dominante. Aplicar remoção de média/tendência e janela Hann conforme especificação experimental.

## Período dominante

Para frequência discreta k diferente de zero, período em amostras Renko T = N/k. Este período é contado em tijolos, não em tempo cronológico. A seleção deve respeitar faixa de frequência, resolução espectral e critérios mínimos de proeminência/estabilidade.

## Regressão harmônica

x_t = a cos(omega t) + b sin(omega t) + epsilon_t.

Amplitude A = sqrt(a²+b²). A fase deve usar convenção documentada e teste de referência; não comparar fases sem alinhar convenções e origem temporal.

## Energia e entropia

S_k = |X_k|²; p_k = S_k / sum_j S_j, quando a soma for positiva. Entropia espectral normalizada H = -sum_k p_k ln(p_k) / ln(M), para M > 1 bins válidos. Casos degenerados devem retornar estado explícito, não NaN silencioso.

## Módulos

- FCD: frequência/período dominante, força e estabilidade do ciclo.
- FHO: reconstrução harmônica, amplitude, fase e erro.
- FES: energia por bandas, concentração e entropia.
- FED: evidências combinadas de contração de amplitude, instabilidade e divergência de fluxo; nunca declarar reversão apenas por queda de amplitude.
- FRC: classificação de regime com estado INSUFFICIENT_DATA/NO_RELIABLE_CYCLE quando necessário.
- FGSE: vetor de estado e variações entre atualizações.

## Cuidados

Séries financeiras são não estacionárias. FFT, fase e espectro são estimativas dependentes da janela e do pré-processamento. Não interpretar pico espectral como ciclo persistente sem validação fora da amostra. Não tratar amplitude elevada como sinônimo de tendência.
