"""Single-sided DFT spectrum with explicit amplitude normalization."""
from dataclasses import dataclass
import numpy as np
from numpy.typing import ArrayLike, NDArray
from .preprocessing import prepare_signal
from .validation import as_finite_1d

@dataclass(frozen=True)
class Spectrum:
    frequencies: NDArray[np.float64]
    complex_coefficients: NDArray[np.complex128]
    amplitude: NDArray[np.float64]
    power: NDArray[np.float64]
    dominant_frequency: float | None
    dominant_period: float | None
    total_power: float
    sample_count: int
    window: str
    removed_mean: float
    has_reliable_cycle: bool

def compute_spectrum(values: ArrayLike, *, window: str = "hann",
                     detrend: bool = True, min_frequency: float = 0.0,
                     max_frequency: float = 0.5,
                     variance_epsilon: float = 1e-12) -> Spectrum:
    """Frequency units are cycles/sample (cycles/brick for Renko sequences).

    Amplitude is peak amplitude corrected by window coherent gain. Power is
    squared magnitude of the windowed DFT and is for relative comparisons
    using the same length/window; it is not a calibrated PSD.
    """
    x = as_finite_1d(values, min_size=8)
    if not (0.0 <= min_frequency < max_frequency <= 0.5):
        raise ValueError("require 0 <= min_frequency < max_frequency <= 0.5")
    if variance_epsilon < 0:
        raise ValueError("variance_epsilon must be non-negative")
    y, w, removed_mean = prepare_signal(x, detrend=detrend, window=window)
    coeff = np.fft.rfft(y)
    freq = np.fft.rfftfreq(x.size, d=1.0)
    gain = float(np.sum(w))
    if gain <= 0:
        raise ValueError("window coherent gain must be positive")
    amp = np.abs(coeff) / gain
    if x.size % 2 == 0:
        if amp.size > 2:
            amp[1:-1] *= 2.0
    elif amp.size > 1:
        amp[1:] *= 2.0
    power = np.abs(coeff) ** 2
    eligible = ((freq > 0) & (freq >= min_frequency) & (freq <= max_frequency))
    reliable = bool(np.var(x) > variance_epsilon and np.any(eligible))
    dom_f = dom_p = None
    if reliable:
        ids = np.flatnonzero(eligible)
        peak = int(ids[np.argmax(power[ids])])
        dom_f = float(freq[peak])
        dom_p = 1.0 / dom_f
    return Spectrum(freq.astype(float), coeff.astype(complex), amp.astype(float),
                    power.astype(float), dom_f, dom_p, float(power.sum()),
                    int(x.size), window, removed_mean, reliable)
