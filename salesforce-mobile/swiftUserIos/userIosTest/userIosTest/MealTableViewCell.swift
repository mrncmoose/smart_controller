//
//  MealTableViewCell.swift
//  userIosTest
//
//  Created by moose on 2/23/17.
//  Copyright © 2017 Salesforce. All rights reserved.
//

import UIKit

class MealTableViewCell: UITableViewCell {

//MARK: Properties
    
@IBOutlet weak var mealNameLabel: UILabel!
    
    
    override func awakeFromNib() {
        super.awakeFromNib()
        // Initialization code
    }

    override func setSelected(_ selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)

        // Configure the view for the selected state
    }

}
