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
    
    //MARK:  Initialization
    init?(temperature: String, when: String) {
        self.temperature = temperature
        self.when = when
        
        if(temperature.isEmpty || when.isEmpty) {
            return nil
        }
    }
}
