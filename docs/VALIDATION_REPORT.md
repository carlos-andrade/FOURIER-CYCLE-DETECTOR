# Relatório de validação

## Python mathematical core — 0.2.0
Implementados: FFT, regressão harmônica por mínimos quadrados, amplitude/fase, potência espectral, concentração e entropia. Testes sintéticos iniciais adicionados.

## Verificação numérica preliminar
As fórmulas centrais foram verificadas com sete cenários sintéticos independentes no ambiente de análise: recuperação de frequência/período, correção de amplitude Hann, rejeição de série constante, recuperação de amplitude/fase/offset, amostragem com posições explícitas, métricas espectrais e energia nula. Este resultado não substitui a execução da suíte pytest no próprio repositório.

## Automação
Workflow GitHub Actions `.github/workflows/tests.yml` adicionado para executar `python -m pytest -q` em pushes, pull requests e acionamento manual.

## Estado
Validação unitária automatizada aguardando resultado do workflow. Não foram processados dados históricos WINFUT. Não houve walk-forward, validação preditiva/econômica ou equivalência NTSL.

Nenhum módulo está certificado para negociação. Atualizar este relatório com o resultado efetivo do CI.
