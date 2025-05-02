import Foundation

/// Holds results from a Monte Carlo simulation
struct SimulationResult {
    /// Raw simulated values
    let values: [Double]
    /// Computed metrics dictionary (e.g., mean, variance, std_dev, percentiles, CIs)
    let metrics: [String: Double]

    /// Convenience accessor for mean
    var mean: Double { metrics["mean"] ?? 0.0 }
    /// Convenience accessor for variance
    var variance: Double { metrics["variance"] ?? 0.0 }
    /// Convenience accessor for standard deviation
    var stdDev: Double { metrics["std_dev"] ?? 0.0 }
}