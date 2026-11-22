import numpy as np
from fourier_gyroscope.mathematics.fft_engine import compute_spectrum

def test_prefix_result_is_invariant_to_unobserved_future():
    t=np.arange(128)
    prefix=np.sin(2*np.pi*7*t/128)
    future=np.sin(2*np.pi*19*np.arange(40)/128+.4)
    first=compute_spectrum(prefix)
    replay=compute_spectrum(np.concatenate((prefix,future))[:128])
    assert first.dominant_frequency == replay.dominant_frequency
    assert np.allclose(first.power,replay.power)
