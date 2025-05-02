"""
Monte Carlo simulation module.

This module defines the entry point for running simulations and returning data.
"""
import numpy as np
import pandas as pd
from stats import compute_metrics

def run_simulation(n_runs, parameter):
    """
    Run a Monte Carlo simulation based on the given parameter.

    Args:
        n_runs (int): number of simulation runs
        parameter (float or dict):
            - If float: treated as std deviation for a normal distribution.
            - If dict: must include 'type' key: 'normal', 'gbm', or 'poisson',
              with corresponding parameters.

    Returns:
        tuple: (DataFrame of results, dict of metrics)
            - 'normal': DataFrame with 'values'
            - 'gbm': DataFrame with 'final'
            - 'poisson': DataFrame with 'count'
    """
    # Determine configuration from parameter
    if hasattr(parameter, 'get'):
        config = parameter
    else:
        config = {'type': 'normal', 'std': float(parameter)}

    model_type = config.get('type', 'normal')

    if model_type == 'normal':
        std = float(config.get('std', 1.0))
        data = np.random.randn(n_runs) * std
        df = pd.DataFrame({'values': data})
        metrics = compute_metrics(df['values'])

    elif model_type == 'gbm':
        initial = float(config.get('initial', 1.0))
        mu = float(config.get('mu', 0.0))
        sigma = float(config.get('sigma', 1.0))
        T = float(config.get('T', 1.0))
        steps = int(config.get('steps', 100))
        dt = T / steps
        # Simulate geometric Brownian motion final prices
        rand = np.random.randn(n_runs, steps)
        increments = np.exp((mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * rand)
        final_prices = initial * np.prod(increments, axis=1)
        df = pd.DataFrame({'final': final_prices})
        metrics = compute_metrics(df['final'])

    elif model_type == 'poisson':
        rate = float(config.get('rate', 1.0))
        T = float(config.get('T', 1.0))
        lam = rate * T
        data = np.random.poisson(lam, size=n_runs)
        df = pd.DataFrame({'count': data})
        metrics = compute_metrics(df['count'])

    else:
        raise ValueError(f"Unknown model type: {model_type}")

    return df, metrics