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
- Corrected CI: SUCCESS, run 45063506164, commit 9b78cefc4442ff725844c24c91a79b92a6b84746 (2026-11-22). The mathematical-tests job completed successfully, including mathematical, causality and market-data tests.

## Declared chart configuration

- Platform: Profit One.
- Chart: 60K Trades.
- This is the user-confirmed target configuration for the project.

## Initial inspection of the user-provided WINFUT workbook

- Workbook: FASE 2 — WINFUT.xlsx; sheet Folha1; 13,390 data rows and 65 columns.
- SHA-256: 5e0005c96f3642aa7dbf956cee62883a042057a6eb08b16b084537b266639c7f.
- Observed period: 2026-04-22 09:04 through 2026-11-19 18:07; 147 sessions.
- OHLC completeness and internal high/low/open/close consistency passed the initial structural checks.
- Candle counter restarts at 1 and is continuous within all 147 sessions.
- 27 timestamps repeat; exported precision is minute-level.
- 6,908 rows have at least one OHLC value that is not a multiple of 5.
- No explicit trade_count or volume column was identified. Two indicator columns, BMFB_001 and BMFB_002, are entirely empty.
- Detailed findings and limitations: docs/FASE2_DATASET_AUDIT.md.

## Interpretation

The workbook supports an initial structural audit of OHLC records and per-session candle counter continuity. It does not prove that each bar contains 60,000 trades. It does not provide explicit trade count or volume for reconciliation. Price tick conformity, timestamp semantics, instrument/contract identity, session boundaries and incomplete-bar behavior remain unresolved. The indicator output columns are not treated as primary market data.

## B3 source interpretation

Reviewed private project contracts:
- CONTRATO_DADOS_B3_V2.0.md
- CONTRATO_CANONICO_INGESTAO_FONTES_EXTERNAS_V2.0.md
- ARQUITETURA_DUAL_COTAHIST_NEGOCIOS_INTRADIARIOS_2026-11-05.md
- PROVEDORES_E_GRANULARIDADE.md
- ativos/futuros/README.md

COTAHIST is daily consolidated data, not tick-by-tick. Trade events and order-book feeds have separate contracts and granularities. Tick direction is not treated as aggressor side. UMDF, FIX/FAST, historical replay and other channels require independent entitlement evidence.

## Not certified

- The 60K Trades per-bar construction has not been empirically certified.
- OHLC price tick semantics have not been reconciled to the underlying instrument/export.
- No explicit per-bar trade_count or volume field has been validated.
- No real-time provider connection exists.
- No acquisition, storage licence, retention right or redistribution right is inferred.
- No profitability or operational performance claim is made.
- No NTSL equivalence or BrickMaster integration has been performed.
