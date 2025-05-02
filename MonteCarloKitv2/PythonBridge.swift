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
    static let shared: PythonBridge = {
        do {
            return try PythonBridge()
        } catch {
            fatalError("Unable to initialize PythonBridge: \(error)")
        }
    }()

    private let simulation: PythonObject

    /// Initialize Python environment and load modules
    private init() throws {
        let sys = Python.import("sys")
        // Compute path to 'python' directory relative to this Swift file
        // Determine path to the 'python' folder at the repository root
        let sourceFileURL = URL(fileURLWithPath: #file)
        let swiftFileDir = sourceFileURL.deletingLastPathComponent()
        // swiftFileDir is .../<repo>/MonteCarloKitv2
        let repoRoot = swiftFileDir.deletingLastPathComponent()
        // repoRoot is .../<repo>
        let pythonDir = repoRoot.appendingPathComponent("python").path
        // Prepend to Python sys.path
        sys.path.insert(0, PythonObject(pythonDir))
        // Import simulation module (fallback to None on failure)
        let simMod: PythonObject
        do {
            simMod = try Python.import("simulation")
        } catch {
            print("Warning: failed to import Python module 'simulation': \(error)")
            simMod = Python.None
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
        // If Python module not available, return empty result
        if simulation == Python.None {
            return SimulationResult(values: [], metrics: [:])
        }
        // Call Python function with bridged parameter
        let result = simulation.run_simulation(nRuns, parameter)
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