use reqwest::{Client, header::{self, HeaderMap, HeaderValue}};
use serde::Deserialize;
use std::time::{Duration, Instant};
use tokio::time::timeout;

// Constants
const API_BASE: &str = "http://127.0.0.1:5000";
const REQUEST_TIMEOUT: Duration = Duration::from_secs(5);
const POOL_IDLE_TIMEOUT: Duration = Duration::from_secs(90);
const MAX_RETRIES: u32 = 2;

#[derive(Debug, Deserialize)]
struct TokenResponse {
    access_token: String,
    #[serde(rename = "token_type")]
    _token_type: String,
}

#[derive(Debug, Deserialize)]
struct PhoneNumberResponse {
    username: String,
    phnumber: String,
}

#[derive(Debug)]
struct TimingInfo {
    token_fetch: Duration,
    data_fetch: Duration,
    total: Duration,
}

impl TimingInfo {
    fn display(&self) {
        println!("\nTiming Breakdown:");
        println!("├─ Total time: {:.2?}", self.total);
        println!("├─ Token fetch: {:.2?}", self.token_fetch);
        println!("└─ Data fetch: {:.2?}", self.data_fetch);
    }
}

// Custom error type
#[derive(Debug)]
enum ApiError {
    Network(reqwest::Error),
    Auth(String),
    Api(String),
    Timeout,
}

impl std::fmt::Display for ApiError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            ApiError::Network(e) => write!(f, "Network error: {}", e),
            ApiError::Auth(msg) => write!(f, "Authentication error: {}", msg),
            ApiError::Api(msg) => write!(f, "API error: {}", msg),
            ApiError::Timeout => write!(f, "Request timed out"),
        }
    }
}

impl std::error::Error for ApiError {}

impl From<reqwest::Error> for ApiError {
    fn from(err: reqwest::Error) -> Self {
        ApiError::Network(err)
    }
}

impl From<tokio::time::error::Elapsed> for ApiError {
    fn from(_: tokio::time::error::Elapsed) -> Self {
        ApiError::Timeout
    }
}

// API Client struct to manage state and reuse
struct ApiClient {
    client: Client,
    cached_token: Option<(String, Instant)>,
    token_expiry: Duration,
}

impl ApiClient {
    fn new() -> Self {
        let mut headers = HeaderMap::new();
        headers.insert(
            header::CONTENT_TYPE,
            HeaderValue::from_static("application/x-www-form-urlencoded"),
        );

        let client = Client::builder()
            .timeout(REQUEST_TIMEOUT)
            .pool_idle_timeout(POOL_IDLE_TIMEOUT)
            .default_headers(headers)
            .build()
            .expect("Failed to create HTTP client");

        Self {
            client,
            cached_token: None,
            token_expiry: Duration::from_secs(60 * 29), // 29 minutes (just under the 30-minute server expiry)
        }
    }

    async fn get_access_token(&mut self, username: &str, password: &str) -> Result<String, ApiError> {
        // Check cached token
        if let Some((token, created_at)) = &self.cached_token {
            if created_at.elapsed() < self.token_expiry {
                return Ok(token.clone());
            }
        }

        let start = Instant::now();
        
        let params = [("username", username), ("password", password)];
        let response = timeout(
            REQUEST_TIMEOUT,
            self.client
                .post(format!("{}/token", API_BASE))
                .form(&params)
                .send()
        ).await??;

        if !response.status().is_success() {
            let duration = start.elapsed();
            println!("Failed request took {:.2?}", duration);
            return Err(ApiError::Auth("Invalid credentials".to_string()));
        }

        let token_data: TokenResponse = response.json().await?;
        let duration = start.elapsed();
        println!("Token fetch took {:.2?}", duration);
        
        // Cache the token
        self.cached_token = Some((token_data.access_token.clone(), Instant::now()));
        Ok(token_data.access_token)
    }

    async fn get_phone_number(
        &mut self,
        search_username: &str,
        login_username: &str,
        login_password: &str,
    ) -> Result<(PhoneNumberResponse, TimingInfo), ApiError> {
        let start = Instant::now();
        let mut last_error = None;

        // Retry logic for network errors
        for attempt in 0..MAX_RETRIES {
            if attempt > 0 {
                println!("Retry attempt {}", attempt);
            }

            match self.try_get_phone_number(search_username, login_username, login_password, start).await {
                Ok(result) => return Ok(result),
                Err(e) => {
                    match &e {
                        ApiError::Network(_) | ApiError::Timeout => {
                            last_error = Some(e);
                            continue;
                        }
                        _ => return Err(e),
                    }
                }
            }
        }

        Err(last_error.unwrap_or_else(|| ApiError::Api("Max retries exceeded".to_string())))
    }

    async fn try_get_phone_number(
        &mut self,
        search_username: &str,
        login_username: &str,
        login_password: &str,
        start: Instant,
    ) -> Result<(PhoneNumberResponse, TimingInfo), ApiError> {
        let token = self.get_access_token(login_username, login_password).await?;
        let token_time = start.elapsed();
        println!("Successfully logged in!");

        let response = timeout(
            REQUEST_TIMEOUT,
            self.client
                .get(format!("{}/get_phnumber", API_BASE))
                .query(&[("username", search_username)])
                .header(header::AUTHORIZATION, format!("Bearer {}", token))
                .send()
        ).await??;

        if !response.status().is_success() {
            return Err(ApiError::Api(format!(
                "Could not find phone number for username: {}", 
                search_username
            )));
        }

        let data = response.json().await?;
        let end_time = start.elapsed();

        Ok((data, TimingInfo {
            total: end_time,
            token_fetch: token_time,
            data_fetch: end_time - token_time,
        }))
    }
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("Starting API request...");
    let overall_start = Instant::now();

    let mut client = ApiClient::new();

    // Using test_user credentials
    println!("\nTesting test_user credentials");
    match client.get_phone_number("dada", "test_user", "test123").await {
        Ok((result, timing)) => {
            println!("Phone number result: {:?}", result);
            timing.display();
            let overall_duration = overall_start.elapsed();
            println!("\nTotal script execution time: {:.2?}", overall_duration);

            // Make a second request to demonstrate token caching
            println!("\nMaking second request (should be faster due to token caching)");
            let second_start = Instant::now();
            let (result2, timing2) = client.get_phone_number("dada", "test_user", "test123").await?;
            println!("Second request result: {:?}", result2);
            timing2.display();
            println!("\nSecond request total time: {:.2?}", second_start.elapsed());
        }
        Err(e) => {
            let overall_duration = overall_start.elapsed();
            eprintln!("Error: {}", e);
            eprintln!("Script failed after {:.2?}", overall_duration);
        }
    }

    Ok(())
}