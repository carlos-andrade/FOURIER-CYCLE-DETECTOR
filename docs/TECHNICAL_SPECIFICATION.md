# Especificação técnica

## Escopo V1

WINFUT, dados Renko 30R exportados do Profit, pesquisa em Python e atualização em tijolos fechados. Sem execução de ordens.

## Parâmetros experimentais iniciais

- Janelas candidatas: 128 e 256 tijolos.
- Janela espectral: Hann.
- Frequência candidata: 1/64 a 1/4 ciclos por tijolo, sujeita a análise de resolução e sensibilidade.
- Harmônicos de reconstrução: até 3 como hipótese inicial.
- Atualização: fechamento de cada tijolo.
- Histórico mínimo: definido pelo maior requisito entre os módulos; não inferir validade só por atingir 256 observações.

Estes valores são parâmetros de laboratório, não parâmetros otimizados nem certificados.

## Saídas

Cada módulo deve retornar valores, estado de validade, timestamp/índice de referência, configuração, versão do algoritmo e métricas de qualidade.

## Desempenho

Medir latência por atualização, uso de memória e estabilidade numérica em dados reais e sintéticos. Otimização só após perfilamento.
