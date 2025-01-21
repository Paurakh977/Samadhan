// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use serde::{Deserialize, Serialize};
use reqwest::Client;
use tokio;
use winreg::enums::*;
use winreg::RegKey;
use serde_json;

#[derive(Debug, Deserialize)]
struct TokenResponse {
    access_token: String,
    token_type: String,
}

#[derive(Debug, Deserialize)]
struct PhoneNumberResponse {
    username: String,
    phnumber: String,
}

#[derive(Debug, Deserialize, Serialize)]
struct ManualLoginResponse {
    success: bool,
    username: String,
    email: String
}

#[derive(Debug, Serialize)]
struct GoogleLoginResponse {
    email: String,
    username: Option<String>
}

#[derive(Debug, Deserialize, Serialize)]
struct LoginStatus {
    is_logged_in: bool,
    email: Option<String>,
    username: Option<String>
}

#[tauri::command]
fn get_serial_number() -> Result<String, String> {
    let hklm = RegKey::predef(HKEY_LOCAL_MACHINE);
    let key = hklm.open_subkey("SOFTWARE\\Microsoft\\Cryptography")
        .map_err(|e| format!("Failed to open registry key: {}", e))?;
    
    let machine_guid: String = key.get_value("MachineGuid")
        .map_err(|e| format!("Failed to get MachineGuid: {}", e))?;
    
    Ok(machine_guid)
}

#[tauri::command]
async fn handle_manual_login(email: String, password: String) -> Result<ManualLoginResponse, String> {
    let client = Client::new();
    
    // Get machine's serial number
    let serial_id = get_serial_number()?;
    
    // Send login request
    let response = client
        .post("http://localhost:5000/api/v1/auth/manual-login")
        .query(&[
            ("email", &email),
            ("password", &password),
            ("serial_id", &serial_id)
        ])
        .send()
        .await
        .map_err(|e| format!("Network error: {}", e))?;

    if !response.status().is_success() {
        let error_text = response.text().await
            .unwrap_or_else(|_| "Unknown error".to_string());
        return Err(format!("Login failed: {}", error_text));
    }

    // Parse the response and get first name
    let mut login_data = response.json::<ManualLoginResponse>()
        .await
        .map_err(|e| format!("Failed to parse response: {}", e))?;
    
    // Update username to only include first name
    login_data.username = login_data.username.split_whitespace()
        .next()
        .unwrap_or(&login_data.username)
        .to_string();
    
    Ok(login_data)
}

#[tauri::command]
async fn handle_google_login(serialId: String) -> Result<GoogleLoginResponse, String> {
    println!("Received serialId: {}", serialId); // Debug log
    
    let client = reqwest::Client::new();
    let response = client
        .post("http://localhost:5000/api/v1/auth/google-login")
        .query(&[("serial_id", &serialId)])
        .send()
        .await
        .map_err(|e| {
            println!("Network error: {}", e); // Debug log
            e.to_string()
        })?;

    if response.status().is_success() {
        let data: serde_json::Value = response.json().await.map_err(|e| e.to_string())?;
        println!("Response data: {:?}", data); // Debug log
        
        let email = data.get("email")
            .and_then(|v| v.as_str())
            .ok_or("Email not found in response")?;
        
        // Get first name from username
        let username = data.get("username")
            .and_then(|v| v.as_str())
            .map(|full_name| full_name.split_whitespace().next().unwrap_or(full_name).to_string());
        
        Ok(GoogleLoginResponse { 
            email: email.to_string(),
            username
        })
    } else {
        let error_text = response.text().await.map_err(|e| e.to_string())?;
        println!("Error response: {}", error_text); // Debug log
        Err(format!("Login failed: {}", error_text))
    }
}

#[tauri::command]
async fn handle_logout(email: String) -> Result<String, String> {
    let client = Client::new();
    let response = client
        .post("http://localhost:5000/api/v1/auth/logout")
        .query(&[("email", &email)])
        .send()
        .await
        .map_err(|e| e.to_string())?;

    if response.status().is_success() {
        Ok("Logged out successfully".to_string())
    } else {
        let error_text = response.text().await.map_err(|e| e.to_string())?;
        Err(format!("Logout failed: {}", error_text))
    }
}

#[tauri::command]
async fn check_login_status() -> Result<LoginStatus, String> {
    let serial_id = get_serial_number().map_err(|e| e.to_string())?;
    
    let client = reqwest::Client::new();
    let response = client
        .get("http://localhost:5000/api/v1/auth/check-login")
        .query(&[("serial_id", serial_id)])
        .send()
        .await
        .map_err(|e| format!("Failed to send request: {}", e))?;

    if response.status().is_success() {
        let status = response
            .json::<LoginStatus>()
            .await
            .map_err(|e| format!("Failed to parse response: {}", e))?;
        Ok(status)
    } else {
        let error_text = response
            .text()
            .await
            .unwrap_or_else(|_| "Unknown error".to_string());
        Err(format!("Login check failed: {}", error_text))
    }
}

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![
            handle_manual_login,
            handle_google_login,
            handle_logout,
            get_serial_number,
            check_login_status
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
