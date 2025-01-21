from datetime import timedelta
from typing import Any, Dict
from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import bcrypt
from app.core.security import create_access_token, verify_password
from app.core.config import settings, Settings
from app.db.database import get_db
from app.models.user import User
from app.schemas.token import Token
from app.schemas.user import User as UserSchema
from app.core.deps import get_current_user
from app.core.auth import fake_users_db
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os
import json
import logging
import mysql.connector
from dotenv import load_dotenv

# Load environment variables from the correct .env file
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))), '.env')
load_dotenv(env_path)

settings = Settings()
db_config = {
    'host': settings.DB_HOST,
    'user': settings.DB_USER,
    'password': settings.DB_PASSWORD,
    'database': settings.DB_NAME
}

router = APIRouter()

# Fixed salt for consistent hashing
FIXED_SALT = b"$2b$12$WMDnjnQGHfHlO7xVxtsUj."

def hash_password(password: str) -> str:
    """Hash password using fixed salt"""
    hashed = bcrypt.hashpw(password.encode("utf-8"), FIXED_SALT)
    return hashed.decode("utf-8")

def check_password(stored_password: str, provided_password: str) -> bool:
    """Check if provided password matches stored hash"""
    try:
        # Hash the provided password
        hashed_provided = hash_password(provided_password)
        print(f"Stored password hash: {stored_password}")
        print(f"Provided password hash: {hashed_provided}")
        return stored_password == hashed_provided
    except Exception as e:
        print(f"Password check error: {e}")
        return False

@router.post("/manual-login")
async def manual_login(
    email: str = Query(...),
    password: str = Query(...),
    serial_id: str = Query(...)
) -> Dict[str, Any]:
    """Manual login endpoint"""
    try:
        # Connect to database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # First check if user exists with email
        cursor.execute(
            "SELECT * FROM user_info_manual WHERE email = %s",
            (email,)
        )
        user = cursor.fetchone()

        if not user:
            raise HTTPException(
                status_code=401,
                detail="Incorrect email or password"
            )

        # Verify password
        if not check_password(user['password'], password):
            raise HTTPException(
                status_code=401,
                detail="Incorrect email or password"
            )

        # Check if device exists
        cursor.execute(
            "SELECT * FROM user_info_manual WHERE email = %s AND serial_id = %s",
            (email, serial_id)
        )
        device = cursor.fetchone()

        if device:
            # Update login status for this device
            cursor.execute(
                "UPDATE user_info_manual SET logged_in_status = 1 WHERE email = %s AND serial_id = %s",
                (email, serial_id)
            )
            # Log out other devices
            cursor.execute(
                "UPDATE user_info_manual SET logged_in_status = 0 WHERE email = %s AND serial_id != %s",
                (email, serial_id)
            )
        else:
            # Add new device for this user
            cursor.execute(
                """
                INSERT INTO user_info_manual 
                (email, password, username, serial_id, logged_in_status) 
                VALUES (%s, %s, %s, %s, 1)
                """,
                (email, user['password'], user['username'], serial_id)
            )
            # Log out other devices
            cursor.execute(
                "UPDATE user_info_manual SET logged_in_status = 0 WHERE email = %s AND serial_id != %s",
                (email, serial_id)
            )

        conn.commit()
        return {
            "success": True,
            "email": user['email'],
            "username": user['username']
        }

    except HTTPException as e:
        raise e
    except Exception as e:
        logging.error(f"Error in manual login: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Login failed: {str(e)}"
        )
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    # Check if user exists in fake_users_db
    if form_data.username not in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = fake_users_db[form_data.username]
    if not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    # Use user_id 1 for test_user and 2 for admin in the token
    user_id = 1 if form_data.username == "test_user" else 2
    access_token = create_access_token(
        user_id, expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }

@router.get("/get_phnumber")
def get_phone_number(
    username: str,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get phone number for any username if authenticated
    """
    db = next(get_db())
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail=f"User {username} not found"
        )
    return {
        "username": user.username,
        "phnumber": user.phnumber
    }

@router.post("/google-login")
async def google_login(
    serial_id: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Google OAuth login endpoint - Only for existing users"""
    try:
        # Load credentials from the correct .env file
        client_id = os.getenv("GOOGLE_CLIENT_ID")
        client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
        
        if not client_id or not client_secret:
            logging.error("Missing Google OAuth credentials in environment variables")
            raise HTTPException(
                status_code=400,
                detail="Authentication configuration error"
            )
            
        creds_data = {
            "installed": {
                "client_id": client_id,
                "client_secret": client_secret,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": ["http://localhost"]
            }
        }
        
        scopes = [
            "https://www.googleapis.com/auth/userinfo.profile",
            "https://www.googleapis.com/auth/userinfo.email",
            "openid",
        ]

        try:
            flow = InstalledAppFlow.from_client_config(creds_data, scopes)
            creds = flow.run_local_server(port=0)
        except Exception as e:
            logging.error(f"Google OAuth Flow Error: {str(e)}")
            raise HTTPException(status_code=400, detail="Failed to authenticate with Google")

        try:
            service = build("people", "v1", credentials=creds)
            profile = service.people().get(
                resourceName="people/me",
                personFields="names,emailAddresses"
            ).execute()

            name = profile.get("names", [{}])[0].get("displayName", "N/A")
            email = profile.get("emailAddresses", [{}])[0].get("value", "N/A")
            
            logging.info(f"Google login attempt - Email: {email}, Name: {name}")

            # Connect to database
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor(dictionary=True)

            try:
                # First check if user exists with this email
                cursor.execute(
                    "SELECT * FROM user_info_google WHERE email = %s",
                    (email,)
                )
                user = cursor.fetchone()

                if not user:
                    # User doesn't exist - they need to sign up first
                    raise HTTPException(
                        status_code=401,
                        detail="GOOGLE_USER_NOT_FOUND"
                    )

                # User exists, handle device login
                    cursor.execute(
                        "SELECT * FROM user_info_google WHERE email = %s AND serial_id = %s",
                        (email, serial_id)
                    )
                    device = cursor.fetchone()

                    if device:
                        # Update login status for this device
                        cursor.execute(
                            "UPDATE user_info_google SET logged_in_status = 1 WHERE email = %s AND serial_id = %s",
                            (email, serial_id)
                        )
                    else:
                        # Add new device for existing user
                        cursor.execute(
                            "INSERT INTO user_info_google (username, email, serial_id, logged_in_status) VALUES (%s, %s, %s, 1)",
                        (user['username'], email, serial_id)
                        )

                        # Log out other devices
                        cursor.execute(
                            "UPDATE user_info_google SET logged_in_status = 0 WHERE email = %s AND serial_id != %s",
                            (email, serial_id)
                    )

                conn.commit()
                return {
                    "success": True,
                    "username": user['username'],
                    "email": email
                }

            finally:
                cursor.close()
                conn.close()

        except HTTPException as e:
            raise e
        except Exception as e:
            logging.error(f"Error getting user info from Google: {str(e)}")
            raise HTTPException(status_code=400, detail="Failed to get user info")

    except Exception as e:
        logging.error(f"Google login error: {str(e)}")
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=400, detail="LOGIN_FAILED")

@router.post("/logout")
async def logout(email: str) -> Dict[str, Any]:
    """Logout endpoint to update logged_in_status in both tables"""
    try:
        conn = mysql.connector.connect(
            host=settings.DB_HOST,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            database=settings.DB_NAME
        )
        cursor = conn.cursor()

        # Update Google users table
        cursor.execute(
            "UPDATE user_info_google SET logged_in_status = 0 WHERE email = %s",
            (email,)
        )

        # Update Manual users table
        cursor.execute(
            "UPDATE user_info_manual SET logged_in_status = 0 WHERE email = %s",
            (email,)
        )

        conn.commit()
        logging.info(f"User {email} logged out successfully")
        
        return {"success": True, "message": "Logged out successfully"}

    except mysql.connector.Error as e:
        logging.error(f"Database error during logout: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error during logout"
        )
    finally:
        cursor.close()
        conn.close()

@router.get("/check-login")
async def check_login_status(serial_id: str) -> Dict[str, Any]:
    """Check if user is logged in based on serial_id"""
    try:
        conn = mysql.connector.connect(
            host=settings.DB_HOST,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            database=settings.DB_NAME
        )
        cursor = conn.cursor()

        # Check Google users first
        cursor.execute(
            "SELECT email, username FROM user_info_google WHERE serial_id = %s AND logged_in_status = 1",
            (serial_id,)
        )
        records = cursor.fetchone()
        
        if records:
            return {
                "is_logged_in": True,
                "email": records[0],
                "username": records[1]
            }
        
        # Check Manual users if not found in Google
        cursor.execute(
            "SELECT email, username FROM user_info_manual WHERE serial_id = %s AND logged_in_status = 1",
            (serial_id,)
        )
        records = cursor.fetchone()
        
        if records:
            return {
                "is_logged_in": True,
                "email": records[0],
                "username": records[1]
            }
        
        return {
            "is_logged_in": False,
            "email": None,
            "username": None
        }

    except mysql.connector.Error as e:
        logging.error(f"Database error checking login status: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error while checking login status"
        )
    finally:
        cursor.close()
        conn.close()

@router.post("/manual-signup")
async def manual_signup(
    email: str = Query(...),
    password: str = Query(...),
    username: str = Query(...),
    serial_id: str = Query(...)
):
    try:
        # Connect to database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Check if email already exists
        cursor.execute("SELECT * FROM user_info_manual WHERE email = %s", (email,))
        if cursor.fetchone():
            raise HTTPException(
                status_code=400,
                detail="Email already registered"
            )

        # Hash password
        hashed_password = hash_password(password)

        # Insert new user
        cursor.execute(
            """
            INSERT INTO user_info_manual 
            (email, password, username, serial_id, logged_in_status) 
            VALUES (%s, %s, %s, %s, 0)
            """,
            (email, hashed_password, username, serial_id)
        )
        conn.commit()

        return {"success": True, "message": "User registered successfully"}

    except HTTPException as e:
        raise e
    except Exception as e:
        logging.error(f"Error in manual signup: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

@router.post("/google-signup")
async def google_signup(
    serial_id: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Google OAuth signup endpoint - Only for new users"""
    try:
        # Load credentials from the correct .env file
        client_id = os.getenv("GOOGLE_CLIENT_ID")
        client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
        
        if not client_id or not client_secret:
            logging.error("Missing Google OAuth credentials in environment variables")
            raise HTTPException(
                status_code=400,
                detail="Authentication configuration error"
            )
            
        creds_data = {
            "installed": {
                "client_id": client_id,
                "client_secret": client_secret,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": ["http://localhost"]
            }
        }
        
        scopes = [
            "https://www.googleapis.com/auth/userinfo.profile",
            "https://www.googleapis.com/auth/userinfo.email",
            "openid",
        ]

        try:
            flow = InstalledAppFlow.from_client_config(creds_data, scopes)
            creds = flow.run_local_server(port=0)
        except Exception as e:
            logging.error(f"Google OAuth Flow Error: {str(e)}")
            raise HTTPException(status_code=400, detail="Failed to authenticate with Google")

        try:
            service = build("people", "v1", credentials=creds)
            profile = service.people().get(
                resourceName="people/me",
                personFields="names,emailAddresses"
            ).execute()

            name = profile.get("names", [{}])[0].get("displayName", "N/A")
            email = profile.get("emailAddresses", [{}])[0].get("value", "N/A")
            
            logging.info(f"Google signup attempt - Email: {email}, Name: {name}")

            # Connect to database
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor(dictionary=True)

            try:
                # Check if user already exists
                cursor.execute(
                    "SELECT * FROM user_info_google WHERE email = %s",
                    (email,)
                )
                user = cursor.fetchone()

                if user:
                    # User already exists - they should login instead
                    raise HTTPException(
                        status_code=400,
                        detail="GOOGLE_USER_EXISTS"
                    )

                # Create new user with active login status
                cursor.execute(
                    "INSERT INTO user_info_google (username, email, serial_id, logged_in_status) VALUES (%s, %s, %s, 1)",
                    (name, email, serial_id)
                )
                
                conn.commit()
                return {
                    "success": True,
                    "username": name,
                    "email": email
                }

            finally:
                cursor.close()
                conn.close()

        except HTTPException as e:
            raise e
        except Exception as e:
            logging.error(f"Error getting user info from Google: {str(e)}")
            raise HTTPException(status_code=400, detail="Failed to get user info")

    except Exception as e:
        logging.error(f"Google signup error: {str(e)}")
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=400, detail="SIGNUP_FAILED") 