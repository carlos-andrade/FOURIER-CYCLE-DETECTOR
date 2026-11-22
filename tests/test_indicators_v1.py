import numpy as np

from fourier_gyroscope.indicators_v1 import (
    calculate_indicators, fcd, fes, fho,
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
    x = signal()
    result = fes(
        x, window=128, min_period=8, max_period=64,
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
    try:
        fcd(np.ones((10, 2)))
    except ValueError:
        pass
    else:
        raise AssertionError("two-dimensional input must be rejected")

    try:
        fcd([1.0, np.nan, 2.0])
    except ValueError:
        pass
    else:
        raise AssertionError("non-finite input must be rejected")
