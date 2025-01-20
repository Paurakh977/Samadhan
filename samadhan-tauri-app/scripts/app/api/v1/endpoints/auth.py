from datetime import timedelta
from typing import Any, Dict
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import bcrypt
from app.core.security import create_access_token, verify_password
from app.core.config import settings
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
def manual_login(
    email: str,
    password: str,
    serial_id: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Manual login endpoint"""
    print(f"Login attempt - Email: {email}, Password: {password}")
    
    # First check if user exists with email and password
    hashed_password = hash_password(password)
    user = db.query(User).filter(
        User.email == email,
        User.password == hashed_password
    ).first()

    if not user:
        print("User not found")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    print(f"Found user: {user.username}")

    # Check if user exists with this serial_id
    user_with_serial = db.query(User).filter(
        User.email == email,
        User.serial_id == serial_id
    ).first()

    if user_with_serial:
        # Update logged_in status for this device
        db.query(User).filter(
            User.email == email,
            User.serial_id == serial_id
        ).update({"logged_in_status": True})
        
        # Set logged_out for other devices
        db.query(User).filter(
            User.email == email,
            User.serial_id != serial_id
        ).update({"logged_in_status": False})
        
        db.commit()
        
        return {
            "success": True,
            "username": user.username,
            "email": user.email
        }
    else:
        # Create new entry for this device
        new_device = User(
            username=user.username,
            phnumber=user.phnumber,
            email=user.email,
            password=user.password,
            radio_button=user.radio_button,
            serial_id=serial_id,
            logged_in_status=True
        )
        db.add(new_device)
        
        # Set logged_out for other devices
        db.query(User).filter(
            User.email == email,
            User.serial_id != serial_id
        ).update({"logged_in_status": False})

        db.commit()
        
        return {
            "success": True,
            "username": user.username,
            "email": user.email
        }

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
    """Google OAuth login endpoint"""
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
            conn = mysql.connector.connect(
                host=settings.DB_HOST,
                user=settings.DB_USER,
                password=settings.DB_PASSWORD,
                database=settings.DB_NAME
            )
            cursor = conn.cursor(dictionary=True)

            try:
                # First check if user exists with this email
                cursor.execute(
                    "SELECT * FROM user_info_google WHERE email = %s",
                    (email,)
                )
                user = cursor.fetchone()

                if user:
                    logging.info(f"Found existing user: {email}")
                    # Check if this device exists for the user
                    cursor.execute(
                        "SELECT * FROM user_info_google WHERE email = %s AND serial_id = %s",
                        (email, serial_id)
                    )
                    device = cursor.fetchone()

                    if device:
                        logging.info(f"Device found for user {email}: {serial_id}")
                        # Update login status for this device
                        cursor.execute(
                            "UPDATE user_info_google SET logged_in_status = 1 WHERE email = %s AND serial_id = %s",
                            (email, serial_id)
                        )
                        # Log out other devices
                        cursor.execute(
                            "UPDATE user_info_google SET logged_in_status = 0 WHERE email = %s AND serial_id != %s",
                            (email, serial_id)
                        )
                        
                        # Get username
                        cursor.execute(
                            "SELECT username FROM user_info_google WHERE email = %s",
                            (email,)
                        )
                        record = cursor.fetchone()
                        if record:
                            name = record['username']
                    else:
                        logging.info(f"Adding new device for user {email}: {serial_id}")
                        # Add new device for existing user
                        cursor.execute(
                            "INSERT INTO user_info_google (username, email, serial_id, logged_in_status) VALUES (%s, %s, %s, 1)",
                            (name, email, serial_id)
                        )
                        # Log out other devices
                        cursor.execute(
                            "UPDATE user_info_google SET logged_in_status = 0 WHERE email = %s AND serial_id != %s",
                            (email, serial_id)
                        )
                    
                    conn.commit()
                    return {
                        "success": True,
                        "username": name,
                        "email": email
                    }
                else:
                    logging.warning(f"No account found for email: {email}")
                    conn.close()
                    raise HTTPException(
                        status_code=401,
                        detail="USER_NOT_FOUND"
                    )

            finally:
                cursor.close()
                conn.close()

        except Exception as e:
            logging.error(f"Error getting user info from Google: {str(e)}")
            raise HTTPException(status_code=400, detail="Failed to get user info")

    except Exception as e:
        logging.error(f"Google login error: {str(e)}")
        raise HTTPException(status_code=400, detail="LOGIN_FAILED") 