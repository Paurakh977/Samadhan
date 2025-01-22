// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use serde::{Deserialize, Serialize};
use reqwest::Client;
use tokio;
use winreg::enums::*;
use winreg::RegKey;
use serde_json;
use urlencoding;
use std::collections::HashMap;
use std::sync::Mutex;
use once_cell::sync::Lazy;

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

// App logo URLs dictionary
static APP_LOGOS: Lazy<HashMap<&'static str, &'static str>> = Lazy::new(|| {
    let mut m = HashMap::new();
    // Entertainment Apps
    m.insert("Netflix", "https://upload.wikimedia.org/wikipedia/commons/0/08/Netflix_2015_logo.svg");
    m.insert("YouTube", "https://upload.wikimedia.org/wikipedia/commons/e/ef/Youtube_logo.png");
    m.insert("Spotify", "https://upload.wikimedia.org/wikipedia/commons/1/19/Spotify_logo_without_text.svg");
    m.insert("Disney+", "https://upload.wikimedia.org/wikipedia/commons/3/3d/Disney%2B_logo.svg");
    m.insert("TikTok", "https://upload.wikimedia.org/wikipedia/commons/e/ef/TikTok_logo.svg");
    m.insert("Twitch", "https://upload.wikimedia.org/wikipedia/commons/2/26/Twitch_logo.svg");
    
    // Productivity Apps
    m.insert("Microsoft 365", "https://upload.wikimedia.org/wikipedia/commons/4/44/Microsoft_logo.svg");
    m.insert("Google Workspace", "https://cdn2.hubspot.net/hubfs/53/image8-2.jpg");
    m.insert("Slack", "https://upload.wikimedia.org/wikipedia/commons/d/d5/Slack_icon_2019.svg");
    m.insert("Zoom", "https://upload.wikimedia.org/wikipedia/commons/7/7b/Zoom_Communications_Logo.svg");
    m.insert("Notion", "https://upload.wikimedia.org/wikipedia/commons/4/45/Notion_app_logo.png");
    m.insert("Google Drive", "https://upload.wikimedia.org/wikipedia/commons/d/da/Google_Drive_logo.png");
    
    // Social Networking Apps
    m.insert("Facebook", "https://upload.wikimedia.org/wikipedia/commons/6/6c/Facebook_Logo_2023.png");
    m.insert("Instagram", "https://upload.wikimedia.org/wikipedia/commons/9/95/Instagram_logo_2022.svg");
    m.insert("X", "https://banner2.cleanpng.com/20240119/sut/transparent-x-logo-logo-brand-identity-company-organization-black-background-white-x-logo-for-1710916376217.webp");
    m.insert("LinkedIn", "https://upload.wikimedia.org/wikipedia/commons/c/ca/LinkedIn_logo_initials.png");
    m.insert("WhatsApp", "https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg");
    m.insert("Discord", "https://static.vecteezy.com/system/resources/previews/006/892/625/non_2x/discord-logo-icon-editorial-free-vector.jpg");
    m.insert("Reddit", "https://redditinc.com/hs-fs/hubfs/Reddit%20Inc/Brand/Reddit_Logo.png");
    m.insert("Telegram", "https://upload.wikimedia.org/wikipedia/commons/8/82/Telegram_logo.svg");
    
    // Other Common Apps
    m.insert("Google", "https://cdn2.hubspot.net/hubfs/53/image8-2.jpg");
    m.insert("Microsoft", "https://upload.wikimedia.org/wikipedia/commons/4/44/Microsoft_logo.svg");
    m.insert("Apple", "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fa/Apple_logo_black.svg/135px-Apple_logo_black.svg.png");
    m.insert("mail", "https://png.pngtree.com/template/20190725/ourmid/pngtree-gmail-logo-png-image_282635.jpg");
    m.insert("Hamro Patro","https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Hamro_Patro_wordmark.svg/1200px-Hamro_Patro_wordmark.svg.png");
    m.insert("GitLab", "data:image/png;base64,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");
    m
});

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
    // First check if we have the logo URL in our dictionary
    if let Some(url) = APP_LOGOS.get(app_name.as_str()) {
        return Ok(url.to_string());
    }

    println!("not found {}", app_name);  // Added this line to log missing apps

    // If not found in dictionary, try Google Custom Search API
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
