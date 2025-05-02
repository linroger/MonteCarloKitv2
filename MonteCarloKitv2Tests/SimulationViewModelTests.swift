import XCTest
@testable import MonteCarloKitv2

final class SimulationViewModelTests: XCTestCase {
    func testBuildParameter_normal() {
        let vm = SimulationViewModel()
        vm.modelType = .normal
        vm.normalStd = 2.5
        let param = vm.buildParameter()
        // Should be a Double for normal model
        XCTAssertTrue(param is Double)
        XCTAssertEqual(param as? Double, 2.5)
    }

    func testBuildParameter_gbm() {
        let vm = SimulationViewModel()
        vm.modelType = .gbm
        vm.gbmInitial = 5.0
        vm.gbmMu = 0.1
        vm.gbmSigma = 0.2
        vm.gbmT = 2.0
        vm.gbmSteps = 10
        let param = vm.buildParameter()
        // Should be a dictionary for GBM model
        guard let dict = param as? [String: Any] else {
            return XCTFail("Expected Dictionary for GBM parameter, got \(type(of: param))")
        }
        XCTAssertEqual(dict["type"] as? String, "gbm")
        XCTAssertEqual(dict["initial"] as? Double, 5.0)
        XCTAssertEqual(dict["mu"] as? Double, 0.1)
        XCTAssertEqual(dict["sigma"] as? Double, 0.2)
        XCTAssertEqual(dict["T"] as? Double, 2.0)
        // Steps may be bridged as Int or Double
        if let stepsInt = dict["steps"] as? Int {
            XCTAssertEqual(stepsInt, 10)
        } else if let stepsDouble = dict["steps"] as? Double {
            XCTAssertEqual(stepsDouble, 10.0)
        } else {
            XCTFail("Unexpected type for 'steps': \(type(of: dict["steps"]))")
        }
    }

    func testBuildParameter_poisson() {
        let vm = SimulationViewModel()
        vm.modelType = .poisson
        vm.poissonRate = 3.5
        vm.poissonT = 4.0
        let param = vm.buildParameter()
        guard let dict = param as? [String: Any] else {
            return XCTFail("Expected Dictionary for Poisson parameter, got \(type(of: param))")
        }
        XCTAssertEqual(dict["type"] as? String, "poisson")
        XCTAssertEqual(dict["rate"] as? Double, 3.5)
        XCTAssertEqual(dict["T"] as? Double, 4.0)
    }
}