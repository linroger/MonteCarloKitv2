<!-- Changelog for MonteCarloKitv2 re-architecture -->
# Changelog

## [Unreleased]

### Current State
- The app is a SwiftUI macOS application with integrated Python backend via PythonKit.
- Python modules under `python/` implement Monte Carlo simulations (Normal, GBM, Poisson) and statistical metrics (`stats.py`).
- `PythonBridge.swift` configures PythonKit and exposes `run_simulation` to Swift.
- `SimulationViewModel` manages model parameters (`.normal`, `.gbm`, `.poisson`) and invokes Python backend.
- `SimulationView` provides UI for model selection, parameter configuration, simulation execution, charting results, and metrics display.
- Unit tests cover Python backend (`python/test_simulation.py`) and Swift parameter building (`SimulationViewModelTests.swift`).

### Objectives
- Re-architect the app to use SwiftUI as the front end and Python (via PythonKit) as the backend.
- Implement Monte Carlo simulations, stochastic model, and stochastic rate models in Python for performance.
- Use pandas to collect simulation results and compute statistical metrics in Python.
- Bridge results to SwiftUI: invoke Python backend, retrieve results, and render charts and metrics.

### High-Level Plan
1. Integrate PythonKit and organize a Python backend directory. **(Completed)**
   - Added `python/` directory with modules: `__init__.py`, `simulation.py`, `stats.py`.
2. Create Python modules implementing Monte Carlo simulation and statistical analysis. **(Completed)**
   - `python/simulation.py` provides `run_simulation` supporting model types:
     - normal (Gaussian) with configurable std deviation
     - gbm (geometric Brownian motion) with parameters: initial, mu, sigma, T, steps
     - poisson (Poisson process counts) with parameters: rate, T
   - `python/stats.py` computes robust metrics on results:
     - count, mean, variance, std_dev
     - median, min, max, percentiles (5,25,50,75,95)
     - 95% confidence interval (ci_lower, ci_upper)
3. Implement Swift bridging code. **(Completed)**
   - Added `MonteCarloKitv2/PythonBridge.swift` to initialize PythonKit, configure `sys.path`, and load the `simulation` module.
   - Added `MonteCarloKitv2/SimulationResult.swift` defining `SimulationResult` for values and metrics.
   - `runSimulation(nRuns:parameter:)` API implemented to call Python, convert results to Swift types.
4. Extend Swift data models and view models. **(Completed)**
   - Added `SimulationViewModel.swift` defining `SimulationViewModel`:
     - Published properties for runs, selected `ModelType`, and parameters for Normal, GBM, and Poisson models.
     - Builds a Swift dictionary or Double for PythonKit bridging.
     - Calls `PythonBridge` to trigger simulations based on modelType.
5. Update SwiftUI interface. **(Completed)**
   - Added `SimulationView.swift`:
     - Includes a segmented Picker for model selection.
     - Dynamic parameter controls (Sliders, Steppers) per model type.
     - "Run Simulation" button with progress indicator.
     - Bar chart rendering and detailed metrics display (count, mean, variance, std_dev, CI).
   - Updated `ContentView.swift` to host `SimulationView` exclusively.
6. Add unit tests and integration tests:
   - Python backend tests added (`python/test_simulation.py`) **(Comprehensive: compute_metrics, normal, GBM, Poisson)**
   - Swift wrapper tests **(SimulationViewModel parameter mapping)**
     - Added `SimulationViewModelTests` verifying `buildParameter()` for Normal, GBM, and Poisson.
   - SwiftUI integration tests **(TODO)**
7. Iterate, document, and refine. **(Ongoing)**
   - Resolved SwiftData macro errors in `Scenario.swift`: removed explicit `= nil` initializers on transformable properties to avoid ambiguous type inference.
   - Xcode build now passes compilation; code signing settings may need adjusting (valid development certificate/team) before running.

---
*This file will be updated with progress on each step.*
### Detailed Re-Architecture Plan
1. Extend Python backend with additional stochastic asset price models: **(Scaffolded)**
   - Random Walk, GBM (with full time series support), GARCH, ARIMA, ARMA, SARIMAX, Jump Diffusion, Poisson Process, Martingale, Lévy Process, Ornstein–Uhlenbeck Process, Bernoulli Process.
   - Implement each model as a Python function returning a pandas DataFrame of simulated paths or final values.
2. Implement one-factor and multi-factor short rate models in Python:
   - Black–Derman–Toy, Black–Karasinski, Cox–Ingersoll–Ross, Ho–Lee, Hull–White (1F & 2F), Kalotay–Williams–Fabozzi, Merton, Rendleman–Bartter, Vasicek, Longstaff–Schwartz, Chen.
   - Support discrete vs. continuous-time simulation options.
3. Refactor Python package structure:
   - Create `python/models/asset.py` and `python/models/rate.py`.
   - Update `python/simulation.py` (or create `core.py`) to dispatch to specific model functions.
   - Add `python/analysis.py` for advanced metrics (e.g., VaR, CVaR, skewness, kurtosis).
4. Update Swift bridging layer (`PythonBridge.swift`):
   - Support dynamic model selection and parameter passing for new models.
   - Enhance DataFrame-to-Swift conversion for time series and multi-dimensional arrays.
5. Extend Swift model enumerations:
   - Define `AssetModelType` and `RateModelType` enums matching Python API identifiers.
6. Update `SimulationViewModel`:
   - Manage dynamic parameter sets per model type, including volatility, drift, jumps, AR coefficients, etc.
   - Include discrete/continuous-time toggle.
7. Redesign SwiftUI interface:
   - Add sidebar navigation grouping asset price and rate models.
   - Create dynamic parameter forms for each model.
   - Add toolbar with actions: Reset Parameters, Export Data (CSV/JSON), About.
8. Implement result rendering:
   - Asset models: time series line charts (Swift Charts), distribution histograms.
   - Rate models: term structure plots, yield curve animations.
9. Comprehensive testing:
   - Write Python unit tests for all new model functions.
   - Add Swift unit tests for parameter mapping and result parsing.
   - Add SwiftUI integration tests for UI flows.
10. Documentation and packaging:
   - Update `README.md` and create `instructions.md` with setup and usage guides.
   - Maintain `changelog.md` through each milestone.