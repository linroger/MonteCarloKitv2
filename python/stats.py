"""
Statistical metrics module.

This module computes basic statistics for simulation data.
"""
import numpy as np  # noqa: F401
import pandas as pd

def compute_metrics(values):
    """
    Compute basic statistical metrics for a sequence of values.

    Args:
        values (array-like): sequence of numeric values

    Returns:
        dict: metrics including count, mean, variance, std_dev,
              median, min, max, percentiles (5,25,75,95),
              and 95% confidence interval.
    """
    # Convert to pandas Series for robust statistics
    ser = pd.Series(values).dropna()
    n = len(ser)
    mean_val = float(ser.mean())
    var_val = float(ser.var(ddof=0))
    std_val = float(ser.std(ddof=0))

    # Percentiles
    p05 = float(ser.quantile(0.05))
    p25 = float(ser.quantile(0.25))
    p50 = float(ser.quantile(0.50))
    p75 = float(ser.quantile(0.75))
    p95 = float(ser.quantile(0.95))

    # 95% confidence interval for the mean
    z = 1.96
    ci_err = (z * std_val / np.sqrt(n)) if n > 0 else None
    ci_lower = mean_val - ci_err if ci_err is not None else None
    ci_upper = mean_val + ci_err if ci_err is not None else None

    return {
        'count': n,
        'mean': mean_val,
        'variance': var_val,
        'std_dev': std_val,
        'median': p50,
        'min': float(ser.min()),
        'max': float(ser.max()),
        'p05': p05,
        'p25': p25,
        'p75': p75,
        'p95': p95,
        'ci_lower': ci_lower,
        'ci_upper': ci_upper
    }