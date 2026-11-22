# Roadmap

## FASE 0 — Reconhecimento e baseline
CONCLUÍDA: repositório reconhecido, licença MIT preservada, governança e arquitetura inicial documentadas.

## FASE 1 — Núcleo matemático Python
EM IMPLEMENTAÇÃO: FFT, regressão harmônica, amplitude/fase e métricas espectrais implementadas em baseline 0.2.0; testes sintéticos iniciais adicionados. Pendentes testes avançados, revisão e execução reproduzível da suíte.

Critério de saída: testes matemáticos de referência e casos degenerados aprovados.

## FASE 2 — Dados WINFUT Renko 30R
Adaptador e validação do contrato com exportações reais do Profit. Documentar regra Renko, timestamps, volume e origem.

## FASE 3 — Indicadores e FGSE
Implementar FCD, FHO, FES, FED, FRC e agregador FGSE.

## FASE 4 — Validação estatística
Causalidade, estabilidade, walk-forward, falsos positivos e análise econômica com custos.

## FASE 5 — NTSL
Portar componentes viáveis e comparar NTSL com referência Python; validar no Profit Pro.

## FASE 6 — Integração controlada com BrickMaster
Somente após certificação; inicialmente observacional/simulação, sem envio de ordens.
