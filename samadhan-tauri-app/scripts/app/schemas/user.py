from typing import Optional
from pydantic import BaseModel, EmailStr, Field
import re

# Shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    phnumber: Optional[str] = Field(None, pattern=r'^\+?1?\d{9,15}$')
    radio_button: Optional[str] = None
    logged_in_status: Optional[bool] = False
    serial_id: Optional[str] = None

# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    username: str
    password: str

# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None

# Properties shared by models stored in DB
class UserInDBBase(UserBase):
    user_id: int
    email: EmailStr
    username: str

    class Config:
        from_attributes = True

# Additional properties to return via API
class User(UserInDBBase):
    pass

# Additional properties stored in DB
class UserInDB(UserInDBBase):
    password: str 