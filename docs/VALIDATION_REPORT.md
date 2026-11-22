# Relatório de validação

## Python mathematical core — 0.2.x

### Implementado
- FFT real e espectro unilateral.
- Correção de amplitude pelo ganho coerente da janela.
- Seleção de frequência dominante com exclusão de DC e limites configuráveis.
- Regressão harmônica por mínimos quadrados.
- Estimação de amplitude, fase, offset, RMSE e R².
- Energia espectral relativa, concentração e entropia normalizada.
- Tratamento explícito de sinal constante/energia nula e entradas inválidas.

## Testes automatizados

A suíte original foi aprovada no GitHub Actions (14 casos, incluindo parametrizações), conforme execução registrada no histórico do repositório.

### Robustez sintética — nova bateria
Adicionados testes para:
- Sinais com duas frequências resolvíveis.
- Ruído gaussiano determinístico moderado.
- Contração de amplitude observada em segmentos.
- Alteração da frequência dominante entre segmentos.
- Mudança abrupta entre regimes sintéticos.
- Comparação de janelas para uma frequência centrada em bin.

**Estado desta nova bateria:** aguardando execução no GitHub Actions. Não declarar aprovada antes de observar o resultado da execução.

## Escopo efetivamente validado até a bateria anterior

Os testes cobrem séries sintéticas determinísticas: frequência/período, amplitude com janela Hann, série constante, entradas inválidas, regressão harmônica, posições amostrais explícitas, entropia/concentração, energia nula e invariância básica do prefixo observado.

## Limitações abertas
- Nenhum histórico real de WINFUT foi processado.
- Nenhum ciclo foi validado como persistente ou preditivo no mercado.
- Não houve walk-forward, validação econômica ou avaliação de custos.
- O teste de prefixo é uma verificação básica, não uma prova completa de causalidade em tempo real.
- Não existe equivalência NTSL/Python validada.
- Nenhum módulo está certificado para negociação.

## Estado
**TESTED — primitivas matemáticas Python, apenas no escopo dos testes que passaram no CI.**  
**NOT VALIDATED — comportamento empírico em WINFUT permanece pendente.**  
**NOT CERTIFIED — nenhuma autorização para operar ou enviar ordens.**
