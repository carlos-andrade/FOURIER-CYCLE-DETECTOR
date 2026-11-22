# FOURIER CYCLE DETECTOR — MASTER INSTRUCTIONS

## Mission
We design, implement and validate mathematical market INDICATORS. We are not primarily building a trading strategy, robot, broker integration or order-execution system. The product is an original Fourier-based indicator family for Profit One, with Python as mathematical reference and NTSL as target implementation where supported.

Every task must serve indicator specification, mathematics, implementation, validation, visual design, NTSL porting or indicator integration. If a task does not serve this mission, classify it OUT_OF_SCOPE and ask before changing direction.

## Fixed context
- Initial instrument: WINFUT.
- Platform: Profit One.
- Chart: 60K Trades (60000T).
- Each completed candle represents exactly 60,000 trades, as specified by the project owner.
- One candle is one event-time observation. Elapsed calendar time between candles varies.
- Do not substitute Renko, time bars or another chart type unless the owner explicitly changes the specification.
- B3 repository: https://github.com/carlos-andrade/B3

## Approved indicator family
- FCD — Fourier Cycle Detector: dominant cycle/frequency and period in bars.
- FHO — Fourier Harmonic Oscillator: harmonic phase and amplitude behaviour.
- FES — Fourier Energy Spectrum: spectral energy distribution and concentration.
- FED — Fourier Event Detector: material changes in spectral/cycle structure.
- FRC — Fourier Regime Classifier: persistent cycle, transition, noise or no identifiable cycle.
- Fourier Gyroscope: integrated analytical view of the indicator family.

This is the approved target architecture. Do not rename, replace, reorder or expand it without explicit owner approval. Do not claim a module is implemented merely because it appears in this list.

## Required development sequence
For each indicator: define purpose; specify inputs, outputs, units, parameters, lookback and warm-up; document equations and edge cases; implement a Python reference; add deterministic synthetic tests; add causality/prefix-invariance tests; test noise, nonstationarity, frequency drift, missing bars and session boundaries; define Profit One visual semantics; port to NTSL only after Python validation; compare Python and Profit One outputs bar-by-bar; document and update roadmap.

## What tests mean here
Prioritize signal-processing correctness: spectral resolution/leakage, window effects, phase continuity, amplitude calibration, cycle persistence, frequency drift, transition detection, false positives, warm-up, numerical stability and causal behaviour.

A trading backtest, P&L optimization, Profit Factor, win rate, order simulation or strategy recommendation is NOT the default next step. Only perform strategy work if the owner explicitly requests a separate study. It must never replace indicator development.

## Data invariants
- Use event index, not uniform calendar-time assumptions.
- Use completed 60K candles by default.
- Never confuse candle count with trade count, contract quantity or financial volume.
- Never alter OHLC to force a tick grid.
- Do not use exported indicator/strategy columns as independent Fourier inputs unless formulas, provenance and causality are established.
- Never commit proprietary market exports.
- Unknown timestamp semantics do not block event-index experiments, but must be stated for calendar-time interpretations.

## Prohibited drift unless explicitly requested
Buy/sell rules, entry/exit strategy, automated orders, broker/order-routing integrations, P&L parameter optimization, profitability claims, changing instrument/platform/chart basis, Renko 30R, or skipping mathematical specification and tests.

## Mandatory response protocol
Classify each substantial task as INDICATOR_SPECIFICATION, INDICATOR_MATHEMATICS, INDICATOR_IMPLEMENTATION, INDICATOR_VALIDATION, NTSL_PORT, VISUAL_DESIGN, INTEGRATION, DOCUMENTATION or OUT_OF_SCOPE. Identify the indicator, objective, deliverable and validation method. If the user says "continue", inspect repository state and continue the next incomplete indicator task; do not reinterpret this as permission for strategy development.

## Source of truth
1. Explicit current instructions from the owner.
2. This AGENTS.md and approved governance.
3. Existing docs and specifications.
4. Existing tested code.
5. Assistant inference (lowest authority).

Resolve conflicts explicitly; never silently override project scope.

## Definition of done
Report files changed, mathematical behaviour delivered, tests and results, known limitations, and next indicator-development step.

NORTH STAR: build trustworthy mathematical indicators for Profit One. Do not turn this repository into a trading robot project.
