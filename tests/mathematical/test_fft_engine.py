import numpy as np
import pytest
from fourier_gyroscope.mathematics.fft_engine import compute_spectrum

def test_frequency_and_period_recovery():
    n=256; f=8/n; t=np.arange(n)
    result=compute_spectrum(3*np.sin(2*np.pi*f*t+0.2), min_frequency=1/64, max_frequency=1/4)
    assert result.has_reliable_cycle
    assert result.dominant_frequency == pytest.approx(f)
    assert result.dominant_period == pytest.approx(32)

def test_hann_amplitude_correction():
    n=256; t=np.arange(n); f=10/n
    result=compute_spectrum(2.5*np.cos(2*np.pi*f*t))
    idx=int(np.argmax(result.power[1:])+1)
    assert result.amplitude[idx] == pytest.approx(2.5, rel=0.015)

def test_flat_signal_does_not_invent_cycle():
    result=compute_spectrum(np.ones(64))
    assert not result.has_reliable_cycle
    assert result.dominant_frequency is None
    assert result.dominant_period is None

@pytest.mark.parametrize("values", [[1,2,3,4,5,6,7], [1,2,3,4,5,6,7,np.nan]])
def test_invalid_inputs_rejected(values):
    with pytest.raises(ValueError): compute_spectrum(values)

def test_invalid_frequency_bounds_rejected():
    with pytest.raises(ValueError): compute_spectrum(np.arange(32), min_frequency=.3, max_frequency=.2)
