import numpy as np
from fourier_gyroscope.mathematics.fft_engine import compute_spectrum
from fourier_gyroscope.mathematics.spectral_metrics import compute_spectral_metrics

def test_entropy_and_concentration_are_bounded():
    t=np.arange(256)
    x=np.sin(2*np.pi*8*t/256)+.2*np.sin(2*np.pi*27*t/256)
    m=compute_spectral_metrics(compute_spectrum(x))
    assert m.valid
    assert 0 <= m.normalized_entropy <= 1
    assert 0 <= m.energy_concentration <= 1
    assert np.isclose(m.probabilities.sum(),1)

def test_zero_energy_is_explicitly_invalid():
    m=compute_spectral_metrics(compute_spectrum(np.ones(64)))
    assert not m.valid
    assert np.isfinite(m.normalized_entropy)
    assert np.isfinite(m.energy_concentration)
