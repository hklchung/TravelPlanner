//
//  LoginViewController.swift
//  CustomLoginDemo
//
//  Created by Edward on 5/4/2020.
//  Copyright © 2020 Edward. All rights reserved.
//

import UIKit
import Firebase


class LoginViewController: UIViewController {

    
    @IBOutlet weak var emailTextField: UITextField!
    @IBOutlet weak var passwordTextField: UITextField!
    @IBOutlet weak var loginButton: UIButton!
    @IBOutlet weak var errorLabel: UILabel!
    
    
    override func viewDidLoad() {
        super.viewDidLoad()
       
        
        // Do any additional setup after loading the view.
        setUpElements()
    }
    
    func setUpElements() {
        
        // Hide the error label
        errorLabel.alpha = 0
        
        // Style the elements
        Utilities.styleTextField(emailTextField)
        Utilities.styleTextField(passwordTextField)
        Utilities.styleFilledButton(loginButton)
        
    }
    

    func validateFields() -> String? {
    
    // check that all fields are filled in
        if emailTextField.text?.trimmingCharacters(in: .whitespacesAndNewlines) == "" ||
            passwordTextField.text?.trimmingCharacters(in: .whitespacesAndNewlines) == ""  {
            return "Please fill in all fields."
            }
        return nil
        
    }
    

    @IBAction func loginTapped(_ sender: Any) {
        
        // Validate the text field
        let error=validateFields()
        if error != nil {
           showError(error!)
        }
        else {
            
        // Create cleaned text version
            let email = emailTextField.text!.trimmingCharacters(in: .whitespacesAndNewlines)
            let password = passwordTextField.text!.trimmingCharacters(in: .whitespacesAndNewlines)
            
        // Signing in the user
            Auth.auth().signIn(withEmail: email, password: password) { (result, err) in
                if err != nil {
                    // Couldn't sign in
                    self.errorLabel.text = err!.localizedDescription
                    self.errorLabel.alpha = 1
                }
                else {
                    self.transitionToHome()
                }
            }
        }
        
    }
    func showError(_ message:String) {
           errorLabel.text = message
           errorLabel.alpha = 1
       }
       
       func transitionToHome() {
           
           let homeViewController = storyboard?.instantiateViewController(identifier: Constants.Storyboard.homeViewController) as? HomeViewController
           view.window?.rootViewController = homeViewController
           view.window?.makeKeyAndVisible()
       }
    
    
}
