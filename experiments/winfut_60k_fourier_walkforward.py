#!/usr/bin/env python3
"""Exploratory one-step-ahead Fourier walk-forward for WINFUT 60K-trade bars.

Input is a local Profit One XLSX export. Only timestamp, close and candle
counter are used; auxiliary indicator/strategy columns are deliberately ignored.
"""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
import numpy as np
import pandas as pd


def dominant_frequency(y: np.ndarray, min_period: float, max_period: float):
    y = np.asarray(y, dtype=float)
    w = np.hanning(y.size)
    power = np.abs(np.fft.rfft((y - y.mean()) * w)) ** 2
    freq = np.fft.rfftfreq(y.size, d=1.0)
    mask = (freq > 0) & (freq >= 1 / max_period) & (freq <= 1 / min_period)
    if not mask.any() or power[mask].sum() <= 1e-12:
        return None, None
    ids = np.flatnonzero(mask)
    peak = int(ids[np.argmax(power[mask])])
    return float(freq[peak]), float(power[peak] / power[mask].sum())


def harmonic_forecast(y: np.ndarray, frequency: float) -> float:
    t = np.arange(y.size, dtype=float)
    omega = 2 * np.pi * frequency
    design = np.column_stack((np.cos(omega*t), np.sin(omega*t), np.ones(y.size)))
    beta, *_ = np.linalg.lstsq(design, y, rcond=None)
    return float(np.array([np.cos(omega*y.size), np.sin(omega*y.size), 1.0]) @ beta)


def metrics(frame: pd.DataFrame, column: str) -> dict:
    z = frame[frame[column] != 0]
    pnl = z[column].to_numpy(float) * z["actual"].to_numpy(float)
    gp, gl = pnl[pnl > 0].sum(), -pnl[pnl < 0].sum()
    return {
        "trades": int(len(pnl)),
        "hit_rate_pct": float(100*np.mean(pnl > 0)),
        "gross_points": float(pnl.sum()),
        "average_points_per_trade": float(pnl.mean()),
        "profit_factor": float(gp/gl) if gl else None,
        "net_points_cost_10": float(pnl.sum() - 10*len(pnl)),
        "net_points_cost_20": float(pnl.sum() - 20*len(pnl)),
        "net_points_cost_40": float(pnl.sum() - 40*len(pnl)),
    }


def run(path: Path, window: int, min_period: float, max_period: float, holdout: float):
    raw = pd.read_excel(path, sheet_name=0)
    required = ["Data", "Fechamento", "Contador de Candles"]
    if any(c not in raw.columns for c in required):
        raise ValueError(f"XLSX must contain {required}")
    bars = raw[required].copy()
    bars["Data"] = pd.to_datetime(bars["Data"], errors="raise")
    bars["session"] = bars["Data"].dt.date
    bars = bars.sort_values(["Data", "Contador de Candles"]).reset_index(drop=True)

    rows = []
    for session, group in bars.groupby("session", sort=True):
        close = group["Fechamento"].to_numpy(float)
        returns = np.diff(close, prepend=close[0])
        for end in range(window-1, len(returns)-1):
            sample = returns[end-window+1:end+1]
            frequency, concentration = dominant_frequency(sample, min_period, max_period)
            if frequency is None:
                continue
            forecast = harmonic_forecast(sample, frequency)
            rows.append({
                "session": session, "forecast": forecast,
                "actual": float(returns[end+1]), "position": float(np.sign(forecast)),
                "momentum_8": float(np.sign(np.mean(returns[max(0,end-7):end+1]))),
                "momentum_1": float(np.sign(returns[end])),
                "period": float(1/frequency), "concentration": concentration,
            })
    result = pd.DataFrame(rows)
    if result.empty:
        raise ValueError("No forecasts generated.")
    sessions = sorted(result.session.unique())
    split_at = max(1, min(len(sessions)-1, int(len(sessions)*(1-holdout))))
    cutoff = sessions[split_at-1]
    result["split"] = np.where(result.session <= cutoff, "IS", "OOS")
    summary = {}
    for name, part in result.groupby("split", sort=False):
        summary[name] = {
            "fourier_harmonic": metrics(part, "position"),
            "momentum_8": metrics(part, "momentum_8"),
            "momentum_1": metrics(part, "momentum_1"),
            "sessions": int(part.session.nunique()),
        }
    oos = result[result.split == "OOS"].copy()
    oos["pnl"] = oos.position * oos.actual
    daily = oos.groupby("session").pnl.sum().to_numpy()
    rng = np.random.default_rng(20261122)
    boot = np.array([rng.choice(daily, len(daily), replace=True).mean()
                     for _ in range(20000)])
    periods = result.period.value_counts().head(10)
    return {
        "experiment": "WINFUT_60K_FOURIER_HARMONIC_WALK_FORWARD_V1",
        "input_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "bars": int(len(bars)), "sessions_in_file": int(bars.session.nunique()),
        "predictions": int(len(result)), "window_bars": window,
        "period_search_bars": [min_period, max_period],
        "holdout_fraction": holdout, "split_cutoff": str(cutoff),
        "oos_first_session": str(sessions[split_at]),
        "oos_last_session": str(sessions[-1]),
        "median_dominant_period_bars": float(result.period.median()),
        "median_spectral_concentration": float(result.concentration.median()),
        "top_periods": [{"period_bars": float(p), "windows": int(n)}
                        for p,n in periods.items()],
        "metrics": summary,
        "oos_daily_mean_points": float(daily.mean()),
        "oos_positive_sessions_pct": float(100*np.mean(daily > 0)),
        "oos_daily_mean_bootstrap_95pct": [float(v) for v in np.quantile(boot,[.025,.975])],
        "limitations": [
            "Exploratory, not live-certified; close-to-close one-bar holding assumption.",
            "One sample equals one 60K-trade candle; frequency is cycles per bar, not per minute.",
            "No intrabar execution, spread, queue, fees or empirically calibrated slippage.",
            "Costs 10/20/40 are hypothetical round-trip point deductions per trade.",
            "No overnight positions; returns reset at each session.",
            "Only close prices are used; indicator/strategy columns are excluded."
        ],
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("xlsx", type=Path)
    p.add_argument("--window", type=int, default=64)
    p.add_argument("--min-period", type=float, default=6.0)
    p.add_argument("--max-period", type=float, default=32.0)
    p.add_argument("--holdout", type=float, default=0.30)
    p.add_argument("--output", type=Path, default=Path("fourier_winfut_experiment.json"))
    a = p.parse_args()
    if a.window < 16 or not (0 < a.min_period < a.max_period <= a.window/2):
        raise ValueError("Invalid window/period bounds.")
    if not 0.1 <= a.holdout <= 0.5:
        raise ValueError("holdout must be between 0.10 and 0.50")
    result = run(a.xlsx, a.window, a.min_period, a.max_period, a.holdout)
    a.output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
