from datetime import datetime, timedelta
from typing import Optional
import jwt
import bcrypt
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from ..config import settings
from fastapi import HTTPException, status
from ..models.user import UserInDB
from ..services.user_service import UserService

# Add OAuth2 schema definition
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Compare plain password with hashed password"""
    return bcrypt.checkpw(
        plain_password.encode('utf-8'),
        hashed_password.encode('utf-8')
    )

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Generate JWT access token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.jwt_algorithm)

def decode_token(token: str) -> str:
    """Extract email from JWT token"""
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_algorithm])
        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserInDB:
    """
    Validates the JWT token of the current request and returns the corresponding user.
    """
    email = decode_token(token)
    user_service = UserService()
    user = user_service.get_user_by_email(email=email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user