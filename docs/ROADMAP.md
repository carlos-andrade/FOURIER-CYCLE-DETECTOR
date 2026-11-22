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

## FASE 2 — Dados WINFUT Renko 30R
Bloqueio: requer exportação local do Profit Pro e validação semântica do contrato, incluindo construção Renko, timestamps, preço, sessão e origem. COTAHIST não substitui intraday.

## FASE 3 — FCD, FHO, FES, FED, FRC e FGSE
Implementar estados com abstenção explícita, qualidade, causalidade e validade.

## FASE 4 — Validação estatística
Walk-forward, análise fora da amostra, estabilidade, falsos positivos, custos e slippage.

## FASE 5 — NTSL
Portar somente componentes com equivalência numérica testável em relação ao Python.

## FASE 6 — Integração controlada BrickMaster
Apenas após certificação; inicialmente observacional/simulação, sem envio de ordens.