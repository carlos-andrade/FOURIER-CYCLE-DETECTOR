# Roadmap — FOURIER GYROSCOPE

## FASE 0 — Reconhecimento e baseline
Estado: CONCLUÍDA.

## FASE 1 — Núcleo matemático Python
Estado: IMPLEMENTADO EM LABORATÓRIO; testes sintéticos aprovados em CI.
Inclui FFT, regressão harmônica, amplitude, fase, potência e métricas espectrais por banda.

## FASE 1.2 — Métricas espectrais por banda
Estado: CONCLUÍDA COM CI APROVADO.

## FASE 1.3 — Fronteira de dados B3 e ingestão offline
Estado: IMPLEMENTADA; CI APROVADA em 2026-11-22 (run 45063506164).
- Modelos tipados para identidade de instrumento e trade event.
- Separação explícita de agressor OBSERVED, PROXY e UNKNOWN.
- Preservação temporal: event_at, information_available_at e received_at.
- Auditoria de sequência por origem/stream/canal/escopo.
- Adaptador CSV local e read-only.
- Sem conectividade, scraping, feed, aquisição automática ou promoção de datasets.

## FASE 2 — Dados WINFUT em gráfico 60K Trades (Profit One)
Estado: AUDITORIA ESTRUTURAL INICIAL CONCLUÍDA COM RESSALVAS; PARSER XLSX IMPLEMENTADO E CI APROVADA; CERTIFICAÇÃO SEMÂNTICA PENDENTE.
- Configuração declarada pelo utilizador: Profit One, gráfico 60K Trades.
- Amostra Excel recebida e inspecionada; relatório em docs/FASE2_DATASET_AUDIT.md.
- 13.390 registos OHLC em 147 sessões, com contador contínuo por sessão.
- Parser XLSX offline implementado; exige timezone explícito, mantém semântica temporal UNKNOWN e não infere trade_count/volume.
- A amostra não contém trade_count nem volume explícito; portanto, não comprova 60.000 negócios por barra.
- 27 timestamps repetidos com precisão apenas ao minuto; 10.511 registos têm pelo menos um OHLC não múltiplo de 5 (recontagem decimal).
- Timezone da coluna Data confirmado pelo utilizador: America/Sao_Paulo; leitura validada em 13.390 registos sem erros.
- Semântica do timestamp permanece UNKNOWN: ainda não foi confirmado se Data representa abertura ou fecho da barra.
- Requer reconciliação da origem dos preços, semântica temporal, volume e contagem de negócios antes da certificação do adaptador.
- O contrato B3 V2 exige identidade oficial do instrumento com validade temporal e atributos versionados (vencimento, multiplicador, tick size, moeda, segmento e estado); o catálogo B3 consultado não contém atualmente um registo WINFUT datado que permita fechar essa reconciliação.
- A anomalia de grelha de 5 pontos concentra-se nas 121 sessões de 2026-04-22 a 2026-10-13; nas 26 sessões de 2026-10-14 a 2026-11-19 não ocorre. Causa não identificada; não corrigir os preços por arredondamento.
- Implementado diagnóstico reproduzível de grelha candidata por sessão (audit_candidate_price_grid), sem presumir tick oficial e sem modificar OHLC; CI aprovada (run 45078417762, 42 testes).
- Não confundir volume financeiro, quantidade de contratos e número de negócios.
- COTAHIST é dado diário consolidado e não substitui a série intradiária.

## FASE 2.1 — Reconciliação semântica e evidência de origem
Estado: ABERTA; BLOQUEADA POR EVIDÊNCIA EXTERNA À AMOSTRA ATUAL.
- Plano de trabalho e critérios de aceitação: docs/FASE2_1_RECONCILIATION_PLAN.md.
- Ficha estruturada para recolha de metadados e evidências: docs/FASE2_1_EVIDENCE_INTAKE.md.
- Workstreams: identidade/vencimento, construção 60K, trade_count/volume, semântica temporal, quebra da grelha de preços, sessões e direitos de uso.
- Reexportação adicional recebida em 2026-11-22 e auditada em docs/FASE2_REEXPORT_AUDIT_2026-11-22.md; mantém 13.390 registos/147 sessões, mas não inclui trade_count, quantidade de contratos nem volume financeiro explícitos.
- A reexportação está em ordem cronológica inversa; o contador de candles é sequencial por sessão, mas não representa número de negócios.
- Próxima dependência: captura da configuração do gráfico no Profit One, identificação do instrumento/vencimento e provedor, semântica temporal e exportação/documentação de campos de atividade/volume.
- Não alterar OHLC nem inferir trade_count, volume, tick oficial ou semântica temporal.
- Não certificar a FASE 2 até fechar os gates definidos no plano.

## FASE 3 — FCD, FHO, FES, FED, FRC e Fourier Gyroscope
Estado: V1 DE REFERÊNCIA IMPLEMENTADA; VALIDAÇÃO CI E ROBUSTEZ AMPLIADA PENDENTES.
- Primeira implementação integrada em `src/fourier_gyroscope/indicators_v1.py`.
- FCD: frequência dominante, período em candles e quota de potência do pico.
- FHO: amplitude, fase e oscilador harmónico ajustado na frequência dominante.
- FES: potência total, entropia normalizada, concentração e quotas por banda.
- FED: deteção de mudança relativa de frequência e colapso de amplitude.
- FRC: estados descritivos com warm-up, transição, ruído, ciclo persistente e ciclo não identificável.
- Especificação e limitações: `docs/FOURIER_INDICATORS_V1.md`.
- Testes iniciais determinísticos e prefix-invariance: `tests/test_indicators_v1.py`.
- Esta V1 é referência Python experimental; não está certificada, não tem port NTSL e não foi validada candle a candle no Profit One.
- Frequências em ciclos por candle; períodos em candles. Nenhuma hipótese de tempo de calendário uniforme.
- Próxima etapa: CI completa, expansão da matriz de sinais sintéticos e quantificação de erro, leakage, deriva e falsos positivos.

## FASE 4 — Validação estatística
Walk-forward, análise fora da amostra, estabilidade, falsos positivos, custos e slippage.

## FASE 5 — NTSL
Portar somente componentes com equivalência numérica testável em relação ao Python.

## FASE 6 — Integração controlada BrickMaster
Apenas após certificação; inicialmente observacional/simulação, sem envio de ordens.
