# Governança do FOURIER CYCLE DETECTOR

## Escopo

Este repositório é a fonte oficial do projeto FOURIER CYCLE DETECTOR e do motor FOURIER GYROSCOPE. O ativo inicial é WINFUT, com gráfico de 60K Trades no Profit One como representação operacional de referência.

## Regras obrigatórias

1. Preservar histórico Git e licença existente.
2. Alterações relevantes devem ser rastreáveis por commits claros.
3. Código matemático deve possuir documentação, testes e critérios de aceitação.
4. Não declarar validação sem resultados reproduzíveis.
5. Separar pesquisa, validação histórica, simulação e operação.
6. Python é a implementação de referência; NTSL é uma implementação posterior sujeita a equivalência.
7. Não usar dados futuros, repaint retrospectivo ou seleção de parâmetros no conjunto final de teste.
8. Não enviar ordens nem integrar ao BrickMaster sem aprovação e certificação próprias.
9. Dados de mercado devem ter origem, contrato, timezone, regra de construção e limitações documentadas.
10. Não inventar dados ausentes nem inferir parâmetros do gráfico 60K Trades sem evidência.
11. Não confundir contagem de negócios (trade_count), quantidade de contratos/volume e volume financeiro.
12. Não alterar, arredondar ou reescalar preços de origem para forçar conformidade com uma grelha candidata.

## Estados de maturidade

- PROPOSED: especificação proposta.
- IMPLEMENTED: implementação disponível.
- TESTED: testes automatizados aprovados.
- VALIDATED: validação empírica documentada.
- CERTIFIED: critérios de certificação aprovados para escopo explicitamente definido.

Um estado superior não pode ser atribuído por inspeção visual.

## Revisões

Mudanças no modelo matemático, contrato de dados, causalidade ou critérios de aceitação exigem atualização da documentação e dos testes correspondentes.
