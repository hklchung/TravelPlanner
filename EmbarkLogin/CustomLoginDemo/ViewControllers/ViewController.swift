//
//  ViewController.swift
//  CustomLoginDemo
//
//  Created by Edward on 5/4/2020.
//  Copyright © 2020 Edward. All rights reserved.
//

import UIKit
import AVKit

class ViewController: UIViewController {

    var videoPlayer:AVPlayer?
    var videoPlayerLayer:AVPlayerLayer?
    
    
    
    @IBOutlet weak var signUpButton: UIButton!
    @IBOutlet weak var loginButton: UIButton!
    
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
        
        setUpElements()
    }

    override func viewWillAppear(_ animated: Bool) {
        // Set up video at the background
        setUpVideo()
    }
    
    func setUpElements() {
        Utilities.styleFilledButton(signUpButton)
        Utilities.styleFilledButton(loginButton)
        
        
    }
    func setUpVideo(){
        
        // get the path to the resource in the bundle
        let bundlePath = Bundle.main.path(forResource: "bgvideo", ofType: "mp4")
        
        guard bundlePath != nil else {
            return
        }
        
        // Create a url from it
        let url = URL(fileURLWithPath: bundlePath!)
        
        // Create the video player item
        let item = AVPlayerItem(url: url)
        
        // Create the player
        videoPlayer = AVPlayer(playerItem: item)
        
        // Create the layer
        videoPlayerLayer = AVPlayerLayer(player: videoPlayer!)
        
        videoPlayerLayer?.frame = CGRect(x:-self.view.frame.size.width*1.5 , y:0,
                                         width: self.view.frame.size.width*4,
                                         height:self.view.frame.size.height
            )
        
        // Adjust the size and frame
        view.layer.insertSublayer(videoPlayerLayer!, at: 0)
        // Display the frame and play it
        videoPlayer?.playImmediately(atRate: 0.3)
    }
}

