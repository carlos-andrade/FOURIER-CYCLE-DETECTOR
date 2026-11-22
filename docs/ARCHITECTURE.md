# Arquitetura

## Visão geral

Pipeline: dados Renko/mercado → validação e pré-processamento → estimadores matemáticos → cinco módulos analíticos → Fourier Gyroscope State Engine (FGSE) → visualização/relatórios.

## Componentes

- core: contratos, pré-processamento e agregação de estado.
- mathematics: FFT, regressão harmônica, fase, janelamento e energia.
- indicators: FCD, FHO, FES, FED e FRC.
- market: adaptadores de Renko e métricas de mercado (VWAP, TWAP, volume e delta, quando disponíveis).
- validation: walk-forward, causalidade, estabilidade e backtest.
- visualization: espectro, séries e painel de diagnóstico.
- ntsl: implementação posterior e testes de equivalência com Python.

## Separação de responsabilidades

Os módulos matemáticos não devem depender da camada de visualização ou de execução de ordens. O FGSE agrega estimativas e indicadores de qualidade; não converte automaticamente uma classificação em ordem.

## Causalidade

Cada atualização usa somente observações disponíveis até o fechamento do tijolo corrente. A janela móvel pode produzir uma nova estimativa a cada atualização, mas decisões já emitidas devem permanecer registradas como foram conhecidas naquele instante.

## Limitação do eixo Renko

A FFT sobre sequência de tijolos estima periodicidade em eventos Renko, não em segundos ou minutos. O timestamp deve ser preservado para análises em tempo cronológico separadas.
