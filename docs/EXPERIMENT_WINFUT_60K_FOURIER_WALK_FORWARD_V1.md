# WINFUT 60K Trades — Fourier walk-forward experiment V1

**Status:** exploratory research; not a live strategy or profitability certification.  
**Input:** local Profit One XLSX export, SHA-256 `497e28690131332e36d81893d9d28a7df5f5100b20054661919e6bd4cd957235`.  
**Data used:** 13,390 OHLC rows across 147 sessions. Only `Data`, `Fechamento` and `Contador de Candles` were used. The proprietary XLSX was not committed.

## Experiment

- User-declared bar construction: exactly 60,000 trades per completed candle.
- Event-time sampling: one sample per 60K-trade candle; frequency is measured in cycles per bar, not cycles per minute.
- Returns: close-to-close point changes, reset at each session.
- Rolling lookback: 64 returns.
- Spectral search: dominant FFT peak with Hann window, periods 6–32 bars.
- Forecast: least-squares harmonic regression at the selected frequency; forecast one bar ahead.
- Execution assumption: direction selected at current close, evaluated over the next close-to-close bar. No overnight carry.
- Chronological split: first 70% of sessions with forecasts for IS; final 30% for OOS.
- Benchmarks: sign of the trailing 8-return mean and sign of the last return.
- Cost sensitivity: hypothetical round-trip deductions of 10, 20 and 40 index points per trade.

## Results

### Out-of-sample (last 30%)

| Metric | Fourier harmonic | Momentum 8 | Momentum 1 |
|---|---:|---:|---:|
| Trades | 2,012 | 2,001 | 1,996 |
| Directional hit rate | 52.04% | 49.93% | 48.95% |
| Gross points | +15,100.11 | -8,712.41 | -4,996.87 |
| Average points/trade | +7.51 | -4.35 | -2.50 |
| Profit factor | 1.088 | 0.952 | 0.972 |

Fourier gross points after hypothetical round-trip costs:

| Cost assumption | OOS points |
|---|---:|
| 0 points/trade | +15,100.11 |
| 10 points/trade | -5,019.89 |
| 20 points/trade | -25,139.89 |
| 40 points/trade | -65,379.89 |

The gross break-even cost ceiling is approximately **7.51 points per trade**, before any unmodelled execution effects. Therefore this first configuration is **not economically viable under a 10-point round-trip cost assumption**.

### In-sample (first 70%)

| Metric | Fourier harmonic | Momentum 8 | Momentum 1 |
|---|---:|---:|---:|
| Trades | 2,002 | 1,994 | 1,982 |
| Directional hit rate | 51.40% | 49.30% | 49.39% |
| Gross points | +13,214.05 | -668.54 | -5,998.98 |
| Average points/trade | +6.60 | -0.34 | -3.03 |
| Profit factor | 1.096 | 0.995 | 0.959 |

## Spectral observations

- Median selected dominant period: **10.67 bars**.
- Median in-band spectral concentration: **0.273**.
- Most frequent selected periods: 6.40 bars (575 windows), 7.11 (518), 21.33 (448), 9.14 (440), 10.67 (439).
- The spread of selected periods indicates that the dominant frequency is not stable enough to be treated as a fixed market cycle. This is a rolling local estimate, not evidence of a persistent physical cycle.

## Uncertainty and interpretation

- OOS daily mean: approximately **+351 points/session**.
- 58.14% of OOS sessions were positive.
- Session-block bootstrap 95% interval for mean daily points: **[-121, +863]**, which includes zero.
- The small directional edge is therefore not yet statistically or economically established.
- This is a one-step exploratory test with one fixed parameter set. It is not a parameter search, not an optimized strategy and not a final holdout test.
- The result depends on a close-to-close execution assumption. It does not model intrabar order, bid/ask spread, queue priority, fees, real slippage, partial bars or contract sizing.
- The fixed 60K-trade bar size gives a meaningful event-time index, but does not make bars equally spaced in calendar time.

## Next experiments

1. Test the same causal framework with 32/96/128-bar windows and compare stability without selecting parameters on the OOS set.
2. Evaluate cycle persistence: peak-frequency drift, phase stability, concentration and out-of-sample forecast decay.
3. Add a no-trade/abstention state and compare coverage versus expectancy.
4. Add execution cost in points from actual WINFUT contract economics and realistic spread/slippage assumptions.
5. Evaluate session-level and regime-level performance, drawdown and tail risk.
6. Preserve a final untouched chronological test segment after the experiment design is frozen.

## Reproduction

Install analysis dependencies and run locally against the original XLSX (do not commit the market data):

```bash
python -m pip install -e ".[analysis,excel]"
python experiments/winfut_60k_fourier_walkforward.py "/path/to/FASE 2 — WINFUT(1).xlsx" --output result.json
```
