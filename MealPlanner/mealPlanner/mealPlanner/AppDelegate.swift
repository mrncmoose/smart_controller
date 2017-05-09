//
//  AppDelegate.swift
//  mealPlanner
//
//  Created by moose on 2/24/17.
//  Copyright © 2017 Fred Dunaway. All rights reserved.
//

import UIKit
import SalesforceSDKCore
import os.log

// Fill these in when creating a new Connected Application on Force.com
let RemoteAccessConsumerKey = "3MVG9uudbyLbNPZMEhXZt1Nfa7alq1Y0qk8KAA4f4zjEOJZCOq_M__H1kmjYaztKyS3niZ0mBdxxwzpAGIbKS";
let OAuthRedirectURI        = "mysampleapp://auth/success";


@UIApplicationMain
class AppDelegate: UIResponder, UIApplicationDelegate {

    var window: UIWindow?
    /// Salesforce Connected App properties (replace with your own…) /* 2 */
    let consumerKey = RemoteAccessConsumerKey
    let redirectURL = URL(string: OAuthRedirectURI)!
    

    override
    init()
    {
        super.init()
        SFLogger.shared().logLevel = .debug
        
        SalesforceSDKManager.shared().connectedAppId = RemoteAccessConsumerKey
        SalesforceSDKManager.shared().connectedAppCallbackUri = OAuthRedirectURI
        SalesforceSDKManager.shared().authScopes = ["web", "api"];
        SalesforceSDKManager.shared().postLaunchAction = {
            [unowned self] (launchActionList: SFSDKLaunchAction) in
            let launchActionString = SalesforceSDKManager.launchActionsStringRepresentation(launchActionList)
            self.log(.info, msg:"Post-launch: launch actions taken: \(launchActionString)");
//            self.setupRootViewController();
        }
        SalesforceSDKManager.shared().launchErrorAction = {
            [unowned self] (error: Error, launchActionList: SFSDKLaunchAction) in
            self.log(.error, msg:"Error during SDK launch: \(error.localizedDescription)")
//            self.initializeAppViewState()
            SalesforceSDKManager.shared().launch()
        }
//        SalesforceSDKManager.shared().postLogoutAction = {
//            [unowned self] in
//            self.handleSdkManagerLogout()
//        }
//        SalesforceSDKManager.shared().switchUserAction = {
//            [unowned self] (fromUser: SFUserAccount?, toUser: SFUserAccount?) -> () in
//            self.handleUserSwitch(fromUser, toUser: toUser)
//        }
    }


    func application(_ application: UIApplication, didFinishLaunchingWithOptions launchOptions: [UIApplicationLaunchOptionsKey: Any]?) -> Bool {
        // Override point for customization after application launch.
        return true
    }
    
    func applicationWillResignActive(_ application: UIApplication) {
        // Sent when the application is about to move from active to inactive state. This can occur for certain types of temporary interruptions (such as an incoming phone call or SMS message) or when the user quits the application and it begins the transition to the background state.
        // Use this method to pause ongoing tasks, disable timers, and invalidate graphics rendering callbacks. Games should use this method to pause the game.
    }

    func applicationDidEnterBackground(_ application: UIApplication) {
        // Use this method to release shared resources, save user data, invalidate timers, and store enough application state information to restore your application to its current state in case it is terminated later.
        // If your application supports background execution, this method is called instead of applicationWillTerminate: when the user quits.
    }

    func applicationWillEnterForeground(_ application: UIApplication) {
        // Called as part of the transition from the background to the active state; here you can undo many of the changes made on entering the background.
    }

    func applicationDidBecomeActive(_ application: UIApplication) {
        // Restart any tasks that were paused (or not yet started) while the application was inactive. If the application was previously in the background, optionally refresh the user interface.
    }

    func applicationWillTerminate(_ application: UIApplication) {
        // Called when the application is about to terminate. Save data if appropriate. See also applicationDidEnterBackground:.
    }

    //MARK:  private methods

}

