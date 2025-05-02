<!-- Changelog for MonteCarloKitv2 re-architecture -->
# Changelog

## [Unreleased]

### Current State
- The app is a basic SwiftUI macOS application using SwiftData.
- Defines a single `Item` model with a timestamp persisted in a SwiftData model container.
- `ContentView` displays a list of timestamps and allows adding or deleting items.
- No Monte Carlo simulation or statistical analysis is implemented.

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