# Referência de dados B3 — FOURIER GYROSCOPE

A documentação privada de `carlos-andrade/B3` é a referência primária do projeto para contratos de dados brasileiros, proveniência, granularidade e restrições de acesso.

## Distinções normativas adotadas

- COTAHIST é histórico consolidado diário; não é uma fita tick-by-tick.
- Negócios individuais são eventos temporais com identidade, sequência e contexto de stream/canal.
- MBO, MBP, TOB e CONFLATED são granularidades distintas.
- Identidade do instrumento depende de identificador e fonte; ticker isolado não basta.
- Agressor OBSERVED, PROXY e UNKNOWN são estados distintos. Direção do tick não é automaticamente agressor.
- `event_at`, `information_available_at` e `received_at` são tempos distintos; backtest point-in-time exige disponibilidade demonstrável.
- Dados RAW, parsed e normalized devem manter hashes e linhagem próprios.

## Limites operacionais

Este componente trabalha somente com ficheiros locais fornecidos pelo utilizador. Não possui HTTP, scraping, UMDF, FIX/FAST, multicast, replay, scheduler ou download automático. A aprovação dos contratos B3 para modelagem não concede licença, entitlement ou autorização de aquisição/armazenamento/redistribuição.

## Documentos consultados no B3

- `docs/ingestao/CONTRATO_DADOS_B3_V2.0.md`
- `docs/ingestao/CONTRATO_CANONICO_INGESTAO_FONTES_EXTERNAS_V2.0.md`
- `docs/ingestao/ARQUITETURA_DUAL_COTAHIST_NEGOCIOS_INTRADIARIOS_2026-11-05.md`
- `dados/market_data/PROVEDORES_E_GRANULARIDADE.md`
- `ativos/futuros/README.md`
