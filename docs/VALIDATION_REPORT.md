# Validation report

## Verified mathematical checkpoints

- Synthetic robustness CI: SUCCESS, run 45062469716.
- Band-limited spectral metrics CI: SUCCESS, run 45062857043.
- These validate only the synthetic tests at their respective commits.

## B3-aligned offline market data boundary

- Typed trade events and instrument identity were added.
- Event timestamps must be timezone-aware.
- OBSERVED / PROXY / UNKNOWN aggressor provenance is enforced.
- Sequence audit detects gaps, duplicates and out-of-order arrivals.
- The CSV adapter reads user-supplied local files only.
- Initial CI exposed a test expectation issue: duplicate repeats were also counted as out-of-order. The rule and test were clarified to avoid double-counting.
- Corrected CI: SUCCESS, run 45063506164, commit 9b78cefc4442ff725844c24c91a79b92a6b84746 (2026-11-22). The `mathematical-tests` job completed successfully, including mathematical, causality and market-data tests.

## B3 source interpretation

Reviewed private project contracts:
- CONTRATO_DADOS_B3_V2.0.md
- CONTRATO_CANONICO_INGESTAO_FONTES_EXTERNAS_V2.0.md
- ARQUITETURA_DUAL_COTAHIST_NEGOCIOS_INTRADIARIOS_2026-11-05.md
- PROVEDORES_E_GRANULARIDADE.md
- ativos/futuros/README.md

COTAHIST is daily consolidated data, not tick-by-tick. Trade events and order-book feeds have separate contracts and granularities. Tick direction is not treated as aggressor side. UMDF, FIX/FAST, historical replay and other channels require independent entitlement evidence.

## Not certified

- No Profit Pro export has been inspected.
- No WINFUT Renko 30R event series has been validated.
- No real-time provider connection exists.
- No acquisition, storage licence, retention right or redistribution right is inferred.
- No profitability or operational performance claim is made.
- No NTSL equivalence or BrickMaster integration has been performed.