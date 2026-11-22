# Especificação técnica

## Escopo V1

WINFUT, gráfico 60K Trades do Profit One, pesquisa em Python e atualização somente após o fechamento da barra. Sem execução de ordens.

## Parâmetros experimentais iniciais

- Janelas candidatas: 128 e 256 barras.
- Janela espectral: Hann.
- Frequência candidata: 1/64 a 1/4 ciclos por barra, sujeita a análise de resolução e sensibilidade.
- Harmônicos de reconstrução: até 3 como hipótese inicial.
- Atualização: fechamento de cada barra.
- Histórico mínimo: definido pelo maior requisito entre os módulos; não inferir validade só por atingir 256 observações.

Estes valores são parâmetros de laboratório, não parâmetros otimizados nem certificados.

## Saídas

Cada módulo deve retornar valores, estado de validade, timestamp/índice de referência, configuração, versão do algoritmo e métricas de qualidade.

## Desempenho

Medir latência por atualização, uso de memória e estabilidade numérica em dados reais e sintéticos. Otimização só após perfilamento.
