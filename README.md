# FOURIER CYCLE DETECTOR — FOURIER GYROSCOPE

Engine research for causal Fourier/harmonic market-state analysis, initially focused on WINFUT and Profit Pro Renko 30R.

## Governing principles
- Closed bricks only in operational evaluation; no look-ahead.
- FFT frequencies over Renko are cycles per brick, not cycles per second.
- Synthetic tests are not empirical market validation.
- No forced cycle declaration: insufficient/no-cycle states must remain possible.
- No automatic order execution.
- Python is the numerical reference implementation; later NTSL port requires equivalence tests.

## Data sources
For Brazilian exchange data contracts, provenance and access boundaries, the primary project reference is the private repository [carlos-andrade/B3](https://github.com/carlos-andrade/B3). See `docs/B3_DATA_REFERENCE.md`.
The implementation in `src/fourier_gyroscope/market_data` is offline-only and accepts local files. It does not connect to UMDF or distributors and does not acquire data.

## Current components
- Mathematical core: FFT, harmonic regression and spectral diagnostics.
- Market data boundary: typed instruments/trade events, explicit aggressor provenance, sequence continuity audit and CSV local adapter.
- Automated tests: mathematical, causality and market-data contracts.

## Project status
See `docs/ROADMAP.md` and `docs/VALIDATION_REPORT.md`.
