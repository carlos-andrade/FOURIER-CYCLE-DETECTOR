import numpy as np
import pytest

from fourier_gyroscope.indicators_v1 import (
    calculate_indicators, fcd, fed, fes, fho,
)


def signal(length=320, period=16, amplitude=3.0, phase=0.4):
    t = np.arange(length, dtype=float)
    return 100.0 + 0.015 * t + amplitude * np.sin(
        2.0 * np.pi * t / period + phase
    )


def test_fcd_recovers_exact_bin_period_on_synthetic_cycle():
    result = fcd(signal(), window=128, min_period=8, max_period=64)
    assert result.valid[-1]
    assert abs(result.dominant_period_bars[-1] - 16.0) < 1e-10
    assert abs(result.dominant_frequency[-1] - 1.0 / 16.0) < 1e-12


def test_fho_amplitude_is_calibrated_for_single_sine():
    result = fho(signal(amplitude=2.5), window=128, min_period=8, max_period=64)
    assert result.valid[-1]
    assert abs(result.amplitude[-1] - 2.5) < 0.08
    assert -np.pi <= result.phase_radians[-1] <= np.pi


def test_fes_energy_shares_sum_to_one_with_partition_bands():
    result = fes(
        signal(), window=128, min_period=8, max_period=64,
        bands={"all": (8, 64)},
    )
    assert result.valid[-1]
    assert abs(result.band_power_share["all"][-1] - 1.0) < 1e-12
    assert 0.0 <= result.normalized_entropy[-1] <= 1.0
    assert 0.0 <= result.concentration[-1] <= 1.0


def test_warmup_is_explicit_and_no_lookahead_prefix_invariance():
    x = signal()
    full = calculate_indicators(x, window=128, min_period=8, max_period=64)
    prefix = calculate_indicators(x[:240], window=128, min_period=8, max_period=64)
    assert not full.fcd.valid[:127].any()
    assert np.allclose(
        full.fcd.dominant_frequency[:240],
        prefix.fcd.dominant_frequency,
        equal_nan=True,
    )
    assert np.allclose(
        full.fho.amplitude[:240], prefix.fho.amplitude, equal_nan=True
    )
    assert np.allclose(
        full.fes.normalized_entropy[:240],
        prefix.fes.normalized_entropy,
        equal_nan=True,
    )
    assert np.array_equal(full.frc.regime[:240], prefix.frc.regime)


def test_invalid_inputs_are_rejected():
    with pytest.raises(ValueError):
        fcd(np.ones((10, 2)))
    with pytest.raises(ValueError):
        fcd([1.0, np.nan, 2.0])


def test_two_tone_signal_selects_the_stronger_spectral_component():
    t = np.arange(384, dtype=float)
    x = (
        50.0 + 2.0 * np.sin(2.0 * np.pi * t / 16.0)
        + 0.6 * np.sin(2.0 * np.pi * t / 32.0)
    )
    result = fcd(x, window=128, min_period=8, max_period=64)
    assert result.valid[-1]
    assert abs(result.dominant_period_bars[-1] - 16.0) < 1e-10


def test_frequency_step_is_detected_and_new_period_is_recovered():
    t = np.arange(512, dtype=float)
    phase = np.where(t < 256, 2.0 * np.pi * t / 16.0,
                     2.0 * np.pi * 256.0 / 16.0 + 2.0 * np.pi * (t - 256.0) / 32.0)
    x = 100.0 + 2.0 * np.sin(phase)
    result = calculate_indicators(x, window=128, min_period=8, max_period=64)
    assert abs(result.fcd.dominant_period_bars[-1] - 32.0) < 1e-10
    assert np.any(result.fed.event[256:400] == "FREQUENCY_SHIFT")


def test_amplitude_collapse_is_detected():
    t = np.arange(512, dtype=float)
    amplitude = np.where(t < 256, 3.0, 0.5)
    x = 100.0 + amplitude * np.sin(2.0 * np.pi * t / 16.0)
    cycle = fcd(x, window=128, min_period=8, max_period=64)
    harmonic = fho(x, window=128, min_period=8, max_period=64)
    events = fed(cycle, harmonic)
    assert np.any(events.event[256:400] == "AMPLITUDE_COLLAPSE")


def test_white_noise_has_finite_bounded_spectral_metrics():
    rng = np.random.default_rng(20261122)
    result = fes(rng.normal(size=512), window=128, min_period=8, max_period=64)
    assert result.valid[-1]
    assert np.isfinite(result.normalized_entropy[-1])
    assert 0.0 <= result.normalized_entropy[-1] <= 1.0
    assert 0.0 <= result.concentration[-1] <= 1.0


def test_zero_energy_window_abstains_instead_of_claiming_a_cycle():
    result = fcd(np.zeros(256), window=128, min_period=8, max_period=64)
    assert not result.valid[-1]
    assert np.isnan(result.dominant_period_bars[-1])


def test_invalid_fes_band_is_rejected_before_calculation():
    with pytest.raises(ValueError, match="outside configured range"):
        fes(signal(length=64), window=64, min_period=8, max_period=32,
            bands={"invalid": (4, 16)})
