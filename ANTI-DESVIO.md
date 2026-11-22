# ANTI-DESVIO — CONTRATO MESTRE DO FOURIER CYCLE DETECTOR

**Estado:** norma permanente de orientação do projeto  
**Repositório:** `carlos-andrade/FOURIER-CYCLE-DETECTOR`  
**Plataforma:** Profit One  
**Ativo inicial:** WINFUT  
**Gráfico obrigatório:** 60K Trades (60000T)

---

## 1. REGRA FUNDAMENTAL

**ESTAMOS A CRIAR INDICADORES MATEMÁTICOS. NÃO ESTAMOS A CRIAR UMA ESTRATÉGIA DE TRADING.**

O objetivo do FOURIER CYCLE DETECTOR é projetar, implementar e validar uma família de indicadores originais, baseados em análise de Fourier, para utilização no Profit One.

Toda decisão técnica, implementação, teste, documentação ou proposta deve respeitar este objetivo.

Não transformar, por iniciativa própria, o projeto num:
- robô de trading;
- sistema de compra e venda;
- estratégia de entradas e saídas;
- motor de execução de ordens;
- integração com corretoras;
- estudo de otimização de rentabilidade.

Esses assuntos só podem entrar mediante pedido explícito do proprietário e como trabalho separado. Nunca substituem o desenvolvimento dos indicadores.

## 2. CONTEXTO TÉCNICO FIXO

1. Ativo inicial: WINFUT.
2. Plataforma: Profit One.
3. Gráfico: 60K Trades (60000T).
4. Cada candle completo representa exatamente 60.000 trades, conforme configuração declarada pelo proprietário.
5. A amostragem é por evento: cada candle completo é uma observação.
6. O intervalo de relógio entre candles pode variar. Não presumir espaçamento temporal uniforme.
7. A unidade padrão de frequência e período é ciclos por candle e candles por ciclo.
8. Não substituir por Renko, gráfico temporal, gráfico de volume ou outra periodicidade sem autorização explícita.
9. Quando forem necessários dados da B3, usar o repositório de referência: https://github.com/carlos-andrade/B3.

## 3. FAMÍLIA OFICIAL DE INDICADORES

A arquitetura de referência do projeto é:

| Componente | Responsabilidade |
|---|---|
| **FCD — Fourier Cycle Detector** | Detetar ciclos dominantes, frequência e período estimado |
| **FHO — Fourier Harmonic Oscillator** | Acompanhar amplitude, fase e comportamento harmónico |
| **FES — Fourier Energy Spectrum** | Medir distribuição, concentração e dispersão da energia espectral |
| **FED — Fourier Event Detector** | Identificar alterações relevantes na estrutura cíclica |
| **FRC — Fourier Regime Classifier** | Classificar ciclo persistente, transição, ruído ou ausência de ciclo identificável |
| **Fourier Gyroscope** | Integrar e apresentar coerentemente as leituras dos indicadores |

Esta lista define a arquitetura aprovada. Não renomear, substituir, reordenar ou acrescentar componentes sem autorização explícita. A inclusão na arquitetura não significa que um indicador já esteja implementado ou certificado.

## 4. FLUXO OBRIGATÓRIO DE DESENVOLVIMENTO

Cada indicador deve passar pelas seguintes etapas:

1. **Objetivo:** declarar a pergunta analítica que o indicador pretende responder.
2. **Contrato:** definir entradas, saídas, unidades, parâmetros, janela e período de aquecimento.
3. **Matemática:** documentar equações, pressupostos, limites e casos extremos.
4. **Referência Python:** implementar o cálculo de referência, independente da interface do Profit.
5. **Testes sintéticos:** usar sinais conhecidos, com frequências, amplitudes e fases controladas.
6. **Causalidade:** provar que valores passados não dependem de observações futuras, incluindo testes de prefix invariance.
7. **Robustez:** testar ruído, não estacionariedade, deriva de frequência, dados ausentes e fronteiras de sessão.
8. **Validação numérica:** medir erro, estabilidade, resolução espectral, leakage e sensibilidade aos parâmetros.
9. **Desenho visual:** definir linhas, histogramas, bandas, estados, escalas e interpretação no Profit One.
10. **Portabilidade NTSL:** implementar apenas depois de validada a referência matemática.
11. **Paridade:** comparar os resultados Python e Profit One candle a candle, com tolerâncias explícitas.
12. **Documentação:** atualizar especificação, testes, limitações e roadmap.

Não saltar diretamente para NTSL sem especificação matemática. Não declarar uma etapa concluída sem evidências verificáveis.

## 5. O QUE SIGNIFICA TESTAR NESTE PROJETO

Os testes prioritários são testes de engenharia de sinais e de indicadores:

- precisão na deteção de frequência e período;
- resolução espectral;
- leakage e efeitos das janelas;
- calibração de amplitude;
- continuidade e estabilidade de fase;
- persistência e deriva dos ciclos;
- concentração e distribuição da energia;
- deteção de transições;
- falsos positivos em ruído;
- comportamento em regimes não estacionários;
- aquecimento, fronteiras e dados ausentes;
- causalidade e reprodutibilidade;
- equivalência entre Python e NTSL.

**Não confundir validação de indicador com backtest de estratégia.**

Profit Factor, taxa de acerto, P&L, otimização de entradas e saídas, simulação de ordens e rentabilidade não são o próximo passo automático. Só devem ser estudados se o proprietário solicitar expressamente uma investigação estratégica separada.

## 6. REGRAS DE DADOS

- Usar o índice de candles como eixo de observação.
- Por padrão, calcular sobre candles completos.
- Não tratar o tempo entre candles como constante.
- Não confundir contador de candles com contador de negócios.
- Não confundir número de trades, quantidade de contratos e volume financeiro.
- Não arredondar nem modificar OHLC para forçar uma grelha de preços.
- Não alimentar o núcleo Fourier com colunas auxiliares de indicadores ou estratégias sem conhecer fórmulas, proveniência e causalidade.
- Não publicar ficheiros proprietários de mercado no GitHub.
- Distinguir factos observados, declarações do proprietário, hipóteses e inferências.

## 7. PROTOCOLO ANTI-DESVIO PARA O ASSISTENTE

Antes de executar qualquer tarefa substancial, identificar:

- **TIPO:** especificação, matemática, implementação, validação, NTSL, desenho visual, integração ou documentação;
- **INDICADOR:** FCD, FHO, FES, FED, FRC ou Fourier Gyroscope;
- **OBJETIVO:** o que o indicador deve medir ou revelar;
- **ENTREGA:** fórmula, código, teste, especificação visual ou documentação;
- **VALIDAÇÃO:** como será demonstrado que o resultado está correto.

Se o pedido do proprietário for «PROSSIGA», «SIGA» ou «CONTINUE»:
1. consultar o estado atual do repositório;
2. ler este ficheiro e `AGENTS.md`;
3. verificar o roadmap e o trabalho já existente;
4. retomar a próxima tarefa incompleta de desenvolvimento de indicadores;
5. não reiniciar auditorias já concluídas sem motivo;
6. não interpretar a autorização para continuar como autorização para criar estratégias de trading.

Se a tarefa parecer exigir estratégia, ordens ou alteração do escopo, parar e pedir autorização. Não fazer essa mudança silenciosamente.

## 8. HIERARQUIA DE DECISÃO

Em caso de conflito, respeitar esta ordem:

1. instruções explícitas e atuais do proprietário;
2. este ficheiro `ANTI-DESVIO.md` e o contrato mestre `AGENTS.md`;
3. governança e especificações aprovadas em `docs/`;
4. implementação e testes existentes;
5. inferências do assistente.

Nunca substituir uma decisão explícita do proprietário por uma suposição do assistente.

## 9. CRITÉRIOS DE CONCLUSÃO

Toda entrega substancial deve informar:

1. indicador e etapa trabalhados;
2. ficheiros criados ou alterados;
3. comportamento matemático implementado;
4. testes executados e resultados;
5. estado da implementação no Profit One/NTSL;
6. limitações conhecidas;
7. próxima tarefa de desenvolvimento do indicador.

Não declarar sucesso sem testes. Não declarar integração sem confirmação no repositório. Não declarar equivalência NTSL sem comparação numérica.

## 10. DECLARAÇÃO FINAL — REGRA INEGOCIÁVEL

> **O FOURIER CYCLE DETECTOR EXISTE PARA CRIAR INDICADORES MATEMÁTICOS FOURIER PARA O PROFIT ONE.**
>
> O WINFUT em gráfico de 60K Trades é o contexto inicial.
>
> Python é a referência matemática; NTSL é o meio de implementação no Profit One, após validação.
>
> O Fourier Gyroscope integra os indicadores.
>
> Estratégias, rentabilidade e execução de ordens não definem nem substituem este projeto.

**Se uma tarefa não contribuir para projetar, implementar, validar, visualizar ou integrar os indicadores, não a executar como se fizesse parte do FOURIER CYCLE DETECTOR.**
