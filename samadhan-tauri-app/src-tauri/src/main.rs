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

#[derive(Debug, Deserialize)]
struct ManualLoginResponse {
    success: bool,
    username: String,
    email: String
}

fn get_serial_number() -> Result<String, String> {
    let hklm = RegKey::predef(HKEY_LOCAL_MACHINE);
    let key = hklm.open_subkey("SOFTWARE\\Microsoft\\Cryptography")
        .map_err(|e| format!("Failed to open registry key: {}", e))?;
    
    let machine_guid: String = key.get_value("MachineGuid")
        .map_err(|e| format!("Failed to get MachineGuid: {}", e))?;
    
    Ok(machine_guid)
}

#[tauri::command]
async fn handle_manual_login(email: String, password: String) -> Result<String, String> {
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

    let login_data: ManualLoginResponse = response
        .json()
        .await
        .map_err(|e| format!("Failed to parse response: {}", e))?;

    if login_data.success {
        Ok(login_data.username)
    } else {
        Err("Login failed".to_string())
    }
}

#[tauri::command]
async fn handle_google_login() -> Result<String, String> {
    let serial_id = get_serial_number().map_err(|e| e.to_string())?;
    
    let client = reqwest::Client::new();
    let response = client
        .post("http://localhost:5000/api/v1/auth/google-login")
        .query(&[("serial_id", &serial_id)])
        .send()
        .await
        .map_err(|e| e.to_string())?;

    if response.status().is_success() {
        let data: serde_json::Value = response.json().await.map_err(|e| e.to_string())?;
        if let Some(username) = data.get("username").and_then(|v| v.as_str()) {
            Ok(username.to_string())
        } else {
            Err("Username not found in response".to_string())
        }
    } else {
        let error_text = response.text().await.map_err(|e| e.to_string())?;
        Err(format!("Login failed: {}", error_text))
    }
}

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![
            handle_manual_login,
            handle_google_login
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
