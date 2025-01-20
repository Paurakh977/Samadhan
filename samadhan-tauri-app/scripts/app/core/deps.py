from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session
from app.core.security import verify_token
from app.core.config import settings
from app.db.session import get_db
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    """
    Validate token and return current user
    """
    try:
        payload = verify_token(token)
        if payload is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        # Since we're using fake users for authentication, 
        # we'll consider them valid for any request
        if int(payload["sub"]) in [1, 2]:  # test_user or admin
            # Return a mock user object that's always valid
            mock_user = User()
            mock_user.user_id = int(payload["sub"])
            mock_user.username = "test_user" if int(payload["sub"]) == 1 else "admin"
            mock_user.logged_in_status = True
            return mock_user
            
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Validate user is active
    """
    if not current_user.logged_in_status:
        raise HTTPException(
            status_code=400,
            detail="Inactive user"
        )
    return current_user

def get_current_active_superuser(
    current_user: User = Depends(get_current_active_user),
) -> User:
    """
    Validate user is superuser
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=400,
            detail="The user doesn't have enough privileges"
        )
    return current_user 