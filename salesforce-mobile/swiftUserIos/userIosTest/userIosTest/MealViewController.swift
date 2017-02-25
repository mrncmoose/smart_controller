//
//  MealViewController.swift
//  userIosTest
//
//  Created by moose on 2/23/17.
//  Copyright © 2017 Salesforce. All rights reserved.
//

import Foundation
import UIKit
import SalesforceSDKCore

class MealViewController : UITableViewController, SFRestDelegate, UITextFieldDelegate
{
    var dataRows = [NSDictionary]()
    var mealNameTxt: String = ""
    var mealTypeVal: String = ""
    var numberServedInt: Int16 = 2
    
    //MARK: Properties
    @IBOutlet weak var MealName: UITextField!
    
    @IBOutlet weak var MealType: UITextField!
    @IBOutlet weak var NumberServed: UISlider!
    @IBOutlet weak var MealDate: UIDatePicker!
    @IBOutlet weak var mealSaveButton: UIButton!
    
    // MARK: - View lifecycle
    override func loadView()
    {
        super.loadView()
        self.title = "Edit meal"
        MealName.delegate = self;
        MealType.delegate = self;
        
        
        //Here we use a query that should work on either Force.com or Database.com
        let request = SFRestAPI.sharedInstance().request(forQuery:"select Name, moosewareinc__type__c, moosewareinc__Number_served__c, moosewareinc__Meal_Date__c from moosewareinc__Meal__c where Id = ??");
        SFRestAPI.sharedInstance().send(request, delegate: self);
    }
    
    // MARK: - SFRestDelegate
    func request(_ request: SFRestRequest, didLoadResponse jsonResponse: Any)
    {
        self.dataRows = (jsonResponse as! NSDictionary)["records"] as! [NSDictionary]
        self.log(.debug, msg: "request:didLoadResponse: #records: \(self.dataRows.count)")
        DispatchQueue.main.async(execute: {
            self.tableView.reloadData()
        })
    }
    
    func request(_ request: SFRestRequest, didFailLoadWithError error: Error)
    {
        self.log(.debug, msg: "didFailLoadWithError: \(error)")
        // Add your failed error handling here
    }
    
    func requestDidCancelLoad(_ request: SFRestRequest)
    {
        self.log(.debug, msg: "requestDidCancelLoad: \(request)")
        // Add your failed error handling here
    }
    
    func requestDidTimeout(_ request: SFRestRequest)
    {
        self.log(.debug, msg: "requestDidTimeout: \(request)")
        // Add your failed error handling here
    }
    
    //MARK: UITextFieldDelegate
    
    
    func textFieldShouldReturn(_ textField: UITextField) -> Bool {
        textField.resignFirstResponder()
        return true
    }
    
    func textFieldDidBeginEditing(_ textField: UITextField) {
        // disable save while editing
        mealSaveButton.isEnabled = false
    }
    
    func textFieldDidEndEditing(_ textField: UITextField) {
        mealNameTxt = MealName.text!
        mealTypeVal = MealType.text!
        numberServedInt = Int16(Int(round(NumberServed.value)))
        mealSaveButton.isEnabled = true
    }
    


    //MARK: Actions
    
    @IBAction func MealSave(_ sender: UIButton) {
    
    }
}
