# FASE 2.1 — Plano de reconciliação semântica WINFUT 60K Trades

Estado: ABERTA — dependente de evidência de origem que ainda não consta da amostra auditada.

## Objetivo

Transformar a auditoria estrutural da amostra Profit One numa reconciliação semântica reproduzível. Esta fase não altera OHLC, não adquire dados externos e não certifica a construção 60K por presunção.

## Baseline imutável

- Plataforma declarada: Profit One.
- Gráfico declarado: 60K Trades.
- Ativo de trabalho: WINFUT, ainda sujeito à identificação do contrato/vencimento na exportação.
- Amostra auditada: `FASE 2 — WINFUT.xlsx`, SHA-256 `5e0005c96f3642aa7dbf956cee62883a042057a6eb08b16b084537b266639c7f`.
- Dimensão: 13.390 barras, 147 sessões, 2026-04-22 a 2026-11-19.
- Timezone informado para a coluna Data: `America/Sao_Paulo`.
- Semântica do timestamp: UNKNOWN.
- Não há colunas explícitas de trade_count ou volume na amostra.
- Não arredondar, reescalar, interpolar nem corrigir valores OHLC para satisfazer uma grelha candidata.

## Workstream A — Identidade do instrumento e contrato

Recolher evidência da exportação/plataforma que permita identificar:
- símbolo completo exibido no Profit One;
- vencimento/contrato efetivamente selecionado em cada período;
- eventual regra de série contínua, rolagem ou ajuste histórico;
- fonte/provedor e modalidade de dados;
- metadados oficiais aplicáveis ao instrumento e respetiva validade temporal.

Critério de aceitação: identidade inequívoca por intervalo temporal, compatível com o contrato canónico B3 V2. Ticker genérico isolado não é suficiente.

## Workstream B — Construção 60K Trades

Recolher uma nova exportação que preserve, quando disponível:
- OHLC;
- contador/índice original da barra;
- quantidade de negócios por barra (trade_count), ou eventos individuais que permitam contagem;
- volume negociado, com unidade documentada;
- início e fim da barra ou precisão temporal original;
- indicador explícito de barra em formação/incompleta, se a plataforma o disponibilizar.

Critério de aceitação: demonstrar como o Profit One constrói a barra de 60K Trades, incluindo comportamento de barras parciais, primeira/última barra da sessão e exportação no fim do período. Não substituir trade_count por contratos negociados ou volume financeiro.

## Workstream C — Semântica temporal

Confirmar documentalmente se a coluna Data representa:
- abertura da barra;
- fecho da barra;
- timestamp do último negócio;
- ou outro marco definido pelo Profit One/provedor.

Registar timezone IANA, precisão, comportamento em timestamps iguais e ordenação original. O timezone confirmado não resolve, por si só, a semântica temporal.

Critério de aceitação: definição inequívoca de timestamp e regra de ordenação, validada numa amostra com eventos/barra adjacentes.

## Workstream D — Quebra de regime da grelha de preços

Investigar a diferença observada:
- 2026-04-22 a 2026-10-13: 121 sessões com barras que apresentam campos OHLC não divisíveis por 5;
- 2026-10-14 a 2026-11-19: 26 sessões sem ocorrências dessa condição.

Hipóteses a testar sem as assumir como verdade: mudança de contrato/vencimento, ajuste de série contínua, alteração de fornecedor, configuração/exportação ou transformação intermediária.

Critério de aceitação: causa identificada por evidência de origem, ou anomalia formalmente classificada como não resolvida. O incremento 5 é apenas uma grelha candidata; não constitui prova do tick oficial. Valores originais permanecem imutáveis.

## Workstream E — Sessões e completude

Documentar calendário/horários aplicáveis, sessões overnight quando relevantes, interrupções, leilões, barras iniciais/finais e barras parciais. Não inferir sessão apenas pela data civil quando o instrumento exigir calendário de sessão.

Critério de aceitação: regra de sessão explícita e testes para limites de sessão, timestamps duplicados e barras incompletas.

## Evidência necessária para avançar

1. Nova exportação Profit One de uma amostra curta, com todos os campos de dados disponíveis (não apenas indicadores), incluindo trade_count e volume se a plataforma os disponibilizar.
2. Captura ou registo dos parâmetros do gráfico: símbolo completo, vencimento, tipo de gráfico 60K Trades, provedor e opções de exportação.
3. Confirmação do significado da coluna Data e da precisão temporal.
4. Evidência que explique a mudança observada em 14/10/2026, incluindo eventual rolagem/ajuste/alteração de fonte.
5. Documentação ou referência oficial que permita validar os atributos do contrato por validade temporal.

Não colocar dados proprietários, credenciais, tokens ou ficheiros cuja licença não permita redistribuição no Git. A amostra original permanece fora do repositório; usar fixtures sintéticas ou amostras autorizadas/anonimizadas.

## Matriz de decisão

| Dimensão | Estado atual | Evidência para fechar |
|---|---|---|
| Estrutura OHLC e contador | TESTED | Já coberta pela auditoria inicial |
| Identidade instrumento/vencimento | PENDING | Símbolo completo e metadados com validade |
| Construção 60K / trade_count | PENDING | Contagem por barra ou eventos individuais |
| Volume e unidade | PENDING | Campo documentado e reconciliação |
| Semântica temporal | PENDING | Definição do timestamp e precisão |
| Grelha/tick e quebra temporal | PENDING | Origem, contrato e transformação reconciliados |
| Sessões e barras parciais | PENDING | Calendário e regras de completude |
| Direitos de uso/armazenamento | PENDING | Evidência de licença/entitlement aplicável |

## Gate de saída

A FASE 2.1 só pode ser encerrada quando cada dimensão crítica estiver:
- VALIDATED com evidência reproduzível; ou
- explicitamente BLOCKED com causa, impacto e decisão de não certificação.

A FASE 2 não recebe estado CERTIFIED enquanto identidade, construção 60K, semântica temporal, proveniência dos preços e direitos de uso não estiverem resolvidos. CI verde de testes sintéticos não substitui este gate.

## Próxima ação

Aguardar a amostra/exportação e os metadados de configuração do Profit One. Após receção, executar reconciliação local, gerar fixtures autorizadas e atualizar `docs/FASE2_DATASET_AUDIT.md` e `docs/VALIDATION_REPORT.md` com resultados e hashes.
