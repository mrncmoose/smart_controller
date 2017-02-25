//
//  MealTableViewController.swift
//  userIosTest
//
//  Created by moose on 2/24/17.
//  Copyright © 2017 Salesforce. All rights reserved.
//

import UIKit
import SalesforceSDKCore

class MealTableViewController: UITableViewController, SFRestDelegate {
    var dataRows = [NSDictionary]()

    override func viewDidLoad() {
        super.viewDidLoad()

        // Uncomment the following line to preserve selection between presentations
        // self.clearsSelectionOnViewWillAppear = false

        // Uncomment the following line to display an Edit button in the navigation bar for this view controller.
        self.navigationItem.rightBarButtonItem = self.editButtonItem
        
        //Here we use a query that should work on either Force.com or Database.com
        //let request = SFRestAPI.sharedInstance().request(forQuery:"SELECT Name FROM User LIMIT 10");
        let request = SFRestAPI.sharedInstance().request(forQuery:"select Id, Name, moosewareinc__type__c, moosewareinc__Number_served__c, moosewareinc__Meal_Date__c from moosewareinc__Meal__c limit 10");
        SFRestAPI.sharedInstance().send(request, delegate: self);
        //REST info
        // get resource:  /services/data/v37.0/sobjects/moosewareinc__Meal__c
        // put message:
        //{"Name" : "Meal 3","moosewareinc__Number_served__c" : "2","moosewareinc__Meal_Date__c" : "2016-04-01"}
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


    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }

    // MARK: - Table view data source

    override func numberOfSections(in tableView: UITableView) -> Int {
        return 1
    }

    override func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return self.dataRows.count
    }

    
    override func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
//        let cell = tableView.dequeueReusableCell(withIdentifier: "reuseIdentifier", for: indexPath)
        
        let cellIdentifier = "MealTableViewCell"
        guard let cell = tableView.dequeueReusableCell(withIdentifier: cellIdentifier, for: indexPath) as? MealTableViewCell  else {
            fatalError("The dequeued cell is not an instance of MealTableViewCell.")
        }
        
        // Configure the cell to show the data.
        let obj = dataRows[indexPath.row]
//        cell.textLabel!.text = obj["Name"] as? String
        cell.mealNameLabel.text = obj["Name"] as? String

        return cell
    }
    

    /*
    // Override to support conditional editing of the table view.
    override func tableView(_ tableView: UITableView, canEditRowAt indexPath: IndexPath) -> Bool {
        // Return false if you do not want the specified item to be editable.
        return true
    }
    */

    /*
    // Override to support editing the table view.
    override func tableView(_ tableView: UITableView, commit editingStyle: UITableViewCellEditingStyle, forRowAt indexPath: IndexPath) {
        if editingStyle == .delete {
            // Delete the row from the data source
            tableView.deleteRows(at: [indexPath], with: .fade)
        } else if editingStyle == .insert {
            // Create a new instance of the appropriate class, insert it into the array, and add a new row to the table view
        }    
    }
    */

    /*
    // Override to support rearranging the table view.
    override func tableView(_ tableView: UITableView, moveRowAt fromIndexPath: IndexPath, to: IndexPath) {

    }
    */

    /*
    // Override to support conditional rearranging of the table view.
    override func tableView(_ tableView: UITableView, canMoveRowAt indexPath: IndexPath) -> Bool {
        // Return false if you do not want the item to be re-orderable.
        return true
    }
    */

    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destinationViewController.
        // Pass the selected object to the new view controller.
    }
    */

}
