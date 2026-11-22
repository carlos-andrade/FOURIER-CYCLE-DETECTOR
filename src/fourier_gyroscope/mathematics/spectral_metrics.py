"""Relative spectral energy, concentration and normalized entropy."""
from dataclasses import dataclass
import numpy as np
from .fft_engine import Spectrum

@dataclass(frozen=True)
class SpectralMetrics:
    total_energy: float
    normalized_entropy: float
    energy_concentration: float
    probabilities: np.ndarray
    valid: bool

def compute_spectral_metrics(spectrum: Spectrum, *, exclude_dc: bool = True) -> SpectralMetrics:
    power = np.asarray(spectrum.power, dtype=float)
    if power.ndim != 1 or power.size == 0:
        raise ValueError("spectrum power must be a non-empty 1-D array")
    selected = power[1:] if exclude_dc and power.size > 1 else power.copy()
    selected = np.maximum(selected, 0.0)
    total = float(selected.sum())
    if selected.size < 2 or not np.isfinite(total) or total <= np.finfo(float).eps:
        return SpectralMetrics(total, 0.0, 0.0, np.zeros_like(selected), False)
    p = selected/total
    positive = p[p > 0]
    entropy = -float(np.sum(positive*np.log(positive)))/float(np.log(selected.size))
    concentration = float(np.max(p))
    return SpectralMetrics(total, float(np.clip(entropy, 0, 1)),
                           concentration, p.astype(float), True)
