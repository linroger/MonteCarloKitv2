"""
Asset price simulation models.
"""
import numpy as np
import pandas as pd
from stats import compute_metrics

def random_walk(n_runs, config):
    """
    Simulate arithmetic random walk paths.
    Returns DataFrame of shape (n_runs, steps+1) and metrics on final values.
    """
    initial = float(config.get('initial', 0.0))
    mu = float(config.get('mu', 0.0))
    sigma = float(config.get('sigma', 1.0))
    T = float(config.get('T', 1.0))
    steps = int(config.get('steps', 100))
    dt = T / steps
    rand = np.random.randn(n_runs, steps)
    returns = mu * dt + sigma * np.sqrt(dt) * rand
    price_paths = np.zeros((n_runs, steps + 1))
    price_paths[:, 0] = initial
    for t in range(1, steps + 1):
        price_paths[:, t] = price_paths[:, t-1] + returns[:, t-1]
    cols = [f"t{i}" for i in range(steps + 1)]
    df = pd.DataFrame(price_paths, columns=cols)
    metrics = compute_metrics(price_paths[:, -1])
    return df, metrics

def gbm_path(n_runs, config):
    """
    Simulate geometric Brownian motion full paths.
    Returns DataFrame of shape (n_runs, steps+1) and metrics on final values.
    """
    initial = float(config.get('initial', 1.0))
    mu = float(config.get('mu', 0.0))
    sigma = float(config.get('sigma', 1.0))
    T = float(config.get('T', 1.0))
    steps = int(config.get('steps', 100))
    dt = T / steps
    rand = np.random.randn(n_runs, steps)
    increments = np.exp((mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * rand)
    paths = np.empty((n_runs, steps + 1))
    paths[:, 0] = initial
    for t in range(1, steps + 1):
        paths[:, t] = paths[:, t-1] * increments[:, t-1]
    cols = [f"t{i}" for i in range(steps + 1)]
    df = pd.DataFrame(paths, columns=cols)
    metrics = compute_metrics(paths[:, -1])
    return df, metrics

# Stubs for additional asset models
def garch(n_runs, config):
    """
    Simulate GARCH(1,1) process on asset price paths.
    Returns DataFrame of shape (n_runs, steps+1) and metrics on final values.
    """
    initial = float(config.get('initial', 1.0))
    mu = float(config.get('mu', 0.0))
    omega = float(config.get('omega', 0.1))
    alpha = float(config.get('alpha', 0.1))
    beta = float(config.get('beta', 0.8))
    T = float(config.get('T', 1.0))
    steps = int(config.get('steps', 100))
    dt = T / steps
    prices = np.zeros((n_runs, steps + 1))
    prices[:, 0] = initial
    # Initialize variance
    var = np.full(n_runs, omega / (1 - alpha - beta))
    for t in range(1, steps + 1):
        # generate shocks
        eps = np.random.randn(n_runs) * np.sqrt(var)
        # update price via log returns
        prices[:, t] = prices[:, t-1] * np.exp(mu * dt + eps * np.sqrt(dt))
        # update variance
        var = omega + alpha * eps**2 + beta * var
    df = pd.DataFrame(prices, columns=[f"t{i}" for i in range(steps + 1)])
    metrics = compute_metrics(prices[:, -1])
    return df, metrics

def arima(n_runs, config):
    """
    Simulate ARIMA(p,d,q) process (default p=1,d=0,q=1).
    Returns DataFrame of shape (n_runs, steps+1) and metrics on final values.
    """
    p = int(config.get('p', 1))
    d = int(config.get('d', 0))
    q = int(config.get('q', 1))
    T = float(config.get('T', 1.0))
    steps = int(config.get('steps', 100))
    dt = T / steps
    paths = np.zeros((n_runs, steps + 1))
    for i in range(n_runs):
        eps = np.random.randn(steps)
        series = np.zeros(steps + 1)
        # ARMA part
        for t in range(1, steps + 1):
            ar = config.get('phi1', 0.5) * series[t - 1] if p >= 1 else 0
            ma = config.get('theta1', 0.5) * eps[t - 1] if q >= 1 else 0
            series[t] = ar + ma + eps[t - 1]
        # Integration
        if d > 0:
            for _ in range(d):
                series = np.cumsum(series)
        paths[i, :] = series
    df = pd.DataFrame(paths, columns=[f"t{i}" for i in range(steps + 1)])
    metrics = compute_metrics(paths[:, -1])
    return df, metrics

def arma(n_runs, config):
    """
    Simulate ARMA(p,q) process (default p=1, q=1).
    Returns DataFrame of shape (n_runs, steps+1) and metrics on final values.
    """
    p = int(config.get('p', 1))
    q = int(config.get('q', 1))
    T = float(config.get('T', 1.0))
    steps = int(config.get('steps', 100))
    dt = T / steps
    paths = np.zeros((n_runs, steps + 1))
    for i in range(n_runs):
        eps = np.random.randn(steps)
        series = np.zeros(steps + 1)
        for t in range(1, steps + 1):
            ar = config.get('phi1', 0.5) * series[t - 1] if p >= 1 else 0
            ma = config.get('theta1', 0.5) * eps[t - 1] if q >= 1 else 0
            series[t] = ar + ma + eps[t - 1]
        paths[i, :] = series
    df = pd.DataFrame(paths, columns=[f"t{i}" for i in range(steps + 1)])
    metrics = compute_metrics(paths[:, -1])
    return df, metrics

def sarimax(n_runs, config):
    """
    Placeholder SARIMAX simulation; maps to ARIMA for now.
    """
    # For now, fallback to ARIMA simulation
    return arima(n_runs, config)

def jump_diffusion(n_runs, config):
    """
    Simulate Merton jump diffusion full paths.
    Returns DataFrame of shape (n_runs, steps+1) and metrics on final values.
    """
    initial = float(config.get('initial', 1.0))
    mu = float(config.get('mu', 0.0))
    sigma = float(config.get('sigma', 1.0))
    lam = float(config.get('lam', 0.1))  # jump intensity
    mu_j = float(config.get('mu_j', 0.0))  # mean jump size (log-normal)
    sigma_j = float(config.get('sigma_j', 0.1))  # std dev jump size (log-normal)
    T = float(config.get('T', 1.0))
    steps = int(config.get('steps', 100))
    dt = T / steps
    paths = np.empty((n_runs, steps + 1))
    paths[:, 0] = initial
    # Precompute Poisson probabilities
    for t in range(1, steps + 1):
        z = np.random.randn(n_runs)
        # Continuous diffusion increment
        diffusion = np.exp((mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * z)
        # Jump component
        # Number of jumps in dt ~ Poisson(lam*dt)
        Nj = np.random.poisson(lam * dt, size=n_runs)
        # Jump sizes Y ~ lognormal(mu_j, sigma_j)
        if Nj.sum() > 0:
            # For runs with jumps, generate sum of jumps
            jumps = np.ones(n_runs)
            for i in range(n_runs):
                if Nj[i] > 0:
                    # multiplicative jump factor
                    Y = np.random.lognormal(mean=mu_j, sigma=sigma_j, size=Nj[i])
                    jumps[i] = np.prod(Y)
        else:
            jumps = np.ones(n_runs)
        paths[:, t] = paths[:, t-1] * diffusion * jumps
    cols = [f"t{i}" for i in range(steps + 1)]
    df = pd.DataFrame(paths, columns=cols)
    metrics = compute_metrics(paths[:, -1])
    return df, metrics

def poisson_process(n_runs, config):
    """
    Simulate Poisson counting process full paths.
    Returns DataFrame of shape (n_runs, steps+1) and metrics on final counts.
    """
    rate = float(config.get('rate', 1.0))
    T = float(config.get('T', 1.0))
    steps = int(config.get('steps', 100))
    dt = T / steps
    paths = np.zeros((n_runs, steps + 1), dtype=int)
    for t in range(1, steps + 1):
        # increments ~ Poisson(rate*dt)
        incr = np.random.poisson(rate * dt, size=n_runs)
        paths[:, t] = paths[:, t-1] + incr
    cols = [f"t{i}" for i in range(steps + 1)]
    df = pd.DataFrame(paths, columns=cols)
    metrics = compute_metrics(paths[:, -1])
    return df, metrics

def martingale_process(n_runs, config):
    """
    Simulate a simple martingale (zero-drift random walk) full paths.
    Returns DataFrame of shape (n_runs, steps+1) and metrics on final values.
    """
    initial = float(config.get('initial', 0.0))
    sigma = float(config.get('sigma', 1.0))
    T = float(config.get('T', 1.0))
    steps = int(config.get('steps', 100))
    dt = T / steps
    paths = np.zeros((n_runs, steps + 1))
    paths[:, 0] = initial
    for t in range(1, steps + 1):
        dw = np.random.randn(n_runs) * np.sqrt(dt)
        paths[:, t] = paths[:, t-1] + sigma * dw
    cols = [f"t{i}" for i in range(steps + 1)]
    df = pd.DataFrame(paths, columns=cols)
    metrics = compute_metrics(paths[:, -1])
    return df, metrics

def levy_process(n_runs, config):
    """
    Simulate an approximate Lévy process using Cauchy increments.
    Returns DataFrame of shape (n_runs, steps+1) and metrics on final values.
    """
    initial = float(config.get('initial', 0.0))
    alpha = float(config.get('alpha', 1.0))  # scale parameter
    T = float(config.get('T', 1.0))
    steps = int(config.get('steps', 100))
    dt = T / steps
    paths = np.zeros((n_runs, steps + 1))
    paths[:, 0] = initial
    for t in range(1, steps + 1):
        # Cauchy increments
        incr = np.random.standard_cauchy(size=n_runs) * (alpha * dt)
        paths[:, t] = paths[:, t-1] + incr
    cols = [f"t{i}" for i in range(steps + 1)]
    df = pd.DataFrame(paths, columns=cols)
    metrics = compute_metrics(paths[:, -1])
    return df, metrics

def ornstein_uhlenbeck(n_runs, config):
    """
    Simulate Ornstein–Uhlenbeck mean-reverting process full paths.
    Returns DataFrame of shape (n_runs, steps+1) and metrics on final values.
    """
    initial = float(config.get('initial', 0.0))
    mu = float(config.get('mu', 0.0))
    theta = float(config.get('theta', 1.0))
    sigma = float(config.get('sigma', 1.0))
    T = float(config.get('T', 1.0))
    steps = int(config.get('steps', 100))
    dt = T / steps
    paths = np.zeros((n_runs, steps + 1))
    paths[:, 0] = initial
    for t in range(1, steps + 1):
        z = np.random.randn(n_runs)
        paths[:, t] = paths[:, t-1] + theta * (mu - paths[:, t-1]) * dt + sigma * np.sqrt(dt) * z
    cols = [f"t{i}" for i in range(steps + 1)]
    df = pd.DataFrame(paths, columns=cols)
    metrics = compute_metrics(paths[:, -1])
    return df, metrics

def bernoulli_process(n_runs, config):
    """
    Simulate Bernoulli counting process (binomial trials) full paths.
    Returns DataFrame of shape (n_runs, steps+1) and metrics on final counts.
    """
    p = float(config.get('p', 0.5))
    steps = int(config.get('steps', 100))
    paths = np.zeros((n_runs, steps + 1), dtype=int)
    for t in range(1, steps + 1):
        trials = np.random.rand(n_runs) < p
        paths[:, t] = paths[:, t-1] + trials.astype(int)
    cols = [f"t{i}" for i in range(steps + 1)]
    df = pd.DataFrame(paths, columns=cols)
    metrics = compute_metrics(paths[:, -1])
    return df, metrics