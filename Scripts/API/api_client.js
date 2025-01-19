// Import node-fetch
import fetch from 'node-fetch';

const API_BASE = 'http://0.0.0.0:5000';

// Function to get access token with custom credentials
async function getAccessToken(username, password) {
    const startTime = performance.now();
    try {
        const response = await fetch(`${API_BASE}/token`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `username=${username}&password=${password}`
        });

        if (!response.ok) {
            throw new Error(`Login failed! Check your username and password`);
        }

        const data = await response.json();
        const endTime = performance.now();
        console.log(`Token fetch took ${(endTime - startTime).toFixed(2)}ms`);
        return data.access_token;
    } catch (error) {
        const endTime = performance.now();
        console.error('Error getting token:', error.message);
        console.error(`Failed request took ${(endTime - startTime).toFixed(2)}ms`);
        throw error;
    }
}

// Function to get phone number by username
async function getPhoneNumber(searchUsername, loginUsername, loginPassword) {
    const startTime = performance.now();
    try {
        // First get the token using provided credentials
        const token = await getAccessToken(loginUsername, loginPassword);
        const tokenTime = performance.now();
        console.log('Successfully logged in!');

        // Then use the token to get the phone number
        const response = await fetch(`${API_BASE}/get_phnumber?username=${searchUsername}`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (!response.ok) {
            throw new Error(`Could not find phone number for username: ${searchUsername}`);
        }

        const data = await response.json();
        const endTime = performance.now();
        
        // Calculate timing breakdowns
        const totalTime = endTime - startTime;
        const tokenFetchTime = tokenTime - startTime;
        const dataFetchTime = endTime - tokenTime;
        
        console.log('\nTiming Breakdown:');
        console.log(`├─ Total time: ${totalTime.toFixed(2)}ms`);
        console.log(`├─ Token fetch: ${tokenFetchTime.toFixed(2)}ms`);
        console.log(`└─ Data fetch: ${dataFetchTime.toFixed(2)}ms`);
        
        return data;
    } catch (error) {
        const endTime = performance.now();
        console.error('Error:', error.message);
        console.error(`Failed request took ${(endTime - startTime).toFixed(2)}ms`);
        throw error;
    }
}

// Example usage
async function main() {
    console.log('Starting API request...');
    const overallStart = performance.now();
    
    try {
        // Using test_user credentials
        console.log('\nTesting test_user credentials');
        const result = await getPhoneNumber('dada', 'test_user', 'test123');
        console.log('Phone number result:', result);
        
        const overallEnd = performance.now();
        console.log(`\nTotal script execution time: ${(overallEnd - overallStart).toFixed(2)}ms`);
    } catch (error) {
        const overallEnd = performance.now();
        console.error('Main error:', error.message);
        console.error(`Script failed after ${(overallEnd - overallStart).toFixed(2)}ms`);
    }
}

// Run the example
main(); 