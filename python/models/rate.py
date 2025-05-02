"""
Short rate simulation models.
"""
import numpy as np
import pandas as pd
from stats import compute_metrics

# Stubs for short rate models
def black_derman_toy(n_runs, config):
    """
    Simulate Black–Derman–Toy short rate model (lognormal) full paths.
    dr/r = -0.5*sigma**2 dt + sigma dW
    Returns DataFrame of shape (n_runs, steps+1) and metrics on final rates.
    """
    initial = float(config.get('initial', 0.03))
    sigma = float(config.get('sigma', 0.01))
    T = float(config.get('T', 1.0))
    steps = int(config.get('steps', 100))
    dt = T / steps
    rates = np.zeros((n_runs, steps + 1))
    rates[:, 0] = initial
    for t in range(1, steps + 1):
        z = np.random.randn(n_runs)
        rates[:, t] = rates[:, t-1] * np.exp(-0.5 * sigma**2 * dt + sigma * np.sqrt(dt) * z)
    df = pd.DataFrame(rates, columns=[f"t{i}" for i in range(steps + 1)])
    metrics = compute_metrics(rates[:, -1])
    return df, metrics

def black_karasinski(n_runs, config):
    """
    Simulate Black–Karasinski short rate model: log-rate Ornstein–Uhlenbeck.
    dX = a*(theta - X) dt + sigma dW, r = exp(X).
    Returns DataFrame of paths and metrics on final rates.
    """
    initial = float(config.get('initial', 0.03))
    a = float(config.get('a', 1.0))
    sigma = float(config.get('sigma', 0.01))
    theta = float(config.get('theta', 0.0))
    T = float(config.get('T', 1.0))
    steps = int(config.get('steps', 100))
    dt = T / steps
    X = np.zeros((n_runs, steps + 1))
    X[:, 0] = np.log(initial)
    for t in range(1, steps + 1):
        z = np.random.randn(n_runs)
        X[:, t] = X[:, t-1] + a*(theta - X[:, t-1])*dt + sigma*np.sqrt(dt)*z
    rates = np.exp(X)
    df = pd.DataFrame(rates, columns=[f"t{i}" for i in range(steps + 1)])
    metrics = compute_metrics(rates[:, -1])
    return df, metrics

def cox_ingersoll_ross(n_runs, config):
    """
    Simulate Cox–Ingersoll–Ross (CIR) short rate model: dr = a*(b - r)dt + sigma*sqrt(r) dW.
    Returns DataFrame of paths and metrics on final rates.
    """
    initial = float(config.get('initial', 0.03))
    a = float(config.get('a', 1.0))
    b = float(config.get('b', 0.05))
    sigma = float(config.get('sigma', 0.01))
    T = float(config.get('T', 1.0))
    steps = int(config.get('steps', 100))
    dt = T / steps
    rates = np.zeros((n_runs, steps + 1))
    rates[:, 0] = initial
    for t in range(1, steps + 1):
        z = np.random.randn(n_runs)
        r_prev = np.maximum(rates[:, t-1], 0)
        dr = a*(b - r_prev)*dt + sigma*np.sqrt(r_prev*dt)*z
        rates[:, t] = np.maximum(r_prev + dr, 0)
    df = pd.DataFrame(rates, columns=[f"t{i}" for i in range(steps + 1)])
    metrics = compute_metrics(rates[:, -1])
    return df, metrics

def ho_lee(n_runs, config):
    """
    Simulate Ho–Lee short rate model: dr = theta dt + sigma dW.
    Returns DataFrame of paths and metrics on final rates.
    """
    initial = float(config.get('initial', 0.03))
    theta = float(config.get('theta', 0.0))
    sigma = float(config.get('sigma', 0.01))
    T = float(config.get('T', 1.0))
    steps = int(config.get('steps', 100))
    dt = T / steps
    rates = np.zeros((n_runs, steps + 1))
    rates[:, 0] = initial
    for t in range(1, steps + 1):
        z = np.random.randn(n_runs)
        rates[:, t] = rates[:, t-1] + theta*dt + sigma*np.sqrt(dt)*z
    df = pd.DataFrame(rates, columns=[f"t{i}" for i in range(steps + 1)])
    metrics = compute_metrics(rates[:, -1])
    return df, metrics

def hull_white_one_factor(n_runs, config):
    """
    Simulate Hull–White one-factor model (OU on r): dr = a*(theta - r)dt + sigma dW.
    Returns DataFrame of paths and metrics on final rates.
    """
    initial = float(config.get('initial', 0.03))
    a = float(config.get('a', 1.0))
    sigma = float(config.get('sigma', 0.01))
    theta = float(config.get('theta', 0.0))
    T = float(config.get('T', 1.0))
    steps = int(config.get('steps', 100))
    dt = T / steps
    rates = np.zeros((n_runs, steps + 1))
    rates[:, 0] = initial
    for t in range(1, steps + 1):
        z = np.random.randn(n_runs)
        rates[:, t] = rates[:, t-1] + a*(theta - rates[:, t-1])*dt + sigma*np.sqrt(dt)*z
    df = pd.DataFrame(rates, columns=[f"t{i}" for i in range(steps + 1)])
    metrics = compute_metrics(rates[:, -1])
    return df, metrics

def hull_white_two_factor(n_runs, config):
    """
    Simulate Hull–White two-factor model as sum of two OU factors.
    Returns DataFrame of paths and metrics on final rates.
    """
    initial = float(config.get('initial', 0.03))
    a1 = float(config.get('a1', 1.0))
    sigma1 = float(config.get('sigma1', 0.01))
    a2 = float(config.get('a2', 1.0))
    sigma2 = float(config.get('sigma2', 0.01))
    theta1 = float(config.get('theta1', 0.0))
    theta2 = float(config.get('theta2', 0.0))
    T = float(config.get('T', 1.0))
    steps = int(config.get('steps', 100))
    dt = T / steps
    X1 = np.zeros((n_runs, steps + 1))
    X2 = np.zeros((n_runs, steps + 1))
    X1[:, 0] = initial / 2
    X2[:, 0] = initial / 2
    for t in range(1, steps + 1):
        z1 = np.random.randn(n_runs)
        z2 = np.random.randn(n_runs)
        X1[:, t] = X1[:, t-1] + a1*(theta1 - X1[:, t-1])*dt + sigma1*np.sqrt(dt)*z1
        X2[:, t] = X2[:, t-1] + a2*(theta2 - X2[:, t-1])*dt + sigma2*np.sqrt(dt)*z2
    rates = X1 + X2
    df = pd.DataFrame(rates, columns=[f"t{i}" for i in range(steps + 1)])
    metrics = compute_metrics(rates[:, -1])
    return df, metrics

def kalotay_williams_fabozzi(n_runs, config):
    """
    Simulate Kalotay–Williams–Fabozzi model as log-rate OU.
    Returns DataFrame of paths and metrics on final rates.
    """
    initial = float(config.get('initial', 0.03))
    k = float(config.get('k', 1.0))
    X = float(config.get('X', 0.05))
    sigma = float(config.get('sigma', 0.01))
    T = float(config.get('T', 1.0))
    steps = int(config.get('steps', 100))
    dt = T / steps
    Y = np.zeros((n_runs, steps + 1))
    Y[:, 0] = np.log(initial)
    for t in range(1, steps + 1):
        z = np.random.randn(n_runs)
        Y[:, t] = Y[:, t-1] + k*(X - Y[:, t-1])*dt + sigma*np.sqrt(dt)*z
    rates = np.exp(Y)
    df = pd.DataFrame(rates, columns=[f"t{i}" for i in range(steps + 1)])
    metrics = compute_metrics(rates[:, -1])
    return df, metrics

def merton_rate(n_runs, config):
    """
    Simulate Merton jump-diffusion on short rate.
    d r/r = mu dt + sigma dW + (J - 1) dN.
    Returns DataFrame of paths and metrics on final rates.
    """
    initial = float(config.get('initial', 0.03))
    mu = float(config.get('mu', 0.0))
    sigma = float(config.get('sigma', 0.01))
    lam = float(config.get('lam', 0.1))
    mu_j = float(config.get('mu_j', 0.0))
    sigma_j = float(config.get('sigma_j', 0.1))
    T = float(config.get('T', 1.0))
    steps = int(config.get('steps', 100))
    dt = T / steps
    rates = np.zeros((n_runs, steps + 1))
    rates[:, 0] = initial
    for t in range(1, steps + 1):
        z = np.random.randn(n_runs)
        diffusion = np.exp((mu - 0.5*sigma**2)*dt + sigma*np.sqrt(dt)*z)
        Nj = np.random.poisson(lam*dt, size=n_runs)
        jumps = np.ones(n_runs)
        for i in range(n_runs):
            if Nj[i] > 0:
                J = np.random.lognormal(mean=mu_j, sigma=sigma_j, size=Nj[i])
                jumps[i] = np.prod(J)
        rates[:, t] = rates[:, t-1] * diffusion * jumps
    df = pd.DataFrame(rates, columns=[f"t{i}" for i in range(steps + 1)])
    metrics = compute_metrics(rates[:, -1])
    return df, metrics

def rendleman_bartter(n_runs, config):
    """
    Simulate Rendleman–Bartter model (lognormal with drift) on short rate.
    dr/r = mu dt + sigma dW.
    """
    initial = float(config.get('initial', 0.03))
    mu = float(config.get('mu', 0.0))
    sigma = float(config.get('sigma', 0.01))
    T = float(config.get('T', 1.0))
    steps = int(config.get('steps', 100))
    dt = T / steps
    rates = np.zeros((n_runs, steps + 1))
    rates[:, 0] = initial
    for t in range(1, steps + 1):
        z = np.random.randn(n_runs)
        rates[:, t] = rates[:, t-1] * np.exp((mu - 0.5*sigma**2)*dt + sigma*np.sqrt(dt)*z)
    df = pd.DataFrame(rates, columns=[f"t{i}" for i in range(steps + 1)])
    metrics = compute_metrics(rates[:, -1])
    return df, metrics

def vasicek(n_runs, config):
    """
    Simulate Vasicek model: dr = a*(b - r)dt + sigma dW.
    """
    initial = float(config.get('initial', 0.03))
    a = float(config.get('a', 1.0))
    b = float(config.get('b', 0.05))
    sigma = float(config.get('sigma', 0.01))
    T = float(config.get('T', 1.0))
    steps = int(config.get('steps', 100))
    dt = T / steps
    rates = np.zeros((n_runs, steps + 1))
    rates[:, 0] = initial
    for t in range(1, steps + 1):
        z = np.random.randn(n_runs)
        rates[:, t] = rates[:, t-1] + a*(b - rates[:, t-1])*dt + sigma*np.sqrt(dt)*z
    df = pd.DataFrame(rates, columns=[f"t{i}" for i in range(steps + 1)])
    metrics = compute_metrics(rates[:, -1])
    return df, metrics

def longstaff_schwartz(n_runs, config):
    """
    Simulate Longstaff–Schwartz short rate model (proxy via Vasicek).
    """
    return vasicek(n_runs, config)

def chen(n_runs, config):
    """
    Simulate Chen model: OU plus proportional jumps.
    dr = a*(theta - r)dt + sigma dW + gamma * r dN.
    """
    initial = float(config.get('initial', 0.03))
    a = float(config.get('a', 1.0))
    theta = float(config.get('theta', 0.0))
    sigma = float(config.get('sigma', 0.01))
    gamma = float(config.get('gamma', 0.5))
    lam = float(config.get('lam', 0.1))
    T = float(config.get('T', 1.0))
    steps = int(config.get('steps', 100))
    dt = T / steps
    rates = np.zeros((n_runs, steps + 1))
    rates[:, 0] = initial
    for t in range(1, steps + 1):
        z = np.random.randn(n_runs)
        dN = np.random.poisson(lam*dt, size=n_runs)
        jump = 1 + gamma * dN
        rates[:, t] = rates[:, t-1] + a*(theta - rates[:, t-1])*dt + sigma*np.sqrt(dt)*z + (rates[:, t-1]*(jump - 1))
    df = pd.DataFrame(rates, columns=[f"t{i}" for i in range(steps + 1)])
    metrics = compute_metrics(rates[:, -1])
    return df, metrics