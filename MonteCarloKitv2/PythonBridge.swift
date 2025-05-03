import Foundation
#if canImport(PythonKit)
import PythonKit

/// Errors thrown by PythonBridge
/// Errors thrown by PythonBridge when PythonKit is available
enum PythonBridgeError: Error {
    /// Failed to import the specified Python module
    case moduleImportFailed(String)
}

/// Bridge to Python backend for running Monte Carlo simulations
final class PythonBridge {
    /// Shared singleton instance
    static let shared = PythonBridge()

    private let simulation: PythonObject?

    /// Initialize Python environment and load modules
    private init() {
        var simMod: PythonObject? = nil
        do {
            // Import key modules
            let sys = Python.import("sys")
            // Determine path to 'python' folder at repo root
            let sourceFileURL = URL(fileURLWithPath: #file)
            let swiftFileDir = sourceFileURL.deletingLastPathComponent()
            let repoRoot = swiftFileDir.deletingLastPathComponent()
            let pythonDir = repoRoot.appendingPathComponent("python").path
            // Prepend to Python sys.path
            sys.path.insert(0, PythonObject(pythonDir))
            // Import simulation module via builtins
            let builtins = Python.import("builtins")
            simMod = try builtins.__import__("simulation")
        } catch {
            print("PythonBridge init warning, module load failed: \(error)")
            simMod = nil
        }
        simulation = simMod
    }

    /// Run the Monte Carlo simulation via Python
    /// - Parameters:
    ///   - nRuns: Number of simulation runs
    ///   - parameter: Configuration for the simulation
    ///       May be a Swift Double (normal std) or a Dictionary for other models
    /// - Returns: SimulationResult containing raw values and all computed metrics
    func runSimulation(nRuns: Int, parameter: Any) async throws -> SimulationResult {
        // If Python backend not loaded, return empty result
        guard let sim = simulation else {
            return SimulationResult(values: [], metrics: [:])
        }
        // Call Python function with bridged parameter
        let result = sim.run_simulation(nRuns, parameter)
        let df = result[0]
        let metricsPy = result[1]

        // Extract raw values: look for first column
        // Extract raw values from the first column in the DataFrame
        var values = [Double]()
        // Determine first column name
        if let firstColName = String(df.columns[0]) {
            let pyArr = df[firstColName].to_numpy()
            for v in pyArr {
                if let dv = Double(v) {
                    values.append(dv)
                }
            }
        }

        // Extract all metrics from Python dict
        var metrics = [String: Double]()
        for key in metricsPy.keys() {
            if let keyStr = String(key), let val = Double(metricsPy[key]) {
                metrics[keyStr] = val
            }
        }

        return SimulationResult(values: values, metrics: metrics)
    }
}
#else
/// Stub errors when PythonKit is unavailable
enum PythonBridgeError: Error {
    /// PythonKit not available
    case noPythonKit
}

/// Dummy bridge that returns empty results
final class PythonBridge {
    static let shared = PythonBridge()
    private init() {}
    func runSimulation(nRuns: Int, parameter: Any) async throws -> SimulationResult {
        return SimulationResult(values: [], metrics: [:])
    }
}
#endif