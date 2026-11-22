# FOURIER INDICATORS — VERSION 1.0 (REFERENCE PYTHON)

**Status:** first integrated prototype; not certified for operational use in Profit One.  
**Scope:** mathematical indicator implementation only.  
**Input context:** WINFUT, completed 60K Trades bars, one observation per completed bar.

## 1. Purpose and conventions

Version 1 establishes a common causal reference implementation for FCD, FHO, FES, FED and FRC. It consumes a one-dimensional series of completed-bar observations. The caller must choose and document the input series (for example, close); this implementation does not silently choose or transform OHLC.

All spectral frequencies are **cycles per bar** and periods are **bars per cycle**. Calendar-time frequency is not inferred because event-time bars are not equally spaced in clock time.

The implementation rejects NaN and infinite values rather than silently interpolating or forward-filling them. The first valid result occurs after a complete rolling window.

## 2. Shared spectral method

For each trailing window of length (N):

1. Fit and remove a local linear trend by least squares.
2. Apply a Hann taper.
3. Calculate the real FFT.
4. Restrict the search to the configured period interval ([P_{min}, P_{max}]).
5. Exclude the zero-frequency component.
6. Calculate one-sided spectral power.

Defaults: (N=128), (P_{min}=8), (P_{max}=64) bars.

The FFT bin spacing is (1/N) cycles per bar. Consequently, period estimates are quantized to available FFT bins; they are not continuous-frequency estimates. Zero padding, interpolation and multi-taper methods are deliberately not included in V1.

## 3. FCD — Fourier Cycle Detector

Outputs:
- `dominant_frequency`: cycles per bar;
- `dominant_period_bars`: reciprocal of dominant frequency;
- `peak_power_share`: dominant-bin power divided by total power in the allowed band;
- `valid`: whether a non-zero spectral peak was available.

The dominant peak is the maximum-power FFT bin in the allowed period range. The peak share is a concentration diagnostic, not a probability that a cycle is real.

## 4. FHO — Fourier Harmonic Oscillator

Uses the FCD dominant frequency and fits, over the same trailing window:

[
x_t = eta_0 + eta_1t + acos(2pi ft) + bsin(2pi ft) + epsilon_t
]

Outputs:
- `amplitude`: (sqrt{a^2+b^2}), in the input series' units;
- `phase_radians`: fitted phase at the latest bar, wrapped to ([-pi,pi]);
- `oscillator`: fitted harmonic component at the latest bar;
- `valid`.

This is a rolling single-frequency harmonic fit. It is not a forecast and does not imply direction or a trade.

## 5. FES — Fourier Energy Spectrum

Outputs:
- `total_power`: summed one-sided power within the configured period range;
- `normalized_entropy`: Shannon entropy of normalized in-band power, divided by the maximum entropy;
- `concentration`: largest normalized spectral-bin power;
- `band_power_share`: power share for each caller-supplied period band;
- `valid`.

Default bands are fast, medium and slow partitions of the configured period range. For controlled comparisons, pass explicit non-overlapping period bands. Shares are calculated independently; overlapping user bands can therefore sum to more than one.

Entropy near zero indicates concentration in few bins; entropy near one indicates diffuse energy. Neither value alone proves a market regime.

## 6. FED — Fourier Event Detector

Compares each valid observation with the immediately preceding valid observation:
- relative change in dominant frequency;
- relative change in fitted harmonic amplitude;
- event label: `FREQUENCY_SHIFT`, `AMPLITUDE_COLLAPSE` or `NONE`.

Default thresholds: 20% relative frequency shift and -35% relative amplitude change. These are transparent engineering defaults, not empirically calibrated thresholds. Frequency shift has precedence if both conditions occur simultaneously.

## 7. FRC — Fourier Regime Classifier

Descriptive states:
- `WARMUP`: insufficient history or invalid spectrum;
- `TRANSITION`: FED reports a material event;
- `NOISE`: normalized spectral entropy is at least 0.85;
- `PERSISTENT_CYCLE`: peak concentration is at least 0.35 and no higher-priority state applies;
- `NO_IDENTIFIABLE_CYCLE`: valid spectrum without the above conditions.

Confidence is currently a bounded heuristic, concentration multiplied by one minus normalized entropy. It is not a calibrated statistical probability. Thresholds are provisional and must be validated against synthetic and real market regimes before use.

## 8. Causality and warm-up

Each output at index (t) uses only the trailing window ending at (t). No centered windows, future observations or full-sample normalization are used. Prefix-invariance tests compare a complete run with a run truncated at an earlier index.

Only completed bars should be supplied. The library cannot independently know whether a caller has passed an unfinished Profit One bar.

## 9. V1 limitations and explicit non-claims

- No NTSL implementation is included.
- No Python-to-Profit One numerical parity has been demonstrated.
- No empirical market-performance or profitability claim is made.
- No cycle is guaranteed to exist; invalid/warm-up states are retained.
- FFT resolution is limited by the window length.
- Hann taper and linear detrending reduce, but do not eliminate, spectral leakage.
- Rapidly changing frequency within a window can smear spectral energy.
- FED compares adjacent rolling estimates and can react to estimation noise.
- FRC thresholds and confidence are provisional heuristics.
- Missing bars are rejected; no gap repair is attempted.
- No time-domain spectral analysis is performed.
- The input series and its units must be selected by the caller and documented.
- The existing WINFUT export does not itself certify that each bar contains 60,000 trades; that source-data limitation remains separate from this event-index prototype.

## 10. Files

- `src/fourier_gyroscope/indicators_v1.py`: implementation.
- `tests/test_indicators_v1.py`: deterministic synthetic tests and prefix-invariance checks.
- `docs/FOURIER_INDICATORS_V1.md`: this specification.

## 11. Next engineering gates

1. Run the complete repository CI and fix any regression.
2. Expand tests for frequency drift, amplitude modulation, two-tone mixtures, white noise, low-amplitude cycles, abrupt transitions and session gaps.
3. Quantify period bias, leakage, false detections and phase error across a documented parameter matrix.
4. Decide the official input series and bar-completion contract for the Profit One adapter.
5. Design the visual contract for each indicator.
6. Port one indicator at a time to NTSL only after its Python behaviour is accepted; then compare bar-by-bar outputs.

No trading strategy or order execution is part of these gates.
