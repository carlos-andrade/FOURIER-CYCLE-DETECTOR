# INDICATOR V1 — VALIDATION MATRIX

**Purpose:** specify reproducible signal-engineering acceptance gates for FCD, FHO, FES, FED and FRC.  
**Out of scope:** trading entries/exits, P&L, win rate, broker execution and strategy optimization.

## 1. Test dimensions

| Dimension | Synthetic input | Expected observation | Required measurement |
|---|---|---|---|
| Exact-bin frequency | Single sinusoid with period aligned to an FFT bin | FCD returns the known bin | Absolute period and frequency error |
| Off-bin frequency | Sinusoid between FFT bins | Peak remains within half a native FFT frequency bin for the deterministic single-tone fixture; leakage is visible | Absolute frequency error, relative period error and peak-power share |
| Two-tone mixture | Two sinusoids with controlled amplitude ratio | Dominant peak follows stronger component when sufficiently separated | Dominant-component accuracy and resolution limit |
| Frequency drift | Linear chirp / gradual period change | FCD follows with lag and bounded smearing | Tracking lag, period error, transition duration |
| Abrupt frequency step | Two constant-frequency segments | FED can mark a transition; FCD eventually settles to new period | Detection delay, false transition count, settling time |
| Amplitude modulation | Slowly varying sinusoid amplitude | FHO tracks envelope with smoothing/lag | Relative amplitude error and lag |
| Amplitude collapse | Abrupt amplitude reduction | FED compares the smoothed FHO amplitude with a configurable lagged reference (64 bars by default) | Detection delay in completed bars and false positives |
| White noise | Fixed-seed Gaussian noise | No deterministic cycle is guaranteed | Entropy distribution, peak concentration, false persistent-cycle rate |
| Zero-energy input | Constant series after detrending | Indicator abstains | Invalid-state correctness |
| Trend-only input | Linear and nonlinear drift without cycle | No strong cycle should be asserted systematically | False-cycle rate |
| Session gap | Same event-index sequence with timestamp gap metadata | Core event-time calculation is unchanged; any time-domain treatment is separate | Explicit policy and no implicit bar insertion |
| Prefix extension | Same prefix with arbitrary future suffix | Historical values remain identical | Prefix-invariance exact/tolerance comparison |

## 2. Parameter matrix

The validation report must enumerate:
- windows: 64, 128, 256 and 512 bars where compatible with the configured period range;
- periods: exact-bin and off-bin values across the supported interval;
- amplitudes: multiple scales, including near-noise-floor cases;
- noise: zero, low, medium and high signal-to-noise ratios;
- frequency behaviour: stationary, gradual drift and abrupt step;
- phase: several initial phases across ([-pi,pi]).

The matrix must be deterministic and use fixed random seeds. Every run records the parameter tuple and software revision.

## 3. Acceptance principles

No universal threshold is asserted in advance. Before a threshold is adopted:
1. define the measurement and units;
2. estimate the baseline error on exact-bin signals;
3. measure off-bin and noisy degradation;
4. separate estimation lag from numerical error;
5. report false positives and abstentions, not only successful detections;
6. freeze thresholds on a calibration set and report results on a separate synthetic holdout set.

The existing V1 thresholds (20% frequency shift, -35% amplitude collapse, 64-bar amplitude reference, 0.35 concentration and 0.85 entropy) are provisional engineering defaults. They are not certified.

## 4. Numerical definitions to standardize

- Frequency error: `estimated_cycles_per_bar - true_cycles_per_bar`.
- Relative period error: `(estimated_period_bars - true_period_bars) / true_period_bars`.
- Amplitude relative error: `(estimated_amplitude - true_amplitude) / true_amplitude`, only when true amplitude is non-zero.
- Phase error: wrapped angular difference in radians under the documented cosine convention.
- Detection delay: number of completed bars between the known synthetic event and first qualifying FED event.
- False-event rate: non-event FED detections divided by known non-event opportunities.
- Abstention rate: invalid or no-cycle outcomes divided by evaluated windows.
- Prefix invariance: maximum absolute difference in historical numeric outputs, plus exact categorical equality.

## 5. Spectral power comparability

V1 `total_power` is raw windowed FFT power. Its magnitude depends on input units, window length and taper energy. Do not compare its absolute value across different window lengths or taper choices. A future normalized power/variance measure must be separately specified, tested and versioned; do not silently redefine the V1 field.

## 6. Gate to NTSL

NTSL implementation is not authorized by passing synthetic tests alone. Before porting an indicator:
- freeze its mathematical contract and parameter defaults;
- define missing-data and warm-up behaviour;
- establish reference fixtures with known expected outputs;
- define numeric tolerances;
- implement a candle-by-candle Python/NTSL parity harness;
- demonstrate parity over stationary, non-stationary, noisy and boundary cases.

The first NTSL port must be one indicator at a time. No visual or trading interpretation may override numerical mismatch.

## 7. Current status

The deterministic suite additionally checks an off-bin 18.5-bar sinusoid against a half-native-bin frequency-error bound and exact-bin period recovery at window lengths 64, 128, 256 and 512 bars. These are controlled single-tone fixtures, not general accuracy guarantees. The broader suite covers two-tone dominance, abrupt frequency change, amplitude collapse, white noise, zero-energy abstention and invalid FES bands. The FED amplitude-collapse comparison uses a 64-bar lag because the 128-bar FHO rolling fit smooths abrupt amplitude steps; the resulting detection delay is explicitly tested. The GitHub Actions workflow executes the complete `tests/` tree.

No V1 certification is claimed until the complete CI is green and the broader numerical matrix has been measured.
