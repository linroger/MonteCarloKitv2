"""
Basic smoke tests for Python backend modules (simulation and stats).

Run with: python3 python/test_simulation.py
"""
import sys
try:
    import numpy  # noqa: F401
    import pandas  # noqa: F401
except ImportError as e:
    print(f"Skipping Python backend tests: missing dependency: {e}")
    sys.exit(0)
from simulation import run_simulation
from stats import compute_metrics

def main():
    # Test compute_metrics basic keys and values
    values = [0, 2, 4]
    metrics = compute_metrics(values)
    # Expect count and statistical keys
    expected_keys = {
        'count', 'mean', 'variance', 'std_dev', 'median',
        'min', 'max', 'p05', 'p25', 'p75', 'p95',
        'ci_lower', 'ci_upper'
    }
    missing = expected_keys - set(metrics.keys())
    assert not missing, f"Missing metric keys: {missing}"
    assert metrics['count'] == 3, f"Expected count 3, got {metrics['count']}"

    # Test normal simulation default
    df_norm, metrics_norm = run_simulation(50, 1.0)
    assert 'values' in df_norm.columns, "DataFrame missing 'values' column for normal model"
    assert metrics_norm['count'] == 50, f"Expected count 50, got {metrics_norm['count']}"

    # Test GBM with zero volatility (deterministic)
    cfg_gbm = {'type': 'gbm', 'initial': 10.0, 'mu': 0.0, 'sigma': 0.0, 'T': 1.0, 'steps': 1}
    df_gbm, metrics_gbm = run_simulation(5, cfg_gbm)
    assert 'final' in df_gbm.columns, "DataFrame missing 'final' column for GBM model"
    assert df_gbm['final'].tolist() == [10.0] * 5, f"Expected all finals = 10.0, got {df_gbm['final'].tolist()}"
    assert metrics_gbm['mean'] == 10.0 and metrics_gbm['variance'] == 0.0 and metrics_gbm['std_dev'] == 0.0

    # Test Poisson with zero rate (deterministic)
    cfg_poi = {'type': 'poisson', 'rate': 0.0, 'T': 1.0}
    df_poi, metrics_poi = run_simulation(5, cfg_poi)
    assert 'count' in df_poi.columns, "DataFrame missing 'count' column for Poisson model"
    assert df_poi['count'].tolist() == [0] * 5, f"Expected all counts = 0, got {df_poi['count'].tolist()}"
    assert metrics_poi['mean'] == 0.0 and metrics_poi['variance'] == 0.0 and metrics_poi['std_dev'] == 0.0

    print("Python backend comprehensive tests passed.")

if __name__ == "__main__":
    main()