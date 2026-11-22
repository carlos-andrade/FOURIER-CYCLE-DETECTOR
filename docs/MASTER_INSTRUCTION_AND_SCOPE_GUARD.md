# Master Instruction and Scope Guard

Project: FOURIER CYCLE DETECTOR. Human-readable operating contract. Agent contract: AGENTS.md. Reusable skill: .github/skills/fourier-indicator-engineering/SKILL.md.

## Mission
Design original Fourier mathematical indicators for Profit One. Initial context: WINFUT, 60K Trades (60000T), one completed candle per 60,000 trades. This is indicator engineering. Strategy and order execution are separate, opt-in workstreams.

## Indicator portfolio
| Component | Responsibility | Outputs |
|---|---|---|
| FCD | Dominant cycle detection | Dominant frequency, period in bars, quality |
| FHO | Harmonic behaviour | Amplitude, phase, phase change |
| FES | Spectral energy | Energy by band, concentration, dispersion |
| FED | Structural events | Frequency shift, amplitude collapse, phase discontinuity |
| FRC | Regime classification | Persistent cycle, transition, noise, no identifiable cycle |
| Fourier Gyroscope | Integration | Coherent analytical state and visual dashboard |

These are target responsibilities. Each requires its own mathematical contract; listing is not proof of implementation.

## Development gates
G0 Purpose → G1 Mathematical specification → G2 Python reference → G3 synthetic, robustness and causality validation → G4 Profit One visual contract → G5 NTSL parity → G6 integration. A gate passes only with evidence.

## Sampling model
60K Trades is event-indexed. Candle index is the default sampling coordinate. Calendar spacing varies. Express frequency and period in candles/cycles per candle unless a validated time-normalization method is introduced.

## Out of scope by default
Buy/sell rules, automated orders, broker integrations, P&L optimization, profitability claims, switching to Renko/time bars, or treating candle sequence as individual trade count.

## AI operating protocol
Before substantial work, identify indicator, stage, deliverable and validation. Read AGENTS.md and relevant existing docs. On "continue", inspect roadmap and repository state and resume the next incomplete indicator. Do not restart, create parallel architecture, or pivot to strategy work.

Only the owner can authorize changes to mission, instrument, platform, chart basis, indicator portfolio or strategy/execution scope. Document explicit scope changes.

## Completion report
Indicator/stage; files changed; mathematical behaviour; tests/results; Profit One/NTSL status; limitations; next indicator task.

Permanent rule: FOURIER CYCLE DETECTOR CREATES INDICATORS.
