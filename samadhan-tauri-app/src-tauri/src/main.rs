// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use serde::{Deserialize, Serialize};
use reqwest::Client;
use tokio;

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

#[tauri::command]
async fn handle_login(username: String) -> Result<String, String> {
    let client = Client::new();
    
    // First get access token using test_user's credentials from fake_users_db
    let token_response = client
        .post("http://localhost:5000/api/v1/auth/login")
        .form(&[
            ("username", "test_user"),
            ("password", "test123")
        ])
        .send()
        .await
        .map_err(|e| format!("Network error: {}", e))?;

    if !token_response.status().is_success() {
        let error_text = token_response.text().await
            .unwrap_or_else(|_| "Unknown error".to_string());
        return Err(format!("Authentication failed: {}", error_text));
    }

    let token_data: TokenResponse = token_response
        .json()
        .await
        .map_err(|e| format!("Failed to parse token response: {}", e))?;

    // Now use that token to get phone number for the username from frontend
    let phone_response = client
        .get("http://localhost:5000/api/v1/auth/get_phnumber")
        .query(&[("username", username)])
        .header(
            "Authorization",
            format!("Bearer {}", token_data.access_token)
        )
        .send()
        .await
        .map_err(|e| format!("Failed to fetch phone number: {}", e))?;

    if !phone_response.status().is_success() {
        let error_text = phone_response.text().await
            .unwrap_or_else(|_| "Unknown error".to_string());
        return Err(format!("Phone number fetch failed: {}", error_text));
    }

    let phone_data: PhoneNumberResponse = phone_response
        .json()
        .await
        .map_err(|e| format!("Failed to parse phone response: {}", e))?;

    Ok(phone_data.phnumber)
}

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![handle_login])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
