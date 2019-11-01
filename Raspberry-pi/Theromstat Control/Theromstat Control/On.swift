//
//  OnOff.swift
//  Theromstat Control
//
//  Created by moose on 5/7/17.
//  Copyright © 2017 Fred Dunaway. All rights reserved.
//

import UIKit

class On {
    
    //MARK: Properties
    var temperature: String
    var when: String
    var motionDelaySeconds: Float
    
    //MARK:  Initialization
    init?(temperature: String, when: String, motionDelaySeconds: Float) {
        self.temperature = temperature
        self.when = when
        self.motionDelaySeconds = motionDelaySeconds
        
        if(temperature.isEmpty || when.isEmpty) {
            return nil
        }
        if(motionDelaySeconds.isNaN) {
            return nil
        }
    }
}
