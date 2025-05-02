
import Foundation
import Combine
import PythonKit
/// ViewModel for managing Monte Carlo simulation state
/// Types of supported simulation models
enum ModelType: String, CaseIterable, Identifiable {
    case normal
    case gbm
    case poisson

    var id: String { rawValue }
    var displayName: String {
        switch self {
        case .normal: return "Normal"
        case .gbm: return "Geometric BM"
        case .poisson: return "Poisson"
        }
    }
}

/// ViewModel for managing Monte Carlo simulation state
@MainActor
final class SimulationViewModel: ObservableObject {
    /// Number of simulation runs
    @Published var nRuns: Int = 1000
    /// Selected model type
    @Published var modelType: ModelType = .normal
    // Normal distribution parameter
    @Published var normalStd: Double = 1.0
    // GBM parameters
    @Published var gbmInitial: Double = 1.0
    @Published var gbmMu: Double = 0.0
    @Published var gbmSigma: Double = 1.0
    @Published var gbmT: Double = 1.0
    @Published var gbmSteps: Int = 100
    // Poisson parameters
    @Published var poissonRate: Double = 1.0
    @Published var poissonT: Double = 1.0
    /// Indicates if simulation is in progress
    @Published var isRunning: Bool = false
    /// Result of the simulation
    @Published var result: SimulationResult?

    /// Trigger the simulation via PythonBridge
    func runSimulation() {
        isRunning = true
        Task {
            defer { isRunning = false }
            do {
                let param = buildParameter()
                let simResult = try await PythonBridge.shared.runSimulation(
                    nRuns: nRuns,
                    parameter: param
                )
                result = simResult
            } catch {
                print("Simulation error: \(error)")
            }
        }
    }
    
    /// Build the parameter payload for PythonBridge based on selected model
    func buildParameter() -> PythonObject {
        switch modelType {
        case .normal:
            return PythonObject(normalStd)
        case .gbm:
                return PythonObject([
                    "type": PythonObject("gbm"),
                    "initial": PythonObject(gbmInitial),
                    "mu": PythonObject(gbmMu),
                    "sigma": PythonObject(gbmSigma),
                    "T": PythonObject(gbmT),
                    "steps": PythonObject(gbmSteps)
                ])
        case .poisson:
            return PythonObject([
                "type": PythonObject("poisson"),
                "rate": PythonObject(poissonRate),
                "T": PythonObject(poissonT)
            ])
        }
    }
}
