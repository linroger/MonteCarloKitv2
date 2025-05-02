
import Foundation
import Combine

/// ViewModel for managing Monte Carlo simulation state
/// Types of supported simulation models
enum ModelType: String, CaseIterable, Identifiable {
    // Asset price models
    case normal
    case gbm
    case gbm_path
    case random_walk
    case jump_diffusion
    case garch
    case arima
    case arma
    case sarimax
    case poisson
    case poisson_process
    case martingale_process
    case levy_process
    case ornstein_uhlenbeck
    case bernoulli_process
    // Short rate models
    case black_derman_toy
    case black_karasinski
    case cox_ingersoll_ross
    case ho_lee
    case hull_white_one_factor
    case hull_white_two_factor
    case kalotay_williams_fabozzi
    case merton_rate
    case rendleman_bartter
    case vasicek
    case longstaff_schwartz
    case chen

    var id: String { rawValue }
    var displayName: String {
        switch self {
        // Asset price models
        case .normal: return "Normal"
        case .gbm: return "Geometric BM (final)"
        case .gbm_path: return "Geometric BM (path)"
        case .random_walk: return "Random Walk"
        case .jump_diffusion: return "Jump Diffusion"
        case .garch: return "GARCH"
        case .arima: return "ARIMA"
        case .arma: return "ARMA"
        case .sarimax: return "SARIMAX"
        case .poisson: return "Poisson (final)"
        case .poisson_process: return "Poisson (path)"
        case .martingale_process: return "Martingale"
        case .levy_process: return "Lévy Process"
        case .ornstein_uhlenbeck: return "Ornstein–Uhlenbeck"
        case .bernoulli_process: return "Bernoulli Process"
        // Short rate models
        case .black_derman_toy: return "Black–Derman–Toy"
        case .black_karasinski: return "Black–Karasinski"
        case .cox_ingersoll_ross: return "Cox–Ingersoll–Ross"
        case .ho_lee: return "Ho–Lee"
        case .hull_white_one_factor: return "Hull–White 1F"
        case .hull_white_two_factor: return "Hull–White 2F"
        case .kalotay_williams_fabozzi: return "Kalotay–Williams–Fabozzi"
        case .merton_rate: return "Merton (rate)"
        case .rendleman_bartter: return "Rendleman–Bartter"
        case .vasicek: return "Vasicek"
        case .longstaff_schwartz: return "Longstaff–Schwartz"
        case .chen: return "Chen"
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
    // Poisson parameters (final value)
    @Published var poissonRate: Double = 1.0
    @Published var poissonT: Double = 1.0
    // Random Walk parameters
    @Published var randomWalkInitial: Double = 0.0
    @Published var randomWalkMu: Double = 0.0
    @Published var randomWalkSigma: Double = 1.0
    @Published var randomWalkT: Double = 1.0
    @Published var randomWalkSteps: Int = 100
    // Jump Diffusion parameters
    @Published var jumpInitial: Double = 1.0
    @Published var jumpMu: Double = 0.0
    @Published var jumpSigma: Double = 1.0
    @Published var jumpLam: Double = 0.1
    @Published var jumpMuJ: Double = 0.0
    @Published var jumpSigmaJ: Double = 0.1
    @Published var jumpT: Double = 1.0
    @Published var jumpSteps: Int = 100
    // Poisson process (path) parameters
    @Published var poissonSteps: Int = 100
    // Martingale process parameters
    @Published var martingaleInitial: Double = 0.0
    @Published var martingaleSigma: Double = 1.0
    @Published var martingaleT: Double = 1.0
    @Published var martingaleSteps: Int = 100
    // Lévy process parameters
    @Published var levyInitial: Double = 0.0
    @Published var levyAlpha: Double = 1.0
    @Published var levyT: Double = 1.0
    @Published var levySteps: Int = 100
    // Ornstein–Uhlenbeck process parameters
    @Published var ouInitial: Double = 0.0
    @Published var ouMu: Double = 0.0
    @Published var ouTheta: Double = 1.0
    @Published var ouSigma: Double = 1.0
    @Published var ouT: Double = 1.0
    @Published var ouSteps: Int = 100
    // Bernoulli process parameters
    @Published var bernoulliP: Double = 0.5
    @Published var bernoulliSteps: Int = 100
    
    // Rate model parameters
    // Black–Derman–Toy
    @Published var bdtInitial: Double = 0.03
    @Published var bdtSigma: Double = 0.01
    @Published var bdtT: Double = 1.0
    @Published var bdtSteps: Int = 100
    // Black–Karasinski
    @Published var bkInitial: Double = 0.03
    @Published var bkA: Double = 1.0
    @Published var bkSigma: Double = 0.01
    @Published var bkT: Double = 1.0
    @Published var bkSteps: Int = 100
    // Cox–Ingersoll–Ross
    @Published var cirInitial: Double = 0.03
    @Published var cirA: Double = 1.0
    @Published var cirB: Double = 0.05
    @Published var cirSigma: Double = 0.01
    @Published var cirT: Double = 1.0
    @Published var cirSteps: Int = 100
    // Ho–Lee
    @Published var hlInitial: Double = 0.03
    @Published var hlTheta: Double = 0.001
    @Published var hlSigma: Double = 0.01
    @Published var hlT: Double = 1.0
    @Published var hlSteps: Int = 100
    // Hull–White 1F
    @Published var hw1Initial: Double = 0.03
    @Published var hw1A: Double = 1.0
    @Published var hw1Sigma: Double = 0.01
    @Published var hw1T: Double = 1.0
    @Published var hw1Steps: Int = 100
    // Hull–White 2F
    @Published var hw2Initial: Double = 0.03
    @Published var hw2A1: Double = 1.0
    @Published var hw2Sigma1: Double = 0.01
    @Published var hw2A2: Double = 1.0
    @Published var hw2Sigma2: Double = 0.01
    @Published var hw2T: Double = 1.0
    @Published var hw2Steps: Int = 100
    // Kalotay–Williams–Fabozzi
    @Published var kwfInitial: Double = 0.03
    @Published var kwfK: Double = 1.0
    @Published var kwfX: Double = 0.05
    @Published var kwfSigma: Double = 0.01
    @Published var kwfT: Double = 1.0
    @Published var kwfSteps: Int = 100
    // Merton short rate
    @Published var mrInitial: Double = 0.03
    @Published var mrMu: Double = 0.0
    @Published var mrSigma: Double = 0.01
    @Published var mrLam: Double = 0.1
    @Published var mrMuJ: Double = 0.0
    @Published var mrSigmaJ: Double = 0.1
    @Published var mrT: Double = 1.0
    @Published var mrSteps: Int = 100
    // Rendleman–Bartter
    @Published var rbInitial: Double = 0.03
    @Published var rbMu: Double = 0.0
    @Published var rbSigma: Double = 0.01
    @Published var rbT: Double = 1.0
    @Published var rbSteps: Int = 100
    // Vasicek
    @Published var vasInitial: Double = 0.03
    @Published var vasA: Double = 1.0
    @Published var vasB: Double = 0.05
    @Published var vasSigma: Double = 0.01
    @Published var vasT: Double = 1.0
    @Published var vasSteps: Int = 100
    // Longstaff–Schwartz
    @Published var lsInitial: Double = 0.03
    @Published var lsA: Double = 1.0
    @Published var lsB: Double = 0.05
    @Published var lsSigma: Double = 0.01
    @Published var lsT: Double = 1.0
    @Published var lsSteps: Int = 100
    // Chen model
    @Published var chenInitial: Double = 0.03
    @Published var chenA: Double = 1.0
    @Published var chenTheta: Double = 0.001
    @Published var chenSigma: Double = 0.01
    @Published var chenGamma: Double = 0.5
    @Published var chenT: Double = 1.0
    @Published var chenSteps: Int = 100
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
    func buildParameter() -> Any {
        switch modelType {
        case .normal:
            return normalStd
        case .gbm:
            return [
                "type": "gbm",
                "initial": gbmInitial,
                "mu": gbmMu,
                "sigma": gbmSigma,
                "T": gbmT,
                "steps": gbmSteps
            ]
        case .gbm_path:
            return [
                "type": "gbm_path",
                "initial": gbmInitial,
                "mu": gbmMu,
                "sigma": gbmSigma,
                "T": gbmT,
                "steps": gbmSteps
            ]
        case .random_walk:
            return [
                "type": "random_walk",
                "initial": randomWalkInitial,
                "mu": randomWalkMu,
                "sigma": randomWalkSigma,
                "T": randomWalkT,
                "steps": randomWalkSteps
            ]
        case .jump_diffusion:
            return [
                "type": "jump_diffusion",
                "initial": jumpInitial,
                "mu": jumpMu,
                "sigma": jumpSigma,
                "lam": jumpLam,
                "mu_j": jumpMuJ,
                "sigma_j": jumpSigmaJ,
                "T": jumpT,
                "steps": jumpSteps
            ]
        case .poisson:
            return [
                "type": "poisson",
                "rate": poissonRate,
                "T": poissonT
            ]
        case .poisson_process:
            return [
                "type": "poisson_process",
                "rate": poissonRate,
                "T": poissonT,
                "steps": poissonSteps
            ]
        case .martingale_process:
            return [
                "type": "martingale_process",
                "initial": martingaleInitial,
                "sigma": martingaleSigma,
                "T": martingaleT,
                "steps": martingaleSteps
            ]
        case .levy_process:
            return [
                "type": "levy_process",
                "initial": levyInitial,
                "alpha": levyAlpha,
                "T": levyT,
                "steps": levySteps
            ]
        case .ornstein_uhlenbeck:
            return [
                "type": "ornstein_uhlenbeck",
                "initial": ouInitial,
                "mu": ouMu,
                "theta": ouTheta,
                "sigma": ouSigma,
                "T": ouT,
                "steps": ouSteps
            ]
        case .bernoulli_process:
            return [
                "type": "bernoulli_process",
                "p": bernoulliP,
                "steps": bernoulliSteps
            ]
        // Rate models
        case .black_derman_toy:
            return [
                "type": "black_derman_toy",
                "initial": bdtInitial,
                "sigma": bdtSigma,
                "T": bdtT,
                "steps": bdtSteps
            ]
        case .black_karasinski:
            return [
                "type": "black_karasinski",
                "initial": bkInitial,
                "a": bkA,
                "sigma": bkSigma,
                "T": bkT,
                "steps": bkSteps
            ]
        case .cox_ingersoll_ross:
            return [
                "type": "cox_ingersoll_ross",
                "initial": cirInitial,
                "a": cirA,
                "b": cirB,
                "sigma": cirSigma,
                "T": cirT,
                "steps": cirSteps
            ]
        case .ho_lee:
            return [
                "type": "ho_lee",
                "initial": hlInitial,
                "theta": hlTheta,
                "sigma": hlSigma,
                "T": hlT,
                "steps": hlSteps
            ]
        case .hull_white_one_factor:
            return [
                "type": "hull_white_one_factor",
                "initial": hw1Initial,
                "a": hw1A,
                "sigma": hw1Sigma,
                "T": hw1T,
                "steps": hw1Steps
            ]
        case .hull_white_two_factor:
            return [
                "type": "hull_white_two_factor",
                "initial": hw2Initial,
                "a1": hw2A1,
                "sigma1": hw2Sigma1,
                "a2": hw2A2,
                "sigma2": hw2Sigma2,
                "T": hw2T,
                "steps": hw2Steps
            ]
        case .kalotay_williams_fabozzi:
            return [
                "type": "kalotay_williams_fabozzi",
                "initial": kwfInitial,
                "k": kwfK,
                "X": kwfX,
                "sigma": kwfSigma,
                "T": kwfT,
                "steps": kwfSteps
            ]
        case .merton_rate:
            return [
                "type": "merton_rate",
                "initial": mrInitial,
                "mu": mrMu,
                "sigma": mrSigma,
                "lam": mrLam,
                "mu_j": mrMuJ,
                "sigma_j": mrSigmaJ,
                "T": mrT,
                "steps": mrSteps
            ]
        case .rendleman_bartter:
            return [
                "type": "rendleman_bartter",
                "initial": rbInitial,
                "mu": rbMu,
                "sigma": rbSigma,
                "T": rbT,
                "steps": rbSteps
            ]
        case .vasicek:
            return [
                "type": "vasicek",
                "initial": vasInitial,
                "a": vasA,
                "b": vasB,
                "sigma": vasSigma,
                "T": vasT,
                "steps": vasSteps
            ]
        case .longstaff_schwartz:
            return [
                "type": "longstaff_schwartz",
                "initial": lsInitial,
                "a": lsA,
                "b": lsB,
                "sigma": lsSigma,
                "T": lsT,
                "steps": lsSteps
            ]
        case .chen:
            return [
                "type": "chen",
                "initial": chenInitial,
                "a": chenA,
                "theta": chenTheta,
                "sigma": chenSigma,
                "gamma": chenGamma,
                "T": chenT,
                "steps": chenSteps
            ]
        default:
            // Models not yet parameterized in UI (GARCH, ARIMA, SARIMAX)
            return ["type": modelType.rawValue]
        }
    }
}