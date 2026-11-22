"""Band-limited relative spectral energy, concentration and entropy."""
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
    selected_bin_count: int


def compute_spectral_metrics(
    spectrum: Spectrum,
    *,
    exclude_dc: bool = True,
    min_frequency: float | None = None,
    max_frequency: float | None = None,
) -> SpectralMetrics:
    """Compute relative metrics only over the requested frequency band.

    Bounds use cycles/sample (cycles/brick for Renko). The upper bound is
    inclusive. No reliability threshold is inferred from entropy or
    concentration; these are descriptive diagnostics, not a cycle verdict.
    """
    power = np.asarray(spectrum.power, dtype=float)
    frequencies = np.asarray(spectrum.frequencies, dtype=float)
    if power.ndim != 1 or power.size == 0 or frequencies.shape != power.shape:
        raise ValueError("spectrum frequencies and power must be matching non-empty 1-D arrays")
    if not np.all(np.isfinite(power)) or not np.all(np.isfinite(frequencies)):
        raise ValueError("spectrum values must be finite")
    if min_frequency is not None and (not np.isfinite(min_frequency) or min_frequency < 0):
        raise ValueError("min_frequency must be finite and non-negative")
    if max_frequency is not None and (not np.isfinite(max_frequency) or max_frequency <= 0):
        raise ValueError("max_frequency must be finite and positive")
    if min_frequency is not None and max_frequency is not None and min_frequency >= max_frequency:
        raise ValueError("min_frequency must be lower than max_frequency")

    mask = np.ones(power.size, dtype=bool)
    if exclude_dc:
        mask &= frequencies > 0
    if min_frequency is not None:
        mask &= frequencies >= min_frequency
    if max_frequency is not None:
        mask &= frequencies <= max_frequency
    selected = np.maximum(power[mask], 0.0)
    total = float(selected.sum())
    if selected.size < 2 or not np.isfinite(total) or total <= np.finfo(float).eps:
        return SpectralMetrics(total, 0.0, 0.0, np.zeros_like(selected), False, int(selected.size))
    probabilities = selected / total
    positive = probabilities[probabilities > 0]
    entropy = -float(np.sum(positive * np.log(positive))) / float(np.log(selected.size))
    concentration = float(np.max(probabilities))
    return SpectralMetrics(
        total, float(np.clip(entropy, 0.0, 1.0)),
        concentration, probabilities.astype(float), True, int(selected.size)
    )
