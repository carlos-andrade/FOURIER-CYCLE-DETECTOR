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
- Project default configuration and package metadata now target 60K Trades bars; stale Renko 30R defaults were removed from README, mathematical model, technical specification, package metadata and market-data granularity enum.

## Initial inspection of the user-provided WINFUT workbook

- Workbook: FASE 2 — WINFUT.xlsx; sheet Folha1; 13,390 data rows and 65 columns.
- SHA-256: 5e0005c96f3642aa7dbf956cee62883a042057a6eb08b16b084537b266639c7f.
- Observed period: 2026-04-22 09:04 through 2026-11-19 18:07; 147 sessions.
- OHLC completeness and internal high/low/open/close consistency passed the initial structural checks.
- Candle counter restarts at 1 and is continuous within all 147 sessions.
- 27 timestamps repeat; exported precision is minute-level.
- 10,511 rows have at least one OHLC value that is not a multiple of 5 (recounted with Decimal arithmetic; previous 6,908 figure was incorrect).
- No explicit trade_count or volume column was identified. Two indicator columns, BMFB_001 and BMFB_002, are entirely empty.
- User confirmed the `Data` column timezone as `America/Sao_Paulo`; the six-column parser logic was applied to all 13,390 rows with zero parsing/OHLC/counter errors.
- After chronological sorting by timestamp and source counter, all 147 session counters are continuous; 27 duplicate-minute timestamp groups are preserved.
- Timestamp semantics remain UNKNOWN; timezone confirmation does not establish whether `Data` is bar-open or bar-close time.
- The 10,511 non-multiple-of-5 finding is a corrected Decimal-based recount; it is not a conclusion that those values are invalid.
- Detailed findings: docs/FASE2_DATASET_AUDIT.md.

## Offline XLSX bar model and adapter

- Added MarketBar with typed OHLC, source counter, timestamp semantics, optional trade_count/volume and raw-file SHA-256.
- Added iter_profit_one_xlsx, reading only the six source OHLC/counter columns and ignoring indicator outputs.
- The adapter requires an explicit IANA timezone and leaves timestamp semantics UNKNOWN unless supplied by the caller.
- It does not infer trade_count, volume, instrument tick size or 60K compliance.
- Added optional `excel` dependency and CI coverage.
- CI SUCCESS: run 45072681348, commit 602b8e07438d84f302cb0d625b4bb76aa6748c5e (2026-11-22); 36 tests passed.
- Latest test-suite CI SUCCESS: run [45075958293](https://github.com/carlos-andrade/FOURIER-CYCLE-DETECTOR/actions/runs/45075958293), commit `fcf0352475a4860f7b7fdddb3337f549c250f7d9`; 37 tests passed. The preceding run 45075888081 failed because the newly added test fixture violated OHLC bounds; the fixture was corrected and the subsequent full suite passed. The latest documentation-only commits do not change executable code.

## Temporal price-grid regime check

A deeper Decimal-based grouping by session found a sharply segmented pattern:

- 2026-04-22 through 2026-10-13: 121 sessions and 10,511 bars; every bar in this interval has at least one OHLC value not divisible by 5.
- 2026-10-14 through 2026-11-19: 26 sessions and 2,879 bars; no OHLC field in these bars violates divisibility by 5.
- Of the 10,511 affected bars, 10,443 have all four OHLC fields outside the 5-point grid; 68 have two or three affected fields.
- All 2,879 bars in the later interval have all four OHLC fields divisible by 5.

This is evidence of a temporal representation/regime break, not proof of its cause or proof that earlier prices are invalid. At the boundary, the final close on 2026-10-13 is 210,690.00 and the first open on 2026-10-14 is 210,500.00: the nominal price scale remains similar, so the observation does not look like a simple 1,000x unit conversion. This does not identify the cause or rule out other transformations. Do not round, rescale or rewrite source OHLC values. Reconcile source instrument/expiry, historical adjustment, export configuration and any transformation before certification.

## Interpretation

The workbook supports an initial structural audit of OHLC records and per-session candle counter continuity. It does not prove that each bar contains 60,000 trades. It does not provide explicit trade count or volume for reconciliation. Price tick conformity, timestamp semantics, instrument/contract identity, session boundaries and incomplete-bar behavior remain unresolved. The indicator output columns are not treated as primary market data.

## B3 source interpretation

Reopened B3 repository references:
- [CONTRATO_DADOS_B3_V2.0.md](https://github.com/carlos-andrade/B3/blob/main/docs/ingestao/CONTRATO_DADOS_B3_V2.0.md)
- [CONTRATO_CANONICO_INGESTAO_FONTES_EXTERNAS_V2.0.md](https://github.com/carlos-andrade/B3/blob/main/docs/ingestao/CONTRATO_CANONICO_INGESTAO_FONTES_EXTERNAS_V2.0.md)
- [ARQUITETURA_DUAL_COTAHIST_NEGOCIOS_INTRADIARIOS_2026-11-05.md](https://github.com/carlos-andrade/B3/blob/main/docs/ingestao/ARQUITETURA_DUAL_COTAHIST_NEGOCIOS_INTRADIARIOS_2026-11-05.md)
- [PARTE03_B3_INTRADAY_CONTRATO_V1.0.md](https://github.com/carlos-andrade/B3/blob/main/docs/ingestao/PARTE03_B3_INTRADAY_CONTRATO_V1.0.md)
- [PARTE03_B3_NEGOCIO_A_NEGOCIO_ESPECIFICACAO_V1.0.md](https://github.com/carlos-andrade/B3/blob/main/docs/ingestao/PARTE03_B3_NEGOCIO_A_NEGOCIO_ESPECIFICACAO_V1.0.md)
- [ativos/futuros/README.md](https://github.com/carlos-andrade/B3/blob/main/ativos/futuros/README.md)

The B3 V2 instrument contract requires instrument identity from an official identifier/source with temporal validity; contract expiry, multiplier, tick size, currency, segment and status are versioned attributes. A ticker or generic symbol alone is not a key. The inspected B3 futures catalogue currently supplies only the category-level README, not a WINFUT contract record with a dated tick-size value. Therefore this workbook cannot yet be matched to a specific instrument/expiry or certified against an authoritative tick size.

The B3 dual-ingestion architecture distinguishes daily consolidated COTAHIST from intraday trade events. COTAHIST is not a tick-by-tick substitute. Trade events and order-book feeds have separate contracts and granularities. Tick direction is not treated as aggressor side. UMDF/FIX/FAST and historical replay require independent entitlement evidence.

## Not certified

- The 60K Trades per-bar construction has not been empirically certified.
- OHLC price tick semantics have not been reconciled to the underlying instrument/export.
- No explicit per-bar trade_count or volume field has been validated.
- No real-time provider connection exists.
- No acquisition, storage licence, retention right or redistribution right is inferred.
- No profitability or operational performance claim is made.
- No NTSL equivalence or BrickMaster integration has been performed.
