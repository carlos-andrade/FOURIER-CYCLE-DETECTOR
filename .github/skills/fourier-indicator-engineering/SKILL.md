---
name: fourier-indicator-engineering
description: Mandatory skill for all FOURIER CYCLE DETECTOR tasks. Designs, implements, validates and ports Fourier analytical indicators for Profit One on WINFUT 60K Trades; prevents drift into trading strategies and order execution.
---

# Fourier Indicator Engineering Skill

Read repository-root AGENTS.md first. It is the master project contract.

The deliverable is an INDICATOR, not a trading strategy. Fixed context: Profit One, WINFUT, 60K Trades. One completed candle is one 60,000-trade event-time sample; calendar spacing varies.

## Indicator family
FCD — Fourier Cycle Detector; FHO — Fourier Harmonic Oscillator; FES — Fourier Energy Spectrum; FED — Fourier Event Detector; FRC — Fourier Regime Classifier; Fourier Gyroscope — integrated analytical system. Do not invent or rename modules without owner approval.

## Workflow
1. State purpose and analytical question.
2. Define inputs, outputs, units, parameters and warm-up.
3. Write equations, assumptions and edge cases.
4. Implement Python reference.
5. Test synthetic signals with known frequencies, phases and amplitudes.
6. Test causality/prefix invariance.
7. Test noise, nonstationarity, frequency drift, missing bars and session boundaries.
8. Specify visual presentation in Profit One.
9. Port to NTSL only after Python validation.
10. Verify Python-to-NTSL parity.
11. Document the result.

## Default test scope
Signal-processing correctness, spectral leakage/resolution, phase continuity, amplitude calibration, persistence, transition detection, false positives, warm-up and numerical stability.

Do not default to entries/exits, P&L, Profit Factor, win rate, strategy optimization or order execution. These are separate workstreams and require an explicit request.

## Data rules
Use event index, not equal clock-time assumptions. Use completed 60K candles by default. Never confuse candle count with trade count, contract volume or financial volume. Exclude auxiliary indicator/strategy columns unless formula and causal provenance are proven. Never modify OHLC to force a tick grid or commit proprietary market data.

## Required task report
- Indicator
- Objective
- Mathematical deliverable
- Validation
- Profit One / NTSL impact
- Remaining limitations

If the user says "continue", continue the current indicator stage from repository state. Do not restart, create parallel architecture or pivot to strategy research.

Stop and ask before changing chart, instrument, platform, approved indicator family or entering strategy/execution work.

North star: indicator engineering for Profit One.
