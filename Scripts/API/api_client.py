import aiohttp
import asyncio
import time
from dataclasses import dataclass
from typing import Optional, Tuple, Dict
from datetime import datetime, timedelta

# Constants
API_BASE = "http://127.0.0.1:5000"
REQUEST_TIMEOUT = 5.0  # seconds
MAX_RETRIES = 2

@dataclass
class TokenResponse:
    access_token: str
    token_type: str

@dataclass
class PhoneNumberResponse:
    username: str
    phnumber: str

@dataclass
class TimingInfo:
    token_fetch: float
    data_fetch: float
    total: float

    def display(self):
        print("\nTiming Breakdown:")
        print(f"├─ Total time: {self.total*1000:.2f}ms")
        print(f"├─ Token fetch: {self.token_fetch*1000:.2f}ms")
        print(f"└─ Data fetch: {self.data_fetch*1000:.2f}ms")

class ApiError(Exception):
    pass

class NetworkError(ApiError):
    pass

class AuthError(ApiError):
    pass

class ApiResponseError(ApiError):
    pass

class ApiClient:
    def __init__(self):
        self.timeout = aiohttp.ClientTimeout(total=REQUEST_TIMEOUT)
        self.cached_token: Optional[Tuple[str, float]] = None
        self.token_expiry = 29 * 60  # 29 minutes in seconds
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            timeout=self.timeout,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def get_access_token(self, username: str, password: str) -> str:
        # Check cached token
        if self.cached_token:
            token, created_at = self.cached_token
            if time.time() - created_at < self.token_expiry:
                return token

        start_time = time.perf_counter()
        try:
            async with self.session.post(
                f"{API_BASE}/token",
                data={"username": username, "password": password}
            ) as response:
                duration = time.perf_counter() - start_time
                
                if not response.ok:
                    print(f"Failed request took {duration*1000:.2f}ms")
                    raise AuthError("Invalid credentials")
                
                data = await response.json()
                print(f"Token fetch took {duration*1000:.2f}ms")
                
                # Cache the token
                self.cached_token = (data["access_token"], time.time())
                return data["access_token"]
                
        except aiohttp.ClientError as e:
            raise NetworkError(f"Network error: {e}")

    async def get_phone_number(
        self,
        search_username: str,
        login_username: str,
        login_password: str
    ) -> Tuple[PhoneNumberResponse, TimingInfo]:
        start_time = time.perf_counter()
        last_error = None

        # Retry logic for network errors
        for attempt in range(MAX_RETRIES):
            if attempt > 0:
                print(f"Retry attempt {attempt}")

            try:
                result = await self._try_get_phone_number(
                    search_username, 
                    login_username, 
                    login_password, 
                    start_time
                )
                return result
            except (NetworkError, asyncio.TimeoutError) as e:
                last_error = e
                continue
            except ApiError as e:
                raise e

        raise last_error or ApiError("Max retries exceeded")

    async def _try_get_phone_number(
        self,
        search_username: str,
        login_username: str,
        login_password: str,
        start_time: float
    ) -> Tuple[PhoneNumberResponse, TimingInfo]:
        # First get the token
        token = await self.get_access_token(login_username, login_password)
        token_time = time.perf_counter() - start_time
        print("Successfully logged in!")

        # Then use the token to get the phone number
        try:
            async with self.session.get(
                f"{API_BASE}/get_phnumber",
                params={"username": search_username},
                headers={"Authorization": f"Bearer {token}"}
            ) as response:
                if not response.ok:
                    raise ApiResponseError(f"Could not find phone number for username: {search_username}")
                
                data = await response.json()
                end_time = time.perf_counter() - start_time
                
                timing = TimingInfo(
                    token_fetch=token_time,
                    data_fetch=end_time - token_time,
                    total=end_time
                )
                
                return PhoneNumberResponse(**data), timing
                
        except aiohttp.ClientError as e:
            raise NetworkError(f"Network error: {e}")

async def main():
    print("Starting API request...")
    overall_start = time.perf_counter()
    
    async with ApiClient() as client:
        try:
            # Using test_user credentials
            print("\nTesting test_user credentials")
            result, timing = await client.get_phone_number(
                "dada", "test_user", "test123"
            )
            print(f"Phone number result: {result}")
            timing.display()
            
            overall_duration = time.perf_counter() - overall_start
            print(f"\nTotal script execution time: {overall_duration*1000:.2f}ms")

            # Make a second request to demonstrate token caching
            print("\nMaking second request (should be faster due to token caching)")
            second_start = time.perf_counter()
            result2, timing2 = await client.get_phone_number(
                "dada", "test_user", "test123"
            )
            print(f"Second request result: {result2}")
            timing2.display()
            print(f"\nSecond request total time: {(time.perf_counter() - second_start)*1000:.2f}ms")
            
        except ApiError as e:
            overall_duration = time.perf_counter() - overall_start
            print(f"Error: {e}")
            print(f"Script failed after {overall_duration*1000:.2f}ms")

if __name__ == "__main__":
    asyncio.run(main()) 