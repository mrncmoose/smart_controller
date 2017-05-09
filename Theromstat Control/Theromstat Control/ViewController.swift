//
//  ViewController.swift
//  Theromstat Control
//
//  Created by moose on 3/14/17.
//  Copyright © 2017 Fred Dunaway. All rights reserved.
//

import UIKit
import Alamofire
import SwiftyJSON


class ViewController: UIViewController {
    @IBOutlet weak var SetButton: UIButton!
    @IBOutlet weak var OnTempLabel: UILabel!
    @IBOutlet weak var OffTempLabel: UILabel!
    @IBOutlet weak var CurrentTemp: UILabel!
    @IBOutlet weak var OnDatePicker: UIDatePicker!
    @IBOutlet weak var OffDatePicker: UIDatePicker!
    @IBOutlet weak var OnTempSlider: UISlider!
    @IBOutlet weak var OffTempSlider: UISlider!
    
    var timer: Timer!
    let timerVal = 10.0
    var setEventsUrl: String?


    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
        loadCurrentTemp()
        self.loadEvents(url: setEventsUrl!)
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    @IBAction func OnTempSliderChanged(_ sender: UISlider) {
        self.OnTempLabel.text = String(format: "On: %.1f", self.OnTempSlider.value)
        self.OnTempLabel.reloadInputViews()
    }
    
    @IBAction func OffTempSliderAction(_ sender: UISlider) {
        self.OffTempLabel.text = String(format: "Off %.1f", self.OffTempSlider.value)
        self.OffTempLabel.reloadInputViews()
    }
    
    @IBAction func OnDateAction(_ sender: UIDatePicker) {
        
    }
    
    @IBAction func OffDateAction(_ sender: UIDatePicker) {
        
    }
    
    @IBAction func SetTempButtonAction(_ sender: UIButton) {
        setEvents(url: setEventsUrl!)
        
    }
    
    func loadCurrentTemp() {
        let path = Bundle.main.path(forResource: "Info", ofType: "plist")
        let dict = NSDictionary(contentsOfFile: path!)
        let baseUrl = dict?["server"] as! String
        let tempResource = dict?["temperatureResource"] as! String
        let eventResource = dict?["eventResource"] as! String
        setEventsUrl  = baseUrl + eventResource
        let currentTempUrl = baseUrl + tempResource
        getCurrentTemp(url: currentTempUrl, completionHandler: {(currentTempStr, error) in
            if currentTempStr != nil {
                print("About to load current temp of: " + currentTempStr!)
                self.CurrentTemp.text = "Current temperature: " + currentTempStr! + " C"
                self.CurrentTemp.reloadInputViews()
            } else {
                print("failed to get current temp with error: " + error.debugDescription)
            }
            DispatchQueue.main.async {
                self.CurrentTemp.reloadInputViews()
            }
        })
    }
    
    func getCurrentTemp(url: String, completionHandler: @escaping(_ retVal: String?, NSError?) -> Void) -> Void {
        print("Attempting to get current temp from url: " + url)
        var retVal: String? = nil
        Alamofire.request(url).validate().responseJSON { (responseData) -> Void in
            if((responseData.result.value) != nil) {
                debugPrint(responseData)
                let swiftyJsonVar = JSON(responseData.result.value!)
                retVal = swiftyJsonVar["current_temp"].stringValue
                print("Current temp: " + retVal!)
                completionHandler(retVal, nil)
            } else {
                print("Got back nil calling resource: " + url)
                completionHandler(nil, responseData.error! as NSError)
            }
        }
        return;
    }
    
    func loadEvents(url: String) {
        getEvents(url: url)
    }
    
    func getEvents(url: String) {
        Alamofire.request(url).validate().responseJSON { (rData) -> Void in
            if((rData.result.value) != nil) {
                let onOffdateFormatter = DateFormatter()
                onOffdateFormatter.locale = Locale(identifier: "en_US_POSIX")
                onOffdateFormatter.dateFormat = "yyyy-MM-dd HH:mm"
//                debugPrint(rData)
                let json = JSON(rData.result.value!)
                for event in json["events"].arrayValue {
                    self.OnDatePicker.setDate(onOffdateFormatter.date(from: event["on"]["when"].stringValue)!, animated: true)
                    self.OnTempLabel.text = "On: " + event["on"]["temperature"].stringValue + " C"
                    self.OnTempSlider.value = Float(event["on"]["temperature"].stringValue)!
                    
                    self.OffDatePicker.setDate(onOffdateFormatter.date(from: event["off"]["when"].stringValue)!, animated: true)
                    self.OffTempLabel.text = "Off: " + event["off"]["temperature"].stringValue + " C"
                    self.OffTempSlider.value = Float(event["off"]["temperature"].stringValue)!
                    self.view.reloadInputViews()
    
                }
            } else {
                print("Error attempting to get events data from: " + url)
            }
        }
        return;
    }
    
    func setEvents(url: String) {
        print("about to post events to: " + url)
        let currentTimeFormatter = DateFormatter()
        currentTimeFormatter.locale = Locale(identifier: "en_US_POSIX")
        currentTimeFormatter.dateFormat = "yyyy-MM-dd HH:mm:ss"
        let currentDate = Date()
        let onOffdateFormatter = DateFormatter()
        onOffdateFormatter.locale = Locale(identifier: "en_US_POSIX")
        onOffdateFormatter.dateFormat = "yyyy-MM-dd HH:mm"
        let params: Parameters = ["events": [["current_timestamp": currentTimeFormatter.string(from: currentDate), "off": ["temperature": String(format: "%.2f", self.OffTempSlider.value), "when": onOffdateFormatter.string(from: self.OffDatePicker.date)], "on": ["temperature":String(format: "%.2f", self.OnTempSlider.value), "when": onOffdateFormatter.string(from: self.OnDatePicker.date)]]]]
        Alamofire.request(url, method: .post, parameters: params, encoding: JSONEncoding.default)
            .responseJSON { response in
                if response.result.isFailure {
                    let err = response.result.error
                    let alert = UIAlertController(title: "Error", message: "Error attempting to save thermal events: " + (err?.localizedDescription)!, preferredStyle: UIAlertControllerStyle.alert)
                    alert.addAction(UIAlertAction(title: "OK", style: UIAlertActionStyle.default, handler: nil))
                    self.present(alert, animated: true, completion: nil)
                } else {
                    let alert = UIAlertController(title: "Set Event", message: "Successfully saved thermal event", preferredStyle: UIAlertControllerStyle.alert)
                    alert.addAction(UIAlertAction(title: "OK", style: UIAlertActionStyle.default, handler: nil))
                    self.present(alert, animated: true, completion: nil)
                }
        }
    }
    
    override func viewDidAppear(_ animated: Bool) {
        self.timer = Timer.scheduledTimer(timeInterval: timerVal, target: self, selector: #selector(self.updateCountdown), userInfo: nil, repeats: true)
    }

    func updateCountdown() {
        loadCurrentTemp()
    }
}

