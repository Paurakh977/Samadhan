from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from pydantic import BaseModel
import mysql.connector
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (replace "*" with specific origins in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")  # Get from environment or use default
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Database configuration from environment variables
db_config = {
    "host": os.getenv("DB_HOST", "127.0.0.1"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "samadhandb"),
}

# Mock user database (replace with your actual database)
fake_users_db = {
    "admin": {
        "username": "admin",
        "hashed_password": pwd_context.hash(os.getenv("API_ADMIN_PASSWORD", "adminpassword")),
    },
    "test_user": {
        "username": "test_user",
        "hashed_password": pwd_context.hash(os.getenv("API_TEST_USER_PASSWORD", "test123")),
    }
}

# Pydantic model for token
class Token(BaseModel):
    access_token: str
    token_type: str

# Pydantic model for user
class User(BaseModel):
    username: str

# Function to verify password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Function to authenticate user
def authenticate_user(username: str, password: str):
    if username not in fake_users_db:
        return False
    user = fake_users_db[username]
    if not verify_password(password, user["hashed_password"]):
        return False
    return user

# Function to create access token
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Dependency to get current user from token
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    if username not in fake_users_db:
        raise credentials_exception
    return User(username=username)

# Token endpoint
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Function to fetch phone number by username
def get_phnumber_by_username(username: str) -> str | None:
    try:
        # Connect to the database
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        # Query to fetch the phone number
        query = "SELECT phnumber FROM user_info_manual WHERE username = %s"
        cursor.execute(query, (username,))

        # Fetch the result
        result = cursor.fetchone()

        # Close the cursor and connection
        cursor.close()
        connection.close()

        # Return the phone number if found, else None
        return result["phnumber"] if result else None

    except Exception as e:
        logger.error(f"Error fetching phone number for username {username}: {e}")
        return None

# API endpoint to get phone number by username
@app.get("/get_phnumber")
async def get_phnumber(
    username: str = Query(..., description="The username to search for"),
    current_user: User = Depends(get_current_user),  # Require authentication
):
    if not username:
        logger.warning("Username not provided in request")
        raise HTTPException(status_code=400, detail="Username is required")

    # Fetch the phone number
    phnumber = get_phnumber_by_username(username)

    if phnumber:
        logger.info(f"Phone number found for username {username}")
        return {"username": username, "phnumber": phnumber}
    else:
        logger.warning(f"Username {username} not found")
        raise HTTPException(status_code=404, detail="Username not found")

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Run the FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)