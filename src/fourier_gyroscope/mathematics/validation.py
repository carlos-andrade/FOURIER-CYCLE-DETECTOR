"""Input validation shared by mathematical modules."""
import numpy as np
from numpy.typing import ArrayLike, NDArray

def as_finite_1d(values: ArrayLike, min_size: int = 2) -> NDArray[np.float64]:
    array = np.asarray(values, dtype=np.float64)
    if array.ndim != 1:
        raise ValueError("signal must be one-dimensional")
    if array.size < min_size:
        raise ValueError(f"signal must contain at least {min_size} observations")
    if not np.all(np.isfinite(array)):
        raise ValueError("signal must contain only finite values")
    return array.copy()
