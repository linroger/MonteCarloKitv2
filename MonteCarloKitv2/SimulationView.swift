import SwiftUI
import Charts

/// SwiftUI view for configuring and running Monte Carlo simulations
struct SimulationView: View {
    @StateObject private var viewModel = SimulationViewModel()

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 16) {
                // Model selection
                Picker("Model", selection: $viewModel.modelType) {
                    ForEach(ModelType.allCases) { model in
                        Text(model.displayName).tag(model)
                    }
                }
                // Use macOS pop-up button style for many model types
                .pickerStyle(PopUpButtonPickerStyle())
                .padding(.horizontal)

                Form {
                    Section("General") {
                        Stepper("Number of runs: \(viewModel.nRuns)", value: $viewModel.nRuns, in: 1...1_000_000)
                    }

                    Section("Parameters") {
                        switch viewModel.modelType {
                        case .normal:
                            HStack {
                                Text("Std Dev:")
                                Slider(value: $viewModel.normalStd, in: 0.0...10.0)
                                Text(String(format: "%.2f", viewModel.normalStd))
                            }

                        case .gbm:
                            VStack(alignment: .leading) {
                                HStack {
                                    Text("Initial:")
                                    Slider(value: $viewModel.gbmInitial, in: 0.1...100.0)
                                    Text(String(format: "%.2f", viewModel.gbmInitial))
                                }
                                HStack {
                                    Text("Mu:")
                                    Slider(value: $viewModel.gbmMu, in: -1.0...1.0)
                                    Text(String(format: "%.2f", viewModel.gbmMu))
                                }
                                HStack {
                                    Text("Sigma:")
                                    Slider(value: $viewModel.gbmSigma, in: 0.0...5.0)
                                    Text(String(format: "%.2f", viewModel.gbmSigma))
                                }
                                HStack {
                                    Text("T:")
                                    Slider(value: $viewModel.gbmT, in: 0.1...10.0)
                                    Text(String(format: "%.2f", viewModel.gbmT))
                                }
                                Stepper("Steps: \(viewModel.gbmSteps)", value: $viewModel.gbmSteps, in: 1...1_000)
                            }

                        case .poisson:
                            VStack(alignment: .leading) {
                                HStack {
                                    Text("Rate:")
                                    Slider(value: $viewModel.poissonRate, in: 0.0...10.0)
                                    Text(String(format: "%.2f", viewModel.poissonRate))
                                }
                                HStack {
                                    Text("T:")
                                    Slider(value: $viewModel.poissonT, in: 0.1...10.0)
                                    Text(String(format: "%.2f", viewModel.poissonT))
                                }
                            }
                        default:
                            Text("Parameters for \(viewModel.modelType.displayName) coming soon.")
                        }
                    }
                }
                .padding(.horizontal)

                Button(action: viewModel.runSimulation) {
                    Text("Run Simulation")
                        .frame(maxWidth: .infinity)
                }
                .padding(.horizontal)
                .buttonStyle(.borderedProminent)

                if viewModel.isRunning {
                    ProgressView("Running...")
                        .frame(maxWidth: .infinity, alignment: .center)
                        .padding()
                }

                if let result = viewModel.result {
                    Chart {
                        ForEach(Array(result.values.enumerated()), id: \.0) { idx, value in
                            BarMark(
                                x: .value("Index", idx),
                                y: .value("Value", value)
                            )
                        }
                    }
                    .frame(height: 200)
                    .padding(.horizontal)

                    VStack(alignment: .leading, spacing: 8) {
                        Text("Count: \(result.metrics["count"] ?? 0, specifier: "%.0f")")
                        Text("Mean: \(result.mean, specifier: "%.4f")")
                        Text("Variance: \(result.variance, specifier: "%.4f")")
                        Text("Std Dev: \(result.stdDev, specifier: "%.4f")")
                        if let ciLower = result.metrics["ci_lower"], let ciUpper = result.metrics["ci_upper"] {
                            Text("95% CI: [\(ciLower, specifier: "%.4f"), \(ciUpper, specifier: "%.4f")]" )
                        }
                    }
                    .padding(.horizontal)
                }
            }
            .padding(.vertical)
        }
    }
}

#Preview {
    SimulationView()
}