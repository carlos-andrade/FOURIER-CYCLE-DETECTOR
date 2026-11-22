"""Least-squares harmonic model and explicit phase convention."""
from dataclasses import dataclass
import numpy as np
from numpy.typing import ArrayLike, NDArray
from .validation import as_finite_1d

@dataclass(frozen=True)
class HarmonicFit:
    frequency: float
    angular_frequency: float
    cosine_coefficient: float
    sine_coefficient: float
    offset: float
    amplitude: float
    phase_radians: float
    fitted: NDArray[np.float64]
    residuals: NDArray[np.float64]
    rmse: float
    r_squared: float

def fit_harmonic(values: ArrayLike, frequency: float, *,
                 sample_positions: ArrayLike | None = None) -> HarmonicFit:
    """Fit x(t)=offset+a*cos(w*t)+b*sin(w*t).

    Convention: fitted=offset+amplitude*cos(w*t-phase), phase=atan2(b,a).
    Frequency is cycles/sample and must be in (0, 0.5].
    """
    x = as_finite_1d(values, min_size=3)
    if not np.isfinite(frequency) or not (0.0 < frequency <= 0.5):
        raise ValueError("frequency must be finite and in (0, 0.5]")
    if sample_positions is None:
        t = np.arange(x.size, dtype=float)
    else:
        t = np.asarray(sample_positions, dtype=float)
        if t.ndim != 1 or t.size != x.size or not np.all(np.isfinite(t)):
            raise ValueError("sample_positions must be finite, 1-D and match signal length")
    omega = 2*np.pi*float(frequency)
    design = np.column_stack((np.cos(omega*t), np.sin(omega*t), np.ones(x.size)))
    beta, _, _, _ = np.linalg.lstsq(design, x, rcond=None)
    a, b, offset = map(float, beta)
    fitted = design @ beta
    residuals = x - fitted
    rmse = float(np.sqrt(np.mean(residuals**2)))
    amplitude = float(np.hypot(a, b))
    phase = float(np.arctan2(b, a))
    total = float(np.sum((x-x.mean())**2))
    rss = float(np.sum(residuals**2))
    r2 = 1.0-rss/total if total > np.finfo(float).eps else 0.0
    return HarmonicFit(float(frequency), omega, a, b, offset, amplitude, phase,
                       fitted.astype(float), residuals.astype(float), rmse, float(r2))
