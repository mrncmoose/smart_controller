//
//  thermaEvent.swift
//  Theromstat Control
//
//  Created by moose on 5/7/17.
//  Copyright © 2017 Fred Dunaway. All rights reserved.
//

import UIKit

class Event {
    //Mark: Properties
    
    var current_timestamp: String
    var on: On
    
    //MARK:  Initialization
    init?(current_timestamp: String, on: On, motionDelaySeconds: Float) {
        self.current_timestamp = current_timestamp
        self.on = on
        if(current_timestamp.isEmpty) {
            return nil
        }
        if(motionDelaySeconds.isNaN) {
            return nil
        }
    }
}
