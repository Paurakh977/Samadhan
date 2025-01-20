from datetime import timedelta
from typing import Any, Dict
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import bcrypt
from app.core.security import create_access_token, verify_password
from app.core.config import settings
from app.db.session import get_db
from app.models.user import User
from app.schemas.token import Token
from app.schemas.user import User as UserSchema
from app.core.deps import get_current_user
from app.core.auth import fake_users_db

router = APIRouter()

# Fixed salt for consistent hashing
FIXED_SALT = b"$2b$12$WMDnjnQGHfHlO7xVxtsUj."

def hash_password(password: str) -> bytes:
    """Hash password using fixed salt"""
    return bcrypt.hashpw(password.encode("utf-8"), FIXED_SALT)

def check_password(stored_password: str, provided_password: str) -> bool:
    """Check if provided password matches stored hash"""
    return bcrypt.checkpw(
        provided_password.encode("utf-8"), 
        stored_password.encode("utf-8")
    )

@router.post("/manual-login")
def manual_login(
    email: str,
    password: str,
    serial_id: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Manual login endpoint that checks email, password and serial_id
    """
    # First check if user exists with email and password
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    # Check password using bcrypt
    if not check_password(user.password, password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

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
            email=user.email,
            password=user.password,  # Use the same hashed password
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