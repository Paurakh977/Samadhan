// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use serde::{Deserialize, Serialize};
use reqwest::Client;
use tokio;
use winreg::enums::*;
use winreg::RegKey;
use serde_json;
use urlencoding;

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

#[derive(Debug, Serialize)]
struct SignupResponse {
    success: bool,
    message: String
}

#[derive(Debug, Serialize)]
struct ActivityData {
    success: bool,
    data: Option<serde_json::Value>,
    error: Option<String>
}

#[derive(Debug, Serialize, Deserialize)]
struct GoogleSearchResponse {
    items: Option<Vec<GoogleSearchItem>>,
}

#[derive(Debug, Serialize, Deserialize)]
struct GoogleSearchItem {
    link: String,
}

const API_KEY: &str = "AIzaSyDn9muIE2c8RTXEfpf7D4vxfGKr8SrYP4A";
const SEARCH_ENGINE_ID: &str = "13a14d4f3d2c2486d";

#[derive(Debug, Serialize)]
struct AppUsageWithLogo {
    success: bool,
    data: Option<serde_json::Value>,
    error: Option<String>
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
async fn handle_google_signup(serialId: String) -> Result<GoogleLoginResponse, String> {
    println!("Received serialId for Google signup: {}", serialId); // Debug log
    
    let client = reqwest::Client::new();
    let response = client
        .post("http://localhost:5000/api/v1/auth/google-signup")
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
        Err(format!("Signup failed: {}", error_text))
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

#[tauri::command]
async fn handle_manual_signup(
    email: String,
    password: String,
    username: String,
) -> Result<SignupResponse, String> {
    let client = Client::new();
    
    // Get machine's serial number
    let serial_id = get_serial_number()?;
    
    // Send signup request
    let response = client
        .post("http://localhost:5000/api/v1/auth/manual-signup")
        .query(&[
            ("email", &email),
            ("password", &password),
            ("username", &username),
            ("serial_id", &serial_id),
        ])
        .send()
        .await
        .map_err(|e| format!("Network error: {}", e))?;

    if response.status().is_success() {
        Ok(SignupResponse {
            success: true,
            message: "Signup successful! Please login to continue.".to_string()
        })
    } else {
        let error_text = response.text().await
            .unwrap_or_else(|_| "Unknown error".to_string());
        Err(format!("Signup failed: {}", error_text))
    }
}

#[tauri::command]
async fn fetch_activity_data(email: String) -> Result<ActivityData, String> {
    let serial_id = get_serial_number()?;
    let client = reqwest::Client::new();
    
    let response = client
        .get("http://localhost:5000/api/v1/activity/daily")
        .query(&[
            ("email", &email),
            ("serial_id", &serial_id)
        ])
        .send()
        .await
        .map_err(|e| format!("Failed to send request: {}", e))?;

    if response.status().is_success() {
        let data = response
            .json::<serde_json::Value>()
            .await
            .map_err(|e| format!("Failed to parse response: {}", e))?;
        
        Ok(ActivityData {
            success: true,
            data: Some(data),
            error: None
        })
    } else {
        let error_text = response
            .text()
            .await
            .unwrap_or_else(|_| "Unknown error".to_string());
        
        Ok(ActivityData {
            success: false,
            data: None,
            error: Some(error_text)
        })
    }
}

#[tauri::command]
async fn fetch_app_usage_info(email: String) -> Result<AppUsageWithLogo, String> {
    let serial_id = get_serial_number()?;
    let client = reqwest::Client::new();
    
    // First, get the app usage data
    let response = client
        .get("http://localhost:5000/api/v1/activity/app-usage")
        .query(&[
            ("email", &email),
            ("serial_id", &serial_id)
        ])
        .send()
        .await
        .map_err(|e| format!("Failed to send request: {}", e))?;

    if !response.status().is_success() {
        let error_text = response
            .text()
            .await
            .unwrap_or_else(|_| "Unknown error".to_string());
        
        return Ok(AppUsageWithLogo {
            success: false,
            data: None,
            error: Some(error_text)
        });
    }

        let data = response
            .json::<serde_json::Value>()
            .await
            .map_err(|e| format!("Failed to parse response: {}", e))?;
        
    // Get the apps array from the nested data structure
    let apps = data["data"]["apps"].as_array();
    if let Some(apps) = apps {
        let mut processed_data = data.clone();
        let mut processed_apps = Vec::new();

        // Try to get cached logos first
        let cache_key = format!("app_logos_{}", email);
        let cached_logos = get_cached_logos(&cache_key);

        for app in apps {
            let mut app = app.clone();
            if let Some(tab_name) = app["tab_name"].as_str() {
                // Check cache first
                let logo_url = if let Some(cached_url) = cached_logos.get(tab_name) {
                    cached_url.clone()
                } else {
                    // If not in cache, fetch new logo
                    let logo_result = fetch_app_logo_internal(tab_name.to_string()).await;
                    match logo_result {
                        Ok(url) => {
                            // Cache the new URL
                            cache_logo(&cache_key, tab_name, &url);
                            url
                        }
                        Err(_) => String::new()
                    }
                };

                if let Some(obj) = app.as_object_mut() {
                    obj.insert("logo_url".to_string(), serde_json::Value::String(logo_url));
                }
            }
            processed_apps.push(app);
        }

        // Update the apps array in the processed data
        if let Some(obj) = processed_data["data"].as_object_mut() {
            obj.insert("apps".to_string(), serde_json::Value::Array(processed_apps));
        }

        Ok(AppUsageWithLogo {
            success: true,
            data: Some(processed_data),
            error: None
        })
    } else {
        Ok(AppUsageWithLogo {
            success: true,
            data: Some(data),
            error: None
        })
    }
}

// Internal function to fetch app logo
async fn fetch_app_logo_internal(app_name: String) -> Result<String, String> {
    let query = format!("application logo:{} logo filetype:png", app_name);
    let url = format!(
        "https://www.googleapis.com/customsearch/v1?q={}&key={}&cx={}&searchType=image",
        urlencoding::encode(&query),
        API_KEY,
        SEARCH_ENGINE_ID
    );

    match reqwest::get(&url).await {
        Ok(response) => {
            if response.status().is_success() {
                match response.json::<GoogleSearchResponse>().await {
                    Ok(data) => {
                        if let Some(items) = data.items {
                            for item in items {
                                if item.link.to_lowercase().ends_with(".png") {
                                    return Ok(item.link);
                                }
                            }
                        }
                        Err("No PNG image found".to_string())
                    }
                    Err(e) => Err(format!("Failed to parse response: {}", e))
                }
            } else {
                Err(format!("API request failed with status: {}", response.status()))
            }
        }
        Err(e) => Err(format!("Request failed: {}", e))
    }
}

// Cache management functions
use std::collections::HashMap;
use std::sync::Mutex;
use once_cell::sync::Lazy;

static LOGO_CACHE: Lazy<Mutex<HashMap<String, HashMap<String, String>>>> = 
    Lazy::new(|| Mutex::new(HashMap::new()));

fn get_cached_logos(cache_key: &str) -> HashMap<String, String> {
    LOGO_CACHE
        .lock()
        .unwrap()
        .get(cache_key)
        .cloned()
        .unwrap_or_default()
}

fn cache_logo(cache_key: &str, app_name: &str, logo_url: &str) {
    let mut cache = LOGO_CACHE.lock().unwrap();
    let app_cache = cache.entry(cache_key.to_string()).or_insert_with(HashMap::new);
    app_cache.insert(app_name.to_string(), logo_url.to_string());
}

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![
            handle_manual_login,
            handle_google_login,
            handle_google_signup,
            handle_logout,
            get_serial_number,
            check_login_status,
            handle_manual_signup,
            fetch_activity_data,
            fetch_app_usage_info,
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
