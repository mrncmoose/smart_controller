//
//  ViewController.swift
//  Smart Temperature Controller UI
//
//  Created by moose on 10/27/19.
//  Copyright © 2019 Fred Dunaway. All rights reserved.
//

import Alamofire
import SwiftyJSON
import UIKit

class ViewController: UIViewController {

    @IBOutlet weak var EnterBuildingDate: UIDatePicker!
    @IBOutlet weak var motionMinutesSlider: UISlider!
    @IBOutlet weak var tempUnitSwitch: UISwitch!
    @IBOutlet weak var tempSetPointSlider: UISlider!
    @IBOutlet weak var setValuesButton: UIButton!
    @IBOutlet weak var motionDelayMinutesLabel: UILabel!
    @IBOutlet weak var tempUnitLabel: UILabel!
    @IBOutlet weak var tempSetPointLabel: UILabel!
    @IBOutlet weak var currentTempLabel: UILabel!
    
    var timer: Timer!
    let timerVal = 10.0
    var setEventsUrl: String?
    var tControllerUser: String = ""
    var tControllerPass: String = ""
    var apiKey: String = ""
    var tempUnit: String = "C"
    var plistURL : URL {
        let documentDirectoryURL =  try! FileManager.default.url(for: .documentDirectory, in: .userDomainMask, appropriateFor: nil, create: false)
        return documentDirectoryURL.appendingPathComponent("controllerSettings.plist")
    }
    
    @IBAction func OnDateAction(_ sender: UIDatePicker) {
    }
    @IBAction func motionMinutesAction(_ sender: UISlider) {
        self.motionDelayMinutesLabel.text = String(format: "Motion Delay: %.0f min", self.motionMinutesSlider.value)
        self.motionDelayMinutesLabel.reloadInputViews()
    }
    @IBAction func tempUnitAction(_ sender: UISwitch) {
    }
    @IBAction func tempSetPointActino(_ sender: UISlider) {
        self.tempSetPointLabel.text = String(format: "Set Temp: %.1f C", self.tempSetPointSlider.value)
        self.tempSetPointLabel.reloadInputViews()
    }
    @IBAction func setValuesAction(_ sender: UIButton) {
        setEvents(url: setEventsUrl!)
    }

    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
        loadCurrentTemp()
        self.loadEvents(url: setEventsUrl!)
    }

    func loadCurrentTemp() {
            let path = Bundle.main.path(forResource: "Info", ofType: "plist")
            let dict = NSDictionary(contentsOfFile: path!)
            let baseUrl = dict?["server"] as! String
            let tempResource = dict?["temperatureResource"] as! String
            let eventResource = dict?["eventResource"] as! String
    //        tControllerUser = (dict?["thermalControllerUser"] as! String)
    //        tControllerPass = (dict?["thermalControllerPass"] as! String)
            apiKey = "?api_id=" + (dict?["apiKey"] as! String)
            
            setEventsUrl  = baseUrl + eventResource + apiKey
            let currentTempUrl = baseUrl + tempResource + apiKey
            getCurrentTemp(url: currentTempUrl, completionHandler: {(currentTempStr, error) in
                if currentTempStr != nil {
    //                print("About to load current temp of: " + currentTempStr!)
                    self.currentTempLabel.text = "Current temperature: " + currentTempStr! + " C"
                    self.currentTempLabel.reloadInputViews()
                } else {
                    print("failed to get current temp with error: " + error.debugDescription)
                }
                DispatchQueue.main.async {
                    self.currentTempLabel.reloadInputViews()
                }
            })
        }
        
        func getCurrentTemp(url: String, completionHandler: @escaping(_ retVal: String?, NSError?) -> Void) -> Void {
    //        print("Attempting to get current temp from url: " + url)
            var retVal: String? = nil
            Alamofire.request(url).validate().responseJSON { (responseData) -> Void in
                if((responseData.result.value) != nil) {
    //                debugPrint(responseData)
                    let swiftyJsonVar = JSON(responseData.result.value!)
                    retVal = swiftyJsonVar["current_temp"].stringValue
    //                print("Current temp: " + retVal!)
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
    //        Alamofire.request(url).authenticate(user: tControllerUser, password: tControllerPass).validate().responseJSON { (rData) -> Void in
            Alamofire.request(url).validate().responseJSON { (rData) -> Void in
                if((rData.result.value) != nil) {
                    let onOffdateFormatter = DateFormatter()
                    onOffdateFormatter.locale = Locale(identifier: "en_US_POSIX")
                    onOffdateFormatter.dateFormat = "yyyy-MM-dd HH:mm"
                    debugPrint(rData)
                    let json = JSON(rData.result.value!)
                    for event in json["events"].arrayValue {
                        self.EnterBuildingDate.setDate(onOffdateFormatter.date(from: event["on"]["when"].stringValue)!, animated: true)
                        self.tempSetPointLabel.text = "Set Temp: " + event["on"]["temperature"].stringValue + " C"
                        self.tempSetPointSlider.value = Float(event["on"]["temperature"].stringValue)!
                        let motionDelayMins:Float = Float(event["on"]["motion_delay_seconds"].stringValue)!/60
                        self.motionMinutesSlider.value = motionDelayMins
                        self.motionDelayMinutesLabel.text = String(format: "Motion Delay: %.0f min", motionDelayMins)
                        self.view.reloadInputViews()
        
                    }
                } else {
                    print("Error attempting to get events data from: " + url)
                }
            }
            return;
        }
        
        func setEvents(url: String) {
    //        print("about to post events to: " + url)
            let currentTimeFormatter = DateFormatter()
            currentTimeFormatter.locale = Locale(identifier: "en_US_POSIX")
            currentTimeFormatter.dateFormat = "yyyy-MM-dd HH:mm:ss"
    //        let currentDate = Date()
            let onOffdateFormatter = DateFormatter()
            let motionDelaySecs:Int = Int(self.motionMinutesSlider.value*60);
            onOffdateFormatter.locale = Locale(identifier: "en_US_POSIX")
            onOffdateFormatter.dateFormat = "yyyy-MM-dd HH:mm"
            let params: [String: Any] = [
                "events": [[
                    "off": ["temperature":"-42"],
                    "on":
                        [
                        "temperature":String(format: "%.2f", self.tempSetPointSlider.value),
                        "when": onOffdateFormatter.string(from: self.EnterBuildingDate.date),
                        "motion_delay_seconds":String(format: "%d", motionDelaySecs),
                        ]
                ]]
            ]
    //        debugPrint(params)
            Alamofire.request(url, method: .post, parameters: params, encoding: JSONEncoding.default).authenticate(user: tControllerUser, password: tControllerPass)
                .responseJSON { response in
                    if response.result.isFailure {
                        let err = response.result.error
                        let alert = UIAlertController(title: "Error", message: "Error attempting to save thermal events: " + (err?.localizedDescription)!, preferredStyle: UIAlertController.Style.alert)
                        alert.addAction(UIAlertAction(title: "OK", style: UIAlertAction.Style.default, handler: nil))
                        self.present(alert, animated: true, completion: nil)
                    } else {
                        let alert = UIAlertController(title: "Set Event", message: "Successfully saved thermal event", preferredStyle: UIAlertController.Style.alert)
                        alert.addAction(UIAlertAction(title: "OK", style: UIAlertAction.Style.default, handler: nil))
                        self.present(alert, animated: true, completion: nil)
                    }
            }
        }
    
        override func viewDidAppear(_ animated: Bool) {
            self.timer = Timer.scheduledTimer(timeInterval: timerVal, target: self, selector: #selector(self.updateCountdown), userInfo: nil, repeats: true)
        }

        @objc func updateCountdown() {
            loadCurrentTemp()
        }

}

