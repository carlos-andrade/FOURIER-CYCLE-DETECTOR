"""First causal reference implementation of the Fourier indicator family.

All frequencies are measured in cycles per completed 60K Trades bar.
This module is analytical only: it does not generate orders or trading signals.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np
from numpy.typing import NDArray

FloatArray = NDArray[np.float64]


@dataclass(frozen=True)
class FCDResult:
    dominant_frequency: FloatArray
    dominant_period_bars: FloatArray
    peak_power_share: FloatArray
    valid: NDArray[np.bool_]


@dataclass(frozen=True)
class FHOResult:
    amplitude: FloatArray
    phase_radians: FloatArray
    oscillator: FloatArray
    valid: NDArray[np.bool_]


@dataclass(frozen=True)
class FESResult:
    total_power: FloatArray
    normalized_entropy: FloatArray
    concentration: FloatArray
    band_power_share: dict[str, FloatArray]
    valid: NDArray[np.bool_]


@dataclass(frozen=True)
class FEDResult:
    frequency_shift: FloatArray
    relative_amplitude_change: FloatArray
    event: NDArray[np.str_]
    valid: NDArray[np.bool_]


@dataclass(frozen=True)
class FRCResult:
    regime: NDArray[np.str_]
    confidence: FloatArray
    valid: NDArray[np.bool_]


@dataclass(frozen=True)
class FourierIndicatorSet:
    fcd: FCDResult
    fho: FHOResult
    fes: FESResult
    fed: FEDResult
    frc: FRCResult


def _validate(values: Iterable[float], window: int, min_period: int,
              max_period: int) -> FloatArray:
    x = np.asarray(values, dtype=np.float64)
    if x.ndim != 1:
        raise ValueError("values must be a one-dimensional sequence")
    if window < 16:
        raise ValueError("window must be >= 16 bars")
    if min_period < 2 or max_period <= min_period:
        raise ValueError("require 2 <= min_period < max_period")
    if max_period > window:
        raise ValueError("max_period cannot exceed window")
    if not np.all(np.isfinite(x)):
        raise ValueError("values must be finite; handle missing bars explicitly")
    return x


def _spectrum(segment: FloatArray, min_period: int,
              max_period: int) -> tuple[FloatArray, FloatArray, FloatArray]:
    """Return positive frequencies, one-sided power and windowed coefficients."""
    n = segment.size
    t = np.arange(n, dtype=np.float64)
    # Remove local linear trend; this reduces low-frequency leakage.
    slope, intercept = np.polyfit(t, segment, 1)
    residual = segment - (slope * t + intercept)
    taper = np.hanning(n)
    coeff = np.fft.rfft(residual * taper)
    frequencies = np.fft.rfftfreq(n, d=1.0)
    power = np.abs(coeff) ** 2
    if power.size > 2:
        power[1:-1] *= 2.0
    allowed = (frequencies >= 1.0 / max_period) & (
        frequencies <= 1.0 / min_period
    )
    allowed[0] = False
    return frequencies, power, allowed


def _dominant(segment: FloatArray, min_period: int,
              max_period: int) -> tuple[float, float, float, FloatArray, FloatArray]:
    frequencies, power, allowed = _spectrum(segment, min_period, max_period)
    total = float(power[allowed].sum())
    if not np.any(allowed) or total <= np.finfo(float).eps:
        return np.nan, np.nan, 0.0, frequencies, power
    candidates = np.flatnonzero(allowed)
    peak_idx = int(candidates[np.argmax(power[allowed])])
    frequency = float(frequencies[peak_idx])
    share = float(power[peak_idx] / total)
    return frequency, 1.0 / frequency, share, frequencies, power


def fcd(values: Iterable[float], window: int = 128, min_period: int = 8,
        max_period: int = 64) -> FCDResult:
    """Causal rolling dominant-cycle detector (period in bars)."""
    x = _validate(values, window, min_period, max_period)
    size = x.size
    freq = np.full(size, np.nan)
    period = np.full(size, np.nan)
    share = np.full(size, np.nan)
    valid = np.zeros(size, dtype=bool)
    for end in range(window - 1, size):
        segment = x[end - window + 1:end + 1]
        f, p, q, _, _ = _dominant(segment, min_period, max_period)
        if np.isfinite(f):
            freq[end], period[end], share[end], valid[end] = f, p, q, True
    return FCDResult(freq, period, share, valid)


def fho(values: Iterable[float], window: int = 128, min_period: int = 8,
        max_period: int = 64) -> FHOResult:
    """Causal harmonic fit at the FCD dominant frequency."""
    x = _validate(values, window, min_period, max_period)
    size = x.size
    amplitude = np.full(size, np.nan)
    phase = np.full(size, np.nan)
    oscillator = np.full(size, np.nan)
    valid = np.zeros(size, dtype=bool)
    for end in range(window - 1, size):
        segment = x[end - window + 1:end + 1]
        frequency, _, _, _, _ = _dominant(segment, min_period, max_period)
        if not np.isfinite(frequency):
            continue
        t = np.arange(window, dtype=np.float64)
        design = np.column_stack((
            np.ones(window), t, np.cos(2.0 * np.pi * frequency * t),
            np.sin(2.0 * np.pi * frequency * t)
        ))
        beta, *_ = np.linalg.lstsq(design, segment, rcond=None)
        cosine, sine = float(beta[2]), float(beta[3])
        amp = float(np.hypot(cosine, sine))
        phase_offset = float(np.arctan2(sine, cosine))
        current_phase = float(
            np.angle(np.exp(1j * (2.0 * np.pi * frequency * (window - 1)
                                 - phase_offset)))
        )
        amplitude[end] = amp
        phase[end] = current_phase
        oscillator[end] = (
            cosine * np.cos(2.0 * np.pi * frequency * (window - 1))
            + sine * np.sin(2.0 * np.pi * frequency * (window - 1))
        )
        valid[end] = True
    return FHOResult(amplitude, phase, oscillator, valid)


def fes(values: Iterable[float], window: int = 128, min_period: int = 8,
        max_period: int = 64,
        bands: dict[str, tuple[int, int]] | None = None) -> FESResult:
    """Causal spectral energy distribution, entropy and peak concentration."""
    x = _validate(values, window, min_period, max_period)
    definitions = bands or {
        "fast": (min_period, max(min_period, (min_period + max_period) // 3)),
        "medium": (max(min_period, (min_period + max_period) // 3 + 1),
                   max(min_period, 2 * (min_period + max_period) // 3)),
        "slow": (max(min_period, 2 * (min_period + max_period) // 3 + 1),
                 max_period),
    }
    for name, (low_period, high_period) in definitions.items():
        if low_period < min_period or high_period > max_period:
            raise ValueError(f"period band outside configured range: {name}")
        if high_period < low_period:
            raise ValueError(f"invalid period band: {name}")
    size = x.size
    total = np.full(size, np.nan)
    entropy = np.full(size, np.nan)
    concentration = np.full(size, np.nan)
    shares = {name: np.full(size, np.nan) for name in definitions}
    valid = np.zeros(size, dtype=bool)
    for end in range(window - 1, size):
        frequencies, power, allowed = _spectrum(
            x[end - window + 1:end + 1], min_period, max_period
        )
        selected = power[allowed]
        energy = float(selected.sum())
        if selected.size == 0 or energy <= np.finfo(float).eps:
            continue
        probabilities = selected / energy
        h = -float(np.sum(probabilities * np.log(probabilities + 1e-15)))
        entropy[end] = h / np.log(probabilities.size) if probabilities.size > 1 else 0.0
        concentration[end] = float(probabilities.max())
        total[end] = energy
        for name, (low_period, high_period) in definitions.items():
            band = (frequencies >= 1.0 / high_period) & (
                frequencies <= 1.0 / low_period
            )
            band &= allowed
            shares[name][end] = float(power[band].sum() / energy)
        valid[end] = True
    return FESResult(total, entropy, concentration, shares, valid)


def fed(cycle: FCDResult, harmonic: FHOResult,
        frequency_shift_threshold: float = 0.20,
        amplitude_collapse_threshold: float = -0.35) -> FEDResult:
    """Detect material changes versus the immediately preceding valid bar."""
    if not 0.0 < frequency_shift_threshold < 1.0:
        raise ValueError("frequency_shift_threshold must be between 0 and 1")
    if not -1.0 < amplitude_collapse_threshold < 0.0:
        raise ValueError("amplitude_collapse_threshold must be between -1 and 0")
    n = cycle.valid.size
    shift = np.full(n, np.nan)
    amplitude_change = np.full(n, np.nan)
    event = np.full(n, "NONE", dtype="<U24")
    valid = np.zeros(n, dtype=bool)
    for i in range(1, n):
        if not (cycle.valid[i] and cycle.valid[i - 1]
                and harmonic.valid[i] and harmonic.valid[i - 1]):
            continue
        previous = cycle.dominant_frequency[i - 1]
        current = cycle.dominant_frequency[i]
        shift[i] = abs(current - previous) / previous if previous else np.nan
        old_amp = harmonic.amplitude[i - 1]
        new_amp = harmonic.amplitude[i]
        amplitude_change[i] = (
            (new_amp - old_amp) / old_amp if old_amp > 1e-12 else np.nan
        )
        if np.isfinite(shift[i]) and shift[i] >= frequency_shift_threshold:
            event[i] = "FREQUENCY_SHIFT"
        elif (np.isfinite(amplitude_change[i])
              and amplitude_change[i] <= amplitude_collapse_threshold):
            event[i] = "AMPLITUDE_COLLAPSE"
        valid[i] = True
    return FEDResult(shift, amplitude_change, event, valid)


def frc(spectrum: FESResult, events: FEDResult,
        persistent_concentration: float = 0.35,
        noise_entropy: float = 0.85) -> FRCResult:
    """Conservative descriptive regime labels; no directional/trade meaning."""
    if not 0.0 < persistent_concentration <= 1.0:
        raise ValueError("persistent_concentration must be in (0, 1]")
    if not 0.0 <= noise_entropy <= 1.0:
        raise ValueError("noise_entropy must be in [0, 1]")
    n = spectrum.valid.size
    regime = np.full(n, "WARMUP", dtype="<U28")
    confidence = np.full(n, np.nan)
    valid = spectrum.valid.copy()
    for i in range(n):
        if not valid[i]:
            continue
        concentration = spectrum.concentration[i]
        entropy = spectrum.normalized_entropy[i]
        confidence[i] = max(0.0, min(1.0, concentration * (1.0 - entropy)))
        if events.valid[i] and events.event[i] != "NONE":
            regime[i] = "TRANSITION"
        elif entropy >= noise_entropy:
            regime[i] = "NOISE"
        elif concentration >= persistent_concentration:
            regime[i] = "PERSISTENT_CYCLE"
        else:
            regime[i] = "NO_IDENTIFIABLE_CYCLE"
    return FRCResult(regime, confidence, valid)


def calculate_indicators(values: Iterable[float], window: int = 128,
                         min_period: int = 8,
                         max_period: int = 64) -> FourierIndicatorSet:
    """Calculate the first integrated, causal version of the five indicators."""
    x = _validate(values, window, min_period, max_period)
    cycle = fcd(x, window, min_period, max_period)
    harmonic = fho(x, window, min_period, max_period)
    spectrum = fes(x, window, min_period, max_period)
    events = fed(cycle, harmonic)
    regimes = frc(spectrum, events)
    return FourierIndicatorSet(cycle, harmonic, spectrum, events, regimes)
