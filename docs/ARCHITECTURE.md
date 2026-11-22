# Arquitetura

## Visão geral

Pipeline: série de barras 60K Trades do Profit One / dados de mercado → validação e pré-processamento → estimadores matemáticos → cinco módulos analíticos → Fourier Gyroscope State Engine (FGSE) → visualização/relatórios.

## Componentes

- core: contratos, pré-processamento e agregação de estado.
- mathematics: FFT, regressão harmônica, fase, janelamento e energia.
- indicators: FCD, FHO, FES, FED e FRC.
- market: adaptadores de barras 60K Trades e métricas de mercado (VWAP, TWAP, volume e delta, quando disponíveis).
- validation: walk-forward, causalidade, estabilidade e backtest.
- visualization: espectro, séries e painel de diagnóstico.
- ntsl: implementação posterior e testes de equivalência com Python.

## Separação de responsabilidades

Os módulos matemáticos não devem depender da camada de visualização ou de execução de ordens. O FGSE agrega estimativas e indicadores de qualidade; não converte automaticamente uma classificação em ordem.

## Eixo de amostragem e causalidade

A série primária do projeto é indexada por barras construídas pela contagem de negócios (configuração 60K Trades). A FFT aplicada ao índice de barras estima periodicidade em unidades de barras/trades; não deve ser interpretada diretamente como periodicidade em segundos ou minutos.

Os timestamps de início/fim devem ser preservados para análises em tempo cronológico separadas. A duração de cada barra pode variar conforme o fluxo de negócios. A validação deve usar somente observações disponíveis até ao fecho da barra corrente. Decisões já emitidas devem permanecer registadas como foram conhecidas naquele instante.

## Limites da fonte

A configuração declarada não substitui a inspeção da exportação real do Profit One. A semântica de trade_count, timestamps, volume, barra incompleta e sessão deve ser confirmada empiricamente antes da certificação do adaptador. Não assumir acesso a feed em tempo real ou direitos de aquisição/redistribuição.
