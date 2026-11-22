import numpy as np
import pytest
from fourier_gyroscope.mathematics.harmonic_regression import fit_harmonic

def test_amplitude_phase_offset_and_fit():
    n=128; f=5/n; phase=.73; t=np.arange(n)
    x=4.2*np.cos(2*np.pi*f*t-phase)+1.7
    result=fit_harmonic(x,f)
    assert result.amplitude == pytest.approx(4.2, abs=1e-10)
    assert result.phase_radians == pytest.approx(phase, abs=1e-10)
    assert result.offset == pytest.approx(1.7, abs=1e-10)
    assert result.r_squared == pytest.approx(1.0, abs=1e-12)
    assert result.rmse < 1e-10

def test_explicit_sample_positions():
    t=np.arange(40)*1.5; f=.1
    x=2*np.cos(2*np.pi*f*t-.4)-3
    result=fit_harmonic(x,f,sample_positions=t)
    assert result.amplitude == pytest.approx(2, abs=1e-10)
    assert result.phase_radians == pytest.approx(.4, abs=1e-10)

@pytest.mark.parametrize("frequency", [0, .6, float("nan")])
def test_invalid_frequency(frequency):
    with pytest.raises(ValueError): fit_harmonic(np.arange(16),frequency)
