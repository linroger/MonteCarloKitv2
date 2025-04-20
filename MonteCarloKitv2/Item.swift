//
//  Item.swift
//  MonteCarloKitv2
//
//  Created by Roger Lin on 4/19/25.
//

import Foundation
import SwiftData

@Model
final class Item {
    var timestamp: Date
    
    init(timestamp: Date) {
        self.timestamp = timestamp
    }
}
