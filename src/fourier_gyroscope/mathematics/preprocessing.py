"""Deterministic signal preprocessing."""
import numpy as np
from numpy.typing import ArrayLike, NDArray
from .validation import as_finite_1d

def make_window(length: int, name: str = "hann") -> NDArray[np.float64]:
    if length < 1:
        raise ValueError("length must be positive")
    key = name.lower()
    if key in {"rect", "rectangular", "none"}:
        return np.ones(length, dtype=np.float64)
    if key == "hann":
        return np.ones(1) if length == 1 else np.hanning(length).astype(np.float64)
    raise ValueError(f"unsupported window: {name}")

def prepare_signal(values: ArrayLike, *, detrend: bool = True,
                   window: str = "hann"):
    signal = as_finite_1d(values)
    removed_mean = float(np.mean(signal)) if detrend else 0.0
    coefficients = make_window(signal.size, window)
    return (signal - removed_mean) * coefficients, coefficients, removed_mean
