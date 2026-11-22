# Relatório de validação

## Python mathematical core — 0.2.0

Implementados:
- FFT real e espectro unilateral.
- Correção de amplitude pelo ganho coerente da janela.
- Seleção de frequência dominante com exclusão de DC e limites configuráveis.
- Regressão harmônica por mínimos quadrados.
- Estimação de amplitude, fase, offset, RMSE e R².
- Energia espectral relativa, concentração e entropia normalizada.
- Tratamento explícito de sinal constante/energia nula e entradas inválidas.

## Testes automatizados

GitHub Actions: **SUCCESS**  
Workflow: Python tests  
Run: [45061967302](https://github.com/carlos-andrade/FOURIER-CYCLE-DETECTOR/actions/runs/45061967302)  
Commit testado: `8772772e1b45d5602f114f23c04f61c12439b706`

Etapas de instalação e execução de `python -m pytest -q` concluídas com sucesso. A suíte contém 14 casos de teste, incluindo parametrizações.

## Escopo efetivamente validado

Os testes cobrem séries sintéticas determinísticas: frequência/período, amplitude com janela Hann, série constante, entradas inválidas, regressão harmônica (amplitude/fase/offset), posições amostrais explícitas, entropia/concentração, energia nula e invariância básica do prefixo observado.

## Limitações ainda abertas

- Nenhum histórico real de WINFUT foi processado.
- Nenhum ciclo foi validado como persistente ou preditivo no mercado.
- Não houve walk-forward, validação econômica ou avaliação de custos.
- O teste de prefixo é uma verificação básica, não uma prova completa de causalidade do sistema em tempo real.
- Não existe equivalência NTSL/Python validada.
- Nenhum módulo está certificado para negociação.

## Estado

**TESTED — primitivas matemáticas Python 0.2.0, no escopo dos testes acima.**  
**NOT VALIDATED — comportamento empírico em WINFUT permanece pendente.**  
**NOT CERTIFIED — proibido interpretar esta etapa como autorização para operar ou enviar ordens.**

A próxima etapa é ampliar testes de robustez (multi-frequência, ruído, modulação, frequência variável e regimes) e depois validar o contrato com dados exportados do Profit.
