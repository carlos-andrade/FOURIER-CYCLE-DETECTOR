import numpy as np
import pytest

from fourier_gyroscope.mathematics.fft_engine import compute_spectrum
from fourier_gyroscope.mathematics.spectral_metrics import compute_spectral_metrics


def test_entropy_and_concentration_are_bounded():
    t = np.arange(256)
    x = np.sin(2 * np.pi * 8 * t / 256) + .2 * np.sin(2 * np.pi * 27 * t / 256)
    metrics = compute_spectral_metrics(compute_spectrum(x))
    assert metrics.valid
    assert 0 <= metrics.normalized_entropy <= 1
    assert 0 <= metrics.energy_concentration <= 1
    assert np.isclose(metrics.probabilities.sum(), 1)


def test_zero_energy_is_explicitly_invalid():
    metrics = compute_spectral_metrics(compute_spectrum(np.ones(64)))
    assert not metrics.valid
    assert np.isfinite(metrics.normalized_entropy)
    assert np.isfinite(metrics.energy_concentration)


def test_frequency_band_excludes_energy_outside_band():
    t = np.arange(512)
    x = np.sin(2 * np.pi * 12 * t / 512) + 2 * np.sin(2 * np.pi * 90 * t / 512)
    spectrum = compute_spectrum(x, window="rectangular")
    low_band = compute_spectral_metrics(spectrum, min_frequency=10/512, max_frequency=20/512)
    assert low_band.valid
    assert low_band.selected_bin_count == 11
    assert low_band.energy_concentration > 0.99
    assert low_band.total_energy < spectrum.power.sum()


def test_invalid_frequency_band_is_rejected():
    spectrum = compute_spectrum(np.sin(2 * np.pi * np.arange(64) / 16))
    with pytest.raises(ValueError):
        compute_spectral_metrics(spectrum, min_frequency=.2, max_frequency=.1)
