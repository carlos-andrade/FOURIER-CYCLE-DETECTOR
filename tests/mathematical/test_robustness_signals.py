import numpy as np
import pytest

from fourier_gyroscope.mathematics.fft_engine import compute_spectrum
from fourier_gyroscope.mathematics.harmonic_regression import fit_harmonic


def _peak_frequencies(signal, count=2):
    spectrum = compute_spectrum(signal, window="hann", min_frequency=1/128, max_frequency=0.4)
    power = spectrum.power.copy()
    power[0] = 0.0
    selected = []
    for _ in range(count):
        index = int(np.argmax(power))
        selected.append(float(spectrum.frequencies[index]))
        lo, hi = max(0, index-1), min(power.size, index+2)
        power[lo:hi] = 0.0
    return selected


def test_two_resolvable_frequencies_are_present_in_spectrum():
    n = 512
    t = np.arange(n)
    f1, f2 = 12/n, 37/n
    x = 2.0*np.sin(2*np.pi*f1*t) + 0.8*np.cos(2*np.pi*f2*t + 0.2)
    peaks = _peak_frequencies(x)
    assert any(abs(f-f1) < 1e-12 for f in peaks)
    assert any(abs(f-f2) < 1e-12 for f in peaks)


def test_dominant_frequency_survives_moderate_deterministic_noise():
    rng = np.random.default_rng(20261122)
    n = 512
    t = np.arange(n)
    frequency = 24/n
    clean = 2*np.sin(2*np.pi*frequency*t + 0.4)
    noisy = clean + rng.normal(0.0, 0.35, n)
    result = compute_spectrum(noisy, min_frequency=1/128, max_frequency=0.4)
    assert result.has_reliable_cycle
    assert result.dominant_frequency == pytest.approx(frequency, abs=1/n)


def test_amplitude_modulation_is_visible_in_separate_halves():
    n = 512
    t = np.arange(n)
    envelope = np.linspace(2.0, 0.4, n)
    x = envelope*np.sin(2*np.pi*24*t/n)
    first = fit_harmonic(x[:256], 24/n)
    second = fit_harmonic(x[256:], 24/n)
    assert first.amplitude > second.amplitude
    assert first.amplitude-second.amplitude > 0.5


def test_frequency_change_is_detected_by_segment_estimates():
    n = 512
    t = np.arange(n)
    x = np.concatenate((
        np.sin(2*np.pi*12*np.arange(256)/256),
        np.sin(2*np.pi*31*np.arange(256)/256),
    ))
    first = compute_spectrum(x[:256], min_frequency=1/128, max_frequency=0.4)
    second = compute_spectrum(x[256:], min_frequency=1/128, max_frequency=0.4)
    assert first.dominant_period == pytest.approx(256/12)
    assert second.dominant_period == pytest.approx(256/31)
    assert first.dominant_frequency != second.dominant_frequency


def test_regime_shift_changes_dominant_spectral_peak():
    n = 512
    left = np.sin(2*np.pi*10*np.arange(n)/n)
    right = 1.5*np.sin(2*np.pi*42*np.arange(n)/n)
    first = compute_spectrum(left, min_frequency=1/128, max_frequency=0.4)
    second = compute_spectrum(right, min_frequency=1/128, max_frequency=0.4)
    assert first.dominant_frequency == pytest.approx(10/n)
    assert second.dominant_frequency == pytest.approx(42/n)


def test_window_choice_does_not_move_bin_centered_tone():
    n = 256
    t = np.arange(n)
    frequency = 17/n
    x = 1.7*np.cos(2*np.pi*frequency*t + 0.1)
    hann = compute_spectrum(x, window="hann")
    rectangular = compute_spectrum(x, window="rectangular")
    assert hann.dominant_frequency == pytest.approx(frequency)
    assert rectangular.dominant_frequency == pytest.approx(frequency)
