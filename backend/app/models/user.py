from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str

class UserInDB(BaseModel):
    id: str
    email: EmailStr
    username: str
    hashed_password: str
    created_at: datetime = datetime.utcnow()
    is_active: bool = True

class User(UserBase):
    id: str
    is_active: bool 

class UserResponse(BaseModel):
    id: str
    email: EmailStr
    
    class Config:
        from_attributes = True